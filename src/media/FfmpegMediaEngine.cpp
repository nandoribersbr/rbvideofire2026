#include "FfmpegMediaEngine.h"

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <libavutil/error.h>
#include <libavutil/imgutils.h>
#include <libavutil/rational.h>
#include <libswscale/swscale.h>
}

#include <algorithm>
#include <array>
#include <memory>
#include <stdexcept>
#include <string>

#ifdef _WIN32
#include <Windows.h>
#endif

namespace rbvf {
namespace {

std::string ffmpegError(int errorCode)
{
    std::array<char, AV_ERROR_MAX_STRING_SIZE> buffer{};
    av_strerror(errorCode, buffer.data(), buffer.size());
    return std::string(buffer.data());
}

std::string pathToUtf8(const std::filesystem::path& path)
{
#ifdef _WIN32
    const std::wstring wide = path.wstring();
    if (wide.empty()) {
        return {};
    }

    const int size = WideCharToMultiByte(
        CP_UTF8,
        0,
        wide.c_str(),
        static_cast<int>(wide.size()),
        nullptr,
        0,
        nullptr,
        nullptr
    );

    if (size <= 0) {
        throw std::runtime_error("Falha ao converter o caminho do arquivo para UTF-8.");
    }

    std::string utf8(static_cast<std::size_t>(size), '\0');

    WideCharToMultiByte(
        CP_UTF8,
        0,
        wide.c_str(),
        static_cast<int>(wide.size()),
        utf8.data(),
        size,
        nullptr,
        nullptr
    );

    return utf8;
#else
    return path.string();
#endif
}

double rationalToDouble(AVRational value)
{
    if (value.num == 0 || value.den == 0) {
        return 0.0;
    }
    return av_q2d(value);
}

double streamDurationSeconds(const AVStream* stream)
{
    if (!stream || stream->duration == AV_NOPTS_VALUE) {
        return 0.0;
    }

    return static_cast<double>(stream->duration) * av_q2d(stream->time_base);
}

struct FormatContextDeleter {
    void operator()(AVFormatContext* context) const noexcept
    {
        if (context) {
            avformat_close_input(&context);
        }
    }
};

struct CodecContextDeleter {
    void operator()(AVCodecContext* context) const noexcept
    {
        if (context) {
            avcodec_free_context(&context);
        }
    }
};

struct FrameDeleter {
    void operator()(AVFrame* frame) const noexcept
    {
        if (frame) {
            av_frame_free(&frame);
        }
    }
};

struct PacketDeleter {
    void operator()(AVPacket* packet) const noexcept
    {
        if (packet) {
            av_packet_free(&packet);
        }
    }
};

struct SwsContextDeleter {
    void operator()(SwsContext* context) const noexcept
    {
        if (context) {
            sws_freeContext(context);
        }
    }
};

} // namespace

MediaInfo FfmpegMediaEngine::probe(const std::filesystem::path& file)
{
    if (file.empty()) {
        throw std::invalid_argument("Caminho de mídia vazio.");
    }

    if (!std::filesystem::exists(file)) {
        throw std::runtime_error("Arquivo não encontrado.");
    }

    const std::string inputPath = pathToUtf8(file);

    AVFormatContext* rawContext = nullptr;
    int result = avformat_open_input(&rawContext, inputPath.c_str(), nullptr, nullptr);
    if (result < 0) {
        throw std::runtime_error(
            "FFmpeg não conseguiu abrir o arquivo: " + ffmpegError(result)
        );
    }

    std::unique_ptr<AVFormatContext, FormatContextDeleter> context(rawContext);

    result = avformat_find_stream_info(context.get(), nullptr);
    if (result < 0) {
        throw std::runtime_error(
            "FFmpeg não conseguiu ler os streams: " + ffmpegError(result)
        );
    }

    MediaInfo info;

    if (context->duration != AV_NOPTS_VALUE) {
        info.durationSeconds =
            static_cast<double>(context->duration) / static_cast<double>(AV_TIME_BASE);
    }

    for (unsigned int index = 0; index < context->nb_streams; ++index) {
        AVStream* stream = context->streams[index];
        const AVCodecParameters* params = stream->codecpar;

        if (!params) {
            continue;
        }

        if (params->codec_type == AVMEDIA_TYPE_VIDEO && !info.hasVideo) {
            info.hasVideo = true;
            info.width = params->width;
            info.height = params->height;
            info.videoCodec = avcodec_get_name(params->codec_id);

            AVRational frameRate = stream->avg_frame_rate;
            if (frameRate.num == 0 || frameRate.den == 0) {
                frameRate = stream->r_frame_rate;
            }
            info.frameRate = rationalToDouble(frameRate);

            if (info.durationSeconds <= 0.0) {
                info.durationSeconds = streamDurationSeconds(stream);
            }
        } else if (params->codec_type == AVMEDIA_TYPE_AUDIO && !info.hasAudio) {
            info.hasAudio = true;
            info.audioCodec = avcodec_get_name(params->codec_id);

            if (info.durationSeconds <= 0.0) {
                info.durationSeconds = streamDurationSeconds(stream);
            }
        }
    }

    if (!info.hasVideo && !info.hasAudio) {
        throw std::runtime_error("Nenhum stream de áudio ou vídeo foi encontrado.");
    }

    return info;
}

VideoFrame FfmpegMediaEngine::decodeFrameAt(const std::filesystem::path& file, double seconds)
{
    if (file.empty() || !std::filesystem::exists(file)) {
        throw std::runtime_error("Arquivo de preview inválido.");
    }

    const std::string inputPath = pathToUtf8(file);

    AVFormatContext* rawFormat = nullptr;
    int result = avformat_open_input(&rawFormat, inputPath.c_str(), nullptr, nullptr);
    if (result < 0) {
        throw std::runtime_error("Falha ao abrir vídeo: " + ffmpegError(result));
    }

    std::unique_ptr<AVFormatContext, FormatContextDeleter> format(rawFormat);

    result = avformat_find_stream_info(format.get(), nullptr);
    if (result < 0) {
        throw std::runtime_error("Falha ao ler streams: " + ffmpegError(result));
    }

    const int videoStreamIndex =
        av_find_best_stream(format.get(), AVMEDIA_TYPE_VIDEO, -1, -1, nullptr, 0);

    if (videoStreamIndex < 0) {
        throw std::runtime_error("Nenhum stream de vídeo encontrado.");
    }

    AVStream* stream = format->streams[videoStreamIndex];
    const AVCodec* codec = avcodec_find_decoder(stream->codecpar->codec_id);

    if (!codec) {
        throw std::runtime_error("Decoder de vídeo não encontrado.");
    }

    AVCodecContext* rawCodec = avcodec_alloc_context3(codec);
    if (!rawCodec) {
        throw std::runtime_error("Falha ao criar contexto de decoder.");
    }

    std::unique_ptr<AVCodecContext, CodecContextDeleter> codecContext(rawCodec);

    result = avcodec_parameters_to_context(codecContext.get(), stream->codecpar);
    if (result < 0) {
        throw std::runtime_error("Falha ao configurar decoder: " + ffmpegError(result));
    }

    result = avcodec_open2(codecContext.get(), codec, nullptr);
    if (result < 0) {
        throw std::runtime_error("Falha ao abrir decoder: " + ffmpegError(result));
    }

    seconds = std::max(0.0, seconds);
    const int64_t targetTimestamp =
        av_rescale_q(
            static_cast<int64_t>(seconds * AV_TIME_BASE),
            AVRational{1, AV_TIME_BASE},
            stream->time_base
        );

    av_seek_frame(format.get(), videoStreamIndex, targetTimestamp, AVSEEK_FLAG_BACKWARD);
    avcodec_flush_buffers(codecContext.get());

    std::unique_ptr<AVPacket, PacketDeleter> packet(av_packet_alloc());
    std::unique_ptr<AVFrame, FrameDeleter> frame(av_frame_alloc());

    if (!packet || !frame) {
        throw std::runtime_error("Falha ao alocar buffers do FFmpeg.");
    }

    bool gotFrame = false;

    while (av_read_frame(format.get(), packet.get()) >= 0) {
        if (packet->stream_index == videoStreamIndex) {
            result = avcodec_send_packet(codecContext.get(), packet.get());
            if (result >= 0) {
                while ((result = avcodec_receive_frame(codecContext.get(), frame.get())) >= 0) {
                    const int64_t bestTs = frame->best_effort_timestamp;
                    if (bestTs == AV_NOPTS_VALUE || bestTs >= targetTimestamp) {
                        gotFrame = true;
                        break;
                    }
                }
            }
        }

        av_packet_unref(packet.get());

        if (gotFrame) {
            break;
        }
    }

    if (!gotFrame) {
        avcodec_send_packet(codecContext.get(), nullptr);
        if (avcodec_receive_frame(codecContext.get(), frame.get()) >= 0) {
            gotFrame = true;
        }
    }

    if (!gotFrame) {
        throw std::runtime_error("Não foi possível decodificar um frame para o preview.");
    }

    const int width = frame->width;
    const int height = frame->height;
    const int stride = width * 3;

    VideoFrame output;
    output.width = width;
    output.height = height;
    output.stride = stride;
    output.rgb24.resize(static_cast<std::size_t>(stride) * static_cast<std::size_t>(height));

    SwsContext* rawSws = sws_getContext(
        width,
        height,
        static_cast<AVPixelFormat>(frame->format),
        width,
        height,
        AV_PIX_FMT_RGB24,
        SWS_BILINEAR,
        nullptr,
        nullptr,
        nullptr
    );

    if (!rawSws) {
        throw std::runtime_error("Falha ao criar conversor de pixel.");
    }

    std::unique_ptr<SwsContext, SwsContextDeleter> sws(rawSws);

    uint8_t* dstData[4] = { output.rgb24.data(), nullptr, nullptr, nullptr };
    int dstLinesize[4] = { stride, 0, 0, 0 };

    sws_scale(
        sws.get(),
        frame->data,
        frame->linesize,
        0,
        height,
        dstData,
        dstLinesize
    );

    return output;
}

} // namespace rbvf
