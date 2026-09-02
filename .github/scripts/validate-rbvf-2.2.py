from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

cmake = read('CMakeLists.txt')
nsi = read('packaging/rb-videofire/RBVideoFire.nsi')
main = read('app/main.cpp')
qrc = read('app/ui/graphics/graphics.qrc')

assert 'project(rb-videofire VERSION 2.2.0 LANGUAGES CXX)' in cmake
assert '2.2.0 Alpha Professional Editorial' in nsi
assert 'RB VideoFire Setup 2.2.0 Alpha Professional Editorial.exe' in nsi

app_index = main.index('a.reset(new QApplication(argc, argv));')
icon_index = main.index('QApplication::setWindowIcon(QIcon(QStringLiteral(":/graphics/rb-videofire.png")));')
assert icon_index > app_index
assert 'olive-splash.png' not in qrc
assert 'rb-videofire.png' in qrc

print('RB VideoFire 2.2 contract validation passed')