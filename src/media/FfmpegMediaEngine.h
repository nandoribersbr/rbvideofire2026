#pragma once

#include "IMediaEngine.h"

namespace rbvf {

class FfmpegMediaEngine final : public IMediaEngine
{
public:
    MediaInfo probe(const std::filesystem::path& file) override;
};

} // namespace rbvf
