# RB VideoFire Resolve-Class Professional Suite Design

## Objective
Transformar o RB VideoFire em uma suíte profissional integrada de pós-produção com capacidades equivalentes às categorias de recursos descritas no material do DaVinci Resolve 21.1 fornecido pelo usuário, implementadas de forma própria sobre a arquitetura RB VideoFire. O objetivo não é copiar código, interface ou nomes proprietários, e sim oferecer recursos funcionais equivalentes em montagem, mídia, multicâmera, composição, cor, áudio, automação, scripting e entrega.

## Regra de produto
Nenhum recurso entra como botão decorativo, tela simulada ou fluxo sem backend real. Um recurso só é considerado entregue quando: (1) existe caminho funcional no aplicativo; (2) possui estado persistente quando aplicável; (3) participa do undo/redo quando altera projeto; (4) passa testes; (5) não quebra importação, playback, áudio, save/reopen ou exportação.

## Base arquitetural
Manter C++/Qt/CMake/NSIS e o motor nativo já usado no RB VideoFire. Reutilizar ViewerOutput, Timeline, Project, Node Graph, áudio e undo stack existentes. Novos subsistemas entram por interfaces próprias e pequenas, evitando um segundo motor paralelo de timeline, áudio, mídia ou cor.

## Workspaces principais
A interface principal será organizada por workspaces: Mídia | Edição | Composição | Cor | Áudio | Entrega | Assistente.

### Mídia
- Source Monitor preservando proporção nativa da mídia.
- Project Bin com lista e miniaturas.
- Campos editáveis de metadados em lista com navegação por teclado.
- Pesquisa, bins, smart bins, labels e favoritos.
- Estados Original, Proxy e Offline.
- Archive/Consolidate com opção de incluir apenas mídias usadas, originais ou proxies, cache, LUTs e ativos auxiliares do projeto.
- Relink por nome, tamanho, timecode, reel e metadados quando disponíveis.
- Suporte progressivo a mais formatos/câmeras por FFmpeg e bibliotecas licenciadas compatíveis.

### Edição
- J/K/L, shuttle, go to in/out.
- Insert, overwrite, lift, extract.
- Selection, Ripple, Roll, Razor, Slip, Slide, Hand e Zoom.
- Trim quadro a quadro e nudge de 1 frame.
- Track targeting, lock, sync lock e linked A/V quando suportados pelo modelo.
- Markers e navegação por markers.
- Duração de clip opcional na timeline.
- Waveforms autoajustáveis à altura da track.
- Presets de Inspector para vídeo, áudio, transform e transições.
- Preferências de edição para comportamento de scrub/playback e seleção pós-corte.
- Multicam com criação/sincronização por timecode e gaps, Source/Program multicam, troca de ângulos por atalhos e suporte arquitetural para pelo menos 25 ângulos.
- Seleção de tracks por atalhos com arquitetura preparada para pelo menos 32 tracks.

### Composição
- Workspace nodal baseado no node graph nativo.
- Nós iniciais: Media In, Media Out, Transform, Mask, Merge/Blend, Key, Color, Blur/Sharpen, Text.
- Máscaras Bézier, feather e tracking de máscara.
- Point Tracker primeiro; Planar Tracker depois; Camera Tracker em etapa posterior.
- Chroma key, luma key, roto, corner pin e stabilization.
- Macros/presets reutilizáveis com categorias e thumbnails.
- Ferramentas 2D primeiro; 3D modular depois com primitivas, formas, regiões, paths e conexões.
- Lens distortion/calibration e ferramentas de texto multicamada em etapas avançadas.

### Cor
- Primaries: Lift, Gamma, Gain, Offset, Contrast, Pivot, Saturation, Temperature e Tint.
- Curves: Custom, Hue vs Hue, Hue vs Sat, Hue vs Lum, Lum vs Sat.
- Qualifier HSL, máscaras e tracking.
- LUT .cube em níveis Input, Creative e Output.
- Gerenciamento de cor Input -> Working -> Output.
- Suporte progressivo a Log/Wide Gamut e preparação para ACES transforms.
- Scopes: Waveform Luma, RGB Parade, Vectorscope e Histogram.
- Scopes devem consumir o mesmo sinal do Program Monitor.
- Before/After, bypass por node e still/reference comparison.
- Arquitetura para múltiplos trims/deliveries SDR/HDR e caches separados por versão em etapa posterior.

