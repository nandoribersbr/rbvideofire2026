# RB Videofire 0.1 Design

## Goal
Build a fully offline desktop video editor for Windows 10 x64 under the RB Videofire brand, using a local Rust core, Tauri desktop shell, React/TypeScript UI, and bundled FFmpeg/FFprobe.

## Product constraints
- Windows 10 x64 is the primary supported platform.
- No mandatory login, cloud, telemetry, remote API, server, or internet connection.
- Editing is non-destructive and local.
- The app must remain usable without network connectivity after installation.
- The UI must expose only implemented or clearly disabled controls.
- The first release must complete the end-to-end workflow: create project, import media, edit timeline, add audio/text, preview, save, reopen, export MP4.

## Architecture
The product is split into a desktop UI layer and a Rust core. The UI sends commands to the core. The core owns project state, timeline state, serialization, undo/redo, autosave, media metadata, cache, preview coordination, and export planning. FFmpeg/FFprobe are bundled local resources and are invoked through structured process arguments.

Core crates:
- `rbvf-core`: IDs, shared types, errors, events, commands, time math.
- `rbvf-project`: `.rbvf` load/save, validation, migration, autosave, recovery.
- `rbvf-timeline`: tracks, clips, trims, splits, snapping, selection, edit commands.
- `rbvf-media`: import, FFprobe metadata, media registry, offline-media handling.
- `rbvf-audio`: volume, waveform metadata, channel handling.
- `rbvf-preview`: playhead-to-frame coordination and preview quality modes.
- `rbvf-export`: FFmpeg command generation, codec/encoder detection, progress, cancel, CPU fallback.
- `rbvf-cache`: thumbnails, waveforms, proxy-ready cache entries, temp cleanup.

## Desktop stack
- Rust stable toolchain
- Tauri 2.x desktop shell
- TypeScript
- React
- Local CSS/assets only
- FFmpeg and FFprobe bundled under `resources/ffmpeg/`

## `.rbvf` format
The initial format is UTF-8 JSON with explicit versioning.

Required top-level fields:
- `format`: `RBVF`
- `version`: `1`
- `project`
- `sequence`
- `media`
- `tracks`
- `timeline`
- `export`

Entity identifiers use UUIDs. Media entries reference original local files instead of embedding them. Missing media remains represented in the project and can be relinked. Saving uses temp-write, flush/validation, and atomic replacement where supported. Autosaves are stored separately under `%LOCALAPPDATA%\RB Videofire\Autosave\`.

## Timeline 0.1
The timeline supports dynamic video/audio tracks and the following operations: select, move, trim in/out, split, copy, paste, duplicate, delete, ripple delete, snapping, zoom, horizontal/vertical scroll, track lock, audio mute, video visibility. Undo/redo is command-based.

## Preview 0.1
Preview follows the playhead and supports play/pause, scrubbing, frame stepping, Fit/25%/50%/100% display scaling, and 1/4, 1/2, Full preview quality. Preview quality never changes final export quality.

## Text and audio
Text clips support content, font, size, alignment, position, scale, duration, and opacity. Audio clips support playback, volume, mute, waveform cache, and sync with video.

## Export 0.1
Initial export target:
- MP4 container
- H.264 video
- AAC audio
- presets for 720p, 1080p, 1440p, 4K
- FPS: 23.976, 24, 25, 29.97, 30, 50, 59.94, 60
- quality presets: Draft, Standard, High
- hardware encoder detection where available
- mandatory CPU fallback through libx264
- progress, cancel, failure state, and output validation

## Local directories
Application data root: `%LOCALAPPDATA%\RB Videofire\`

Subdirectories:
- `Cache/`
- `Autosave/`
- `Logs/`
- `Temp/`
- `Settings/`

Program installation target: `C:\Program Files\RB Videofire\`.

## Source structure
```text
rb-videofire/
├── apps/desktop/
├── frontend/src/
├── crates/
│   ├── rbvf-core/
│   ├── rbvf-project/
│   ├── rbvf-timeline/
│   ├── rbvf-media/
│   ├── rbvf-audio/
│   ├── rbvf-preview/
│   ├── rbvf-export/
│   └── rbvf-cache/
├── resources/ffmpeg/
├── tests/
├── installer/
├── docs/
├── LICENSES/
├── Cargo.toml
└── README.md
```

## Error handling
Typed error classes cover missing media, unsupported formats, FFmpeg failures, corrupt projects, permission failures, full disk, invalid project data, and unavailable GPU encoders. Heavy jobs run off the UI thread. Invalid media or corrupt projects must not crash the application.

## Testing
Unit tests cover timeline math, trim, split, snapping, serialization, migrations, undo/redo, time conversion, and export command generation. Integration tests cover import to timeline, save/reopen, timeline to preview, timeline to export, missing media relink, crash recovery, and CPU fallback.

## Acceptance criteria
The Windows x64 build is accepted when it installs, launches offline, creates and saves a project, imports MP4/MOV/MP3/WAV/PNG/JPG when codec-supported, edits clips on the timeline, previews the composition with audio, supports text clips, reopens the saved project intact, creates autosaves, offers recovery after interrupted sessions, relinks missing media, and exports a playable H.264/AAC MP4. No principal visible control may be dead.

## Out of scope for 0.1
Cloud collaboration, generative AI, multicam, tracking, rotoscoping, advanced motion graphics, node compositing, HDR mastering, OFX, VST, third-party plugins, automatic speech-to-text, and render farms.
