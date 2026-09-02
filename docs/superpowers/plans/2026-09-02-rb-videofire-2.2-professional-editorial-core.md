# RB VideoFire 2.2 Professional Editorial Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a stable native professional editorial core focused on timeline, trim, media/proxy, recovery and playback/cache.

**Architecture:** Extend the existing Olive-derived C++/Qt architecture through focused RB VideoFire modules and adapters. Preserve existing command/undo, node/render and project serialization contracts wherever possible rather than introducing a parallel engine.

**Tech Stack:** C++17, Qt, CMake/Ninja, CTest, Windows/MSVC, NSIS, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-02-rb-videofire-2.2-professional-editorial-core-design.md`

## Global Constraints
- Native C++/Qt only.
- Preserve stable RB VideoFire 2.1.1 startup/branding behavior.
- No destructive timeline operation without Undo/Redo coverage.
- No proxy/relink operation may alter editorial timing.
- No installer is released unless CTest, startup smoke test and package audit pass.
- Use test-first development for production behavior changes.

---

### Task 1: Establish 2.2 identity and regression gates
**Files:** `.github/scripts/apply-rbvf-2.2.py`, `.github/scripts/validate-rbvf-2.2.py`, `.github/workflows/build-windows.yml`
- [ ] Write validator assertions for 2.2 identity and preservation of 2.1.1 startup safeguards.
- [ ] Run validator against unmodified baseline and verify RED.
- [ ] Implement minimal 2.2 version/package identity patch.
- [ ] Run validator and verify GREEN.
- [ ] Commit.

### Task 2: Professional Timeline command layer
**Files:** existing timeline command/tool sources discovered in extracted native source; focused RB adapters only where required.
- [ ] Add failing tests for Add Edit, Lift, Extract, Ripple, Roll, Slip, Slide and linked A/V invariants.
- [ ] Verify RED for missing/insufficient professional command behavior.
- [ ] Implement minimal command-layer changes using existing undo stack.
- [ ] Verify Undo/Redo and sync tests GREEN.
- [ ] Add long-timeline regression fixture and ensure mutations stay scoped.
- [ ] Commit.

### Task 3: Professional Trim Mode
**Files:** timeline tool/view/controller sources plus focused trim state module.
- [ ] Write failing tests for A-side, B-side and dual-side edit selection.
- [ ] Write failing tests for frame trim and ripple/roll semantics.
- [ ] Implement trim state model and command integration.
- [ ] Wire J/K/L and loop-preview control without bypassing existing playback controller.
- [ ] Verify all trim Undo/Redo tests GREEN.
- [ ] Commit.

### Task 4: RB Media/Proxy Engine
**Files:** project/media serialization, footage/media objects, new focused proxy/relink service where necessary.
- [ ] Write failing tests for persistent media identity, online/offline and proxy metadata.
- [ ] Write failing test proving Original↔Proxy does not change timeline/source timing.
- [ ] Implement media identity and proxy state serialization.
- [ ] Implement relink transaction with validation before path replacement.
- [ ] Add background-job boundary for proxy generation and cancellation.
- [ ] Verify media/proxy tests GREEN.
- [ ] Commit.

### Task 5: Autosave + Crash Recovery
**Files:** project save/session lifecycle plus focused recovery service.
- [ ] Write failing tests for incremental snapshot naming/retention.
- [ ] Write failing tests for clean shutdown vs abnormal shutdown marker.
- [ ] Write failing recovery test proving primary project is never overwritten automatically.
- [ ] Implement snapshot service and retention.
- [ ] Implement session marker and recovery discovery.
- [ ] Wire recovery prompt/session opening.
- [ ] Verify tests GREEN.
- [ ] Commit.

### Task 6: Playback Quality and Cache Engine
**Files:** renderer/playback configuration, cache services, preferences/UI bindings.
- [ ] Write failing tests for Full, 1/2, 1/4, 1/8 quality mapping.
- [ ] Write failing tests for scoped cache invalidation.
- [ ] Implement quality state and renderer mapping.
- [ ] Implement focused frame/waveform/thumbnail cache ownership boundaries.
- [ ] Verify timeline mutations invalidate only relevant cache ranges where supported.
- [ ] Run playback regression tests GREEN.
- [ ] Commit.

### Task 7: Integration and Windows release gate
**Files:** `.github/workflows/build-windows.yml`, package audit scripts, version/package metadata.
- [ ] Run complete CTest suite.
- [ ] Build native Release on Windows runner.
- [ ] Deploy runtime with windeployqt/dependencies.
- [ ] Run startup smoke test and reject fatal Qt/libpng/startup output.
- [ ] Run package audit.
- [ ] Build NSIS installer named `RB VideoFire Setup 2.2.0 Alpha Professional Editorial.exe`.
- [ ] Upload installer and portable artifacts only after all gates pass.
- [ ] Commit final release metadata.