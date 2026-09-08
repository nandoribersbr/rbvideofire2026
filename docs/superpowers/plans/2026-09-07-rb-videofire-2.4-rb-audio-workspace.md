# RB Audio Workspace 2.4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar uma aba de áudio profissional e funcional no RB VideoFire 2.4, integrada ao engine existente e sem copiar código GPL do Audacity.

**Architecture:** O workspace reutiliza a pipeline nativa do editor e adiciona medição, mixer, inspector e Effects Rack como camadas de UI/processamento conectadas aos mesmos objetos de timeline e playback. Dependências externas só entram atrás de interfaces próprias e após auditoria individual de licença.

**Tech Stack:** C++, Qt, CMake, NSIS, GitHub Actions, Windows 10/11 x64.

**Spec:** `docs/superpowers/specs/2026-09-07-rb-videofire-2.4-rb-audio-workspace-design.md`

## Global Constraints

- Não copiar código GPL do Audacity.
- Não criar segundo decoder ou pipeline de playback para alimentar meters/mixer.
- Preservar A/V sync, Undo/Redo, save/reopen e export.
- Audio Monitor usa dBFS real, piso -60 dBFS e clipping somente para valor finito >= 1.0.
- Build Windows continua WIN32 sem console antes da GUI.
- Release final exige 0 Blocker e 0 Critical.

---

### Task 1: Finalizar contrato G1 do Audio Meter

**Files:**
- Modify: `.github/scripts/test-rbvf-2.4-g1-audio.py`
- Modify: `.github/scripts/apply-rbvf-2.4.py`
- Modify: `.github/workflows/build-windows.yml`

**Interfaces:**
- Consumes: `AudioMeterPolicy::LinearToDbfs(double)`, `AudioMeterPolicy::IsClipping(double)`.
- Produces: contrato estável de conversão dBFS e clipping para as tarefas seguintes.

- [ ] **Step 1: Verificar que o run do commit `99b1e0e` passa o gate atual.**

Run: GitHub Actions do branch `rb-videofire-2.4.0-professional-workspace`.
Expected: run GREEN, build/test/package aprovados.

- [ ] **Step 2: Renomear o step obsoleto `G1 audio policy RED gate` para `G1 audio policy tests`.**

- [ ] **Step 3: Restaurar `Upload portable and symbols` se o tail do workflow estiver ausente.**

- [ ] **Step 4: Rodar CI novamente.**

Expected: todos os steps GREEN.

- [ ] **Step 5: Commit.**

```bash
git commit -m "test(audio): finalize G1 meter policy gate"
```

### Task 2: Descobrir e documentar o fluxo real de níveis do engine

**Files:**
- Create: `docs/superpowers/notes/2026-09-07-rbvf-audio-level-flow.md`
- Modify: `.github/scripts/apply-rbvf-2.4.py` only if source diagnostics are required.

**Interfaces:**
- Consumes: classes/sinais reais de playback e output de áudio do source base.
- Produces: nomes exatos de classes, signals/slots e ponto de conexão do Audio Monitor.

- [ ] **Step 1: Localizar no source as classes de Audio Monitor, output, playback e level/meter.**

Search terms: `AudioMonitor`, `AudioMeter`, `meter`, `audio output`, `samples`, `peak`, `MainWindow`, `Panel`.

- [ ] **Step 2: Registrar a cadeia real de dados do engine.**

Expected note must identify source of samples/levels, update cadence, thread context and existing UI target.

- [ ] **Step 3: Verificar que a integração pode consumir dados existentes sem decoder paralelo.**

Expected: um único caminho de playback.

- [ ] **Step 4: Commit.**

```bash
git commit -m "docs(audio): map native audio level flow"
```

### Task 3: Conectar o Audio Monitor ao engine real

**Files:**
- Modify: exact Audio Monitor source identified in Task 2.
- Modify: exact playback/output source identified in Task 2 only where necessary.
- Test: add focused test/contract under existing test structure discovered in source.

**Interfaces:**
- Consumes: real per-channel level data from native engine.
- Produces: live stereo meter input, no simulated values.

- [ ] **Step 1: Escrever teste que falha sem a conexão real.**

The test must assert that the monitor subscribes/consumes the existing engine level path and that no second decoder is instantiated.

- [ ] **Step 2: Rodar e confirmar RED.**

Expected: FAIL because integration is not present.

- [ ] **Step 3: Implementar a conexão mínima.**

Requirements: L/R independent, queued/thread-safe update where required by Qt, no blocking playback.

- [ ] **Step 4: Rodar teste e confirmar GREEN.**

- [ ] **Step 5: Commit.**

```bash
git commit -m "audio: connect native levels to Audio Monitor"
```

### Task 4: Medidor stereo profissional

**Files:**
- Modify: Audio Monitor widget/panel identified in Task 2.
- Modify: `app/professional/professionalcore.h` only if policy helper remains there.
- Test: focused meter tests.

**Interfaces:**
- Consumes: L/R real values from Task 3.
- Produces: visual meter -60..0 dBFS, peak hold and clipping.

- [ ] **Step 1: Escrever testes de peak hold e expiry com tempo determinístico.**

Cases: retain highest peak for 1500 ms; release after expiry; invalid sample does not extend peak.

- [ ] **Step 2: Confirmar RED.**

- [ ] **Step 3: Implementar estado de peak hold com timestamp explícito.**

