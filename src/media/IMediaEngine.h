#pragma once

#include <filesystem>
#include <string>

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

class IMediaEngine
{
public:
    virtual ~IMediaEngine() = default;
    virtual MediaInfo probe(const std::filesystem::path& file) = 0;
};

} // namespace rbvf
