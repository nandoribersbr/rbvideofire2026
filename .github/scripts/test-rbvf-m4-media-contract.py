from pathlib import Path
import sys

root = Path(sys.argv[1])
footage_h = (root / 'app/node/project/footage/footage.h').read_text(encoding='utf-8')
footage_cpp = (root / 'app/node/project/footage/footage.cpp').read_text(encoding='utf-8')
relink_cpp = (root / 'app/dialog/footagerelink/footagerelinkdialog.cpp').read_text(encoding='utf-8')

checks = {
    'M4-001 MediaState enum': 'enum class RBMediaState' in footage_h,
    'M4-002 Original path state': 'original_path_' in footage_h,
    'M4-003 Proxy path state': 'proxy_path_' in footage_h,
    'M4-004 Resolve playback path': 'ResolvePlaybackPath() const' in footage_h and 'Footage::ResolvePlaybackPath() const' in footage_cpp,
    'M4-005 Metadata fields': all(k in footage_h for k in ['reel_', 'scene_', 'take_', 'camera_', 'notes_', 'label_color_', 'favorite_']),
    'M4-006 State serialization': all(k in footage_cpp for k in ['rb_media_state', 'rb_proxy_path', 'rb_reel', 'rb_scene', 'rb_take', 'rb_camera', 'rb_notes', 'rb_label_color', 'rb_favorite']),
    'M4-007 Playback uses resolved path': 'QString file = ResolvePlaybackPath();' in footage_cpp,
    'M4-008 Offline tooltip': 'Offline' in footage_cpp,
    'M4-009 Relink preserves original source state': 'SetOriginalPath' in relink_cpp,
    'M4-010 Proxy assignment UI': 'SetProxyPath' in relink_cpp,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS ' if ok else 'FAIL ') + name)

if failed:
    print(f'M4 media contract failed: {len(failed)} check(s)')
    sys.exit(1)

print('M4 media contract GREEN')
