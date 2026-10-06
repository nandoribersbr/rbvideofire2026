#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace rbvf {

using Tick = std::int64_t;
inline constexpr Tick TicksPerSecond = 1'000'000;

struct Clip {
    std::string id;
    std::string mediaId;
    Tick timelineStart{0};
    Tick sourceIn{0};
    Tick sourceOut{0};
    double playbackRate{1.0};
    double opacity{1.0};
    double audioGain{1.0};
};

struct Track {
    std::string id;
    std::vector<Clip> clips;
};

class Timeline
{
public:
    std::vector<Track>& tracks() noexcept { return m_tracks; }
    const std::vector<Track>& tracks() const noexcept { return m_tracks; }

private:
    std::vector<Track> m_tracks;
};

} // namespace rbvf
