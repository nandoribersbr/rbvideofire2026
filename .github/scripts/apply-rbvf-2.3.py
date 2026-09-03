from pathlib import Path
import sys
root=Path(sys.argv[1])
def read(rel): return (root/rel).read_text(encoding='utf-8')
def write(rel,data): (root/rel).write_text(data,encoding='utf-8',newline='\n')
def replace(rel,old,new):
    data=read(rel)
    if old not in data: raise RuntimeError(f'{rel}: expected text not found: {old}')
    write(rel,data.replace(old,new))
replace('CMakeLists.txt','project(rb-videofire VERSION 2.2.1 LANGUAGES CXX)','project(rb-videofire VERSION 2.3.0 LANGUAGES CXX)')
nsi=read('packaging/rb-videofire/RBVideoFire.nsi').replace('2.2.1 Alpha Stability Audio','2.3.0 Alpha Professional Editing Reliability').replace('RB VideoFire Setup 2.2.1 Alpha Stability Audio.exe','RB VideoFire Setup 2.3.0 Alpha Professional Editing Reliability.exe')
write('packaging/rb-videofire/RBVideoFire.nsi',nsi)
about=read('app/dialog/about/about.cpp').replace('RB VideoFire 2.2.1 Alpha Stability &amp; Audio','RB VideoFire 2.3.0 Alpha Professional Editing Reliability')
write('app/dialog/about/about.cpp',about)
version=read('app/packaging/windows/version.h').replace('2,2,1,0','2,3,0,0').replace('2.2.1.0\\0','2.3.0.0\\0').replace('2.2.1 Alpha Stability Audio\\0','2.3.0 Alpha Professional Editing Reliability\\0')
write('app/packaging/windows/version.h',version)
professional=read('app/professional/professionalcore.h')
marker='namespace olive {\n'
addition='''namespace olive {\n\nclass AVSyncPolicy {\n public:\n  explicit AVSyncPolicy(int tolerance_frames = 1)\n      : tolerance_frames_(tolerance_frames < 0 ? 0 : tolerance_frames) {}\n  int tolerance_frames() const { return tolerance_frames_; }\n  bool IsWithinTolerance(int drift_frames) const {\n    const int magnitude = drift_frames < 0 ? -drift_frames : drift_frames;\n    return magnitude <= tolerance_frames_;\n  }\n private:\n  int tolerance_frames_;\n};\n'''
if 'class AVSyncPolicy' not in professional:
    if marker not in professional: raise RuntimeError('professionalcore namespace marker missing')
    professional=professional.replace(marker,addition,1)
write('app/professional/professionalcore.h',professional)
replace('app/widget/projectexplorer/projectexplorer.cpp','Create Render Cache','Create Proxy Media')
replace('app/widget/projectexplorer/projectexplorer.cpp','Render Cache for','Proxy Media for')
replace('app/task/precache/precachetask.cpp','Creating render cache','Creating proxy media')
print('Applied RB VideoFire 2.3.0 professional editing reliability baseline')
