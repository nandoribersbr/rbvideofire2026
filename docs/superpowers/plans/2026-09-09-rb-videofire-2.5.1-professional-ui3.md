# RB VideoFire 2.5.1 Professional UI 3.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a stable, distinctly RB VideoFire workspace system that never moves the application window, preserves per-workspace customization and gives each professional task a clearly different internal layout.

**Architecture:** Extend the existing RBProfessionalShell instead of replacing native editor engines. Split window geometry persistence from per-workspace dock-state persistence, introduce deterministic workspace defaults, and apply a shell-scoped RB visual hierarchy. Existing native QAction and dock widgets remain the functional backend.

**Tech Stack:** C++17, Qt Widgets, QMainWindow/QDockWidget/QSettings/QAction, CMake/Ninja, NSIS, Python source-contract tests, GitHub Actions Windows x64.

**Spec:** `docs/superpowers/specs/2026-09-09-rb-videofire-2.5.1-professional-ui3-design.md`

## Global Constraints
- Do not resize or move the top-level window during workspace switching.
- One persisted dock-state payload per workspace.
- Preserve native playback, timeline, media, project, undo and audio engines.
- No fake enabled commands.
- Assistente stays disabled until its backend exists.
- M3/M4/Audio M1 regressions must remain green.
- Target: `RB VideoFire 2.5.1 Alpha Professional UI 3.0`.

---

### Task 1: Geometry stability contract
**Files:**
- Create: `.github/scripts/test-rbvf-2.5.1-ui3.py`
- Modify through cumulative patch: `app/shell/rbprofessionalshell.h`, `app/shell/rbprofessionalshell.cpp`

**Interfaces:**
- Produces `QByteArray WorkspaceStateKey(RBWorkspace workspace)` or equivalent deterministic per-workspace key.
- Produces `SaveCurrentWorkspaceState()` and `RestoreWorkspaceState(RBWorkspace)`.

- [ ] Write a failing source contract requiring `WorkspaceStates`, per-workspace save/restore, and forbidding top-level `resize(`, `move(` and `restoreGeometry(` inside `ApplyWorkspace`.
- [ ] Run the contract against the 2.5.0 shell and verify RED.
- [ ] Implement per-workspace dock-state storage using `QMainWindow::saveState()`/`restoreState()` only.
- [ ] Capture current workspace state before switching and restore/apply the target state after switching.
- [ ] Run contract and verify GREEN.
- [ ] Commit `fix: keep RB workspace switching inside window geometry`.

### Task 2: Deterministic workspace defaults
**Files:**
- Modify: cumulative UI3 patch script and generated `rbprofessionalshell.cpp`.

**Interfaces:**
- Produces `ApplyDefaultMediaLayout`, `ApplyDefaultEditLayout`, `ApplyDefaultCompositionLayout`, `ApplyDefaultColorLayout`, `ApplyDefaultAudioLayout`, `ApplyDefaultDeliveryLayout`.

- [ ] Extend RED contract to require six distinct default-layout functions and distinct dominant panel tokens.
- [ ] Verify RED.
- [ ] Implement Mídia with Project/Media + Source/metadata priority and minimized timeline.
- [ ] Implement Edição with Source/Inspector + Program + dominant Timeline + narrow Audio Monitor.
- [ ] Implement Composição with Node Editor central and Program/Inspector visible.
- [ ] Implement Cor with Program + Scopes dominant and compact Timeline.
- [ ] Implement Áudio with Timeline + expanded Audio Monitor priority.
- [ ] Implement Entrega with real export configuration/action area and Program verification.
- [ ] Verify GREEN and prior workspace regression.
- [ ] Commit `feat: differentiate RB professional workspace layouts`.

### Task 3: RB visual hierarchy
**Files:**
- Modify: `rbprofessionalshell.cpp` through patch.

**Interfaces:**
- Produces shell-scoped stylesheet object names `RBWorkspaceBar`, `RBCommandBar`, `RBWorkspaceAction`.

