from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding="utf-8")

def write(rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8", newline="\n")

def replace(rel, old, new):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f"{rel}: expected text not found: {old}")
    write(rel, data.replace(old, new, 1))

# Version contract for the first 2.5 working checkpoint.
replace("CMakeLists.txt",
        "project(rb-videofire VERSION 2.4.0 LANGUAGES CXX)",
        "project(rb-videofire VERSION 2.5.0 LANGUAGES CXX)")

nsi = read("packaging/rb-videofire/RBVideoFire.nsi")
nsi = nsi.replace("2.4.0 Alpha Professional Workspace", "2.5.0 Alpha Multi-Workspace Post")
nsi = nsi.replace("RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe",
                  "RB VideoFire Setup 2.5.0 Alpha Multi-Workspace Post.exe")
write("packaging/rb-videofire/RBVideoFire.nsi", nsi)

about = read("app/dialog/about/about.cpp").replace(
    "RB VideoFire 2.4.0 Alpha Professional Workspace",
    "RB VideoFire 2.5.0 Alpha Multi-Workspace Post")
write("app/dialog/about/about.cpp", about)

version = read("app/packaging/windows/version.h")
version = version.replace("2,4,0,0", "2,5,0,0")
version = version.replace("2.4.0.0\\0", "2.5.0.0\\0")
version = version.replace("2.4.0 Alpha Professional Workspace\\0",
                          "2.5.0 Alpha Multi-Workspace Post\\0")
write("app/packaging/windows/version.h", version)

manager_h = r'''#ifndef RBVF_WORKSPACEMANAGER_H
#define RBVF_WORKSPACEMANAGER_H

#include <QObject>
#include <QMetaType>

namespace olive {

enum class WorkspaceId { Edit = 0, Audio, Color, Effects, Deliver };

class WorkspaceManager : public QObject
{
  Q_OBJECT
public:
  explicit WorkspaceManager(QObject *parent = nullptr);
  WorkspaceId current() const;
  bool activate(WorkspaceId id);

signals:
  void workspaceAboutToChange(olive::WorkspaceId from, olive::WorkspaceId to);
  void workspaceChanged(olive::WorkspaceId id);

private:
  WorkspaceId current_;
};

}

Q_DECLARE_METATYPE(olive::WorkspaceId)

#endif
'''

manager_cpp = r'''#include "workspacemanager.h"

namespace olive {

WorkspaceManager::WorkspaceManager(QObject *parent)
  : QObject(parent), current_(WorkspaceId::Edit)
{
}

WorkspaceId WorkspaceManager::current() const
{
  return current_;
}

bool WorkspaceManager::activate(WorkspaceId id)
{
  if (id == current_) {
    return false;
  }
  const WorkspaceId previous = current_;
  emit workspaceAboutToChange(previous, id);
  current_ = id;
  emit workspaceChanged(current_);
  return true;
}

}
'''

bar_h = r'''#ifndef RBVF_WORKSPACEBAR_H
#define RBVF_WORKSPACEBAR_H

#include <QWidget>
#include <QVector>
#include "workspacemanager.h"

class QButtonGroup;
class QToolButton;

namespace olive {

class WorkspaceBar : public QWidget
{
  Q_OBJECT
public:
  explicit WorkspaceBar(WorkspaceManager *manager, QWidget *parent = nullptr);

private slots:
  void SyncActiveButton(olive::WorkspaceId id);

private:
  WorkspaceManager *manager_;
  QButtonGroup *button_group_;
  QVector<QToolButton*> buttons_;
};

}

#endif
'''

bar_cpp = r'''#include "workspacebar.h"

#include <QButtonGroup>
#include <QHBoxLayout>
#include <QSizePolicy>
#include <QToolButton>
#include <QVariant>

namespace olive {

WorkspaceBar::WorkspaceBar(WorkspaceManager *manager, QWidget *parent)
  : QWidget(parent), manager_(manager), button_group_(new QButtonGroup(this))
{
  setObjectName(QStringLiteral("RBVideoFireWorkspaceBar"));
  setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
  setMinimumHeight(34);

  auto *layout = new QHBoxLayout(this);
  layout->setContentsMargins(8, 2, 8, 2);
  layout->setSpacing(4);
  layout->addStretch(1);

  struct Item { const char *label; WorkspaceId id; };
  const Item items[] = {
    {"Edição", WorkspaceId::Edit},
    {"Áudio", WorkspaceId::Audio},
    {"Cor", WorkspaceId::Color},
    {"Efeitos", WorkspaceId::Effects},
    {"Entrega", WorkspaceId::Deliver}
  };

  button_group_->setExclusive(true);
  for (const auto &item : items) {
    auto *button = new QToolButton(this);
    button->setText(QString::fromUtf8(item.label));
    button->setCheckable(true);
    button->setAutoRaise(true);
    button->setMinimumWidth(84);
    button->setProperty("rbvfWorkspace", true);
    button_group_->addButton(button);
    buttons_.append(button);
    layout->addWidget(button);
    connect(button, &QToolButton::clicked, this, [this, item]() {
      if (manager_) manager_->activate(item.id);
    });
  }
  layout->addStretch(1);

  if (manager_) {
    connect(manager_, &WorkspaceManager::workspaceChanged,
            this, &WorkspaceBar::SyncActiveButton);
    SyncActiveButton(manager_->current());
  }
}

void WorkspaceBar::SyncActiveButton(WorkspaceId id)
{
  const int active = static_cast<int>(id);
  for (int i = 0; i < buttons_.size(); ++i) {
    buttons_.at(i)->setChecked(i == active);
  }
}

}
'''

