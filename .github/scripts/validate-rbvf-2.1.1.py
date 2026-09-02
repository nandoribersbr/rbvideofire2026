from pathlib import Path
import struct
import sys
import zlib

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

# Regression for the fatal crash reported on Windows: constructing QIcon/QPixmap before
# QApplication exists triggers "QPixmap: Must construct a QGuiApplication before a QPixmap".
icon_stmt = 'QApplication::setWindowIcon(QIcon(QStringLiteral(":/graphics/rb-videofire.png")));'
app_stmt = 'a.reset(new QApplication(argc, argv));'
assert icon_stmt in main, "runtime RB icon not applied"
assert app_stmt in main, "QApplication construction marker missing"
assert main.index(icon_stmt) > main.index(app_stmt), "runtime icon is being constructed before QApplication"

# No public Olive splash is allowed in the Qt resource bundle.
assert '<file>rb-videofire.png</file>' in qrc
assert '<file>olive-splash.png</file>' not in qrc, "legacy Olive splash still embedded"

# Deep PNG validation: signature, CRCs, IHDR, zlib stream and adaptive-filter bytes.
# This catches the exact libpng "bad adaptive filter value" failure, not just a file header.
png = root / "app/ui/graphics/rb-videofire.png"
png_bytes = png.read_bytes()
assert png_bytes[:8] == b'\x89PNG\r\n\x1a\n', "RB logo is not a PNG"
pos = 8
idat = []
ihdr = None
while pos < len(png_bytes):
    assert pos + 12 <= len(png_bytes), "truncated PNG chunk"
    length = struct.unpack(">I", png_bytes[pos:pos + 4])[0]
    kind = png_bytes[pos + 4:pos + 8]
    data = png_bytes[pos + 8:pos + 8 + length]
    crc_expected = struct.unpack(">I", png_bytes[pos + 8 + length:pos + 12 + length])[0]
    crc_actual = zlib.crc32(kind)
    crc_actual = zlib.crc32(data, crc_actual) & 0xFFFFFFFF
    assert crc_actual == crc_expected, f"PNG CRC mismatch in {kind!r}"
    if kind == b'IHDR':
        ihdr = data
    elif kind == b'IDAT':
        idat.append(data)
    elif kind == b'IEND':
        break
    pos += 12 + length

assert ihdr is not None and len(ihdr) == 13, "PNG IHDR missing"
width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", ihdr)
assert width >= 256 and height >= 256, f"RB logo is too small: {width}x{height}"
assert bit_depth == 8 and color_type == 6, f"RB logo must be RGBA8, got depth={bit_depth} type={color_type}"
assert compression == 0 and filter_method == 0 and interlace == 0, "unsupported PNG encoding"
raw = zlib.decompress(b''.join(idat))
stride = width * 4
expected = height * (stride + 1)
assert len(raw) == expected, f"unexpected PNG scanline size: {len(raw)} != {expected}"
for row in range(height):
    filter_byte = raw[row * (stride + 1)]
    assert 0 <= filter_byte <= 4, f"bad adaptive filter value {filter_byte} on row {row}"
assert png.stat().st_size > 20000, "RB logo asset is suspiciously small/corrupt"

ico = root / "app/packaging/windows/rb-videofire.ico"
ico_bytes = ico.read_bytes()
assert ico_bytes[:4] == b'\x00\x00\x01\x00', "RB Windows icon is not a valid ICO container"
icon_count = struct.unpack("<H", ico_bytes[4:6])[0]
assert icon_count >= 5, f"RB Windows ICO must contain multiple sizes, got {icon_count}"
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
