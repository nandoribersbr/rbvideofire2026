# RB VideoFire 2.5 Professional Shell Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an own RB VideoFire professional application shell with persistent workspaces, real contextual commands, a dominant editing layout and a non-clipping Windows installer while preserving the existing native editing engines.

**Architecture:** Add a thin RB shell/controller layer around the existing MainWindow, dock widgets and QAction infrastructure. Workspace definitions only orchestrate existing panels/actions; they never create duplicate playback, timeline, media or audio engines. New UI actions are exposed only when backed by a functioning native command.

**Tech Stack:** C++17, Qt Widgets, CMake/Ninja, NSIS, Python source-contract tests, GitHub Actions Windows x64.

**Spec:** `docs/superpowers/specs/2026-09-09-rb-videofire-2.5-professional-shell-design.md`

## Global Constraints

- Preserve native C++/Qt/CMake/NSIS architecture.
- Preserve existing M3 Editorial and M4 Media Intelligence behavior.
- Do not add a second decoder, playback, audio, timeline, undo or project engine.
- No decorative/fake professional controls.
- Workspace and dock state must persist.
- Installer must remain Windows GUI subsystem and must not expose a console.
- Target identity: `RB VideoFire 2.5.0 Alpha Professional Finishing Foundation`.

---

### Task 1: RED contract for the RB Professional Shell

**Files:**
- Create: `.github/scripts/test-rbvf-2.5-professional-shell.py`

**Interfaces:**
- Consumes: extracted cumulative M4 source tree.
- Produces: source contract requiring RB workspace identifiers, shell controller, contextual toolbar and installer display-name fix.

- [ ] **Step 1: Write failing contract checks**

Require source tokens for `RBWorkspace`, `Media`, `Edit`, `Composition`, `Color`, `Audio`, `Delivery`, `Assistant`, `RBProfessionalShell`, `ApplyWorkspace`, `BuildWorkspaceBar`, `BuildCommandBar`, `RestoreWorkspace`, `SaveWorkspace`, plus an NSIS short installer display name.

- [ ] **Step 2: Run RED test before the 2.5 patch**

Run: `python .github/scripts/test-rbvf-2.5-professional-shell.py <source-root>`

Expected: non-zero exit because the RB shell does not yet exist.

- [ ] **Step 3: Commit the RED contract**

Commit message: `test: define RB VideoFire 2.5 professional shell contract`.

### Task 2: RB workspace controller

**Files:**
- Create through cumulative patch: `app/shell/rbprofessionalshell.h`
- Create through cumulative patch: `app/shell/rbprofessionalshell.cpp`
- Modify through cumulative patch: relevant application/MainWindow CMake source list and MainWindow integration.
- Create: `.github/scripts/apply-rbvf-2.5-professional-shell.py`

**Interfaces:**
- Produces: `enum class RBWorkspace { Media, Edit, Composition, Color, Audio, Delivery, Assistant };`
- Produces: `void ApplyWorkspace(RBWorkspace workspace);`
- Produces: `void RestoreWorkspace();`
- Produces: `void SaveWorkspace();`

- [ ] **Step 1: Extend RED test to require persistent workspace state**

Check for a stable QSettings key under `RBVideoFire/Workspace` and explicit save/restore calls.

- [ ] **Step 2: Run test and confirm RED**

Expected: FAIL on missing shell/controller.

- [ ] **Step 3: Implement minimal shell controller**

Controller receives the existing MainWindow/dock/action references, maps each workspace to a dock arrangement, and saves/restores selected workspace plus native dock state. It must not allocate a second viewer/timeline/project/audio pipeline.

- [ ] **Step 4: Run contract test**

Expected: workspace-controller checks PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add RB professional workspace controller`.

### Task 3: Persistent RB workspace bar

**Files:**
- Modify through patch: MainWindow shell integration and `rbprofessionalshell.*`.

**Interfaces:**
- Produces: `QToolBar* BuildWorkspaceBar()`.
- Consumes: `ApplyWorkspace(RBWorkspace)`.

- [ ] **Step 1: Add failing checks for all seven visible workspace labels**

Require Portuguese labels `Mídia`, `Edição`, `Composição`, `Cor`, `Áudio`, `Entrega`, `Assistente` in the shell source/translation path.

- [ ] **Step 2: Verify RED**

Expected: FAIL before implementation.

- [ ] **Step 3: Implement the compact workspace bar**

Create checkable QAction/QToolButton entries in one QActionGroup, route each to `ApplyWorkspace`, and restore the selected action on startup.

- [ ] **Step 4: Verify GREEN**

Expected: all workspace-label and routing checks PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add RB workspace navigation bar`.

### Task 4: Real contextual command bar

**Files:**
- Modify through patch: `rbprofessionalshell.*` and existing MainWindow QAction wiring.

**Interfaces:**
- Produces: `QToolBar* BuildCommandBar()`.
- Consumes: existing native edit/media/playback actions.

- [ ] **Step 1: Add failing tests for action reuse**

