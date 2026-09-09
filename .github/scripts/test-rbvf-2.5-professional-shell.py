from pathlib import Path
import sys

root = Path(sys.argv[1])
h = (root / 'app/window/mainwindow/mainwindow.h').read_text(encoding='utf-8')
cpp = (root / 'app/window/mainwindow/mainwindow.cpp').read_text(encoding='utf-8')
nsi = (root / 'packaging/rb-videofire/RBVideoFire.nsi').read_text(encoding='utf-8')
cmake = (root / 'CMakeLists.txt').read_text(encoding='utf-8')
version_h = (root / 'app/packaging/windows/version.h').read_text(encoding='utf-8')
about = (root / 'app/dialog/about/about.cpp').read_text(encoding='utf-8')

combined = h + '\n' + cpp
labels = ['Mídia', 'Edição', 'Composição', 'Cor', 'Áudio', 'Entrega', 'Assistente']
workspace_names = ['Media', 'Edit', 'Composition', 'Color', 'Audio', 'Delivery', 'Assistant']

checks = {
    'SHELL-001 RBWorkspace enum': 'enum class RBWorkspace' in combined and all(x in combined for x in workspace_names),
    'SHELL-002 RBProfessionalShell controller': 'class RBProfessionalShell' in combined,
    'SHELL-003 workspace application': 'ApplyWorkspace' in combined,
    'SHELL-004 workspace bar': 'BuildWorkspaceBar' in combined and all(label in combined for label in labels),
    'SHELL-005 contextual command bar': 'BuildCommandBar' in combined,
    'SHELL-006 persistent workspace restore': 'RestoreWorkspace' in combined and 'RBVideoFire/Workspace' in combined,
    'SHELL-007 persistent workspace save': 'SaveWorkspace' in combined and 'serializeLayout' in combined,
    'SHELL-008 native action reuse': 'property("id")' in cpp and 'findChildren<QAction*>' in cpp,
    'SHELL-009 professional edit layout': 'RB_EDIT_PROGRAM_PRIORITY' in cpp and 'RB_EDIT_TIMELINE_PRIORITY' in cpp,
    'SHELL-010 source inspector grouping': 'footage_viewer_panel_->addDockWidgetAsTab(param_panel_)' in cpp,
    'SHELL-011 audio monitor native panel': 'audio_monitor_panel_' in cpp and 'RB_AUDIO_NATIVE_MONITOR' in cpp,
    'SHELL-012 version 2.5 project': 'project(rb-videofire VERSION 2.5.0 LANGUAGES CXX)' in cmake,
    'SHELL-013 full product identity retained': '2.5.0 Alpha Professional Finishing Foundation' in version_h and '2.5.0 Alpha Professional Finishing Foundation' in about,
    'SHELL-014 installer short chrome': 'RB VideoFire 2.5.0' in nsi,
    'SHELL-015 old clipped installer label removed': '2.4.0 Alpha Professional Workspace' not in nsi,
    'SHELL-016 no duplicate media engine marker': 'NO_SECOND_PLAYBACK_ENGINE' in cpp,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS ' if ok else 'FAIL ') + name)

if failed:
    print(f'RB VideoFire 2.5 Professional Shell contract failed: {len(failed)} check(s)')
    sys.exit(1)

print('RB VideoFire 2.5 Professional Shell contract GREEN')
