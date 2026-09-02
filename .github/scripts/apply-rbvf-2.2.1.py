from pathlib import Path
import sys
root = Path(sys.argv[1])
def read(rel): return (root / rel).read_text(encoding='utf-8')
def write(rel, data):
    p=root/rel; p.write_text(data, encoding='utf-8', newline='\n')
def replace(rel, old, new):
    data=read(rel)
    if old not in data: raise RuntimeError(f'{rel}: expected text not found: {old}')
    write(rel, data.replace(old,new))

replace('CMakeLists.txt','project(rb-videofire VERSION 2.2.0 LANGUAGES CXX)','project(rb-videofire VERSION 2.2.1 LANGUAGES CXX)')

nsi=read('packaging/rb-videofire/RBVideoFire.nsi')
nsi=nsi.replace('2.2.0 Alpha Professional Editorial','2.2.1 Alpha Stability Audio')
nsi=nsi.replace('RB VideoFire Setup 2.2.0 Alpha Professional Editorial.exe','RB VideoFire Setup 2.2.1 Alpha Stability Audio.exe')
write('packaging/rb-videofire/RBVideoFire.nsi',nsi)

# PreCache renders frames into the render cache. Do not present it as a true proxy workflow.
replace('app/widget/projectexplorer/projectexplorer.cpp','Create Proxy Cache','Create Render Cache')
replace('app/widget/projectexplorer/projectexplorer.cpp','Proxy Cache for','Render Cache for')
replace('app/task/precache/precachetask.cpp','Creating proxy cache','Creating render cache')

# Fix corrupt Portuguese channel-layout translations found by the audit.
pt=read('app/ts/pt_BR.ts')
for channels in ('2.1','5.1','7.1'):
    pt=pt.replace(f'<translation type="unfinished">144p {{{channels}?}}</translation>', f'<translation>{channels}</translation>')
write('app/ts/pt_BR.ts',pt)
print('Applied RB VideoFire 2.2.1 audited stability corrections')
