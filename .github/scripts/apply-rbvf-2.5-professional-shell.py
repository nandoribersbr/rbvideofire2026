from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

def write(rel, data):
    (root / rel).write_text(data, encoding='utf-8', newline='\n')

def replace(rel, old, new, count=1):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f'{rel}: expected anchor not found')
    write(rel, data.replace(old, new, count))

# ---- Product version / identity -------------------------------------------------
replace('CMakeLists.txt',
        'project(rb-videofire VERSION 2.4.0 LANGUAGES CXX)',
        'project(rb-videofire VERSION 2.5.0 LANGUAGES CXX)')

about = read('app/dialog/about/about.cpp')
if 'RB VideoFire 2.4.0 Alpha Professional Workspace' not in about:
    raise RuntimeError('about.cpp: 2.4 identity anchor not found')
about = about.replace('RB VideoFire 2.4.0 Alpha Professional Workspace',
                      'RB VideoFire 2.5.0 Alpha Professional Finishing Foundation')
write('app/dialog/about/about.cpp', about)

version = read('app/packaging/windows/version.h')
version = version.replace('2,4,0,0', '2,5,0,0')
version = version.replace('2.4.0.0\\0', '2.5.0.0\\0')
version = version.replace('2.4.0 Alpha Professional Workspace\\0',
                          '2.5.0 Alpha Professional Finishing Foundation\\0')
write('app/packaging/windows/version.h', version)

# Keep installer chrome concise so the NSIS finish page remains readable at
# common Windows display scaling, while the full build identity stays in About
# and Windows version resources.
nsi = read('packaging/rb-videofire/RBVideoFire.nsi')
old_out = 'RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe'
new_out = 'RB VideoFire Setup 2.5.0 Alpha Professional Finishing Foundation.exe'
if old_out not in nsi:
    raise RuntimeError('RBVideoFire.nsi: installer output anchor not found')
nsi = nsi.replace(old_out, new_out)
nsi = nsi.replace('RB VideoFire 2.4.0 Alpha Professional Workspace', 'RB VideoFire 2.5.0')
nsi = nsi.replace('2.4.0 Alpha Professional Workspace', '2.5.0')
write('packaging/rb-videofire/RBVideoFire.nsi', nsi)

# ---- MainWindow integration -----------------------------------------------------
h = read('app/window/mainwindow/mainwindow.h')
old = '''namespace olive {\n\n/**\n * @brief Olive's main window responsible for docking widgets and the main menu bar.\n */\nclass MainWindow : public KDDockWidgets::MainWindow\n'''
new = '''namespace olive {\n\nenum class RBWorkspace {\n  Media = 0,\n  Edit,\n  Composition,\n  Color,\n  Audio,\n  Delivery,\n  Assistant\n};\n\nclass RBProfessionalShell;\n\n/**\n * @brief RB VideoFire main window responsible for the professional editing station.\n */\nclass MainWindow : public KDDockWidgets::MainWindow\n'''
if old not in h:
    raise RuntimeError('mainwindow.h: namespace/class anchor not found')
h = h.replace(old, new, 1)

old = '''private:\n  TimelinePanel* AppendTimelinePanel();\n'''
new = '''private:\n  friend class RBProfessionalShell;\n\n  TimelinePanel* AppendTimelinePanel();\n'''
if old not in h:
    raise RuntimeError('mainwindow.h: private anchor not found')
h = h.replace(old, new, 1)

old = '''  bool first_show_;\n\n  Project *project_;\n'''
new = '''  bool first_show_;\n\n  RBProfessionalShell *rb_shell_;\n\n  Project *project_;\n'''
if old not in h:
    raise RuntimeError('mainwindow.h: shell member anchor not found')
h = h.replace(old, new, 1)
write('app/window/mainwindow/mainwindow.h', h)

cpp = read('app/window/mainwindow/mainwindow.cpp')
old = '''#include <QApplication>\n#include <QDebug>\n#include <QMessageBox>\n#include <QScreen>\n'''
new = '''#include <QAction>\n#include <QActionGroup>\n#include <QApplication>\n#include <QDebug>\n#include <QMenuBar>\n#include <QMessageBox>\n#include <QSettings>\n#include <QScreen>\n#include <QToolBar>\n#include <QVariant>\n'''
if old not in cpp:
    raise RuntimeError('mainwindow.cpp: Qt include anchor not found')
