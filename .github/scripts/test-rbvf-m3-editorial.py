from pathlib import Path
import sys

root = Path(sys.argv[1])
mainmenu = (root / 'app/window/mainwindow/mainmenu.cpp').read_text(encoding='utf-8')
multicam = (root / 'app/widget/multicam/multicamwidget.cpp').read_text(encoding='utf-8')
param_h = (root / 'app/panel/param/param.h').read_text(encoding='utf-8')
param_cpp = (root / 'app/panel/param/param.cpp').read_text(encoding='utf-8')

checks = {
    'M3-001 insert real command': 'edit_insert_item_' in mainmenu and 'InsertTriggered' in mainmenu,
    'M3-002 overwrite real command': 'edit_overwrite_item_' in mainmenu and 'OverwriteTriggered' in mainmenu,
    'M3-003 nudge left/right': 'NudgeLeftTriggered' in mainmenu and 'NudgeRightTriggered' in mainmenu,
    'M3-004 marker command': 'SetMarkerTriggered' in mainmenu,
    'M3-005 JKL shuttle': 'ShuttleLeftTriggered' in mainmenu and 'ShuttleStopTriggered' in mainmenu and 'ShuttleRightTriggered' in mainmenu,
    'M3-006 professional timeline tools': all(x in mainmenu for x in ['Tool::kRipple','Tool::kRolling','Tool::kRazor','Tool::kSlip','Tool::kSlide','Tool::kHand','Tool::kZoom']),
    'M3-007 multicam 25 shortcut map': 'RB_M3_MULTICAM_25' in multicam and 'source = i + 9' in multicam,
    'M3-008 multicam undo path preserved': 'Switched Multi-Camera Source' in multicam and 'undo_stack()->push' in multicam,
    'M3-009 inspector preset save slot': 'SaveInspectorPreset' in param_h and 'RBVideoFire/InspectorPresets' in param_cpp,
    'M3-010 inspector preset apply slot': 'ApplyInspectorPreset' in param_h and 'GetParamView()->Paste()' in param_cpp,
    'M3-011 Inspector title': 'SetTitle(tr("Inspector"))' in param_cpp,
    'M3-012 preset shortcuts': 'Ctrl+Shift+Alt+S' in param_cpp and 'Ctrl+Shift+Alt+P' in param_cpp,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS ' if ok else 'FAIL ') + name)

if failed:
    print(f'M3 editorial contract failed: {len(failed)} check(s)')
    sys.exit(1)

print('M3 editorial contract GREEN')
