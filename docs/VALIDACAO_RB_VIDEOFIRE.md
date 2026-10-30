# Registro de validação da reconstrução

Base Concat: f0c0169628c61de7311f7fc15ee5be82dd611d2e. Revisão da identidade em 30/10/2026.

## Executado neste ambiente

- concat-core: 64 testes aprovados.
- concat-project: 191 testes aprovados.
- Exemplos de documentação: 2 aprovados.
- Harness com os arquivos reais projects.rs e dirs.rs: 19 testes aprovados, incluindo manifesto nativo, leitura legada, salvamentos concorrentes e isolamento dos dados Concat.
- Regressão do manifesto: falhou ao restaurar concat.json como nome padrão, passou com project.rbvf.
- Cargo metadata --locked: executável RBVideofire e versão 3.0.0 reconhecidos.
- cargo fmt --all --check: aprovado após normalização automática de formatação de arquivos herdados.
- Inventário de tradução: português brasileiro com 951 entradas, sem chaves ausentes ou obsoletas. Termos técnicos como codec, LUT e proxies podem coincidir com o inglês.
- YAML dos workflows, XML do MSI e ICO com sete tamanhos: leitura estrutural aprovada.
- Revisão técnica independente: detectou incompatibilidade entre Windows PowerShell 5.1 e smoke que exige PowerShell 7. O .bat foi corrigido para exigir e executar pwsh.exe e o requisito foi documentado.

## Pendente de execução no Windows

A suíte completa concat-host não chegou à execução local: a compilação de openssl-sys parou por falta de pkg-config e bibliotecas de desenvolvimento nativas do ambiente. Isso não é resultado de falha nos testes do aplicativo.

O workflow executa a suíte completa e produz os pacotes Windows, com testes de inicialização, DLLs e baseline de CPU. Os instaladores, interface em execução, reprodução e exportação no notebook precisam de resultados reais antes de serem declarados validados. O .bat também depende desses testes em Windows.

Os projetos antigos C++ RB Videofire ainda não possuem migração validada. Os recursos herdados de IA não foram exercitados neste ambiente.
