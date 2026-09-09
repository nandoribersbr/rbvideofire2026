# RB VideoFire M3 Resolve-Class Editorial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar um M3 funcional com precisão editorial, multicâmera base e presets de Inspector sobre o motor nativo do RB VideoFire.

**Architecture:** Reutilizar Timeline, ViewerOutput, Project, Node Graph e undo stack existentes. Novas ações editoriais serão adaptadores pequenos sobre comandos reais; multicam será um modelo de sequência/ângulo persistente que aponta para mídia já importada, e presets do Inspector serializarão parâmetros existentes sem criar um segundo sistema de efeitos.

**Tech Stack:** C++17, Qt, KDDockWidgets, CMake, CTest, Python contract tests, GitHub Actions Windows, NSIS.

**Spec:** `docs/superpowers/specs/2026-09-09-rb-videofire-resolve-class-professional-suite-design.md`

## Global Constraints
- Base: RB VideoFire 2.4.0 Workspace M2 + Audio Monitor M1.
- Branch: `rb-videofire-2.4.0-m3-editorial-precision`.
- Não criar segunda timeline, segundo decoder ou controles decorativos.
- Toda mutação de projeto usa undo/redo quando aplicável e persiste em save/reopen.
- Multicam deve manter arquitetura para pelo menos 25 ângulos; seleção de tracks para pelo menos 32 tracks.
- Nenhum recurso posterior M4-M11 será simulado no M3.
- Release Windows final: CTest verde, startup smoke, package audit, PE GUI/no-console e zero Blocker/Critical conhecido.

---

### Task 1: Gate RED e mapa do motor editorial
**Files:**
- Create: `.github/scripts/test-rbvf-m3-editorial-contract.py`
- Create: `docs/superpowers/notes/2026-09-09-rbvf-m3-native-editorial-map.md`
- Inspect: `app/panel/timeline/`, `app/widget/timeline/`, `app/window/mainwindow/`, `app/core/`.

**Interfaces:**
- Consumes: classes nativas de timeline, viewer, undo e shortcuts.
- Produces: contrato `M3_REQUIRED_ACTIONS` e mapa exato dos pontos de integração.

- [ ] **Step 1: escrever teste RED** com asserts para `selection`, `ripple`, `roll`, `razor`, `slip`, `slide`, `jkl`, `insert`, `overwrite`, `lift`, `extract`, `marker`, `multicam`, `inspector_preset`.
- [ ] **Step 2: executar** `python .github/scripts/test-rbvf-m3-editorial-contract.py --source .` e confirmar falha nos contratos M3 ainda ausentes.
- [ ] **Step 3: documentar** classe, arquivo, thread e undo path reais para cada ação já existente.
- [ ] **Step 4: commit** `test(editorial): add M3 RED contract and native map`.

### Task 2: Trim, nudge e ferramentas de timeline
**Files:**
- Modify: arquivos TimelinePanel/TimelineWidget encontrados na Task 1.
- Test: `.github/scripts/test-rbvf-m3-editorial-contract.py`.

**Interfaces:**
- Produces: `NudgeSelectedEdit(int frames)`, `TrimSelectedEdit(side, int frames)` ou equivalentes nativos descobertos, sempre operando em unidades do timebase do projeto.

- [ ] **Step 1: ampliar RED** para nudge `+1/-1 frame`, Ripple/Roll e Undo/Redo.
- [ ] **Step 2: executar RED** e registrar a falha esperada.
- [ ] **Step 3: implementar mínimo** ligando Selection/Ripple/Roll/Razor/Slip/Slide aos comandos existentes e nudge ao frame rate ativo.
- [ ] **Step 4: executar GREEN** e CTest relacionado.
- [ ] **Step 5: commit** `feat(editorial): add frame accurate trim and nudge`.

### Task 3: Transporte e edição de três pontos
**Files:**
- Modify: MainWindow actions/shortcut files e TimelinePanel encontrados na Task 1.

**Interfaces:**
- Produces: ações J/K/L, go-to-in/out, insert, overwrite, lift e extract usando o Viewer/Timeline atuais.

- [ ] **Step 1: RED** para bindings e chamadas reais.
- [ ] **Step 2: implementar** J reverso, K stop, L forward, incluindo repetição de J/L para shuttle somente se o playback nativo suportar velocidades múltiplas; caso contrário limitar a 1x sem UI falsa.
- [ ] **Step 3: implementar** insert/overwrite/lift/extract no modelo de edição existente com undo.
- [ ] **Step 4: GREEN** e regressão play/pause/seek.
- [ ] **Step 5: commit** `feat(editorial): add professional transport and three point editing`.

### Task 4: Track controls e linked A/V
**Files:**
- Modify: track header/model e selection model reais.

**Interfaces:**
- Produces: targeting, lock, sync lock e linked A/V apenas onde houver efeito real no modelo.

- [ ] **Step 1: RED** para lock impedir mutação e linked A/V preservar relação em ripple/delete.
- [ ] **Step 2: implementar** controles ligados ao estado da track, com capacidade estrutural de 32 tracks.
- [ ] **Step 3: testar** linked/unlinked, ripple, delete, undo e save/reopen.
- [ ] **Step 4: GREEN**.
- [ ] **Step 5: commit** `feat(editorial): add track targeting sync and linked av controls`.

