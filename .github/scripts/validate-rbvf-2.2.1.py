from pathlib import Path
import sys
root = Path(sys.argv[1])
def read(rel): return (root / rel).read_text(encoding='utf-8')
cmake = read('CMakeLists.txt')
nsi = read('packaging/rb-videofire/RBVideoFire.nsi')
explorer = read('app/widget/projectexplorer/projectexplorer.cpp')
precache = read('app/task/precache/precachetask.cpp')
pt = read('app/ts/pt_BR.ts')
assert 'project(rb-videofire VERSION 2.2.1 LANGUAGES CXX)' in cmake
assert '2.2.1 Alpha Stability' in nsi
assert 'Create Render Cache' in explorer
assert 'Create Proxy Cache' not in explorer
assert 'Creating render cache' in precache
assert 'Creating proxy cache' not in precache
for channels in ('2.1', '5.1', '7.1'):
    assert f'144p {{{channels}?}}' not in pt
    assert f'<translation>{channels}</translation>' in pt
print('RB VideoFire 2.2.1 stability validation passed')
