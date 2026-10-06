#pragma once

#include <cstdint>
#include <filesystem>
#include <string>
#include <vector>

namespace rbvf {

struct MediaInfo {
    double durationSeconds{0.0};
    int width{0};
    int height{0};
    double frameRate{0.0};
    bool hasVideo{false};
    bool hasAudio{false};
    std::string videoCodec;
    std::string audioCodec;
};

struct VideoFrame {
    int width{0};
    int height{0};
    int stride{0};
    std::vector<std::uint8_t> rgb24;
};

class IMediaEngine
{
public:
    virtual ~IMediaEngine() = default;
    virtual MediaInfo probe(const std::filesystem::path& file) = 0;
    virtual VideoFrame decodeFrameAt(const std::filesystem::path& file, double seconds) = 0;
};

} // namespace rbvf