cpp = cpp.replace(old, new, 1)

anchor = '''#define super KDDockWidgets::MainWindow\n\nMainWindow::MainWindow(QWidget *parent) :\n'''
shell_code = r'''#define super KDDockWidgets::MainWindow

// RB VideoFire Professional Shell intentionally orchestrates the native panel/action
// graph only. NO_SECOND_PLAYBACK_ENGINE: no decoder, viewer, timeline, project or
// audio playback pipeline is duplicated by this layer.
class RBProfessionalShell : public QObject
{
public:
  RBProfessionalShell(MainWindow *owner, QMenuBar *menu)
      : QObject(owner), owner_(owner), menu_(menu), workspace_bar_(nullptr),
        command_bar_(nullptr), workspace_group_(nullptr), current_(RBWorkspace::Edit) {}

  QToolBar *BuildWorkspaceBar()
  {
    if (workspace_bar_) {
      return workspace_bar_;
    }

    workspace_bar_ = new QToolBar(tr("RB Workspaces"), owner_);
    workspace_bar_->setObjectName(QStringLiteral("RBWorkspaceBar"));
    workspace_bar_->setMovable(false);
    workspace_bar_->setFloatable(false);
    workspace_bar_->setToolButtonStyle(Qt::ToolButtonTextOnly);
    workspace_bar_->setStyleSheet(QStringLiteral(
        "QToolBar#RBWorkspaceBar{spacing:2px;padding:2px 4px;border-bottom:1px solid palette(mid);}" 
        "QToolBar#RBWorkspaceBar QToolButton{padding:5px 11px;font-weight:600;}"));
    owner_->addToolBar(Qt::TopToolBarArea, workspace_bar_);

    workspace_group_ = new QActionGroup(workspace_bar_);
    workspace_group_->setExclusive(true);

    struct WorkspaceItem { const char *label; RBWorkspace workspace; bool enabled; };
    const WorkspaceItem items[] = {
      {"Mídia", RBWorkspace::Media, true},
      {"Edição", RBWorkspace::Edit, true},
      {"Composição", RBWorkspace::Composition, true},
      {"Cor", RBWorkspace::Color, true},
      {"Áudio", RBWorkspace::Audio, true},
      {"Entrega", RBWorkspace::Delivery, true},
      {"Assistente", RBWorkspace::Assistant, false}
    };

    for (const WorkspaceItem &item : items) {
      QAction *action = workspace_bar_->addAction(QString::fromUtf8(item.label));
      action->setCheckable(true);
      action->setData(static_cast<int>(item.workspace));
      action->setEnabled(item.enabled);
      if (!item.enabled) {
        action->setToolTip(tr("Disponível quando o backend do Assistente estiver implementado."));
      }
      workspace_group_->addAction(action);
      if (item.enabled) {
        QObject::connect(action, &QAction::triggered, owner_, [this, workspace=item.workspace](bool checked) {
          if (checked) ApplyWorkspace(workspace);
        });
      }
    }

    return workspace_bar_;
  }

  QToolBar *BuildCommandBar()
  {
    if (command_bar_) {
      return command_bar_;
    }
    command_bar_ = new QToolBar(tr("Comandos RB"), owner_);
    command_bar_->setObjectName(QStringLiteral("RBCommandBar"));
    command_bar_->setMovable(false);
    command_bar_->setFloatable(false);
    command_bar_->setIconSize(QSize(18, 18));
    command_bar_->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
    owner_->addToolBar(Qt::TopToolBarArea, command_bar_);
    PopulateCommandBar(current_);
    return command_bar_;
  }

  void ApplyWorkspace(RBWorkspace workspace)
  {
    if (workspace == RBWorkspace::Assistant) {
      return;
    }

    SaveCurrentLayout();
    current_ = workspace;
    CheckWorkspaceAction(workspace);

    QSettings settings;
    settings.beginGroup(QStringLiteral("RBVideoFire/Workspace"));
    const QByteArray saved = settings.value(LayoutKey(workspace)).toByteArray();
    settings.endGroup();

    if (!saved.isEmpty()) {
      KDDockWidgets::LayoutSaver().restoreLayout(saved);
    } else {
      ApplyDefaultWorkspace(workspace);
    }
    PopulateCommandBar(workspace);
  }

  void RestoreWorkspace()
  {
    BuildWorkspaceBar();
    BuildCommandBar();

    QSettings settings;
    settings.beginGroup(QStringLiteral("RBVideoFire/Workspace"));
    int active = settings.value(QStringLiteral("active"), static_cast<int>(RBWorkspace::Edit)).toInt();
    if (active < static_cast<int>(RBWorkspace::Media) || active > static_cast<int>(RBWorkspace::Delivery)) {
      active = static_cast<int>(RBWorkspace::Edit);
    }
    current_ = static_cast<RBWorkspace>(active);
    const QByteArray saved = settings.value(LayoutKey(current_)).toByteArray();
    settings.endGroup();

    CheckWorkspaceAction(current_);
    if (!saved.isEmpty()) {
      KDDockWidgets::LayoutSaver().restoreLayout(saved);
    } else {
      ApplyDefaultWorkspace(current_);
    }
    PopulateCommandBar(current_);
  }

  void SaveWorkspace()
  {
    SaveCurrentLayout();
    QSettings settings;
    settings.beginGroup(QStringLiteral("RBVideoFire/Workspace"));
    settings.setValue(QStringLiteral("active"), static_cast<int>(current_));
    settings.endGroup();
    settings.sync();
  }

private:
  QString LayoutKey(RBWorkspace workspace) const
  {
    return QStringLiteral("layout_%1").arg(static_cast<int>(workspace));
  }

  void SaveCurrentLayout()
  {
    QSettings settings;
    settings.beginGroup(QStringLiteral("RBVideoFire/Workspace"));
    settings.setValue(LayoutKey(current_), KDDockWidgets::LayoutSaver().serializeLayout());
    settings.setValue(QStringLiteral("active"), static_cast<int>(current_));
    settings.endGroup();
  }

  QAction *FindNativeAction(const QString &id) const
  {
    // Reuse QAction instances already wired by MainMenu to native editor commands.
    const QList<QAction*> actions = menu_->findChildren<QAction*>();
    for (QAction *action : actions) {
      if (action->property("id").toString() == id) {
        return action;
      }
    }
    return nullptr;
  }

  void AddNativeAction(const char *id)
  {
    if (QAction *action = FindNativeAction(QString::fromLatin1(id))) {
      command_bar_->addAction(action);
    }
  }

  void PopulateCommandBar(RBWorkspace workspace)
  {
    if (!command_bar_) return;
    command_bar_->clear();

    switch (workspace) {
    case RBWorkspace::Media:
      AddNativeAction("import");
      AddNativeAction("pointertool");
      AddNativeAction("playpause");
      break;
    case RBWorkspace::Edit:
      AddNativeAction("pointertool");
      AddNativeAction("trackselecttool");
      AddNativeAction("edittool");
      AddNativeAction("rippletool");
      AddNativeAction("rollingtool");
      AddNativeAction("razortool");
      AddNativeAction("sliptool");
      AddNativeAction("slidetool");
      command_bar_->addSeparator();
      AddNativeAction("insert");
      AddNativeAction("overwrite");
      AddNativeAction("rippletoin");
      AddNativeAction("rippletoout");
      AddNativeAction("marker");
      command_bar_->addSeparator();
      AddNativeAction("prevcut");
      AddNativeAction("playpause");
      AddNativeAction("nextcut");
      break;
    case RBWorkspace::Composition:
      AddNativeAction("pointertool");
      AddNativeAction("playpause");
      break;
    case RBWorkspace::Color:
      AddNativeAction("prevframe");
      AddNativeAction("playpause");
      AddNativeAction("nextframe");
      break;
    case RBWorkspace::Audio:
      AddNativeAction("gotostart");
      AddNativeAction("playpause");
      AddNativeAction("gotoend");
      break;
    case RBWorkspace::Delivery:
      AddNativeAction("export");
      break;
    case RBWorkspace::Assistant:
      break;
    }
  }

  void ApplyDefaultWorkspace(RBWorkspace workspace)
  {
    // Start from the proven M2 editorial arrangement, then expose the native panel
    // appropriate for the selected RB workspace.
    owner_->SetDefaultLayout();

    switch (workspace) {
    case RBWorkspace::Media:
      owner_->project_panel_->raise();
      owner_->footage_viewer_panel_->raise();
      break;
    case RBWorkspace::Edit:
      // RB_EDIT_PROGRAM_PRIORITY
      owner_->sequence_viewer_panel_->raise();
      // RB_EDIT_TIMELINE_PRIORITY
      owner_->timeline_panels_.first()->raise();
      break;
    case RBWorkspace::Composition:
      owner_->addDockWidget(owner_->node_panel_, KDDockWidgets::Location_OnLeft, owner_->sequence_viewer_panel_);
      owner_->node_panel_->raise();
      owner_->param_panel_->raise();
      break;
    case RBWorkspace::Color:
      owner_->addDockWidget(owner_->scope_panel_, KDDockWidgets::Location_OnRight, owner_->sequence_viewer_panel_);
      owner_->scope_panel_->raise();
      owner_->param_panel_->raise();
      break;
    case RBWorkspace::Audio:
      // RB_AUDIO_NATIVE_MONITOR: the existing AudioMonitorPanel stays on the native Viewer/AudioManager path.
      owner_->addDockWidget(owner_->audio_monitor_panel_, KDDockWidgets::Location_OnRight, owner_->timeline_panels_.first());
      owner_->audio_monitor_panel_->raise();
      break;
    case RBWorkspace::Delivery:
      owner_->sequence_viewer_panel_->raise();
      owner_->timeline_panels_.first()->raise();
      break;
    case RBWorkspace::Assistant:
      break;
    }
  }

  void CheckWorkspaceAction(RBWorkspace workspace)
  {
    if (!workspace_group_) return;
    for (QAction *action : workspace_group_->actions()) {
      if (action->data().toInt() == static_cast<int>(workspace)) {
        action->setChecked(true);
        break;
      }
    }
  }

  MainWindow *owner_;
  QMenuBar *menu_;
  QToolBar *workspace_bar_;
  QToolBar *command_bar_;
  QActionGroup *workspace_group_;
  RBWorkspace current_;
};

MainWindow::MainWindow(QWidget *parent) :
'''
if anchor not in cpp:
    raise RuntimeError('mainwindow.cpp: shell insertion anchor not found')
