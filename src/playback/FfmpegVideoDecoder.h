#pragma once

#include <QImage>

#include <filesystem>
#include <memory>

struct AVCodecContext;
struct AVFormatContext;
struct AVFrame;
struct AVPacket;
struct SwsContext;

namespace rbvf {

class FfmpegVideoDecoder
{
public:
    FfmpegVideoDecoder();
    ~FfmpegVideoDecoder();

    FfmpegVideoDecoder(const FfmpegVideoDecoder&) = delete;
    FfmpegVideoDecoder& operator=(const FfmpegVideoDecoder&) = delete;

    void open(const std::filesystem::path& file);
    void close();

    bool isOpen() const noexcept;
    bool readNextFrame(QImage& image, double& ptsSeconds);
    bool seek(double seconds);

    double durationSeconds() const noexcept;
    double frameRate() const noexcept;

private:
    bool receiveFrame(QImage& image, double& ptsSeconds);
    QImage convertFrame(const AVFrame* frame);

    AVFormatContext* m_format{nullptr};
    AVCodecContext* m_codec{nullptr};
    AVFrame* m_frame{nullptr};
    AVPacket* m_packet{nullptr};
    SwsContext* m_sws{nullptr};

    int m_videoStream{-1};
    double m_durationSeconds{0.0};
    double m_frameRate{0.0};
};

} // namespace rbvf
