from pathlib import Path
import sys

root = Path(sys.argv[1])


def text(rel):
    return (root / rel).read_text(encoding="utf-8")

prefs = text("app/dialog/preferences/tabs/preferencesgeneraltab.cpp")
core = text("app/core.cpp")
config = text("app/config/config.cpp")
about = text("app/dialog/about/about.cpp")
main = text("app/main.cpp")
cmake = text("CMakeLists.txt")
nsis = text("packaging/rb-videofire/RBVideoFire.nsi")
version = text("app/packaging/windows/version.h")
qrc = text("app/ui/graphics/graphics.qrc")

assert 'QStringLiteral("pt_BR")' in config
assert 'use_locale = QStringLiteral("pt_BR")' in core

for locale in ["pt_BR", "en_US", "es_ES", "it_IT", "fr_FR", "zh_CN", "ja_JP"]:
    assert f'QStringLiteral("{locale}")' in prefs, f"missing selectable locale {locale}"

for locale in ["de_DE", "ru_RU", "zh_TW"]:
    assert f'QStringLiteral("{locale}")' not in prefs, f"unexpected selectable locale {locale}"

# Visual identity contract: embedded logo exists, About uses it with a fallback,
# and QApplication explicitly applies it to all runtime windows/taskbar entries.
assert '<file>rb-videofire.png</file>' in qrc
assert (root / "app/ui/graphics/rb-videofire.png").stat().st_size > 0
assert 'QPixmap rb_icon(QStringLiteral(":/graphics/rb-videofire.png"));' in about or 'QPixmap rb_icon(QStringLiteral(":/graphics/rb-videofire.png"))' in about
assert 'rb_icon.isNull()' in about
assert 'RB\\nVideoFire' in about
assert 'QApplication::setWindowIcon(QIcon(QStringLiteral(":/graphics/rb-videofire.png")));' in main
assert "olive-splash.png" not in about
assert "RB VideoFire 2.1.1 Alpha Editorial" in about
assert "project(rb-videofire VERSION 2.1.1 LANGUAGES CXX)" in cmake
assert '!define VERSION "2.1.1 Alpha Editorial"' in nsis
assert "RB VideoFire Setup 2.1.1 Alpha Editorial.exe" in nsis
assert 'VER_FILEVERSION             2,1,1,0' in version
assert 'VER_PRODUCTVERSION_STR      "2.1.1 Alpha Editorial\\0"' in version

print("RB VideoFire 2.1.1 language/runtime-icon contract OK")
