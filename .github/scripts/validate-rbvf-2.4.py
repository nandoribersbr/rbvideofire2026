from pathlib import Path
import sys
root=Path(sys.argv[1])
def read(rel): return (root/rel).read_text(encoding='utf-8')
cmake=read('CMakeLists.txt')
app=read('app/CMakeLists.txt')
nsi=read('packaging/rb-videofire/RBVideoFire.nsi')
about=read('app/dialog/about/about.cpp')
version=read('app/packaging/windows/version.h')
professional=read('app/professional/professionalcore.h')
assert 'project(rb-videofire VERSION 2.4.0 LANGUAGES CXX)' in cmake
assert 'RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe' in nsi
assert 'RB VideoFire 2.4.0 Alpha Professional Workspace' in about
assert '2,4,0,0' in version and '2.4.0.0\\0' in version
assert 'add_executable(olive-editor WIN32' in app or 'add_executable(RBVideoFire WIN32' in app
assert 'class AudioMeterPolicy' in professional
assert 'LinearToDbfs' in professional
assert 'std::log10' in professional
assert '20.0 * std::log10' in professional
assert 'IsClipping' in professional
assert 'peak_hold_ms' in professional
# QA-029 reference points: 1.0 = 0 dBFS, 0.5 ~= -6.02 dBFS, 0.1 = -20 dBFS.
assert '-60.0' in professional
print('RB VideoFire 2.4 professional workspace validation passed')
