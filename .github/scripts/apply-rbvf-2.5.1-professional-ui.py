from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

def write(rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding='utf-8', newline='\n')

def replace(rel, old, new, count=1):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f'{rel}: expected anchor not found')
    write(rel, data.replace(old, new, count))

# RBProfessionalUI 2.5.1 is deliberately a presentation layer over the native
# editor graph. NO_SECOND_PLAYBACK_ENGINE: it must not duplicate playback,
# timeline, project, audio, proxy or render engines.
replace('CMakeLists.txt', 'project(rb-videofire VERSION 2.5.0 LANGUAGES CXX)',
        'project(rb-videofire VERSION 2.5.1 LANGUAGES CXX)')

for rel in ['app/dialog/about/about.cpp', 'app/packaging/windows/version.h',
            'packaging/rb-videofire/RBVideoFire.nsi']:
    data = read(rel)
    data = data.replace('2.5.0 Alpha Professional Finishing Foundation',
                        '2.5.1 Alpha Professional UI')
    data = data.replace('2.5.0.0', '2.5.1.0').replace('2,5,0,0', '2,5,1,0')
    data = data.replace('2.5.0', '2.5.1')
    write(rel, data)

# Install RB-owned close icon as an application resource. The KDDockWidgets
# titlebar keeps its native close/dock behavior; only presentation is replaced.
asset_src = Path(__file__).resolve().parents[1] / 'assets' / 'rb-panel-close.svg'
asset_dst = root / 'app' / 'resources' / 'icons' / 'rb-panel-close.svg'
asset_dst.parent.mkdir(parents=True, exist_ok=True)
asset_dst.write_text(asset_src.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')

# Professional graphite system. Object-name targeting avoids changing command
# semantics and lets native QActions remain the single source of behavior.
cpp = read('app/window/mainwindow/mainwindow.cpp')
marker = '#define super KDDockWidgets::MainWindow\n'
if marker not in cpp:
    raise RuntimeError('mainwindow.cpp: super marker not found')
style = r'''#define super KDDockWidgets::MainWindow

static const char *kRBProfessionalUI = R"RBQSS(
QMainWindow, QDialog { background:#202225; color:#d8dadd; }
QMenuBar, QMenu, QToolBar { background:#25282c; color:#d8dadd; border-color:#34383d; }
QToolBar { spacing:2px; padding:2px 4px; }
QToolButton { min-height:22px; padding:2px 7px; border:1px solid transparent; border-radius:2px; }
QToolButton:hover { background:#34383d; border-color:#464b52; }
QToolButton:pressed, QToolButton:checked { background:#15171a; border-color:#59616b; }
QSplitter::handle { background:#111315; }
QTabBar::tab { background:#272a2e; color:#bfc3c8; padding:5px 9px; border:1px solid #34383d; }
QTabBar::tab:selected { background:#1d1f22; color:#ffffff; border-bottom-color:#6f879d; }
QScrollBar { background:#1c1e21; }
QScrollBar::handle { background:#484d53; min-width:18px; min-height:18px; border-radius:3px; }
QToolBar#RBWorkspaceBar { background:#1b1d20; border-bottom:1px solid #34383d; spacing:1px; padding:3px 6px; }
QToolBar#RBWorkspaceBar QToolButton { font-weight:600; padding:5px 12px; }
QToolButton#RBPanelCloseButton { qproperty-icon: url(:/icons/rb-panel-close.svg); padding:3px; min-width:20px; max-width:20px; }
QToolButton#RBPanelCloseButton:hover { background:#4a2d31; }
QToolButton#RBPanelCloseButton:pressed { background:#682f36; }
)RBQSS";
'''
cpp = cpp.replace(marker, style, 1)

# Apply style additively so existing application palette and native functionality
# remain intact. RBWorkspaceBar is created by the 2.5 professional shell.
ctor_anchor = 'MainWindow::MainWindow(QWidget *parent) :'
if ctor_anchor not in cpp:
    raise RuntimeError('mainwindow.cpp: constructor anchor not found')
# We cannot safely guess the initializer/body boundary here. Install via first
# QApplication access in the constructor source using a guarded single-shot helper.
include_anchor = '#include <QApplication>\n'
if include_anchor not in cpp:
    raise RuntimeError('mainwindow.cpp: QApplication include not found')
cpp = cpp.replace(include_anchor, include_anchor + '#include <QTimer>\n#include <QToolButton>\n', 1)

body_probe = '{\n'
pos = cpp.find(body_probe, cpp.find(ctor_anchor))
if pos < 0:
    raise RuntimeError('mainwindow.cpp: constructor body not found')
insert_at = pos + len(body_probe)
install = '''  setObjectName(QStringLiteral("RBProfessionalUI"));\n  qApp->setStyleSheet(qApp->styleSheet() + QString::fromUtf8(kRBProfessionalUI));\n  QTimer::singleShot(0, this, [this]() {\n    const auto buttons = findChildren<QToolButton*>();\n    for (QToolButton *button : buttons) {\n      const QString tip = button->toolTip().toLower();\n      const QString name = button->objectName().toLower();\n      if (tip.contains(QStringLiteral("close")) || tip.contains(QStringLiteral("fechar")) ||\n          name.contains(QStringLiteral("close"))) {\n        button->setObjectName(QStringLiteral("RBPanelCloseButton"));\n        button->setIcon(QIcon(QStringLiteral(":/icons/rb-panel-close.svg")));\n      }\n    }\n  });\n'''
cpp = cpp[:insert_at] + install + cpp[insert_at:]
write('app/window/mainwindow/mainwindow.cpp', cpp)

# Register the SVG in the application's existing Qt resource collection.
qrc_candidates = list((root / 'app').rglob('*.qrc'))
if not qrc_candidates:
    raise RuntimeError('no Qt .qrc resource collection found')
qrc = qrc_candidates[0]
data = qrc.read_text(encoding='utf-8')
if 'rb-panel-close.svg' not in data:
    end = data.rfind('</qresource>')
    if end < 0:
        raise RuntimeError(f'{qrc}: qresource closing tag not found')
    rel = Path('resources/icons/rb-panel-close.svg')
    try:
        resource_rel = asset_dst.relative_to(qrc.parent).as_posix()
    except ValueError:
        resource_rel = rel.as_posix()
    data = data[:end] + f'    <file alias="icons/rb-panel-close.svg">{resource_rel}</file>\n' + data[end:]
    qrc.write_text(data, encoding='utf-8', newline='\n')

print('RB VideoFire 2.5.1 Professional UI layer applied')
