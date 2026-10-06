#pragma once

#include <filesystem>

namespace rbvf {

enum class VideoCodec {
    H264
};

enum class AudioCodec {
    AAC
};

struct RenderJob {
    std::filesystem::path output;
    int width{1920};
    int height{1080};
    double fps{30.0};
    int videoBitrate{12'000'000};
    VideoCodec videoCodec{VideoCodec::H264};
    AudioCodec audioCodec{AudioCodec::AAC};
    bool preferHardwareAcceleration{true};
};

} // namespace rbvf
