# RB Videofire 0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the legacy repository contents with a clean, testable RB Videofire 0.1 Windows 10 x64 offline editor foundation that can create/save/reopen `.rbvf` projects, import local media, edit a basic timeline, preview it, and export H.264/AAC MP4 locally.

**Architecture:** A Tauri 2 desktop application hosts a React/TypeScript UI and communicates with a modular Rust workspace. The Rust core owns all persisted project/timeline state and invokes bundled FFmpeg/FFprobe through structured arguments; the UI is a projection of core state rather than the source of truth.

**Tech Stack:** Rust stable, Cargo workspace, Tauri 2.x, React, TypeScript, local CSS/assets, FFmpeg, FFprobe, UUID, Serde/serde_json, Tokio where asynchronous process work is required.

**Spec:** `docs/superpowers/specs/2026-10-01-rb-videofire-0.1-design.md`

## Global Constraints
- Primary target is Windows 10 x64.
- All essential editor functions must work without internet after installation.
- No mandatory account, cloud, remote API, or telemetry.
- Editing is non-destructive.
- `.rbvf` format version is `1` and uses explicit `format: RBVF`.
- Principal visible controls must be functional or clearly disabled.
- FFmpeg/FFprobe are bundled local runtime resources.
- Export baseline is MP4 + H.264 + AAC with mandatory CPU fallback.

## Review Focus
- Corrupt or partially written `.rbvf` files must fail safely without losing the prior valid project.
- Missing or moved media must not invalidate the timeline and must support relinking.
- Unsupported media/FFprobe failure must return a typed error without freezing the UI.
- GPU encoder detection or runtime failure must fall back to CPU export cleanly.
- Interrupted export or application shutdown must not leave the project state corrupt.

---

### Task 1: Replace legacy root with the clean workspace foundation

