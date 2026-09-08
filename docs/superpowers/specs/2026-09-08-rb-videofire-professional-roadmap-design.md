# RB VideoFire Professional Roadmap Design

## Goal
Evoluir a base 2.4.0 M2 em etapas verificáveis até um NLE profissional, priorizando confiabilidade editorial antes de composição, cor e acabamento avançado.

## Regra de arquitetura
Cada marco deve reutilizar o pipeline nativo existente. Não criar motores paralelos falsos para timeline, áudio, cor ou mídia. Cada etapa precisa preservar abertura de projeto, reprodução, áudio, undo/redo, salvamento e exportação já existentes.

## M3 Editorial Precision
Prioridade imediata. Consolidar ferramentas Selection/Ripple/Roll/Razor/Slip/Slide, nudge de 1 frame, JKL, insert/overwrite, lift/extract, track targeting, sync lock, linked A/V, markers e cabeçalhos profissionais de tracks. Trim deve operar no modelo temporal existente e permanecer integrado ao undo stack.

## M4 Media Intelligence
Project Bin com lista/miniaturas, metadados, pesquisa e bins; estados Original/Proxy/Offline; criação e alternância de proxy separada de render cache; relink por nome, tamanho, timecode/reel/metadados quando disponíveis.

## M5 Inspector & Keyframes
Inspector dedicado para Transform, Crop, Opacity, Speed e propriedades de áudio. Keyframes editáveis e persistentes, sem substituir o grafo nativo.

## M6 Color Workspace
Workspace Cor com primaries (Lift/Gamma/Gain/Offset, contraste, pivot, saturação, temperatura e tint), curvas, LUT .cube e scopes Waveform/RGB Parade/Vectorscope/Histogram. O sinal dos scopes deve derivar do mesmo pipeline exibido pelo monitor. Preparar gerenciamento Input/Working/Output color space.

## M7 Composition Foundation
Workspace Composição sobre o node graph existente. Primeiros nós: Media In/Out, Transform, Mask, Key, Blend e Color; depois Point Tracker, planar tracking e ferramentas de roto. Evitar tentar substituir Nuke/Fusion numa única etapa.

## M8 RB Audio Workspace
Mixer por faixa e Master, meters, fader, pan, mute, solo, FX e automação. Cadeia: Clip Gain -> Clip FX -> Track FX -> Fader/Pan -> Bus -> Master FX -> Master Meter -> Output. Implementação própria; dependências externas somente após auditoria individual de licença.

## M9 Performance & GPU
Playback Full/Half/Quarter, Original/Proxy, cache em background, aceleração GPU para transform/color/scopes quando suportada e fallback CPU.

## Release gates
Cada marco usa RED -> implementação mínima -> GREEN -> build Release Windows -> CTest -> startup smoke -> regressão de projeto/reprodução -> empacotamento. Nenhuma etapa é chamada de concluída se houver Blocker ou Critical conhecido.

## Escopo desta execução
Implementar primeiro M3 Editorial Precision sobre a branch derivada do M2. M4-M9 permanecem como marcos separados para reduzir risco e permitir EXEs testáveis entre etapas.