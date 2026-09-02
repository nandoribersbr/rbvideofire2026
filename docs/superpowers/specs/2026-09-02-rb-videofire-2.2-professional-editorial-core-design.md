# RB VideoFire 2.2 Professional Editorial Core — Design

## Goal
Transform RB VideoFire from a branded Olive-derived native editor into a professional editorial NLE foundation optimized for long-form editing while preserving the stable RB VideoFire 2.1.1 startup and packaging baseline.

## Scope
Version: RB VideoFire 2.2 Alpha — Professional Editorial Core.

This release is intentionally limited to five production-critical subsystems:
1. Professional Timeline Engine
2. Professional Trim Mode
3. RB Media/Proxy Engine
4. Autosave + Crash Recovery
5. Playback/Cache Engine

Advanced color finishing, DAW-class audio, AI, large multicam and a proprietary compositor are deferred.

## Architecture principles
- Native C++/Qt only; no Electron compatibility layer.
- Extend existing Olive-native timeline/render/project abstractions instead of building a second incompatible editor core.
- Keep subsystem boundaries explicit and avoid broad global rewrites.
- Every destructive editorial operation must remain undoable/redoable.
- Existing RB VideoFire 2.1.1 behavior that already works must be preserved.
- Performance and stability take priority over feature count.

## Professional Timeline Engine
Strengthen long-form timeline interaction and editorial commands: Selection, Razor/Add Edit, Ripple, Roll, Slip, Slide, Lift, Extract, Insert, Overwrite, linked A/V sync and track targeting. Timeline mutations should invalidate only affected regions and should avoid unnecessary full-scene work.

## Professional Trim Mode
Provide a dedicated trim state around edit points with A-side, B-side and dual-side selection; frame-accurate trim; J/K/L playback around the edit; loop preview; ripple and roll semantics; and deterministic Undo/Redo.

## RB Media/Proxy Engine
Introduce a persistent media identity layer for online/offline state, source paths, proxy paths and relink. Proxy switching must never alter editorial decisions or source timecode. Proxy generation should be structured for background jobs and safe cancellation.

## Autosave + Crash Recovery
Create incremental project snapshots with retention, clean-session markers and abnormal-shutdown detection. Recovery must never overwrite the primary project automatically. A recovered project opens as a recoverable session that the user explicitly saves.

## Playback/Cache Engine
Add playback quality levels Full, 1/2, 1/4 and 1/8 and explicit caches for frames, waveforms and thumbnails. Cache invalidation is scoped to media/timeline changes rather than global resets where possible. Playback should favor immediate responsiveness over background cosmetic work.

## Quality gates
- Test-first development for behavior changes.
- Timeline edit operations tested for Undo and Redo.
- Save/recovery tested against interrupted-session scenarios.
- Proxy/relink tests prove edit/timecode invariance.
- Existing CTest suite remains green.
- Windows GitHub Actions build remains mandatory.
- Startup smoke test must keep RBVideoFire.exe alive and reject fatal Qt/libpng startup errors.
- Packaging/audit must pass before installer upload.

## Delivery strategy
Implement the five subsystems incrementally on branch `rb-videofire-2.2-professional-editorial-core`. Each subsystem must remain independently testable. The 2.2 installer is produced only after all five quality gates pass.