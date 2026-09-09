from pathlib import Path
import sys

root = Path(sys.argv[1])
footage_h = (root / 'app/node/project/footage/footage.h').read_text(encoding='utf-8')
footage_cpp = (root / 'app/node/project/footage/footage.cpp').read_text(encoding='utf-8')
project_model_h = (root / 'app/widget/projectexplorer/projectviewmodel.h').read_text(encoding='utf-8')
project_model_cpp = (root / 'app/widget/projectexplorer/projectviewmodel.cpp').read_text(encoding='utf-8')
project_explorer_cpp = (root / 'app/widget/projectexplorer/projectexplorer.cpp').read_text(encoding='utf-8')

checks = {
    'M4-001 MediaState enum': 'enum class RBMediaState' in footage_h,
    'M4-002 Native persistent proxy input': 'kProxyPathInput' in footage_h and 'NodeValue::kFile' in footage_cpp,
    'M4-003 Native persistent media-state input': 'kMediaStateInput' in footage_h and 'NodeValue::kInt' in footage_cpp,
    'M4-004 Resolve playback path': 'ResolvePlaybackPath() const' in footage_h and 'Footage::ResolvePlaybackPath() const' in footage_cpp,
    'M4-005 Persistent metadata inputs': all(k in footage_h for k in ['kReelInput', 'kSceneInput', 'kTakeInput', 'kCameraInput', 'kNotesInput', 'kLabelColorInput', 'kFavoriteInput']),
    'M4-006 Playback uses resolved path': 'QString file = ResolvePlaybackPath();' in footage_cpp,
    'M4-007 Proxy decoder is separate': 'proxy_decoder_' in footage_h and 'ProbeProxy' in footage_cpp,
    'M4-008 Offline state is visible': 'Offline' in footage_cpp,
    'M4-009 Project Bin metadata columns': all(k in project_model_h for k in ['kMediaState', 'kReel', 'kScene', 'kTake', 'kCamera', 'kLabelColor', 'kFavorite']),
    'M4-010 Metadata edits use undo': 'NodeParamSetStandardValueCommand' in project_model_cpp,
    'M4-011 Proxy assignment UI': 'Assign Proxy Media' in project_explorer_cpp,
    'M4-012 Original/proxy toggle UI': 'Use Original Media' in project_explorer_cpp and 'Use Proxy Media' in project_explorer_cpp,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS ' if ok else 'FAIL ') + name)

if failed:
    print(f'M4 media contract failed: {len(failed)} check(s)')
    sys.exit(1)

print('M4 media contract GREEN')
