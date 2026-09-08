from pathlib import Path
import sys

root = Path(sys.argv[1])
main = root / 'app/window/mainwindow/mainwindow.cpp'
text = main.read_text(encoding='utf-8')

checks = {
    'M2-001 Program Monitor preferred width': 'o.preferredSize = QSize(900, centralAreaGeometry().height());' in text,
    'M2-002 Timeline preferred height': 'o.preferredSize = QSize(0, 420);' in text,
    'M2-003 Node Editor hidden by default': 'node_panel_->close();' in text,
    'M2-004 Node Editor not tabified in default workspace': 'footage_viewer_panel_->addDockWidgetAsTab(node_panel_);' not in text,
    'M2-005 Inspector remains with Source': 'footage_viewer_panel_->addDockWidgetAsTab(param_panel_);' in text,
    'M2-006 Audio Monitor remains docked': 'addDockWidget(audio_monitor_panel_, KDDockWidgets::Location_OnRight, timeline_panels_.first(), o);' in text,
    'M2-007 Layout persistence preserved': 'KDDockWidgets::LayoutSaver().restoreLayout' in text and 'KDDockWidgets::LayoutSaver().serializeLayout' in text,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS ' if ok else 'FAIL ') + name)

if failed:
    print(f'M2 workspace contract failed: {len(failed)} check(s)')
    sys.exit(1)

print('M2 workspace contract GREEN')
