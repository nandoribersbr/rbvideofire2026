from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

def write(rel, data):
    (root / rel).write_text(data, encoding='utf-8', newline='\n')

def replace(rel, old, new):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f'{rel}: expected text not found: {old!r}')
    write(rel, data.replace(old, new))

replace('CMakeLists.txt',
        'project(rb-videofire VERSION 2.1.1 LANGUAGES CXX)',
        'project(rb-videofire VERSION 2.2.0 LANGUAGES CXX)')

replace('packaging/rb-videofire/RBVideoFire.nsi',
        '!define VERSION "2.1.1 Alpha Editorial"',
        '!define VERSION "2.2.0 Alpha Professional Editorial"')
replace('packaging/rb-videofire/RBVideoFire.nsi',
        'RB VideoFire Setup 2.1.1 Alpha Editorial.exe',
        'RB VideoFire Setup 2.2.0 Alpha Professional Editorial.exe')

version = read('app/packaging/windows/version.h')
version = version.replace('2,1,1,0', '2,2,0,0')
version = version.replace('"2.1.1.0\\0"', '"2.2.0.0\\0"')
version = version.replace('"2.1.1 Alpha Editorial\\0"', '"2.2.0 Alpha Professional Editorial\\0"')
write('app/packaging/windows/version.h', version)

about = read('app/dialog/about/about.cpp')
about = about.replace('RB VideoFire 2.1.1 Alpha Editorial • RB8 Digital',
                      'RB VideoFire 2.2.0 Alpha Professional Editorial • RB8 Digital')
write('app/dialog/about/about.cpp', about)

# 2.1 already branded this prompt, so 2.2 evolves from the actual 2.1.1 output.
core = read('app/core.cpp')
first = 'The following projects had unsaved changes when RB VideoFire '
second = 'forcefully quit. Would you like to load them?'
if first not in core or second not in core:
    raise RuntimeError('app/core.cpp: branded auto-recovery prompt literals not found')
core = core.replace(first, 'RB VideoFire found recoverable project snapshots from the previous session. ')
core = core.replace(second, 'Would you like to load them?')
write('app/core.cpp', core)

print('Applied RB VideoFire 2.2 professional editorial identity')