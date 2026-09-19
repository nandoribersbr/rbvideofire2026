from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

apply_script = read('.github/scripts/apply-rbvf-2.5.1-professional-ui.py')
required = [
    'RBProfessionalUI',
    'RBPanelCloseButton',
    'rb-panel-close.svg',
    'QToolBar#RBWorkspaceBar',
    'Mídia', 'Edição', 'Composição', 'Cor', 'Áudio', 'Entrega',
    'NO_SECOND_PLAYBACK_ENGINE',
    '2.5.1 Alpha Professional UI',
]
missing = [token for token in required if token not in apply_script]
if missing:
    raise SystemExit('2.5.1 Professional UI contract missing: ' + ', '.join(missing))

svg = read('.github/assets/rb-panel-close.svg')
if '<svg' not in svg or '<path' not in svg:
    raise SystemExit('RB panel close SVG is invalid')
if 'olive' in svg.lower():
    raise SystemExit('RB panel close SVG must not carry Olive identity')

print('RB VideoFire 2.5.1 Professional UI contract: PASS')
