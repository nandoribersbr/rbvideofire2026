# RB VideoFire 2.1.0 Alpha Editorial — Branding e Build Windows

## Objetivo
Gerar um instalador Windows real do RB VideoFire 2.1.0 Alpha Editorial com identidade pública própria, usando o ícone cinematográfico RB VideoFire aprovado e preservando o núcleo C++/Qt funcional existente.

## Escopo aprovado
- Aplicar o ícone cinematográfico RB VideoFire ao executável e ao instalador Windows.
- Remover da interface, metadados do executável, nomes de produto e textos públicos referências visíveis a Olive.
- Manter atribuições, copyright, GPLv3 e avisos de origem que sejam legalmente necessários no código-fonte e documentação de licenciamento.
- Não renomear em massa namespaces internos `olive::`, classes ou APIs apenas por branding, evitando regressões no núcleo.
- Atualizar versão pública e de empacotamento para `2.1.0 Alpha Editorial`.
- Preservar Source Monitor, Program Monitor, Insert/Overwrite e atalhos J/K/L já funcionais.
- Compilar com GitHub Actions em Windows x64 e publicar o instalador como artifact.

## Arquitetura
A edição continua sendo C++/Qt nativa. A limpeza de identidade ocorre nas camadas públicas: recursos Windows, metadados, títulos, strings visíveis e NSIS. Dependências e símbolos internos de upstream permanecem quando sua alteração não traz benefício funcional ou cria risco de regressão.

## Ícone
Ativo aprovado: `Logo Cinematográfico RB VideoFire.png`, com monograma RB vermelho/prata, película e identidade VideoFire. O build deve produzir recurso `.ico` multirresolução apropriado para Windows e usá-lo no executável/instalador.

## Estratégia de build
O workflow extrai o pacote-fonte cumulativo, aplica/valida a identidade 2.1, configura CMake/Ninja/MSVC, executa testes, usa `windeployqt`, inclui DLLs necessárias, executa auditoria de pacote e gera o instalador NSIS.

## Testes e auditoria
Antes do empacotamento, um contrato automatizado deve verificar:
1. versão 2.1.0;
2. Source Monitor e Program Monitor;
3. ausência de `Record Monitor` e `Reveal in Footage Viewer` nas strings públicas alvo;
4. metadados Windows RB VideoFire / RB8 Digital;
5. nome do instalador 2.1.0 Alpha Editorial;
6. presença do ícone RB VideoFire;
7. preservação da licença GPL e atribuições legais.

Após a compilação, o workflow deve falhar se `RBVideoFire.exe` ou o instalador esperado não forem produzidos.

## Entrega
Artifact principal: `RB VideoFire Setup 2.1.0 Alpha Editorial.exe`.
Artifact secundário: pacote portable 2.1.0 e símbolos de depuração quando emitidos.
