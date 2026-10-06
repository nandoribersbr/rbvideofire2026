# Build no Windows

## Dependências

- Windows 10/11 x64
- Visual Studio 2022
- workload Desktop development with C++
- CMake 3.24+
- Qt 6.x MSVC x64

## Configurar

```powershell
cmake -S . -B build -DCMAKE_PREFIX_PATH="C:/Qt/6.x.x/msvc2022_64"
```

## Compilar

```powershell
cmake --build build --config Release
```

## Próxima etapa

Adicionar o SDK do FFmpeg ao processo de build e implementar FfmpegMediaEngine com libavformat, libavcodec, libavutil, libswscale e libswresample.
