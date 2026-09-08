# RB VideoFire 2.4 RB Audio Workspace Design

## Objetivo

Transformar a aba de áudio do RB VideoFire em um workspace profissional de pós-produção sonora integrado ao mesmo projeto, timeline e engine do editor, inspirado em boas práticas de DAWs e do Audacity, porém com implementação própria do RB VideoFire.

## Regra de licenciamento

- Não copiar código GPL do Audacity para o RB VideoFire.
- Audacity pode ser usado como referência de fluxo, conceitos e comportamento.
- Dependências externas só podem ser integradas após auditoria individual de licença.
- Preferir MIT, BSD, ISC, Apache-2.0 ou equivalente permissiva.
- Toda dependência externa deve ser isolada por uma camada de abstração própria do RB VideoFire.

## Arquitetura de áudio

Fluxo editorial:

`Media -> Clip Gain -> Clip FX -> Track FX -> Track Fader/Pan -> Bus -> Master FX -> Master Meter -> Output`

O RB Audio Workspace não cria um segundo decoder nem uma segunda pipeline de playback. Ele consome o áudio e os níveis já produzidos pelo engine nativo.

## Componentes

### Audio Monitor

- Medidores L/R em dBFS.
- Escala de 0 a -60 dBFS.
- Peak hold configurável, padrão 1500 ms.
- Indicador de clipping para amostras finitas >= 1.0.
- Silêncio, NaN, infinito e valores inválidos no piso de -60 dBFS.
- Atualização não bloqueante durante playback, pause, seek e scrub.

### Audio Mixer

Cada faixa terá:

- fader de volume;
- pan/balance;
- mute;
- solo;
- medidor de nível;
- Effects Rack;
- automação em evolução incremental.

O Master Bus terá fader, medição final e Effects Rack master.

### Inspector de Áudio

Controles de clipe:

- ganho;
- fade in/out;
- normalização;
- conversão mono/stereo quando aplicável;
- fase/inversão quando aplicável;
- parâmetros dos efeitos do clipe.

### Effects Rack

Primeiro conjunto próprio do RB VideoFire:

- Gain;
- Normalize;
- Compressor;
- Limiter;
- Parametric EQ;
- High-pass;
- Low-pass;
- Noise Gate;
- De-esser simples;
- Pan/Balance;
- Phase invert.

Fases posteriores poderão incluir LUFS, analisador de espectro, redução de ruído avançada e compressor multibanda.

## Workspace

Layout alvo em 1920x1080:

- Mixer com canais legíveis.
- Master à direita.
- Audio Monitor sempre acessível.
- Inspector/Effects Rack em dock próprio.
- Timeline continua sendo a timeline editorial principal.
- Painéis são dockáveis e persistem posição/tamanho.

## Integração com a timeline

- Nenhum motor paralelo de edição de áudio.
- Mute/solo/volume/pan devem atuar no caminho real de reprodução.
- Mudanças devem participar do sistema de Undo/Redo quando forem editoriais.
- Save/reopen deve preservar parâmetros de áudio e efeitos.

## Compatibilidade

- Windows 10/11 64-bit.
- Build C++/Qt/CMake/NSIS.
- Sem console antes da GUI.
- Preservar importação, edição, A/V sync, proxy, save/reopen e export existentes.

## Aceitação da fase 2.4 Audio

A fase só é considerada funcional quando o fluxo abaixo passa:

`instalar -> abrir -> importar MP4/MOV -> reproduzir áudio -> ver L/R reais -> ajustar ganho/pan -> mute/solo -> aplicar efeito -> salvar -> fechar -> reabrir -> reproduzir -> exportar`

Critérios de release:

- 0 Blocker.
- 0 Critical.
- Audio Monitor conectado ao engine real.
- Nenhum medidor simulado.
- Nenhum segundo decoder de áudio criado para alimentar a interface.
- Build Release, testes, smoke test e instalador Windows aprovados.