write("app/window/mainwindow/workspacemanager.h", manager_h)
write("app/window/mainwindow/workspacemanager.cpp", manager_cpp)
write("app/window/mainwindow/workspacebar.h", bar_h)
write("app/window/mainwindow/workspacebar.cpp", bar_cpp)

cmake_rel = "app/window/mainwindow/CMakeLists.txt"
cmake = read(cmake_rel)
needle = "  window/mainwindow/mainwindowundo.cpp\n"
if "window/mainwindow/workspacemanager.cpp" not in cmake:
    addition = (needle +
        "  window/mainwindow/workspacemanager.h\n"
        "  window/mainwindow/workspacemanager.cpp\n"
        "  window/mainwindow/workspacebar.h\n"
        "  window/mainwindow/workspacebar.cpp\n")
    if needle not in cmake:
        raise RuntimeError("mainwindow CMake insertion point missing")
    cmake = cmake.replace(needle, addition, 1)
write(cmake_rel, cmake)

main_h_rel = "app/window/mainwindow/mainwindow.h"
main_h = read(main_h_rel)
if '#include "workspacemanager.h"' not in main_h:
    needle = '#include "mainwindowlayoutinfo.h"\n'
    main_h = main_h.replace(needle, needle + '#include "workspacemanager.h"\n#include "workspacebar.h"\n', 1)
if "WorkspaceManager *workspace_manager_;" not in main_h:
    needle = "  Project *project_;\n"
    main_h = main_h.replace(needle,
        "  WorkspaceManager *workspace_manager_;\n  WorkspaceBar *workspace_bar_;\n\n" + needle, 1)
write(main_h_rel, main_h)

main_cpp_rel = "app/window/mainwindow/mainwindow.cpp"
main_cpp = read(main_cpp_rel)
if "workspace_manager_ = new WorkspaceManager" not in main_cpp:
    needle = "  setStatusBar(status_bar);\n"
    addition = (needle +
        "\n  workspace_manager_ = new WorkspaceManager(this);\n"
        "  workspace_bar_ = new WorkspaceBar(workspace_manager_, this);\n"
        "  status_bar->addPermanentWidget(workspace_bar_, 1);\n")
    if needle not in main_cpp:
        raise RuntimeError("MainWindow status bar insertion point missing")
    main_cpp = main_cpp.replace(needle, addition, 1)
write(main_cpp_rel, main_cpp)

# Real unit test is added to Olive's existing General CTest executable.
test_rel = "tests/general/common-tests.cpp"
test = read(test_rel)
if '#include "window/mainwindow/workspacemanager.h"' not in test:
    test = test.replace('#include "common/digit.h"\n',
                        '#include "common/digit.h"\n#include "window/mainwindow/workspacemanager.h"\n', 1)
if "OLIVE_ADD_TEST(WorkspaceManagerTest)" not in test:
    workspace_test = r'''
OLIVE_ADD_TEST(WorkspaceManagerTest)
{
  WorkspaceManager manager;
  OLIVE_ASSERT(manager.current() == WorkspaceId::Edit);
  OLIVE_ASSERT(!manager.activate(WorkspaceId::Edit));
  OLIVE_ASSERT(manager.activate(WorkspaceId::Audio));
  OLIVE_ASSERT(manager.current() == WorkspaceId::Audio);
  OLIVE_ASSERT(manager.activate(WorkspaceId::Color));
  OLIVE_ASSERT(manager.current() == WorkspaceId::Color);
  OLIVE_ASSERT(manager.activate(WorkspaceId::Effects));
  OLIVE_ASSERT(manager.current() == WorkspaceId::Effects);
  OLIVE_ASSERT(manager.activate(WorkspaceId::Deliver));
  OLIVE_ASSERT(manager.current() == WorkspaceId::Deliver);
  OLIVE_TEST_END;
}
'''
    namespace_close = "\n}\n"
    pos = test.rfind(namespace_close)
    if pos < 0:
        raise RuntimeError("tests/general/common-tests.cpp namespace close missing")
    test = test[:pos] + "\n" + workspace_test + test[pos:]
write(test_rel, test)

print("Applied RB VideoFire 2.5 phase 1 workspace shell")
