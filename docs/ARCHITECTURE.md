# Arquitetura RB Videofire 0.1

## Camadas

UI
→ Application
→ Core
→ Media Engine
→ Preview / Audio / Cache / Render

## Princípios

- edição não destrutiva
- UI desacoplada de codecs
- tempo interno em int64_t
- projeto .rbvf pequeno e referencial
- tarefas pesadas fora da thread da interface
- CPU como fallback
- aceleração por GPU adicionada por backend
- modo offline
- distribuição portable-first

## Módulos

### app
Inicialização, janela principal e integração dos painéis.

### core
Modelo de projeto, timeline, tracks e clips.

### media
Leitura de mídia. FFmpeg entra por implementação de IMediaEngine.

### playback
Scheduler, filas de frames, clock e preview. Ainda não implementado.

### audio
Decode, mixagem e saída WASAPI. Ainda não implementado.

### cache
Thumbnails, waveforms, metadata e frame cache. Ainda não implementado.

### render
Fila e pipeline de exportação.

## Pipeline de render

Timeline
→ Decoder
→ Compositor
→ Effects
→ Encoder de vídeo

Audio decoder
→ Mixer
→ Encoder de áudio

Vídeo + áudio
→ Muxer
→ MP4 final

## Marco 0.1

O marco funcional fecha quando o aplicativo consegue importar MP4, colocar mídia na timeline, reproduzir, fazer split/trim, salvar .rbvf, reabrir o projeto e exportar H.264/AAC.
