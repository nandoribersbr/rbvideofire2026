#include "FfmpegMediaEngine.h"

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <libavutil/error.h>
#include <libavutil/rational.h>
}

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

    struct FormatContextDeleter {
        void operator()(AVFormatContext* context) const noexcept
        {
            if (context) {
                avformat_close_input(&context);
            }
        }
    };

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

} // namespace rbvf
