# Reconstrução do RB Videofire sobre Concat

Autorização: o usuário escolheu derivar diretamente do Concat e exigiu a identidade do RB Videofire.

Base fixada: jub0t/Concat em f0c0169628c61de7311f7fc15ee5be82dd611d2e. Preservar o histórico anterior do rbvideofire2026, sem mesclar os motores C++ e Rust. Trabalho em branch própria com revisão por PR.

Produto: RB Videofire 3.0.0, Windows 10/11 x64, Rust/Slint/FFmpeg, processamento local. Aproveitar os módulos existentes de edição, áudio, efeitos, IA e exportação, sem alegar validação de recursos herdados que não foram executados.

Identidade: símbolo RB original em vetor, grafite e laranja, nome na janela, tela inicial, propriedades do executável, instaladores, atalhos e documentação. Português brasileiro por padrão, conservando a escolha posterior de idioma. Configurações independentes, sem mover os dados de instalações Concat.

Projetos novos: pasta com manifesto project.rbvf. Abrir pastas Concat legadas mantendo seus manifestos originais. Os antigos projetos C++ RB Videofire não possuem migração validada; não prometer compatibilidade apenas por compartilharem a extensão.

Distribuição: executável RBVideofire.exe, instalador em português e ZIP portátil; compilador .bat com pré-requisitos documentados. Atualizações consultam somente o repositório RB Videofire. Manter licença AGPL, autores e avisos de terceiros; remover identidade promocional da base da interface de produto.

Alternativas: reimplementar em C++/Qt teria custo elevado e duplicaria os módulos existentes; derivação Rust foi escolhida pelo usuário. Decisões de implementação: versão 3.0.0 distingue a reconstrução dos pacotes antigos; nomes internos concat-* permanecem para limitar riscos de integração.

Validação: conferir recursos visuais, inventário de tradução, Cargo metadata/format, testes de projeto/defaults e workflow Windows com smoke tests. Build Windows pendente até haver execução bem-sucedida no runner.
