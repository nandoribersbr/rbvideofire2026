from pathlib import Path
import struct
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

# Runtime icon may only be instantiated after QApplication exists.
icon_stmt = 'QApplication::setWindowIcon(QIcon(QStringLiteral(":/graphics/rb-videofire.png")));'
assert icon_stmt in main, "runtime RB icon not applied"
assert main.index(icon_stmt) > main.index('a.reset(new QApplication(argc, argv));'), \
       "runtime icon is being constructed before QApplication"

# Public Qt resources must contain only RB branding.
assert '<file>rb-videofire.png</file>' in qrc
assert '<file>olive-splash.png</file>' not in qrc, "legacy Olive splash still embedded"

png = root / "app/ui/graphics/rb-videofire.png"
png_bytes = png.read_bytes()
assert png_bytes[:8] == b'\x89PNG\r\n\x1a\n', "RB logo is not a PNG"
width, height = struct.unpack(">II", png_bytes[16:24])
assert width >= 256 and height >= 256, f"RB logo is too small: {width}x{height}"
assert png.stat().st_size > 20000, "RB logo asset is suspiciously small/corrupt"

ico = root / "app/packaging/windows/rb-videofire.ico"
ico_bytes = ico.read_bytes()
assert ico_bytes[:4] == b'\x00\x00\x01\x00', "RB Windows icon is not a valid ICO container"
assert len(ico_bytes) > 20000, "RB Windows icon asset is suspiciously small/corrupt"

assert 'QPixmap rb_icon(QStringLiteral(":/graphics/rb-videofire.png"));' in about or 'QPixmap rb_icon(QStringLiteral(":/graphics/rb-videofire.png"))' in about
assert 'rb_icon.isNull()' in about
assert 'RB\\nVideoFire' in about
assert "olive-splash.png" not in about
assert "RB VideoFire 2.1.1 Alpha Editorial" in about
assert "project(rb-videofire VERSION 2.1.1 LANGUAGES CXX)" in cmake
assert '!define VERSION "2.1.1 Alpha Editorial"' in nsis
assert "RB VideoFire Setup 2.1.1 Alpha Editorial.exe" in nsis
assert 'VER_FILEVERSION             2,1,1,0' in version
assert 'VER_PRODUCTVERSION_STR      "2.1.1 Alpha Editorial\\0"' in version

print("RB VideoFire 2.1.1 startup/icon/language contract OK")
