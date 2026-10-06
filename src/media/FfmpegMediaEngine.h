#pragma once

#include "IMediaEngine.h"

namespace rbvf {

class FfmpegMediaEngine final : public IMediaEngine
{
public:
    MediaInfo probe(const std::filesystem::path& file) override;
    VideoFrame decodeFrameAt(const std::filesystem::path& file, double seconds) override;
};

} // namespace rbvf
