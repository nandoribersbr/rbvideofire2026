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

# RB VideoFire 2.2 welcome/about copy. Replace the entire text/layout section produced by
# the previous branding layer so cumulative builds cannot restore the older English copy.
about = read('app/dialog/about/about.cpp')
start = about.index('  // Construct RB VideoFire About text')
end = about.index('  QHBoxLayout *btn_layout', start)
welcome_block = '''  // Construct RB VideoFire welcome/about text
  QLabel* label = new QLabel(QStringLiteral(
      "<html><head/><body>"
      "<h2>Bem-vindo ao RB VideoFire</h2>"
      "<p>O RB VideoFire é um editor de vídeo profissional desenvolvido para oferecer velocidade, precisão e liberdade criativa em um ambiente de edição completo.</p>"
      "<p>Organize suas mídias, construa sua narrativa na timeline, trabalhe áudio, efeitos, transições, títulos e finalize seus projetos em um único fluxo de trabalho.</p>"
      "<p>Esta é uma versão Alpha. O software está em desenvolvimento contínuo e novos recursos, melhorias de desempenho e ferramentas profissionais serão incorporados progressivamente.</p>"
      "<p><b>RB VideoFire 2.2.0 Alpha Professional Editorial</b><br/>"
      "Desenvolvido por <b>JOSÉ FERNANDO - RB8 Digital</b></p>"
      "<p><b>Crie. Edite. Conte sua história.</b></p>"
      "</body></html>"));

  label->setAlignment(Qt::AlignLeft | Qt::AlignVCenter);
  label->setWordWrap(true);
  label->setMinimumWidth(420);
  label->setOpenExternalLinks(false);
  label->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Minimum);
  label->setTextInteractionFlags(Qt::TextSelectableByMouse);
  label->setCursor(Qt::IBeamCursor);
  horiz_layout->addWidget(label);

  layout->addLayout(horiz_layout);
  layout->addWidget(new QLabel());

'''
write('app/dialog/about/about.cpp', about[:start] + welcome_block + about[end:])

# 2.1 already branded this prompt, so 2.2 evolves from the actual 2.1.1 output.
core = read('app/core.cpp')
first = 'The following projects had unsaved changes when RB VideoFire '
second = 'forcefully quit. Would you like to load them?'
if first not in core or second not in core:
    raise RuntimeError('app/core.cpp: branded auto-recovery prompt literals not found')
core = core.replace(first, 'RB VideoFire found recoverable project snapshots from the previous session. ')
core = core.replace(second, 'Would you like to load them?')
write('app/core.cpp', core)

print('Applied RB VideoFire 2.2 professional editorial identity and welcome copy')