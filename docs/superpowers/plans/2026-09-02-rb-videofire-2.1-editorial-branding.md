# RB VideoFire 2.1.0 Alpha Editorial Branding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Windows installer for RB VideoFire 2.1.0 Alpha Editorial with RB VideoFire/RB8 Digital public identity, the approved cinematic RB VideoFire icon, and no public-facing Olive branding while preserving upstream GPL notices and compatibility-critical internals.

**Architecture:** Keep the existing 2.0 native source archive as the immutable upstream build input. During GitHub Actions extraction, apply a deterministic 2.1 patch script, decode the approved RB assets, run a branding/editorial contract validation, then compile/test/package with the existing CMake/Ninja/MSVC/NSIS pipeline. Internal namespaces, node IDs, target names, source headers and GPL attribution remain untouched unless they surface to the user.

**Tech Stack:** C++17, Qt 5, CMake, Ninja, MSVC, NSIS, Python 3, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-02-rb-videofire-2.1-editorial-branding-design.md`

## Global Constraints

- Version: `2.1.0 Alpha Editorial`.
- Installer: `RB VideoFire Setup 2.1.0 Alpha Editorial.exe`.
- Company identity: `RB8 Digital`.
- Application identity: `RB VideoFire` / executable `RBVideoFire.exe`.
- Apply the approved cinematic RB VideoFire icon to the Windows executable and installer.
- Remove public-facing Olive branding, links and metadata.
- Preserve GPL license, upstream copyright notices, namespaces, compatibility-critical node IDs and other non-user-facing internals.
- Preserve existing native editing functionality and successful build pipeline.

---

### Task 1: Add RED branding/editorial contract validation

**Files:**
- Create: `.github/scripts/validate-rbvf-2.1.py`

- [ ] Write assertions for 2.1 version, Program Monitor, Source Monitor reveal label, RB8 metadata, RB icon resources and absence of public Olive strings in selected UI paths.
- [ ] Run the validation against extracted 2.0 source and verify it fails for the expected branding/version reasons.
- [ ] Commit the failing contract test.

### Task 2: Add deterministic 2.1 source patch and assets

**Files:**
- Create: `.github/scripts/apply-rbvf-2.1.py`
- Create: `.github/assets/rb-videofire.ico.b64`
- Create: `.github/assets/rb-videofire.png.b64`

- [ ] Decode the approved icon/splash assets into the extracted source tree.
- [ ] Patch CMake and NSIS to version 2.1.0 Alpha Editorial.
- [ ] Patch Windows VERSIONINFO and icon resources to RB VideoFire/RB8 Digital.
- [ ] Patch public UI strings, theme display names, crash messages/URLs and support links that expose Olive branding.
- [ ] Apply Program Monitor and Source Monitor editorial labels.
- [ ] Run validation and verify GREEN.
- [ ] Commit the patch and assets.

### Task 3: Update GitHub Actions build pipeline

**Files:**
- Modify: `.github/workflows/build-windows.yml`

- [ ] Add branch push trigger for this implementation branch plus manual dispatch.
- [ ] Extract 2.0 source archive.
- [ ] Run `apply-rbvf-2.1.py` then `validate-rbvf-2.1.py` before CMake configure.
- [ ] Build, run CTest and package 2.1 installer/portable/symbol artifacts.
- [ ] Ensure artifact names and paths use 2.1.0 Alpha Editorial.
- [ ] Commit workflow update and let the branch push trigger the build.

### Task 4: Verify Windows build artifact

- [ ] Inspect workflow run status and job logs.
- [ ] Require compile, CTest, package audit and artifact upload steps to succeed.
- [ ] Download the installer artifact.
- [ ] Confirm the extracted installer filename is exactly `RB VideoFire Setup 2.1.0 Alpha Editorial.exe`.
- [ ] Compute SHA-256 and provide the actual installer to the user.
