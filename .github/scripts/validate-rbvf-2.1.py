from pathlib import Path
import sys

root = Path(sys.argv[1])
failures = []


def need(path, text):
    data = (root / path).read_text(encoding="utf-8", errors="ignore")
    if text not in data:
        failures.append(f"{path}: missing {text!r}")


def forbid(path, text):
    data = (root / path).read_text(encoding="utf-8", errors="ignore")
    if text in data:
        failures.append(f"{path}: forbidden {text!r}")


need(Path("CMakeLists.txt"), "project(rb-videofire VERSION 2.1.0 LANGUAGES CXX)")
need(Path("app/main.cpp"), 'QCoreApplication::setOrganizationDomain("rb8.com.br")')
forbid(Path("app/main.cpp"), 'setOrganizationName("olivevideoeditor.org")')
forbid(Path("app/main.cpp"), 'setOrganizationDomain("olivevideoeditor.org")')
need(Path("app/panel/sequenceviewer/sequenceviewer.cpp"), 'SetTitle(tr("Program Monitor"));')
forbid(Path("app/panel/sequenceviewer/sequenceviewer.cpp"), 'SetTitle(tr("Record Monitor"));')
need(Path("app/widget/timelinewidget/timelinewidget.cpp"), "Reveal in Source Monitor")
forbid(Path("app/widget/timelinewidget/timelinewidget.cpp"), "Reveal in Footage Viewer")

vh = Path("app/packaging/windows/version.h")
for s in [
    "VER_FILEVERSION             2,1,0,0",
    'VER_COMPANYNAME_STR         "RB8 Digital"',
    'VER_FILEDESCRIPTION_STR     "RB VideoFire"',
    'VER_INTERNALNAME_STR        "RBVideoFire"',
    'VER_ORIGINALFILENAME_STR    "RBVideoFire.exe"',
    'VER_PRODUCTNAME_STR         "RB VideoFire"',
]:
    need(vh, s)
for s in ["Olive Team", '"Olive"', "Olive.exe", "olivevideoeditor.org"]:
    forbid(vh, s)

need(Path("app/packaging/windows/resources.rc"), "rb-videofire.ico")
forbid(Path("app/packaging/windows/resources.rc"), "olive.ico")
forbid(Path("app/packaging/windows/resources.rc"), "olive_ove.ico")

ns = Path("packaging/rb-videofire/RBVideoFire.nsi")
need(ns, '!define VERSION "2.1.0 Alpha Editorial"')
need(ns, "RB VideoFire Setup 2.1.0 Alpha Editorial.exe")
need(ns, '!define MUI_ICON "${SOURCE_ROOT}\\app\\packaging\\windows\\rb-videofire.ico"')
need(ns, '!define MUI_UNICON "${SOURCE_ROOT}\\app\\packaging\\windows\\rb-videofire.ico"')

public_files = [
    "app/window/mainwindow/mainwindow.cpp",
    "app/window/mainwindow/mainmenu.cpp",
    "app/audio/audiomanager.cpp",
    "app/task/project/load/load.cpp",
    "app/task/project/import/importerrordialog.cpp",
    "app/dialog/export/export.cpp",
    "app/dialog/about/about.cpp",
    "app/core.cpp",
    "app/crashhandler/crashhandler.cpp",
    "app/common/crashpadinterface.cpp",
    "app/ui/style/style.cpp",
    "app/widget/viewer/viewerpreventsleep.cpp",
]
for rel in public_files:
    data = (root / rel).read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(data.splitlines(), 1):
        if (
            "Olive" in line
            or "olivevideoeditor.org" in line
            or "github.com/olive-editor/olive/issues" in line
        ) and (
            '"' in line
            or "QStringLiteral" in line
            or "tr(" in line
            or "PaJack_SetClientName" in line
        ):
            if line.lstrip().startswith(("*", "//")):
                continue
            if "OliveMain" in line or "symbol_bin_name" in line or "symbol_filename" in line:
                continue
            failures.append(f"{rel}:{i}: public Olive branding remains: {line.strip()}")

for asset in [
    "app/packaging/windows/rb-videofire.ico",
    "app/ui/graphics/rb-videofire.png",
]:
    if not (root / asset).exists():
        failures.append(f"{asset}: missing")

if failures:
    print("\n".join(failures))
    sys.exit(1)

print("RB VideoFire 2.1 editorial branding validation passed")
