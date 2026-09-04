from pathlib import Path
import sys

root = Path(sys.argv[1])


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8", newline="\n")


manager_h = r'''#ifndef RBVF_WORKSPACEMANAGER_H
#define RBVF_WORKSPACEMANAGER_H

#include <QObject>

namespace olive {

enum class WorkspaceId {
  Edit = 0,
  Audio,
  Color,
  Effects,
  Deliver
};

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
  : QObject(parent),
    current_(WorkspaceId::Edit)
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

namespace olive {

WorkspaceBar::WorkspaceBar(WorkspaceManager *manager, QWidget *parent)
  : QWidget(parent),
    manager_(manager),
    button_group_(new QButtonGroup(this))
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
      if (manager_) {
        manager_->activate(item.id);
      }
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
  const int index = static_cast<int>(id);
  for (int i = 0; i < buttons_.size(); ++i) {
    buttons_.at(i)->setChecked(i == index);
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
addition = (
    "  window/mainwindow/mainwindowundo.cpp\n"
    "  window/mainwindow/workspacemanager.h\n"
    "  window/mainwindow/workspacemanager.cpp\n"
    "  window/mainwindow/workspacebar.h\n"
    "  window/mainwindow/workspacebar.cpp\n"
)
if "window/mainwindow/workspacemanager.cpp" not in cmake:
    if needle not in cmake:
        raise RuntimeError("mainwindow CMake insertion point missing")
    cmake = cmake.replace(needle, addition, 1)
write(cmake_rel, cmake)

main_h_rel = "app/window/mainwindow/mainwindow.h"
main_h = read(main_h_rel)
include_needle = '#include "mainwindowlayoutinfo.h"\n'
if '#include "workspacemanager.h"' not in main_h:
    main_h = main_h.replace(include_needle, include_needle + '#include "workspacemanager.h"\n#include "workspacebar.h"\n', 1)
member_needle = "  Project *project_;\n"
if "WorkspaceManager *workspace_manager_;" not in main_h:
    main_h = main_h.replace(member_needle,
        "  WorkspaceManager *workspace_manager_;\n  WorkspaceBar *workspace_bar_;\n\n" + member_needle, 1)
write(main_h_rel, main_h)

main_cpp_rel = "app/window/mainwindow/mainwindow.cpp"
main_cpp = read(main_cpp_rel)
ctor_needle = "  setStatusBar(status_bar);\n"
ctor_addition = (
    "  setStatusBar(status_bar);\n\n"
    "  // RB VideoFire 2.5: fixed bottom workspace selector.\n"
    "  // Workspaces share the current project/sequence; this control only changes UI context.\n"
    "  workspace_manager_ = new WorkspaceManager(this);\n"
    "  workspace_bar_ = new WorkspaceBar(workspace_manager_, this);\n"
    "  status_bar->addPermanentWidget(workspace_bar_, 1);\n"
)
if "workspace_manager_ = new WorkspaceManager" not in main_cpp:
    if ctor_needle not in main_cpp:
        raise RuntimeError("MainWindow status bar insertion point missing")
    main_cpp = main_cpp.replace(ctor_needle, ctor_addition, 1)
write(main_cpp_rel, main_cpp)

# TDD coverage in existing General test executable.
test_rel = "tests/general/common-tests.cpp"
test = read(test_rel)
if '#include "window/mainwindow/workspacemanager.h"' not in test:
    test = test.replace('#include "common/digit.h"\n', '#include "common/digit.h"\n#include "window/mainwindow/workspacemanager.h"\n', 1)
if "OLIVE_ADD_TEST(WorkspaceManagerTest)" not in test:
    insert = r'''
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
    test = test.replace("\n}\n", "\n" + insert + "}\n", 1)
write(test_rel, test)

print("Applied RB VideoFire 2.5 phase 1 workspace shell")