Require command-bar entries to reference existing QAction instances/action identifiers rather than create duplicate editing engines.

- [ ] **Step 2: Verify RED**

Expected: FAIL on missing command bar.

- [ ] **Step 3: Implement Edit command population**

Expose only real selection/trim/razor/snapping/link/insert/overwrite/lift/extract/marker/multicam/proxy actions that can be resolved in the existing action registry. Missing future actions remain absent or disabled with an explicit unavailable tooltip.

- [ ] **Step 4: Implement workspace-specific population**

Audio exposes the existing real monitor-related actions; Delivery exposes existing real export actions. Color/Composition/Assistant do not pretend unfinished backends exist.

- [ ] **Step 5: Run contract/regression tests**

Expected: shell contract GREEN; M3/M4 contracts GREEN.

- [ ] **Step 6: Commit**

Commit message: `feat: wire RB contextual command bar to native actions`.

### Task 5: RB Edit default layout

**Files:**
- Modify through patch: workspace layout definitions in `rbprofessionalshell.cpp`.

**Interfaces:**
- Consumes: existing Source Monitor, Inspector, Program Monitor, Project, History/Effects, Timeline and Audio Monitor docks.

- [ ] **Step 1: Add failing layout-policy checks**

Require Edit policy tokens for Program Monitor priority, Timeline priority, Source+Inspector grouping, Project lower-left and Audio Monitor right edge.

- [ ] **Step 2: Verify RED**

Expected: FAIL before layout policy exists.

- [ ] **Step 3: Implement Edit arrangement using native Qt dock APIs**

Use `addDockWidget`, `splitDockWidget`, `tabifyDockWidget`, resize/stretch APIs available in the existing MainWindow. Do not create duplicate panel instances.

- [ ] **Step 4: Preserve user customization**

Apply the RB default only on first use/reset; thereafter restore saved dock state.

- [ ] **Step 5: Verify GREEN and M2 workspace regression**

Expected: shell contract and prior workspace contract PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: establish RB professional edit layout`.

### Task 6: Installer clipping and product identity

**Files:**
- Modify through patch: existing NSIS/package metadata generated by cumulative scripts.

**Interfaces:**
- Produces: short installer chrome display name `RB VideoFire 2.5.0` while preserving full product/build metadata elsewhere.

- [ ] **Step 1: Add failing NSIS contract**

Reject the long `Professional Workspace` completion-page title and require the 2.5 short display name plus full version metadata.

- [ ] **Step 2: Verify RED**

Expected: FAIL against the M4 package script.

- [ ] **Step 3: Implement shorter NSIS display/completion strings**

Keep completion text concise and ensure the run-after-install label uses `RB VideoFire 2.5.0` rather than the full marketing suffix.

- [ ] **Step 4: Verify GREEN**

Expected: installer source contract PASS.

- [ ] **Step 5: Commit**

Commit message: `fix: prevent RB VideoFire installer text clipping`.

### Task 7: Windows integration qualification

**Files:**
- Create: `.github/workflows/build-2.5-professional-shell-windows.yml`

**Interfaces:**
- Consumes: baseline archive plus cumulative patches through M4 and the 2.5 shell patch.
- Produces: Windows x64 installer artifact only after all gates pass.

- [ ] **Step 1: Configure workflow to prove RED then GREEN**

Extract baseline, apply cumulative scripts through M4, run 2.5 contract and require failure, apply 2.5 patch, rerun 2.5 plus M3/M4/M2/Audio contracts.

- [ ] **Step 2: Build Release x64**

Run CMake/Ninja with tests enabled and compile the full application.

- [ ] **Step 3: Run CTest and startup smoke**

Expected: all CTest cases pass; GUI starts without a console and remains alive for the smoke interval.

- [ ] **Step 4: Package and audit installer**

Expected filename: `RB VideoFire Setup 2.5.0 Alpha Professional Finishing Foundation.exe`; verify PE/MZ, Windows GUI subsystem, artifact exists and non-zero.

- [ ] **Step 5: Commit workflow**

Commit message: `ci: qualify RB VideoFire 2.5 professional shell on Windows`.

### Task 8: Acceptance evidence

**Files:**
- Create: `docs/superpowers/verification/2026-09-09-rb-videofire-2.5-professional-shell.md`

**Interfaces:**
- Consumes: workflow run/job results and artifact metadata.
- Produces: exact evidence for build, CTest, startup, regressions, installer and SHA-256.

- [ ] **Step 1: Record workflow/run evidence only after fresh success**

Include run ID, head SHA, contract results, build/CTest/startup outcomes and artifact ID.

- [ ] **Step 2: Download/extract installer into the active runtime**

Verify exact path exists before presenting a sandbox link.

- [ ] **Step 3: Calculate SHA-256 and PE audit**

Record size, SHA-256, MZ signature and GUI subsystem result.

- [ ] **Step 4: Do not overclaim scope**

Label the shell gate complete only if all shell acceptance items are evidenced. Do not call the entire G0-G8 2.5 finishing suite complete until its later gates are implemented and qualified.
