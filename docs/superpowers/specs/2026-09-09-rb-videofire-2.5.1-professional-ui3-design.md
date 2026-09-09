# RB VideoFire 2.5.1 Professional UI 3.0 Design

## Goal
Replace the remaining Olive-like workspace presentation with an own RB VideoFire shell whose workspaces are visually and functionally distinct, geometrically stable, and responsive without moving the application window or allowing dock layouts to drift.

## Architecture
Keep the proven native C++/Qt playback, timeline, project, media, undo and audio engines. Replace workspace orchestration with an RB-owned layout controller that treats each workspace as a deterministic internal layout preset. Workspace changes may rearrange only the central application content; they must never resize, move or restore the top-level application window geometry.

## Stable workspace geometry
- Capture top-level window geometry independently from workspace layout state.
- Never call top-level resize/move/restoreGeometry as part of workspace switching.
- Store one dock-state payload per workspace under `RBVideoFire/WorkspaceStates/<workspace>`.
- First entry to a workspace applies its RB default layout. Later entries restore that workspace's saved internal dock state.
- Switching workspaces keeps the outer window rectangle unchanged.
- Each workspace has minimum dock sizes and proportional resize policy suitable for 1920x1080 and smaller resizable windows.
- If space is insufficient, panels tabify/collapse internally rather than pushing content outside the client area.

## RB visual identity
- Replace the thin Olive-like workspace row with a dedicated RB workspace navigator.
- Active workspace must have a strong, unmistakable selected state.
- Inactive workspaces remain compact and lower contrast.
- Use consistent Portuguese panel names and RB terminology.
- Add a compact RB command strip below workspace navigation.
- Reduce reliance on Olive's default dock/header presentation with an RB-specific stylesheet scoped to the shell, workspace navigator, command strip and dock titles.
- Do not imitate DaVinci Resolve, Premiere Pro or Avid UI assets/layout pixel-for-pixel.

## Workspace differentiation
### Mídia
Project/media browser dominates left/center; source preview and metadata/Inspector are prominent. Timeline is hidden or minimized. Focus: ingest, bins, proxy/original/offline state, metadata and preview.

### Edição
Source + Inspector upper-left, large Program Monitor upper-right, Project/History lower-left, dominant Timeline lower-center, Audio Monitor narrow right. This is the primary cutting workspace.

### Composição
Node Editor becomes the central dominant panel, Program Monitor remains visible, Inspector is prominent, Project panel available. Timeline becomes secondary but remains accessible.

### Cor
Program Monitor and Scopes dominate the top area; Inspector/color controls and node graph are visible; Timeline becomes a compact strip. Only functioning color controls are exposed.

### Áudio
Timeline remains visible, Audio Monitor grows, and audio-oriented panels receive priority. Future Mixer/Master/FX controls are only enabled when their real backend exists.

### Entrega
Export/render configuration and queue receive the primary area; Program Monitor remains for verification; editing panels are secondary. Existing real export actions are reused.

### Assistente
Disabled until its backend exists. It must not open an empty fake workspace.

## Command strip
Contextual commands change by workspace and reuse native QAction paths. No fake enabled buttons. Editing shows real cut/trim/snapping/link/multicam/proxy commands available in the current backend. Media shows real import/proxy/relink actions. Delivery shows real export actions. Unsupported future controls are absent or explicitly disabled.

## Persistence and reset
- Persist selected workspace separately from each workspace dock state.
- Persist user customizations per workspace.
- Add `Exibir > Redefinir layout do workspace atual` to discard only the current workspace state and reapply its RB default.
- Application startup restores the last workspace without changing the OS-level window position/size.

## Acceptance
1. Switching repeatedly among Mídia, Edição, Composição, Cor, Áudio and Entrega leaves the top-level window geometry byte-for-byte equivalent at the Qt geometry level.
2. Each workspace has a visibly different panel hierarchy and primary task.
3. No dock leaves the client area at tested 1920x1080 and reduced window size.
4. Workspace customizations survive switch-away/switch-back and restart.
5. Reset affects only the current workspace.
6. Assistente remains disabled until functional.
7. M3, M4, Audio M1 and existing project/timeline/playback regressions stay green.
8. Windows x64 Release build, CTest and startup smoke pass.
9. Installer remains GUI subsystem and launches without console.
10. The shell uses RB-specific navigation/style hierarchy and no longer presents workspaces as near-identical Olive dock presets.

## Version
Target build: `RB VideoFire 2.5.1 Alpha Professional UI 3.0`.