cpp = cpp.replace(anchor, shell_code, 1)

old = '''  first_show_ = true;\n\n  // Create and set main menu\n'''
new = '''  first_show_ = true;\n  rb_shell_ = nullptr;\n\n  // Create and set main menu\n'''
if old not in cpp:
    raise RuntimeError('mainwindow.cpp: initialization anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''  UpdateTitle();\n\n  QMetaObject::invokeMethod(this, &MainWindow::SetDefaultLayout, Qt::QueuedConnection);\n}\n'''
new = '''  UpdateTitle();\n\n  // RB VideoFire owns the application shell; all editing engines remain native.\n  rb_shell_ = new RBProfessionalShell(this, main_menu);\n  rb_shell_->BuildWorkspaceBar();\n  rb_shell_->BuildCommandBar();\n  QMetaObject::invokeMethod(this, [this] { rb_shell_->RestoreWorkspace(); }, Qt::QueuedConnection);\n}\n'''
if old not in cpp:
    raise RuntimeError('mainwindow.cpp: constructor tail anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''void MainWindow::closeEvent(QCloseEvent *e)\n{\n  // Try to close all projects (this will return false if the user chooses not to close)\n'''
new = '''void MainWindow::closeEvent(QCloseEvent *e)\n{\n  // Persist the active RB workspace and dock arrangement before panels are destroyed.\n  if (rb_shell_) {\n    rb_shell_->SaveWorkspace();\n  }\n\n  // Try to close all projects (this will return false if the user chooses not to close)\n'''
if old not in cpp:
    raise RuntimeError('mainwindow.cpp: closeEvent anchor not found')
cpp = cpp.replace(old, new, 1)

write('app/window/mainwindow/mainwindow.cpp', cpp)
print('Applied RB VideoFire 2.5.0 Professional Shell and installer clipping fix')
