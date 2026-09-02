from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

cmake = read('CMakeLists.txt')
nsi = read('packaging/rb-videofire/RBVideoFire.nsi')
main = read('app/main.cpp')
qrc = read('app/ui/graphics/graphics.qrc')
app_cmake = read('app/CMakeLists.txt')
menu = read('app/window/mainwindow/mainmenu.cpp')
viewer = read('app/widget/viewer/viewer.cpp')
explorer = read('app/widget/projectexplorer/projectexplorer.cpp')
config = read('app/config/config.cpp')
core = read('app/core.cpp')
about = read('app/dialog/about/about.cpp')
professional = read('app/professional/professionalcore.h')
professional_test = read('tests/general/rb-professional-core-tests.cpp')
general_tests = read('tests/general/CMakeLists.txt')

assert 'project(rb-videofire VERSION 2.2.0 LANGUAGES CXX)' in cmake
assert '2.2.0 Alpha Professional Editorial' in nsi
assert 'RB VideoFire Setup 2.2.0 Alpha Professional Editorial.exe' in nsi

# Preserve the audited 2.1.1 startup fix.
app_index = main.index('a.reset(new QApplication(argc, argv));')
icon_index = main.index('QApplication::setWindowIcon(QIcon(QStringLiteral(":/graphics/rb-videofire.png")));')
assert icon_index > app_index
assert 'olive-splash.png' not in qrc
assert 'rb-videofire.png' in qrc

# Welcome/About identity must survive cumulative patches.
assert 'Bem-vindo ao RB VideoFire' in about
assert 'O RB VideoFire é um editor de vídeo profissional desenvolvido para oferecer velocidade, precisão e liberdade criativa' in about
assert 'Organize suas mídias, construa sua narrativa na timeline' in about
assert 'Esta é uma versão Alpha.' in about
assert 'RB VideoFire 2.2.0 Alpha Professional Editorial' in about
assert 'JOSÉ FERNANDO - RB8 Digital' in about
assert 'Crie. Edite. Conte sua história.' in about

# Professional core contracts.
assert 'add_subdirectory(professional)' in app_cmake
assert 'class TrimState' in professional
assert 'class PlaybackQuality' in professional
assert 'class MediaProxyState' in professional
assert 'class RecoveryPolicy' in professional
assert 'kDefaultMaximumSnapshots = 50' in professional
assert 'olive_add_test(General rb-professional-core-tests rb-professional-core-tests.cpp)' in general_tests
assert 'OLIVE_ADD_TEST(RBProfessionalTrimState)' in professional_test
assert 'OLIVE_ADD_TEST(RBPlaybackQuality)' in professional_test
assert 'OLIVE_ADD_TEST(RBMediaProxyState)' in professional_test
assert 'OLIVE_ADD_TEST(RBRecoveryPolicy)' in professional_test

# User-visible professional workflow.
assert 'Render Cache Entire Sequence' in menu
assert 'Render Cache In/Out' in menu
assert 'Clear Render Cache' in menu
assert 'Ripple Trim Tool' in menu
assert 'Roll Trim Tool' in menu
assert 'Slip Edit Tool' in menu
assert 'Slide Edit Tool' in menu
assert 'const QVector<int> professional_dividers = {1, 2, 4, 8};' in viewer
assert 'Create Proxy Cache' in explorer
assert 'rb::RecoveryPolicy::kDefaultMaximumSnapshots' in config
assert 'RB VideoFire found recoverable project snapshots' in core

print('RB VideoFire 2.2 professional editorial contract validation passed')