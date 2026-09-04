from pathlib import Path
import sys

root = Path(sys.argv[1])


def text(rel):
    path = root / rel
    if not path.exists():
        raise AssertionError(f"missing file: {rel}")
    return path.read_text(encoding="utf-8")

manager_h = text("app/window/mainwindow/workspacemanager.h")
bar_cpp = text("app/window/mainwindow/workspacebar.cpp")
main_h = text("app/window/mainwindow/mainwindow.h")
main_cpp = text("app/window/mainwindow/mainwindow.cpp")
cmake = text("app/window/mainwindow/CMakeLists.txt")
tests = text("tests/general/common-tests.cpp")

for token in ["Edit", "Audio", "Color", "Effects", "Deliver"]:
    assert token in manager_h, f"WorkspaceId missing {token}"

for label in ["Edição", "Áudio", "Cor", "Efeitos", "Entrega"]:
    assert label in bar_cpp, f"workspace label missing: {label}"

assert "WorkspaceManager *workspace_manager_" in main_h
assert "WorkspaceBar *workspace_bar_" in main_h
assert "addPermanentWidget(workspace_bar_" in main_cpp
assert "workspaceAboutToChange" in manager_h
assert "workspaceChanged" in manager_h
assert "workspacemanager.cpp" in cmake
assert "workspacebar.cpp" in cmake
assert "WorkspaceManagerTest" in tests
assert "OLIVE_ASSERT(manager.current() == WorkspaceId::Edit)" in tests
assert "OLIVE_ASSERT(manager.current() == WorkspaceId::Audio)" in tests

print("RB VideoFire 2.5 phase 1 workspace contract: PASS")
