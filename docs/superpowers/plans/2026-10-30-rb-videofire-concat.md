# RB Videofire Concat Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** reconstruir RB Videofire com o motor Concat e identidade própria.
**Architecture:** preservar os crates Rust; adaptar a interface e a identidade do host e do Windows. Preservar os dois históricos Git em uma branch própria.
**Tech Stack:** Rust 1.93.1, Slint 1.18, FFmpeg, Python, Inno Setup, WiX.
**Spec:** docs/superpowers/specs/2026-10-30-rb-videofire-concat-design.md

## Global Constraints

Windows 10/11 x64; português brasileiro inicial; AGPL-3.0-or-later; manter copyright original; não migrar diretórios Concat; não sobrescrever main.

## Review Focus

Instalação paralela ao Concat deve manter configurações separadas.
Abrir e salvar pastas legadas deve preservar seu manifesto.
Atualizações não podem substituir o produto por uma versão Concat ou RB antiga.
Pacote deve incluir DLLs e ícones, com atalhos para o executável correto.
Idioma escolhido pelo usuário deve sobreviver ao reinício.

### Task 1: Identidade e isolamento
- [x] Adaptar src/crates/concat/src/{prefs,studio,platform,main,launch}.rs e panes/{start,settings}.rs: idioma inicial pt-BR, nome e links RB.
- [x] Adaptar src/crates/concat-host/src/{dirs,updates}.rs: namespace independente e origem própria de atualizações.
- [x] Preservar os nomes de crates, APIs e créditos técnicos.

### Task 2: Interface e projetos
- [x] Criar assets/rb-videofire.svg e ícones; aplicar em app.slint e title-bar.slint, catálogo de traduções e paleta Fire.
- [x] Atualizar build.rs e Cargo.toml: binário RBVideofire e versão 3.0.0.
- [x] Testar criação e reabertura de project.rbvf e leitura legada antes de adaptar projects.rs.

### Task 3: Windows e entrega
- [x] Adaptar build-app.yml para Windows x64 e criar entrada de CI; preservar verificações dos binários e hashes das dependências.
- [x] Atualizar instaladores, GUIDs, idioma e atalhos; adicionar ZIP portátil, iniciar.bat e compilar.bat.
- [x] Documentar origem, build e limitações; conferir traduções, recursos, formato, testes e diff.
- [ ] Publicar a branch e abrir PR sem mesclar main. Relatar resultados reais e verificações pendentes.