- [ ] **Step 4: Implementar visual L/R com escala 0, -6, -12, -20, -40, -60 dBFS.**

- [ ] **Step 5: Implementar clipping visual por canal.**

- [ ] **Step 6: Testar play/pause/seek/scrub e painel fechado/aberto.**

- [ ] **Step 7: Commit.**

```bash
git commit -m "ui(audio): add professional stereo meter"
```

### Task 5: Mixer de faixas e Master Bus

**Files:**
- Create/Modify: focused mixer widget files following existing panel conventions discovered in source.
- Modify: timeline/audio parameter model only through existing APIs.
- Test: focused mixer behavior tests.

**Interfaces:**
- Consumes: track gain/pan/mute/solo APIs already used by the engine, or adds minimal model properties if missing.
- Produces: per-track fader, pan, mute, solo, meter and master channel.

- [ ] **Step 1: Escrever teste para mute/solo/volume/pan persistirem no projeto.**

- [ ] **Step 2: Confirmar RED.**

- [ ] **Step 3: Implementar canal de mixer usando propriedades reais da faixa.**

- [ ] **Step 4: Implementar Master Bus conectado ao output real.**

- [ ] **Step 5: Integrar Undo/Redo onde a alteração for editorial.**

- [ ] **Step 6: Save/reopen regression.**

- [ ] **Step 7: Commit.**

```bash
git commit -m "audio: add track mixer and master bus"
```

### Task 6: Inspector e Effects Rack inicial

**Files:**
- Create/Modify: audio inspector/effects rack files following discovered UI conventions.
- Modify: audio effect registration only through existing effect/plugin architecture.
- Test: effect parameter persistence tests.

**Interfaces:**
- Consumes: selected clip/track and effect model.
- Produces: clip gain, fade, normalize, pan/balance, phase and first effect chain.

- [ ] **Step 1: Escrever teste de persistência de clip gain e ordem da cadeia de efeitos.**

- [ ] **Step 2: Confirmar RED.**

- [ ] **Step 3: Implementar Inspector de Áudio mínimo.**

- [ ] **Step 4: Implementar Effects Rack com ordem explícita e bypass.**

- [ ] **Step 5: Integrar primeiro conjunto seguro: Gain, Normalize, high-pass, low-pass.**

- [ ] **Step 6: Adicionar compressor, limiter, EQ paramétrico, gate e de-esser apenas por implementação própria ou dependência permissiva auditada.**

- [ ] **Step 7: Commit.**

```bash
git commit -m "audio: add inspector and effects rack"
```

### Task 7: Auditoria de dependências permissivas

**Files:**
- Create: `docs/licenses/rb-audio-third-party-audit.md`
- Modify: dependency manifests only for approved libraries.

**Interfaces:**
- Consumes: candidate libraries.
- Produces: approved/rejected list with license and usage boundary.

- [ ] **Step 1: Registrar nome, versão, licença, upstream e finalidade de cada candidato.**

- [ ] **Step 2: Rejeitar qualquer dependência GPL/AGPL para ligação direta ao produto nesta arquitetura.**

- [ ] **Step 3: Integrar somente candidatos permissivos aprovados.**

- [ ] **Step 4: Commit.**

```bash
git commit -m "docs(audio): audit permissive audio dependencies"
```

### Task 8: Workspace de áudio e persistência de layout

**Files:**
- Modify: main window/workspace files discovered from native source.
- Modify/Create: RB Audio Workspace panel arrangement.
- Test: workspace persistence test where supported.

**Interfaces:**
- Consumes: Audio Monitor, Mixer, Inspector, Effects Rack.
- Produces: workspace `Áudio` profissional e dockável.

- [ ] **Step 1: Escrever teste/contract para presença dos painéis do workspace.**

- [ ] **Step 2: Confirmar RED.**

- [ ] **Step 3: Implementar layout 1920x1080 com Mixer, Master, Monitor, Inspector e Timeline.**

- [ ] **Step 4: Persistir posição/tamanho dos docks usando mecanismo existente.**

- [ ] **Step 5: Confirmar que o workspace editorial padrão não sofre regressão.**

- [ ] **Step 6: Commit.**

```bash
git commit -m "ui(audio): add RB Audio Workspace"
```

### Task 9: Regressão, empacotamento e EXE

**Files:**
- Modify: `.github/workflows/build-windows.yml` only as required for validation/artifacts.
- Create: gate reports under build artifacts where practical.

**Interfaces:**
- Consumes: complete 2.4 audio implementation.
- Produces: Windows installer artifact.

- [ ] **Step 1: Rodar unit/integration tests.**

Expected: 100% pass.

- [ ] **Step 2: Rodar fluxo editorial de aceitação.**

`import MP4/MOV -> playback -> L/R meter -> gain/pan -> mute/solo -> effect -> save -> reopen -> export`

- [ ] **Step 3: Verificar A/V sync, Undo/Redo e export sem regressão.**

- [ ] **Step 4: Smoke test de inicialização sem console e fechamento pelo X sem processo órfão.**

- [ ] **Step 5: Gerar instalador Windows e SHA-256.**

Expected installer name: `RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe`.

- [ ] **Step 6: Upload do installer e portable/symbols.**

- [ ] **Step 7: Commit final se necessário.**

```bash
git commit -m "release: qualify RB VideoFire 2.4 audio workspace"
```