- [ ] Extend RED contract for RB object names, active/inactive workspace styling and compact dock-title policy.
- [ ] Verify RED.
- [ ] Implement a stronger active workspace state, compact inactive states and separate command-strip hierarchy without global QWidget selectors.
- [ ] Apply styling only to RB shell-owned widgets to avoid breaking native editor widgets.
- [ ] Verify GREEN.
- [ ] Commit `style: establish RB VideoFire professional shell identity`.

### Task 4: Workspace command differentiation
**Files:**
- Modify: `rbprofessionalshell.cpp` through patch.

**Interfaces:**
- Consumes native QAction registry and existing project/media/export actions.
- Produces `PopulateCommandBar(RBWorkspace)`.

- [ ] Add failing checks that Mídia, Edição and Entrega resolve different native action sets.
- [ ] Verify RED.
- [ ] Wire real Media import/proxy/relink actions where available.
- [ ] Wire real Edit selection/trim/razor/snapping/link/multicam/proxy actions where available.
- [ ] Wire real Delivery/export actions where available.
- [ ] Keep unavailable future functions absent/disabled; disable Assistente workspace action.
- [ ] Verify GREEN plus M3/M4 contracts.
- [ ] Commit `feat: differentiate RB workspace command strips`.

### Task 5: Per-workspace persistence and reset
**Files:**
- Modify: shell controller and MainWindow menu integration through patch.

**Interfaces:**
- Produces `ResetCurrentWorkspace()` and menu action `Redefinir layout do workspace atual`.

- [ ] Add RED checks for current-workspace-only reset and selected-workspace persistence.
- [ ] Verify RED.
- [ ] Persist selected workspace separately from dock states.
- [ ] Implement reset deleting only `RBVideoFire/WorkspaceStates/<current>` then applying that workspace default.
- [ ] Add the reset action under Exibir/View using the existing menu infrastructure.
- [ ] Verify GREEN.
- [ ] Commit `feat: persist and reset RB workspace layouts independently`.

### Task 6: Reduced-window containment policy
**Files:**
- Modify: workspace default layout code.

**Interfaces:**
- Uses dock minimum widths/heights and Qt tabification rather than top-level resize.

- [ ] Add RED contract requiring minimum panel sizes and fallback tabification policy.
- [ ] Verify RED.
- [ ] Set safe minimums for Program, Timeline, Project and side monitors.
- [ ] When client width is constrained, tabify secondary panels instead of widening the main window.
- [ ] Verify GREEN.
- [ ] Commit `fix: contain RB workspaces in reduced window sizes`.

### Task 7: Windows qualification and EXE
**Files:**
- Create: `.github/workflows/build-2.5.1-ui3-windows.yml`

**Interfaces:**
- Applies cumulative baseline through 2.5.0 Professional Shell, proves UI3 RED, applies UI3 patch, proves GREEN, builds and packages Windows x64.

- [ ] Configure RED checkpoint before UI3 patch.
- [ ] Apply UI3 patch and run UI3 + M3 + M4 + M2 + Audio M1 contracts.
- [ ] Configure Release x64 with tests enabled.
- [ ] Compile full application.
- [ ] Run CTest.
- [ ] Deploy runtime and run startup smoke.
- [ ] Package exact installer `RB VideoFire Setup 2.5.1 Alpha Professional UI 3.0.exe`.
- [ ] Audit MZ/PE GUI subsystem and upload artifact only after all previous steps pass.
- [ ] Commit `ci: qualify RB VideoFire 2.5.1 Professional UI 3.0`.

### Task 8: Acceptance evidence
**Files:**
- Create: `docs/superpowers/verification/2026-09-09-rb-videofire-2.5.1-professional-ui3.md`

**Interfaces:**
- Records workflow run ID, head SHA, artifact ID, size, SHA-256 and qualification outcomes.

- [ ] Record only fresh successful evidence.
- [ ] Download and extract the artifact into the active runtime.
- [ ] Verify exact EXE path, MZ signature and SHA-256.
- [ ] Present the EXE as UI3 only; do not claim all 2.5 G0-G8 finishing features are complete.
