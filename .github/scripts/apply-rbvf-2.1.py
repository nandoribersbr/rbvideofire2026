from pathlib import Path
import sys

root = Path(sys.argv[1])
assets = Path(sys.argv[2])


def text(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, data):
    (root / rel).write_text(data, encoding="utf-8", newline="\n")


def replace(rel, old, new):
    s = text(rel)
    if old not in s:
        raise RuntimeError(f"{rel}: expected text not found: {old[:100]!r}")
    write(rel, s.replace(old, new))


replace("CMakeLists.txt", "project(rb-videofire VERSION 2.0.0 LANGUAGES CXX)", "project(rb-videofire VERSION 2.1.0 LANGUAGES CXX)")
replace("app/panel/sequenceviewer/sequenceviewer.cpp", 'SetTitle(tr("Record Monitor"));', 'SetTitle(tr("Program Monitor"));')
replace("app/widget/timelinewidget/timelinewidget.cpp", "Reveal in Footage Viewer", "Reveal in Source Monitor")

replace(
    "app/main.cpp",
    '  QCoreApplication::setOrganizationName("olivevideoeditor.org");\n  QCoreApplication::setOrganizationDomain("olivevideoeditor.org");\n  QCoreApplication::setApplicationName("RB VideoFire");\n  QCoreApplication::setOrganizationName("RB8 Digital");',
    '  QCoreApplication::setOrganizationName("RB8 Digital");\n  QCoreApplication::setOrganizationDomain("rb8.com.br");\n  QCoreApplication::setApplicationName("RB VideoFire");',
)
replace("app/main.cpp", "too old to run Olive.\\n\\n", "too old to run RB VideoFire.\\n\\n")

repls = {
    "app/window/mainwindow/mainwindow.cpp": [
        ("Olive has detected your system is using the Nouveau graphics driver.", "RB VideoFire has detected your system is using the Nouveau graphics driver."),
        ("known to have stability and performance issues with Olive.", "known to have stability and performance issues with RB VideoFire."),
        ("before continuing to use Olive.", "before continuing to use RB VideoFire."),
    ],
    "app/window/mainwindow/mainmenu.cpp": [
        ("https://github.com/olive-editor/olive/issues", "https://github.com/nandoribersbr/rbvideofire2026/issues")
    ],
    "app/audio/audiomanager.cpp": [("PaJack_SetClientName(\"Olive\")", "PaJack_SetClientName(\"RB VideoFire\")")],
    "app/task/project/load/load.cpp": [
        ("a version of Olive that is no longer supported", "a version of RB VideoFire that is no longer supported"),
        ("a newer version of Olive and cannot be opened", "a newer version of RB VideoFire and cannot be opened"),
    ],
    "app/task/project/import/importerrordialog.cpp": [("Olive likely does not", "RB VideoFire likely does not")],
    "app/dialog/export/export.cpp": [
        ("continue using Olive while", "continue using RB VideoFire while"),
        ("Olive couldn't create it.", "RB VideoFire couldn't create it."),
    ],
    "app/core.cpp": [
        ("Olive may not have permission to this directory.", "RB VideoFire may not have permission to this directory."),
        ('tr("Olive Project")', 'tr("RB VideoFire Project")'),
        ('tr("Olive Project (Uncompressed XML)")', 'tr("RB VideoFire Project (Uncompressed XML)")'),
        ("unsaved changes when Olive ", "unsaved changes when RB VideoFire "),
        ("cache is currently full and Olive is having to delete old ", "cache is currently full and RB VideoFire is having to delete old "),
    ],
    "app/ui/style/style.cpp": [
        ('QStringLiteral("Olive Dark")', 'QStringLiteral("RB Dark")'),
        ('QStringLiteral("Olive Light")', 'QStringLiteral("RB Light")'),
    ],
    "app/widget/viewer/viewerpreventsleep.cpp": [('QStringLiteral("Olive Video Editor")', 'QStringLiteral("RB VideoFire")')],
    "app/crashhandler/crashhandler.cpp": [
        ('setWindowTitle(tr("Olive"));', 'setWindowTitle(tr("RB VideoFire"));'),
        ("We're sorry, Olive has crashed.", "We're sorry, RB VideoFire has crashed."),
        ('request.setUrl(QStringLiteral("https://olivevideoeditor.org/crashpad/report.php"));', "request.setUrl(QUrl());"),
    ],
    "app/common/crashpadinterface.cpp": [('"https://olivevideoeditor.org/crashpad/report.php",', '"",')],
}
for rel, pairs in repls.items():
    for old, new in pairs:
        replace(rel, old, new)

