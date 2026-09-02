# RB VideoFire 2.3.0 Professional Editing Reliability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar uma base 2.3.0 mais confiável para edição profissional antes de ampliar efeitos e recursos cosméticos.

**Architecture:** Evolução incremental sobre 2.2.1, mantendo módulos existentes e concentrando políticas editoriais em app/professional. Integrações devem ser pequenas, testáveis e sem refatorações laterais.

**Tech Stack:** C++, Qt, CMake, NSIS, GitHub Actions.

**Spec:** docs/superpowers/specs/2026-09-02-rb-videofire-2.3-professional-editing-reliability-design.md

## Global Constraints
- Preservar módulos já funcionais.
- Priorizar timeline, áudio, proxy e recovery.
- Sem regressões cosméticas ou reestruturações não relacionadas.
- Windows deve abrir sem janela de console.
- Instalador final: RB VideoFire Setup 2.3.0 Alpha Professional Editing Reliability.exe.

---

### Task 1: Versionamento e identidade 2.3.0
- [ ] Atualizar versão CMake para 2.3.0.
- [ ] Atualizar version.h para 2.3.0.0.
- [ ] Atualizar nome e texto do instalador.
- [ ] Atualizar tela Sobre para 2.3.0 Alpha Professional Editing Reliability.
- [ ] Compilar e validar metadados.

### Task 2: Política de sincronismo A/V
- [ ] Escrever teste que falha para drift acima de 1 frame.
- [ ] Implementar AVSyncPolicy com tolerância explícita.
- [ ] Cobrir tolerâncias 0, 1 e valores inválidos.
- [ ] Rodar testes gerais.

### Task 3: Trim profissional conectado ao fluxo existente
- [ ] Mapear chamadas atuais das ferramentas ripple e roll.
- [ ] Escrever teste de regressão para nudge de 1 frame.
- [ ] Conectar estado de trim ao comando real sem duplicar motor de edição.
- [ ] Testar lados A, B e ambos.
- [ ] Testar undo/redo.

### Task 4: Monitoramento de áudio e clipping
- [ ] Localizar origem do monitor de áudio atual.
- [ ] Criar teste para clipping em nível digital máximo.
- [ ] Corrigir atualização do monitor sem bloquear playback.
- [ ] Validar estéreo e layouts multicanal existentes.

### Task 5: Proxy editorial separado de render cache
- [ ] Escrever teste de estado original/proxy/offline.
- [ ] Separar nomenclatura Render Cache de Proxy Media.
- [ ] Garantir que desativar proxy restaure original.
- [ ] Não reutilizar cache como substituto de relink.

### Task 6: Recovery reforçado
- [ ] Confirmar defaults 1 minuto e 50 snapshots.
- [ ] Testar clamps.
- [ ] Validar recovery de alterações não salvas.
- [ ] Evitar sobrescrever projeto principal durante recuperação.

### Task 7: Build, regressão e artefato Windows
- [ ] Rodar build completo no GitHub Actions.
- [ ] Confirmar testes verdes.
- [ ] Confirmar startup sem console.
- [ ] Confirmar nome final do instalador.
- [ ] Verificar integridade do EXE e hash SHA-256.
