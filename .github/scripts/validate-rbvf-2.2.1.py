from pathlib import Path
import sys
root = Path(sys.argv[1])
def read(rel): return (root / rel).read_text(encoding='utf-8')
cmake = read('CMakeLists.txt')
app_cmake = read('app/CMakeLists.txt')
nsi = read('packaging/rb-videofire/RBVideoFire.nsi')
about = read('app/dialog/about/about.cpp')
version = read('app/packaging/windows/version.h')
resources = read('app/packaging/windows/resources.rc')
explorer = read('app/widget/projectexplorer/projectexplorer.cpp')
precache = read('app/task/precache/precachetask.cpp')
pt = read('app/ts/pt_BR.ts')
assert 'project(rb-videofire VERSION 2.2.1 LANGUAGES CXX)' in cmake
assert '2.2.1 Alpha Stability' in nsi
# Windows GUI subsystem: no console/prompt must flash before the Qt application.
assert 'add_executable(olive-editor WIN32' in app_cmake or 'add_executable(RBVideoFire WIN32' in app_cmake
# Welcome text must be 2.2.1 and use ASCII-safe HTML entities for accented Portuguese.
assert 'RB VideoFire 2.2.1 Alpha Stability &amp; Audio' in about
assert 'Bem-vindo ao RB VideoFire' in about
assert '&eacute;' in about and '&iacute;' in about and '&atilde;' in about
assert 'RB VideoFire 2.2.0 Alpha Professional Editorial' not in about
# Windows metadata/icon identity.
assert '2,2,1,0' in version
assert '2.2.1.0\\0' in version
assert 'rb-videofire.ico' in resources
assert 'olive.ico' not in resources
assert 'olive_ove.ico' not in resources
assert 'Create Render Cache' in explorer
assert 'Create Proxy Cache' not in explorer
assert 'Creating render cache' in precache
assert 'Creating proxy cache' not in precache
for channels in ('2.1', '5.1', '7.1'):
    assert f'144p {{{channels}?}}' not in pt
    assert f'<translation>{channels}</translation>' in pt
print('RB VideoFire 2.2.1 stability validation passed')
