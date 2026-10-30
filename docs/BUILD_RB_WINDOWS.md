# Compilar RB Videofire no Windows

## Requisitos

Windows 10/11 x64, Visual Studio Build Tools 2022 com Desenvolvimento para desktop com C++ e Windows SDK, Rust via rustup, CMake, Python 3.12+, PowerShell 7 e LLVM x64 com libclang.dll. O computador precisa de conexão para baixar as dependências na primeira compilação, espaço em disco e tempo para compilar o motor e a interface.

O build utiliza Rust 1.93.1, conforme src/rust-toolchain.toml. O rustup instala essa versão quando o Cargo é executado em src. Se LLVM estiver em uma pasta personalizada, defina LIBCLANG_PATH para sua pasta bin.

## Compilar localmente

Abra compilar.bat. Ele configura o ambiente C++ x64, verifica os requisitos, baixa FFmpeg, ONNX Runtime e sherpa-onnx com os hashes de scripts/ci/deps.lock e compila a fonte. As dependências ficam em .rb-deps; nenhuma instalação Concat é usada ou movida.

O script prepara dist/RBVideofire e dist/RBVideofire-windows-x64-portatil.zip. Essa pasta dist é recriada em cada compilação: não guarde projetos nela. O pacote passa pelos testes --version e --smoke antes do ZIP ser criado.

Esse .bat é um compilador assistido. Ele não substitui o executável e não instala silenciosamente Visual Studio, Rust ou LLVM.

## Compilar pelo GitHub

Abra Actions, escolha RB Videofire Windows e execute o workflow na branch rebuild/rb-videofire-concat. O workflow também roda em pull requests. O artefato Windows inclui instalador .exe, pacote .msi e ZIP portátil. Os pacotes ainda não são assinados, salvo se houver certificado configurado no repositório.

O instalador .exe fala português brasileiro. Os atalhos apontam para RBVideofire.exe; há também um atalho de modo gráfico seguro, com --software. MSI e instalador usam identificadores diferentes dos do Concat.

## Verificar no notebook

Após compilar, confira a abertura normal e o modo gráfico seguro; importe vídeo com áudio, reproduza e faça seek; corte dois clipes; feche e reabra o projeto; exporte MP4 e confira imagem, duração e áudio. Verifique a identidade no menu iniciar, no ícone da janela, nas propriedades do executável e na desinstalação.

Recursos de IA exigem modelos opcionais e devem ser testados separadamente. Não há resultado de teste no notebook antes de essa execução ocorrer.
