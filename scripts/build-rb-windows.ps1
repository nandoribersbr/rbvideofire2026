#Requires -Version 7
# Compila a fonte local e prepara um pacote independente de Qt e de instalacoes Concat.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
foreach ($command in @('cargo', 'rustup', 'cmake', 'python', 'cl')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Ferramenta ausente: $command. Consulte docs/BUILD_RB_WINDOWS.md."
    }
}
if (-not $env:LIBCLANG_PATH) { $env:LIBCLANG_PATH = "$env:ProgramFiles\LLVM\bin" }
if (-not (Test-Path "$env:LIBCLANG_PATH\libclang.dll")) {
    throw 'Instale LLVM x64 ou defina LIBCLANG_PATH para a pasta que contem libclang.dll.'
}
$env:PATH = "$env:LIBCLANG_PATH;$env:PATH"
$deps = Join-Path $root '.rb-deps'
New-Item -ItemType Directory -Force $deps | Out-Null
function Get-PinnedDependency([string]$name, [string]$filename) {
    $rows = @(Get-Content scripts/ci/deps.lock | Where-Object { $_ -match "^$([regex]::Escape($name))\s+" })
    if ($rows.Count -ne 1) { throw "Dependencia nao encontrada no manifesto: $name" }
    $row = $rows[0] -split '\s+'
    $file = Join-Path $deps $filename
    if ((Test-Path $file) -and (Get-FileHash $file -Algorithm SHA256).Hash.ToLowerInvariant() -eq $row[2]) { return $file }
    Write-Host "Baixando $name..."
    Invoke-WebRequest -UseBasicParsing -Uri $row[1] -OutFile $file
    if ((Get-FileHash $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $row[2]) {
        Remove-Item $file
        throw "SHA-256 incorreto em $name. A compilacao foi interrompida."
    }
    return $file
}
$ff = Get-PinnedDependency 'ffmpeg-win64' 'ffmpeg.zip'
$ffRoot = Join-Path $deps 'ffmpeg'
if (-not (Test-Path $ffRoot)) { Expand-Archive -LiteralPath $ff -DestinationPath $ffRoot }
$env:FFMPEG_DIR = (Get-ChildItem $ffRoot -Directory | Select-Object -First 1).FullName
$ort = Get-PinnedDependency 'onnxruntime-win-x64' 'onnxruntime.zip'
$ortRoot = Join-Path $deps 'onnxruntime-win-x64-1.28.0'
if (-not (Test-Path $ortRoot)) { Expand-Archive -LiteralPath $ort -DestinationPath $deps }
$env:ORT_LIB_LOCATION = Join-Path $ortRoot 'lib'
$env:ORT_PREFER_DYNAMIC_LINK = '1'
$sherpa = Get-PinnedDependency 'sherpa-onnx-win-x64-shared-MT-Release-lib' 'sherpa.tar.bz2'
$sherpaRoot = Join-Path $deps 'sherpa-onnx-v1.13.7-win-x64-shared-MT-Release-lib'
if (-not (Test-Path $sherpaRoot)) {
    python -c "import sys,tarfile; tarfile.open(sys.argv[1]).extractall(sys.argv[2], filter='data')" $sherpa $deps
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao extrair sherpa-onnx. E necessario Python 3.12 ou mais recente.' }
}
$libs = Join-Path $deps 'sherpa-libs'
New-Item -ItemType Directory -Force $libs | Out-Null
Copy-Item "$sherpaRoot\lib\sherpa-onnx-*.lib" $libs -Force
$env:SHERPA_ONNX_LIB_DIR = $libs
$env:PATH = "$env:FFMPEG_DIR\bin;$env:ORT_LIB_LOCATION;$sherpaRoot\lib;$env:PATH"
$env:GGML_NATIVE = 'OFF'
$env:GGML_BACKEND_DL = 'ON'
$env:GGML_CPU_ALL_VARIANTS = 'ON'
$env:GGML_AVX2 = 'OFF'
$env:GGML_FMA = 'OFF'
$env:GGML_F16C = 'OFF'
$env:GGML_BMI2 = 'OFF'
Push-Location src
try {
    cargo build --locked --profile app -p concat
    if ($LASTEXITCODE -ne 0) { throw 'Falha na compilacao Rust.' }
} finally { Pop-Location }
$dest = Join-Path $root 'dist\RBVideofire'
# A pasta de distribuicao e exclusiva do build, nunca uma pasta de projetos.
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
New-Item -ItemType Directory -Force "$dest\portable" | Out-Null
Copy-Item 'src\target\app\RBVideofire.exe' $dest
Copy-Item "$env:FFMPEG_DIR\bin\*.dll", "$env:ORT_LIB_LOCATION\*.dll", "$sherpaRoot\lib\sherpa-onnx-*.dll" $dest
$whisper = Get-ChildItem 'src\target\app\build\whisper-rs-sys-*\out\bin\ggml-cpu-x64.dll' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $whisper) { throw 'As bibliotecas dinamicas do Whisper nao foram geradas.' }
Copy-Item "$($whisper.DirectoryName)\whisper.dll", "$($whisper.DirectoryName)\ggml*.dll" $dest
$crt = Get-ChildItem "$env:RB_VS\VC\Redist\MSVC\*\x64\Microsoft.VC14*.CRT" -Directory | Sort-Object FullName -Descending | Select-Object -First 1
if (-not $crt) { throw 'Bibliotecas redistribuiveis do Visual C++ nao encontradas.' }
Copy-Item "$($crt.FullName)\*.dll" $dest
Copy-Item LICENSE, THIRD_PARTY_NOTICES.md, NOTICE_RB_VIDEOFIRE.md, iniciar.bat $dest
Copy-Item assets/icons/rb-videofire.ico $dest
Set-Content "$dest\portable\LEIA-ME.txt" 'Configuracoes e modelos desta copia portatil ficam nesta pasta.'
& scripts/ci/smoke-windows.ps1 -Bundle $dest
if ($LASTEXITCODE -ne 0) { throw 'O pacote nao passou no teste de inicializacao.' }
Compress-Archive -Path "$dest\*" -DestinationPath 'dist\RBVideofire-windows-x64-portatil.zip' -Force
Write-Host "Pacote gerado e testado em $dest"
