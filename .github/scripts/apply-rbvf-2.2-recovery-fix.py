from pathlib import Path
import sys

root = Path(sys.argv[1])
path = root / 'app/core.cpp'
data = path.read_text(encoding='utf-8')

old = '''      AutoRecoveryDialog ard(tr("The following projects had unsaved changes when Olive "
                                "forcefully quit. Would you like to load them?"),'''
new = '''      AutoRecoveryDialog ard(tr("RB VideoFire found recoverable project snapshots from the previous session. "
                                "Would you like to load them?"),'''

if old not in data:
    raise RuntimeError('Split auto-recovery prompt block not found')

path.write_text(data.replace(old, new), encoding='utf-8', newline='\n')
print('Applied RB VideoFire 2.2 recovery prompt fix')