replace(
    "app/dialog/about/about.cpp",
    "QLabel* icon = new QLabel(QStringLiteral(\"<html><img src=':/graphics/olive-splash.png'></html>\"));",
    "QLabel* icon = new QLabel(QStringLiteral(\"<html><img width='256' height='256' src=':/graphics/rb-videofire.png'></html>\"));",
)
s = text("app/dialog/about/about.cpp")
start = s.index("  // Construct About text")
end = s.index("  QHBoxLayout *btn_layout", start)
new_block = '''  // Construct RB VideoFire About text
  QLabel* label =
      new QLabel(QStringLiteral("<html><head/><body>"
                                "<p><b>%1</b> %2</p>"
                                "<p><b>RB8 Digital</b></p>"
                                "<p>%3</p>"
                                "<p>%4</p>"
                                "</body></html>").arg(QApplication::applicationName(),
                                                      QApplication::applicationVersion(),
                                                      tr("Professional non-linear video editor for Windows."),
                                                      tr("Licensed under GNU GPL Version 3. Open-source license and copyright notices are preserved with the software.")));

  label->setAlignment(Qt::AlignLeft | Qt::AlignVCenter);
  label->setWordWrap(true);
  label->setOpenExternalLinks(true);
  label->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Minimum);
  label->setTextInteractionFlags(Qt::TextSelectableByMouse | Qt::LinksAccessibleByMouse);
  label->setCursor(Qt::IBeamCursor);
  horiz_layout->addWidget(label);

  layout->addLayout(horiz_layout);
  layout->addWidget(new QLabel(tr("RB VideoFire 2.1 Alpha Editorial • RB8 Digital")));
  layout->addWidget(new QLabel());

'''
write("app/dialog/about/about.cpp", s[:start] + new_block + s[end:])

qrc = text("app/ui/graphics/graphics.qrc")
if "<file>rb-videofire.png</file>" not in qrc:
    qrc = qrc.replace("<file>olive-splash.png</file>", "<file>olive-splash.png</file>\n        <file>rb-videofire.png</file>")
write("app/ui/graphics/graphics.qrc", qrc)

write(
    "app/packaging/windows/version.h",
    '''#ifndef VERSION_H
#define VERSION_H

#define VER_FILEVERSION             2,1,0,0
#define VER_FILEVERSION_STR         "2.1.0.0\\0"

#define VER_PRODUCTVERSION          2,1,0,0
#define VER_PRODUCTVERSION_STR      "2.1.0 Alpha Editorial\\0"

#define VER_COMPANYNAME_STR         "RB8 Digital"
#define VER_FILEDESCRIPTION_STR     "RB VideoFire"
#define VER_INTERNALNAME_STR        "RBVideoFire"
#define VER_LEGALCOPYRIGHT_STR      "Copyright © 2026 RB8 Digital; upstream notices retained under GNU GPL v3"
#define VER_LEGALTRADEMARKS1_STR    "RB VideoFire"
#define VER_LEGALTRADEMARKS2_STR    VER_LEGALTRADEMARKS1_STR
#define VER_ORIGINALFILENAME_STR    "RBVideoFire.exe"
#define VER_PRODUCTNAME_STR         "RB VideoFire"

#define VER_COMPANYDOMAIN_STR       "rb8.com.br"

#endif // VERSION_H
''',
)

write(
    "app/packaging/windows/resources.rc",
    '''IDI_ICON1   ICON    DISCARDABLE "rb-videofire.ico"
IDI_ICON2   ICON    DISCARDABLE "rb-videofire.ico"

#include <windows.h>
#include "version.h"

VS_VERSION_INFO VERSIONINFO
FILEVERSION     VER_FILEVERSION
PRODUCTVERSION  VER_PRODUCTVERSION
BEGIN
    BLOCK "StringFileInfo"
    BEGIN
        BLOCK "040904E4"
        BEGIN
            VALUE "CompanyName",        VER_COMPANYNAME_STR
            VALUE "FileDescription",    VER_FILEDESCRIPTION_STR
            VALUE "FileVersion",        VER_FILEVERSION_STR
            VALUE "InternalName",       VER_INTERNALNAME_STR
            VALUE "LegalCopyright",     VER_LEGALCOPYRIGHT_STR
            VALUE "LegalTrademarks1",   VER_LEGALTRADEMARKS1_STR
            VALUE "LegalTrademarks2",   VER_LEGALTRADEMARKS2_STR
            VALUE "OriginalFilename",   VER_ORIGINALFILENAME_STR
            VALUE "ProductName",        VER_PRODUCTNAME_STR
            VALUE "ProductVersion",     VER_PRODUCTVERSION_STR
        END
    END

    BLOCK "VarFileInfo"
    BEGIN
        VALUE "Translation", 0x409, 1252
    END
END
''',
)

ns = text("packaging/rb-videofire/RBVideoFire.nsi")
ns = ns.replace('!define VERSION "2.0.0 Alpha Native"', '!define VERSION "2.1.0 Alpha Editorial"')
ns = ns.replace(
    'OutFile "${SOURCE_ROOT}\\dist\\RB VideoFire Setup 2.0.0 Alpha Native.exe"',
    'OutFile "${SOURCE_ROOT}\\dist\\RB VideoFire Setup 2.1.0 Alpha Editorial.exe"',
)
needle = '!define DIST_DIR "${SOURCE_ROOT}\\dist\\portable"\n'
icons = '!define MUI_ICON "${SOURCE_ROOT}\\app\\packaging\\windows\\rb-videofire.ico"\n!define MUI_UNICON "${SOURCE_ROOT}\\app\\packaging\\windows\\rb-videofire.ico"\n'
if icons not in ns:
    ns = ns.replace(needle, needle + icons)
write("packaging/rb-videofire/RBVideoFire.nsi", ns)

# Branding binaries are generated from the canonical SVG by the workflow. Keeping binary
# generation out of this script avoids corrupt/truncated Base64 assets entering the build.
(root / "app/ui/graphics").mkdir(parents=True, exist_ok=True)
(root / "app/packaging/windows").mkdir(parents=True, exist_ok=True)

print("Applied RB VideoFire 2.1 Alpha Editorial patch")
