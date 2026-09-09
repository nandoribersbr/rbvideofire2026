# RB VideoFire 2.5 Professional Shell Design

## Goal
Replace the Olive-like presentation with an own RB VideoFire professional editing shell while preserving the proven native C++/Qt editing, playback, timeline, undo, project, audio and media pipelines underneath.

## Product identity
The main window must read immediately as RB VideoFire rather than a renamed Olive build. Branding changes must be structural and workflow-oriented, not a skin-only recolor.

## Permanent workspace navigation
Expose these top-level workspaces in a persistent RB workspace bar:

- Mídia
- Edição
- Composição
- Cor
- Áudio
- Entrega
- Assistente

Workspace switching changes the visible dock/panel arrangement and the contextual command bar. Existing native dock widgets and engines are reused wherever possible. No duplicate playback, timeline, decoder, audio, undo or project engine is allowed.

## RB command bar
Below the workspace navigation, add a compact contextual command bar. Buttons must call real existing actions or real newly implemented backend actions. Unsupported future functionality must not be represented by fake enabled buttons.

### Edição
Selection, trim, razor, ripple/roll where supported, snapping, linked A/V, insert, overwrite, lift, extract, markers, multicam, proxy/original selection and render-cache controls.

### Cor
Expose only functioning color controls as they are implemented. The shell reserves the workspace for primaries, curves, LUT, masks/tracking and scopes, but a control is enabled only after its processing path exists.

### Áudio
Expose the existing real audio monitor first, followed by mixer/master/effects controls only as their shared native audio path becomes functional.

### Entrega
Expose real export/render-queue commands only. No decorative codec or queue actions.

## Default Edit layout
- Source Monitor + Inspector grouped upper-left.
- Program Monitor is the dominant upper-right viewer.
- Project/Media + Effects/History lower-left.
- Timeline dominates the lower center and width.
- Audio Monitor remains visible at the right edge.
- Node Editor remains available but is not forced into the default Edit workspace.

## Visual language
- Compact dark professional UI.
- RB VideoFire product mark/name in the application shell, discreet rather than oversized.
- Compact panel headers.
- Own workspace bar and command-bar hierarchy.
- Reduce visual dependence on Olive's default menu/dock arrangement.
- Preserve readability at 1920x1080 and Windows display scaling.

## Installer UI fix
The NSIS installer must not clip the product/version title or completion-page text. Use a shorter display name for the installer chrome and keep the full build identity in details/about/version metadata. Completion-page controls must remain inside the visible dialog at common Windows scaling levels.

## Persistence
The selected workspace and custom dock layout must persist through the existing settings mechanism. Users may customize panels without the default RB layout overwriting their saved arrangement on every launch.

## Compatibility constraints
- Native C++/Qt/CMake/NSIS architecture remains.
- Existing M3 and M4 behavior must regress green.
- No second decoder/playback/audio/timeline/project engine.
- No proprietary DaVinci/Fusion code or UI copying.
- No incompatible Audacity GPL source copying.
- No fake or decorative professional controls.

## Acceptance
The shell is accepted only when:

1. Windows Release build and CTest are green.
2. Startup smoke is green and no console appears.
3. Main window shows the RB workspace navigation.
4. Edição opens the intended professional dock layout.
5. Visible command buttons invoke real actions and unavailable future features are absent or disabled with an explicit unavailable state.
6. Program Monitor and Timeline receive priority in the default layout.
7. Existing Audio Monitor M1 remains connected to the native audio path.
8. M3 editorial and M4 media regressions remain green.
9. Workspace/layout survives close and reopen.
10. Installer completion page is not clipped under the tested Windows scaling configuration.

## Version target
RB VideoFire 2.5.0 Alpha Professional Finishing Foundation. The Professional Shell is the first gate of that version and does not by itself imply that all G0-G8 finishing features are complete.
