# RB Videofire 0.1

Nova fundação do RB Videofire, criada do zero.

## Objetivo

Construir um editor de vídeo offline para Windows 10/11 x64, com arquitetura modular e preparada para FFmpeg, timeline multifaixa, preview, áudio, cache e renderização.

## Stack

- C++20
- Qt 6
- CMake
- MSVC
- FFmpeg como backend multimídia
- projeto .rbvf em JSON

## Estado atual

Esta branch principal contém apenas a fundação 0.1.

Fluxo planejado:

- criar projeto
- importar mídia
- timeline
- preview
- split e trim
- salvar e abrir .rbvf
- exportar MP4 H.264/AAC

## Build inicial

Requisitos:

- Windows 10 ou 11 x64
- Visual Studio 2022 com Desktop development with C++
- CMake 3.24+
- Qt 6.x com kit MSVC x64

Comandos:

```powershell
cmake -S . -B build -DCMAKE_PREFIX_PATH="C:/Qt/6.x.x/msvc2022_64"
cmake --build build --config Release
```

O executável será gerado em `build/Release/RBVideofire.exe`.