**Files:**
- Remove legacy distributable ZIP and legacy workflow files from the rebuild branch.
- Create: `Cargo.toml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `LICENSES/README.md`
- Create: `apps/desktop/README.md`
- Create: `resources/ffmpeg/README.md`

**Interfaces:**
- Produces the repository root and workspace conventions consumed by all later tasks.

- [ ] Create the Rust workspace manifest with members for all `rbvf-*` crates.
- [ ] Create repository ignore rules for Rust, Node/Tauri output, caches, installers, and local bundled binaries not committed to source.
- [ ] Create the new project README with offline Windows 10 x64 scope and build prerequisites.
- [ ] Remove the old binary ZIP and legacy GitHub Actions content from the rebuild branch.
- [ ] Verify the repository root contains only the new project foundation and documentation.
- [ ] Commit as `chore: reset repository for RB Videofire 0.1`.

### Task 2: Implement shared core types and error model

**Files:**
- Create: `crates/rbvf-core/Cargo.toml`
- Create: `crates/rbvf-core/src/lib.rs`
- Create: `crates/rbvf-core/src/id.rs`
- Create: `crates/rbvf-core/src/time.rs`
- Create: `crates/rbvf-core/src/error.rs`
- Test: `crates/rbvf-core/tests/core_types.rs`

**Interfaces:**
- Produces `MediaId`, `ClipId`, `TrackId`, `SequenceId`, timeline time types, and `RbvfError`.

- [ ] Write failing tests for UUID-backed IDs, non-negative timeline times, and typed error variants.
- [ ] Run `cargo test -p rbvf-core` and verify failure.
- [ ] Implement the minimal shared types and error enum.
- [ ] Run `cargo test -p rbvf-core` and verify pass.
- [ ] Commit as `feat: add RBVF core types`.

### Task 3: Implement `.rbvf` project schema, safe save/load, validation, and recovery primitives

**Files:**
- Create: `crates/rbvf-project/Cargo.toml`
- Create: `crates/rbvf-project/src/lib.rs`
- Create: `crates/rbvf-project/src/model.rs`
- Create: `crates/rbvf-project/src/io.rs`
- Create: `crates/rbvf-project/src/validation.rs`
- Test: `crates/rbvf-project/tests/project_io.rs`

**Interfaces:**
- Consumes IDs/errors from `rbvf-core`.
- Produces `Project`, `Sequence`, `MediaReference`, `save_project(path, &Project)`, `load_project(path)`, and `validate_project(&Project)`.

- [ ] Write failing tests for `format=RBVF`, `version=1`, round-trip save/load, corrupt JSON rejection, invalid numeric values, and previous-file preservation when save fails.
- [ ] Run `cargo test -p rbvf-project` and verify failure.
- [ ] Implement the schema, validation, temp-write + validation + replacement flow, and `.bak` preservation strategy.
- [ ] Run `cargo test -p rbvf-project` and verify pass.
- [ ] Commit as `feat: add RBVF project persistence`.

### Task 4: Implement timeline model and edit command history

**Files:**
- Create: `crates/rbvf-timeline/Cargo.toml`
- Create: `crates/rbvf-timeline/src/lib.rs`
- Create: `crates/rbvf-timeline/src/model.rs`
- Create: `crates/rbvf-timeline/src/commands.rs`
- Create: `crates/rbvf-timeline/src/snapping.rs`
- Test: `crates/rbvf-timeline/tests/editing.rs`

**Interfaces:**
- Consumes core IDs/time and project media references.
- Produces track/clip structures and commands for move, trim, split, delete, ripple delete, duplicate, copy/paste, mute/visibility/lock, undo, redo.

- [ ] Write failing tests for move, trim boundaries, split source mapping, ripple delete, snapping, undo, redo, and locked-track rejection.
- [ ] Run `cargo test -p rbvf-timeline` and verify failure.
- [ ] Implement minimal command-driven timeline mutations.
- [ ] Run `cargo test -p rbvf-timeline` and verify pass.
- [ ] Commit as `feat: add timeline editing core`.

### Task 5: Implement local media import and FFprobe metadata adapter

**Files:**
- Create: `crates/rbvf-media/Cargo.toml`
- Create: `crates/rbvf-media/src/lib.rs`
- Create: `crates/rbvf-media/src/probe.rs`
- Create: `crates/rbvf-media/src/registry.rs`
- Test: `crates/rbvf-media/tests/media_registry.rs`

**Interfaces:**
- Consumes `MediaId`, `RbvfError`, `MediaReference`.
- Produces `probe_media(path)`, `register_media(path)`, `mark_missing_media`, and relink functions.

- [ ] Write failing tests for missing file, unsupported/invalid media response, metadata mapping, moved-media retention, and relink path replacement.
- [ ] Run `cargo test -p rbvf-media` and verify failure.
- [ ] Implement the structured FFprobe invocation and registry operations.
- [ ] Run `cargo test -p rbvf-media` and verify pass using fixture metadata or a process adapter mock.
- [ ] Commit as `feat: add local media registry`.

### Task 6: Implement cache and audio waveform model

**Files:**
- Create: `crates/rbvf-cache/Cargo.toml`
- Create: `crates/rbvf-cache/src/lib.rs`
- Create: `crates/rbvf-audio/Cargo.toml`
- Create: `crates/rbvf-audio/src/lib.rs`
- Test: `crates/rbvf-cache/tests/cache_keys.rs`
- Test: `crates/rbvf-audio/tests/audio_model.rs`

**Interfaces:**
- Produces deterministic cache keys based on path/size/mtime, cache directory resolution, audio volume/mute data, and waveform cache metadata.

- [ ] Write failing tests for cache invalidation and audio volume/mute bounds.
- [ ] Implement cache keying and local app-data directory resolution.
- [ ] Implement waveform metadata and audio state models.
- [ ] Run both crate test suites.
- [ ] Commit as `feat: add cache and audio foundations`.

### Task 7: Implement export planning and CPU fallback

**Files:**
- Create: `crates/rbvf-export/Cargo.toml`
- Create: `crates/rbvf-export/src/lib.rs`
- Create: `crates/rbvf-export/src/encoder.rs`
- Create: `crates/rbvf-export/src/plan.rs`
- Create: `crates/rbvf-export/src/progress.rs`
- Test: `crates/rbvf-export/tests/export_plan.rs`

**Interfaces:**
- Produces `ExportPreset`, `EncoderChoice`, `build_export_plan`, `detect_encoders`, progress parser, cancellation contract, and mandatory `libx264` fallback.

- [ ] Write failing tests for preset dimensions/FPS, structured arguments, GPU unavailable fallback, GPU runtime failure fallback decision, cancel state, and output path validation.
- [ ] Implement export plan generation without shell string concatenation.
- [ ] Implement encoder detection/fallback policy and progress parsing.
- [ ] Run `cargo test -p rbvf-export` and verify pass.
- [ ] Commit as `feat: add local export engine`.

### Task 8: Implement preview coordination contract

**Files:**
- Create: `crates/rbvf-preview/Cargo.toml`
- Create: `crates/rbvf-preview/src/lib.rs`
- Create: `crates/rbvf-preview/src/playhead.rs`
- Test: `crates/rbvf-preview/tests/playhead.rs`

**Interfaces:**
- Produces playhead state, quality modes `Quarter/Half/Full`, active-clip lookup contract, frame-step calculations, and preview requests used by the desktop shell.

- [ ] Write failing tests for clip activation at boundaries, frame stepping for supported FPS values, and preview-quality independence from export resolution.
- [ ] Implement the coordination model.
- [ ] Run `cargo test -p rbvf-preview` and verify pass.
- [ ] Commit as `feat: add preview coordination core`.

### Task 9: Scaffold Tauri desktop application and local-only UI

**Files:**
- Create: `apps/desktop/src-tauri/*`
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/styles.css`
- Create focused panel components under `frontend/src/panels/`.

**Interfaces:**
- Consumes Rust commands exposed by the core/application layer.
- Produces the main RB Videofire window with Media Bin, Preview, Inspector, Timeline, and Export entry point.

- [ ] Scaffold Tauri/React with no CDN/runtime network dependencies.
- [ ] Add the dark desktop layout and explicit disabled states for unavailable features.
- [ ] Wire project create/open/save and dirty-state close confirmation.
- [ ] Wire local file import and media-bin state.
- [ ] Wire timeline commands and undo/redo.
- [ ] Verify `npm run build` and `cargo check` succeed.
- [ ] Commit as `feat: add RB Videofire desktop shell`.

### Task 10: Integrate preview, text/audio controls, autosave, recovery, and export UI

**Files:**
- Modify desktop/frontend modules from Task 9.
- Create: `frontend/src/panels/InspectorPanel.tsx`
- Create: `frontend/src/panels/ExportPanel.tsx`
- Create: `frontend/src/state/projectStore.ts`
- Create integration tests under `tests/`.

**Interfaces:**
- Connects the end-to-end workflow across all prior crates.

- [ ] Add text-clip creation/edit controls and audio volume/mute controls.
- [ ] Add preview transport, scrubbing, and quality selector.
- [ ] Add 120-second autosave and startup recovery offer.
- [ ] Add export presets, progress, cancel, and CPU fallback messaging.
- [ ] Add missing-media relink flow.
- [ ] Run workspace tests and frontend build.
- [ ] Commit as `feat: complete RB Videofire 0.1 workflow`.

### Task 11: Windows packaging, `.rbvf` association, licenses, and CI

**Files:**
- Create/update Tauri bundle configuration.
- Create: `.github/workflows/windows-build.yml`
- Create: `LICENSES/` notices for redistributed dependencies.
- Create: `docs/testing/windows-acceptance.md`

**Interfaces:**
- Produces the Windows 10 x64 distributable and repeatable build pipeline.

- [ ] Configure Windows x64 packaging and `.rbvf` file association.
- [ ] Configure bundled local resources while avoiding committing unlicensed third-party binaries blindly.
- [ ] Add Windows CI for Rust tests, frontend build, and Tauri build.
- [ ] Document FFmpeg redistribution/license verification requirements before release packaging.
- [ ] Verify the workflow syntax and local build commands.
- [ ] Commit as `build: add Windows packaging pipeline`.

### Task 12: Acceptance gate and replacement of `main`

**Files:**
- No new product files unless fixes are required.

**Interfaces:**
- Promotes the tested rebuild to the repository default development line.

- [ ] Run `cargo test --workspace`.
- [ ] Run the frontend production build.
- [ ] Run Tauri Windows build in CI or a Windows environment.
- [ ] Execute the documented end-to-end acceptance scenario: create project → import two videos → edit → add music/text → save → close/reopen → export → validate playable MP4.
- [ ] Confirm offline launch and CPU export fallback.
- [ ] Confirm no principal visible control is dead.
- [ ] Replace `main` with the accepted rebuild while retaining the backup branch `backup/pre-rb-videofire-0.1-2026-10-01` for rollback.
- [ ] Tag the accepted baseline as `v0.1.0-alpha` only after the acceptance gate passes.
