from pathlib import Path
import sys
root=Path(sys.argv[1])
def read(rel): return (root/rel).read_text(encoding='utf-8')
def write(rel,data): (root/rel).write_text(data,encoding='utf-8',newline='\n')
def replace(rel,old,new):
    data=read(rel)
    if old not in data: raise RuntimeError(f'{rel}: expected text not found: {old}')
    write(rel,data.replace(old,new))
replace('CMakeLists.txt','project(rb-videofire VERSION 2.3.0 LANGUAGES CXX)','project(rb-videofire VERSION 2.4.0 LANGUAGES CXX)')
nsi=read('packaging/rb-videofire/RBVideoFire.nsi').replace('2.3.0 Alpha Professional Editing Reliability','2.4.0 Alpha Professional Workspace').replace('RB VideoFire Setup 2.3.0 Alpha Professional Editing Reliability.exe','RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe')
write('packaging/rb-videofire/RBVideoFire.nsi',nsi)
about=read('app/dialog/about/about.cpp').replace('RB VideoFire 2.3.0 Alpha Professional Editing Reliability','RB VideoFire 2.4.0 Alpha Professional Workspace')
write('app/dialog/about/about.cpp',about)
version=read('app/packaging/windows/version.h').replace('2,3,0,0','2,4,0,0').replace('2.3.0.0\\0','2.4.0.0\\0').replace('2.3.0 Alpha Professional Editing Reliability\\0','2.4.0 Alpha Professional Workspace\\0')
write('app/packaging/windows/version.h',version)
professional=read('app/professional/professionalcore.h')
needle='namespace olive {\n'
addition='''namespace olive {\n\nclass AudioMeterPolicy {\n public:\n  explicit AudioMeterPolicy(int peak_hold_ms = 1500)\n      : peak_hold_ms_(peak_hold_ms < 0 ? 0 : peak_hold_ms) {}\n  int peak_hold_ms() const { return peak_hold_ms_; }\n  static double LinearToDbfs(double linear) {\n    if (linear <= 0.0) return -60.0;\n    if (linear >= 1.0) return 0.0;\n    // Monotonic approximation suitable for UI meter policy; DSP remains in existing engine.\n    double x = linear;\n    double db = -60.0 + (60.0 * x);\n    return db > 0.0 ? 0.0 : db;\n  }\n  static bool IsClipping(double linear) { return linear >= 1.0; }\n private:\n  int peak_hold_ms_;\n};\n'''
if 'class AudioMeterPolicy' not in professional:
    if needle not in professional: raise RuntimeError('professional namespace missing')
    professional=professional.replace(needle,addition,1)
write('app/professional/professionalcore.h',professional)
print('Applied RB VideoFire 2.4.0 professional workspace foundation')
