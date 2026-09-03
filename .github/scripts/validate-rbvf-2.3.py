from pathlib import Path
import sys
root = Path(sys.argv[1])
def read(rel): return (root / rel).read_text(encoding='utf-8')
cmake=read('CMakeLists.txt')
app_cmake=read('app/CMakeLists.txt')
nsi=read('packaging/rb-videofire/RBVideoFire.nsi')
about=read('app/dialog/about/about.cpp')
version=read('app/packaging/windows/version.h')
professional=read('app/professional/professionalcore.h')
explorer=read('app/widget/projectexplorer/projectexplorer.cpp')
precache=read('app/task/precache/precachetask.cpp')
assert 'project(rb-videofire VERSION 2.3.0 LANGUAGES CXX)' in cmake
assert 'RB VideoFire Setup 2.3.0 Alpha Professional Editing Reliability.exe' in nsi
assert 'RB VideoFire 2.3.0 Alpha Professional Editing Reliability' in about
assert '2,3,0,0' in version and '2.3.0.0\\0' in version
assert 'add_executable(olive-editor WIN32' in app_cmake or 'add_executable(RBVideoFire WIN32' in app_cmake
assert 'class AVSyncPolicy' in professional
assert 'IsWithinTolerance' in professional
assert 'Create Proxy Media' in explorer
assert 'Creating proxy media' in precache
assert 'Create Render Cache' not in explorer
print('RB VideoFire 2.3 reliability validation passed')