### Task 5: Markers e legibilidade editorial
**Files:**
- Modify: ruler/marker/project serialization existentes.

**Interfaces:**
- Produces: add/remove/next/previous marker, nome/cor quando o modelo suportar, duração de clip opcional e waveform fit-to-track-height.

- [ ] **Step 1: RED** para marker round-trip e navegação.
- [ ] **Step 2: implementar** markers no modelo persistente e comandos de navegação.
- [ ] **Step 3: implementar** duração opcional junto ao nome do clip e waveform escalada à altura disponível sem alterar amostras.
- [ ] **Step 4: GREEN**, save/reopen e undo/redo.
- [ ] **Step 5: commit** `feat(editorial): add markers and timeline readability controls`.

### Task 6: Multicam base funcional
**Files:**
- Create: `app/multicam/multicammodel.h`
- Create: `app/multicam/multicammodel.cpp`
- Modify: Project serialization, Source/Program viewer integration e TimelinePanel conforme mapa.
- Test: CTest unit para multicam + contract Python.

**Interfaces:**
- `MulticamAngle { QString media_id; int angle_index; }`
- `MulticamSequence { QVector<MulticamAngle> angles; int active_angle; }`
- `SwitchAngle(int angle_index, rational time)` cria uma decisão editorial real na timeline/sequence e entra no undo stack.

- [ ] **Step 1: RED** para criar sequência com 2, 25 e rejeitar índice fora do intervalo.
- [ ] **Step 2: implementar modelo** com limite arquitetural mínimo de 25 ângulos.
- [ ] **Step 3: RED** para sincronização por timecode quando metadata existe e fallback explícito quando não existe.
- [ ] **Step 4: implementar** Source/Program multicam e troca de ângulo por shortcut sem perder playhead.
- [ ] **Step 5: testar** save/reopen, undo, playback e A/V sync.
- [ ] **Step 6: commit** `feat(multicam): add native multicam editorial foundation`.

### Task 7: Inspector presets
**Files:**
- Create: `app/inspector/preset/inspectorpreset.h`
- Create: `app/inspector/preset/inspectorpreset.cpp`
- Modify: Inspector/Parameter Editor existentes e Project/User settings conforme escopo do preset.

**Interfaces:**
- `InspectorPreset { QString name; QString category; QVariantMap parameters; }`
- Categorias: `video`, `audio`, `transform`, `transition`.
- Aplicação usa propriedades reais já expostas pelo Inspector e uma única macro de undo.

- [ ] **Step 1: RED** para save/load/apply e rejeição de parâmetro desconhecido.
- [ ] **Step 2: implementar** serialização versionada e aplicação segura.
- [ ] **Step 3: adicionar** UI salvar/aplicar/excluir preset sem duplicar parâmetros.
- [ ] **Step 4: testar** persistência entre projetos conforme tipo de preset e undo da aplicação.
- [ ] **Step 5: commit** `feat(inspector): add persistent professional presets`.

### Task 8: Preferências editoriais M3
**Files:**
- Modify: settings/preferences existentes.

**Interfaces:**
- Produces: `stop_playback_while_dragging`, `audio_while_frame_step`, `select_clip_after_razor` como flags persistentes conectadas aos comportamentos reais.

- [ ] **Step 1: RED** para defaults e persistência.
- [ ] **Step 2: implementar** flags e pontos de consumo reais.
- [ ] **Step 3: GREEN** com restart/reopen.
- [ ] **Step 4: commit** `feat(editorial): add professional editing preferences`.

### Task 9: Regressão M3 e qualificação Windows
**Files:**
- Create: `.github/scripts/test-rbvf-m3-regression.py`
- Create/Modify: `.github/workflows/build-m3-editorial-windows.yml`.

**Interfaces:**
- Produces: artifact `RB-VideoFire-2.4.0-M3-Editorial-Installer`.

- [ ] **Step 1: gate** verificar aplicação cumulativa M1 + M2 + M3.
- [ ] **Step 2: executar** contract tests e CTest.
- [ ] **Step 3: compilar** Release x64 com subsystem GUI.
- [ ] **Step 4: startup smoke** abrir processo, verificar janela e encerramento sem processo órfão.
- [ ] **Step 5: regressão** import/playback/audio/timeline/trim/undo/save-reopen/multicam/Inspector preset/export path.
- [ ] **Step 6: package audit** identidade RB, ausência de Olive em recursos visíveis, PE válido e sem console.
- [ ] **Step 7: empacotar** `RB VideoFire Setup 2.4.0 Alpha M3 Editorial Precision.exe`.
- [ ] **Step 8: calcular** SHA-256 do EXE extraído e publicar installer + portable/symbols.
- [ ] **Step 9: commit** `build: qualify RB VideoFire 2.4 M3 Editorial Precision`.

## Self-review
- Cobertura: todos os itens M3 da spec estão associados às Tasks 2-8; Task 9 cobre Definition of Done.
- Escopo: M4-M11 permanecem fora deste plano e não recebem UI simulada.
- Tipos: multicam e Inspector presets possuem interfaces explícitas neste plano; demais nomes finais seguem as APIs nativas mapeadas na Task 1 para evitar inventar assinaturas incompatíveis antes da inspeção.
- Licenciamento: nenhuma dependência nova é necessária para M3.