### Áudio
- Audio Monitor L/R dBFS, peak hold e clipping.
- Mixer por track com gain, pan, mute, solo, meter, FX e automation.
- Master Bus com meter e limiter opcional.
- Cadeia: Source -> Clip Gain -> Clip FX -> Track FX -> Fader/Pan -> Bus -> Master FX -> Master Meter -> Output.
- Effects Rack inicial: Gain, Normalize, HPF, LPF, Compressor, Limiter, EQ paramétrico, Noise Gate, De-esser simples, Pan/Balance, Phase invert, mono/stereo conversion.
- LUFS e spectrum analyzer em etapa posterior.
- Nenhuma cópia direta de Audacity; dependências externas só após auditoria de licença.

### Entrega
- Render Queue.
- Batch render.
- Presets H.264, H.265, ProRes quando licenciamento/plataforma permitir, DNxHR, image sequence e WAV.
- Export de projeto arquivado com seleção de ativos.
- Continue editing while queued render quando o backend de render suportar isolamento seguro.
- DCP e entregas HDR avançadas como etapas posteriores.

### Assistente
- Camada de automação por linguagem natural sobre APIs internas do RB VideoFire.
- Ações permitidas: analisar projeto, organizar mídia, aplicar tags, criar bins, localizar clips, preparar highlights, remover clips por critérios explícitos, configurar filas de render e executar batch render.
- Integração com provedores externos via chave/API configurável pelo usuário; sem credenciais embutidas.
- Toda ação destrutiva passa por preview/confirm e usa undo quando aplicável.
- O Assistente não acessa diretamente memória interna arbitrária do editor; usa uma API de comandos estável.

### Scripting/API
- API interna versionada para mídia, timeline, markers, bins, render queue, project metadata e automação.
- Console de scripting separado do processo de playback.
- Primeiro Python/JSON-RPC local ou interface equivalente; extensões externas só depois de estabilizar a API.

### Performance/GPU
- Playback quality Full/Half/Quarter.
- Original/Proxy toggle.
- Background cache.
- GPU acceleration progressiva para transforms, color, scopes e codecs quando bibliotecas/plataforma permitirem.
- Fallback CPU obrigatório.
- Benchmark gates para playback, seek, scrub e render.

## Dependências e licenciamento
- Não copiar código do DaVinci Resolve/Fusion.
- Não copiar código GPL incompatível para módulos que o projeto deseje manter sob outra política; auditar cada dependência.
- Codecs/formatos sujeitos a licenças comerciais só entram se houver implementação legalmente distribuível; quando isso não for possível, expor suporte por backend instalado pelo usuário ou deixar claramente indisponível.

## Persistência e compatibilidade
- O formato de projeto deve versionar novas propriedades sem quebrar projetos antigos.
- Campos desconhecidos devem ser ignorados de forma segura em versões anteriores quando possível.
- Autosave, snapshots e recovery não podem sobrescrever o projeto principal.

## Test strategy
Cada recurso novo segue RED -> GREEN -> refactor. Gates por módulo: unit/contract tests; integração com timeline/project; save/reopen; undo/redo; playback; export/regression. O Windows Release precisa passar CTest, startup smoke, package audit e PE GUI/no-console.

## Roadmap de execução
M3 Editorial Precision: trim, transporte, track controls, markers, multicam base e Inspector presets.
M4 Media Intelligence: metadata, bins, proxy/original/offline, archive e relink.
M5 Inspector & Keyframes: transform/crop/opacity/speed/audio e presets persistentes.
M6 Color: primaries, curves, LUTs, scopes e color-management base.
M7 Composition: nodes, masks, keying, tracker e macros.
M8 Audio: Mixer, Master, FX Rack e automation.
M9 Delivery & Performance: render queue, batch render, cache, quality modes e GPU foundations.
M10 Assistant & Scripting: command API, automação, provedores de IA e scripting.
M11 Advanced Camera/Color/3D: formatos/câmeras adicionais, ACES/log expansions, 3D avançado, HDR multi-trim e features que dependam de bibliotecas/licenças específicas.

## Definition of Done
Um marco só recebe EXE de entrega quando não houver Blocker/Critical conhecido, o workflow Windows estiver verde, o instalador abrir sem console, o smoke test passar e os recursos prometidos naquele marco tiverem caminho funcional demonstrável. Recursos de marcos posteriores não serão simulados antecipadamente.