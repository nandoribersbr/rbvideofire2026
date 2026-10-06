#include "FfmpegMediaEngine.h"

#include <stdexcept>

namespace rbvf {

MediaInfo FfmpegMediaEngine::probe(const std::filesystem::path& file)
{
    if (file.empty()) {
        throw std::invalid_argument("Caminho de mídia vazio.");
    }

    // Integração libavformat/libavcodec entra no próximo marco.
    // Mantemos o backend isolado desde a fundação para não acoplar FFmpeg à UI.
    return {};
}

} // namespace rbvf
