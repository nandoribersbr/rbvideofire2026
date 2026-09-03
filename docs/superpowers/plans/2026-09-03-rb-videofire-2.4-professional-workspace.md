# RB VideoFire 2.4.0 Professional Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar um workspace profissional RB VideoFire com melhor hierarquia editorial e Audio Monitor funcional.

**Architecture:** Evolução incremental sobre 2.3.0. Reutilizar motor de playback, áudio e comandos editoriais existentes; mudanças de interface devem conectar-se ao fluxo nativo e permanecer pequenas e testáveis.

**Tech Stack:** C++, Qt, CMake, NSIS, GitHub Actions.

**Spec:** docs/superpowers/specs/2026-09-03-rb-videofire-2.4-professional-workspace-design.md

## Global Constraints
- Preservar o núcleo funcional 2.3.0.
- Não criar pipeline de áudio paralelo.
- Não duplicar motor de edição para suportar a UI.
- Windows deve abrir sem console.
- Nome final: RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe.

---

### Task 1: Versionamento e contrato 2.4
- [ ] Criar validador RED da identidade 2.4.
- [ ] Atualizar CMake/version.h/Sobre/NSIS.
- [ ] Validar identidade e startup WIN32.

### Task 2: Workspace editorial padrão
- [ ] Mapear criação/restauração dos docks existentes.
- [ ] Escrever validação do layout padrão.
- [ ] Dar prioridade espacial ao Program Monitor e Timeline.
- [ ] Retirar Node Editor do workspace editorial inicial sem removê-lo do menu.
- [ ] Preservar layout customizável.

### Task 3: Audio Monitor
- [ ] Localizar sinal/slot ou modelo que fornece níveis atuais.
- [ ] Escrever teste RED para conversão/limite dBFS e clipping.
- [ ] Conectar medidor ao pipeline existente sem bloquear playback.
- [ ] Implementar peak hold e clipping visual.
- [ ] Validar estéreo e ausência de regressão multicanal.

### Task 4: Tools e Timeline UX
- [ ] Mapear comandos existentes para Selection/Ripple/Roll/Razor/Slip/Slide/Hand/Zoom.
- [ ] Adicionar tooltips e atalhos sem criar comandos duplicados.
- [ ] Melhorar legibilidade dos controles de tracks e timeline.
- [ ] Validar undo/redo dos comandos existentes.

### Task 5: Project Bin e Inspector
- [ ] Manter lista/thumbnails existentes.
- [ ] Tornar importação mais evidente.
- [ ] Expor metadados disponíveis sem nova indexação pesada.
- [ ] Renomear Parameter Editor para Inspector na camada de apresentação quando seguro.

### Task 6: PT-BR e identidade visual
- [ ] Padronizar rótulos principais do workspace em PT-BR.
- [ ] Preservar catálogos dos demais idiomas.
- [ ] Auditar referências Olive visíveis no workspace e remover apenas branding residual seguro.

### Task 7: Build Windows e regressão
- [ ] Rodar validadores RED/GREEN no GitHub Actions.
- [ ] Compilar com BUILD_TESTS=ON.
- [ ] Rodar CTest.
- [ ] Executar startup smoke test.
- [ ] Gerar e auditar instalador.
- [ ] Publicar artefato do EXE e calcular SHA-256.
