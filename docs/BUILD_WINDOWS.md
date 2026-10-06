# Build no Windows

## Dependências

- Windows 10/11 x64
- Visual Studio 2022
- workload Desktop development with C++
- CMake 3.24+
- Qt 6.x MSVC x64
- FFmpeg development package x64 com headers e bibliotecas de importação

O pacote do FFmpeg precisa expor pelo menos:

- include/libavformat/avformat.h
- include/libavcodec/avcodec.h
- include/libavutil/avutil.h
- lib/avformat.lib
- lib/avcodec.lib
- lib/avutil.lib

Também é necessário copiar as DLLs correspondentes do FFmpeg para a pasta do executável antes de executar o programa.

## Configurar

Exemplo:

```powershell
cmake -S . -B build ^
  -DCMAKE_PREFIX_PATH="C:/Qt/6.x.x/msvc2022_64" ^
  -DFFMPEG_ROOT="C:/SDK/ffmpeg"
```

## Compilar

```powershell
cmake --build build --config Release
```

## Executar

Após compilar, copie as DLLs do FFmpeg para:

```text
build/Release/
```

junto de `RBVideofire.exe`.

## Importação de vídeo

A versão 0.1 já usa FFmpeg diretamente para analisar mídia. O menu:

```text
Arquivo > Importar mídia...
```

aceita múltiplos arquivos e preenche a biblioteca com:

- nome do arquivo
- duração
- resolução
- taxa de quadros
- codec de vídeo
- codec de áudio

O backend usa `libavformat`, `libavcodec` e `libavutil`. Não há chamada externa para `ffprobe.exe`.
