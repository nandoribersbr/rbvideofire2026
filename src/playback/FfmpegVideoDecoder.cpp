#include "FfmpegVideoDecoder.h"

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <libavutil/imgutils.h>
#include <libavutil/rational.h>
#include <libswscale/swscale.h>
}

#include <stdexcept>
#include <string>

#ifdef _WIN32
#include <Windows.h>
#endif

namespace rbvf {
namespace {

std::string pathToUtf8(const std::filesystem::path& path)
{
#ifdef _WIN32
    const std::wstring wide = path.wstring();
    if (wide.empty()) {
        return {};
    }

    const int size = WideCharToMultiByte(
        CP_UTF8, 0, wide.c_str(), static_cast<int>(wide.size()),
        nullptr, 0, nullptr, nullptr);

    if (size <= 0) {
        throw std::runtime_error("Falha ao converter caminho para UTF-8.");
    }

    std::string utf8(static_cast<std::size_t>(size), '\0');
    WideCharToMultiByte(
        CP_UTF8, 0, wide.c_str(), static_cast<int>(wide.size()),
        utf8.data(), size, nullptr, nullptr);

    return utf8;
#else
    return path.string();
#endif
}

double streamFrameRate(const AVStream* stream)
{
    AVRational rate = stream->avg_frame_rate;
    if (rate.num == 0 || rate.den == 0) {
        rate = stream->r_frame_rate;
    }
    return (rate.num && rate.den) ? av_q2d(rate) : 0.0;
}

} // namespace

FfmpegVideoDecoder::FfmpegVideoDecoder() = default;

FfmpegVideoDecoder::~FfmpegVideoDecoder()
{
    close();
}

void FfmpegVideoDecoder::open(const std::filesystem::path& file)
{
    close();

    const std::string input = pathToUtf8(file);

    if (avformat_open_input(&m_format, input.c_str(), nullptr, nullptr) < 0) {
        close();
        throw std::runtime_error("Não foi possível abrir o vídeo.");
    }

    if (avformat_find_stream_info(m_format, nullptr) < 0) {
        close();
        throw std::runtime_error("Não foi possível ler os streams do vídeo.");
    }

    m_videoStream = av_find_best_stream(
        m_format, AVMEDIA_TYPE_VIDEO, -1, -1, nullptr, 0);

    if (m_videoStream < 0) {
        close();
        throw std::runtime_error("Nenhum stream de vídeo encontrado.");
    }

    AVStream* stream = m_format->streams[m_videoStream];
    const AVCodec* decoder = avcodec_find_decoder(stream->codecpar->codec_id);

    if (!decoder) {
        close();
        throw std::runtime_error("Codec de vídeo sem decoder disponível.");
    }

    m_codec = avcodec_alloc_context3(decoder);
    if (!m_codec) {
        close();
        throw std::runtime_error("Falha ao criar contexto do decoder.");
    }

    if (avcodec_parameters_to_context(m_codec, stream->codecpar) < 0 ||
        avcodec_open2(m_codec, decoder, nullptr) < 0) {
        close();
        throw std::runtime_error("Falha ao inicializar decoder de vídeo.");
    }

    m_frame = av_frame_alloc();
    m_packet = av_packet_alloc();

    if (!m_frame || !m_packet) {
        close();
        throw std::runtime_error("Falha ao alocar buffers de vídeo.");
    }

    m_frameRate = streamFrameRate(stream);

    if (m_format->duration != AV_NOPTS_VALUE) {
        m_durationSeconds =
            static_cast<double>(m_format->duration) / AV_TIME_BASE;
    } else if (stream->duration != AV_NOPTS_VALUE) {
        m_durationSeconds =
            static_cast<double>(stream->duration) * av_q2d(stream->time_base);
    }
}

void FfmpegVideoDecoder::close()
{
    if (m_sws) {
        sws_freeContext(m_sws);
        m_sws = nullptr;
    }

    if (m_packet) {
        av_packet_free(&m_packet);
    }

    if (m_frame) {
        av_frame_free(&m_frame);
    }

    if (m_codec) {
        avcodec_free_context(&m_codec);
    }

    if (m_format) {
        avformat_close_input(&m_format);
    }

    m_videoStream = -1;
    m_durationSeconds = 0.0;
    m_frameRate = 0.0;
}

bool FfmpegVideoDecoder::isOpen() const noexcept
{
    return m_format && m_codec && m_videoStream >= 0;
}

bool FfmpegVideoDecoder::receiveFrame(QImage& image, double& ptsSeconds)
{
    const int result = avcodec_receive_frame(m_codec, m_frame);

    if (result == AVERROR(EAGAIN) || result == AVERROR_EOF) {
        return false;
    }

    if (result < 0) {
        throw std::runtime_error("Erro durante decode de frame.");
    }

    image = convertFrame(m_frame);

    const AVStream* stream = m_format->streams[m_videoStream];
    const int64_t pts = m_frame->best_effort_timestamp;

    ptsSeconds = pts == AV_NOPTS_VALUE
        ? 0.0
        : static_cast<double>(pts) * av_q2d(stream->time_base);

    return true;
}

bool FfmpegVideoDecoder::readNextFrame(QImage& image, double& ptsSeconds)
{
    if (!isOpen()) {
        return false;
    }

    if (receiveFrame(image, ptsSeconds)) {
        return true;
    }

    while (av_read_frame(m_format, m_packet) >= 0) {
        if (m_packet->stream_index == m_videoStream) {
            const int sendResult = avcodec_send_packet(m_codec, m_packet);
            av_packet_unref(m_packet);

            if (sendResult < 0 && sendResult != AVERROR(EAGAIN)) {
                throw std::runtime_error("Erro ao enviar pacote ao decoder.");
            }

            if (receiveFrame(image, ptsSeconds)) {
                return true;
            }
        } else {
            av_packet_unref(m_packet);
        }
    }

    avcodec_send_packet(m_codec, nullptr);
    return receiveFrame(image, ptsSeconds);
}

bool FfmpegVideoDecoder::seek(double seconds)
{
    if (!isOpen()) {
        return false;
    }

    seconds = std::max(0.0, std::min(seconds, m_durationSeconds));

    AVStream* stream = m_format->streams[m_videoStream];
    const int64_t timestamp =
        static_cast<int64_t>(seconds / av_q2d(stream->time_base));

    if (av_seek_frame(m_format, m_videoStream, timestamp, AVSEEK_FLAG_BACKWARD) < 0) {
        return false;
    }

    avcodec_flush_buffers(m_codec);
    return true;
}

double FfmpegVideoDecoder::durationSeconds() const noexcept
{
    return m_durationSeconds;
}

double FfmpegVideoDecoder::frameRate() const noexcept
{
    return m_frameRate;
}

QImage FfmpegVideoDecoder::convertFrame(const AVFrame* frame)
{
    m_sws = sws_getCachedContext(
        m_sws,
        frame->width,
        frame->height,
        static_cast<AVPixelFormat>(frame->format),
        frame->width,
        frame->height,
        AV_PIX_FMT_BGRA,
        SWS_BILINEAR,
        nullptr,
        nullptr,
        nullptr
    );

    if (!m_sws) {
        throw std::runtime_error("Falha ao criar conversor de pixel.");
    }

    QImage image(frame->width, frame->height, QImage::Format_ARGB32);
    if (image.isNull()) {
        throw std::runtime_error("Falha ao criar imagem de preview.");
    }

    uint8_t* destination[4] = { image.bits(), nullptr, nullptr, nullptr };
    int destinationStride[4] = { static_cast<int>(image.bytesPerLine()), 0, 0, 0 };

    sws_scale(
        m_sws,
        frame->data,
        frame->linesize,
        0,
        frame->height,
        destination,
        destinationStride
    );

    return image;
}

} // namespace rbvf
