from pathlib import Path
import sys
root = Path(sys.argv[1])
def read(rel): return (root / rel).read_text(encoding='utf-8')
def write(rel, data): (root / rel).write_text(data, encoding='utf-8', newline='\n')
def replace(rel, old, new):
    data=read(rel)
    if old not in data: raise RuntimeError(f'{rel}: expected text not found')
    write(rel, data.replace(old,new))
replace('CMakeLists.txt','project(rb-videofire VERSION 2.2.0 LANGUAGES CXX)','project(rb-videofire VERSION 2.2.1 LANGUAGES CXX)')
nsi=read('packaging/rb-videofire/RBVideoFire.nsi').replace('2.2.0 Alpha Professional Editorial','2.2.1 Alpha Stability Audio').replace('RB VideoFire Setup 2.2.0 Alpha Professional Editorial.exe','RB VideoFire Setup 2.2.1 Alpha Stability Audio.exe')
write('packaging/rb-videofire/RBVideoFire.nsi',nsi)
app=read('app/CMakeLists.txt')
if 'add_executable(olive-editor\n' in app: app=app.replace('add_executable(olive-editor\n','add_executable(olive-editor WIN32\n')
elif 'add_executable(RBVideoFire\n' in app: app=app.replace('add_executable(RBVideoFire\n','add_executable(RBVideoFire WIN32\n')
write('app/CMakeLists.txt',app)
about=read('app/dialog/about/about.cpp')
start=about.index('  // Construct RB VideoFire welcome/about text')
end=about.index('  QHBoxLayout *btn_layout', start)
welcome='''  // Construct RB VideoFire welcome/about text
  QLabel* label = new QLabel(QStringLiteral(
      "<html><head/><body>"
      "<h2>Bem-vindo ao RB VideoFire</h2>"
      "<p>O RB VideoFire &eacute; um editor de v&iacute;deo profissional desenvolvido para oferecer velocidade, precis&atilde;o e liberdade criativa em um ambiente de edi&ccedil;&atilde;o completo.</p>"
      "<p>Organize suas m&iacute;dias, construa sua narrativa na timeline, trabalhe &aacute;udio, efeitos, transi&ccedil;&otilde;es, t&iacute;tulos e finalize seus projetos em um &uacute;nico fluxo de trabalho.</p>"
      "<p>Esta &eacute; uma vers&atilde;o Alpha. O software est&aacute; em desenvolvimento cont&iacute;nuo e novos recursos, melhorias de desempenho e ferramentas profissionais ser&atilde;o incorporados progressivamente.</p>"
      "<p><b>RB VideoFire 2.2.1 Alpha Stability &amp; Audio</b><br/>"
      "Desenvolvido por <b>JOS&Eacute; FERNANDO - RB8 Digital</b></p>"
      "<p><b>Crie. Edite. Conte sua hist&oacute;ria.</b></p>"
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
write('app/dialog/about/about.cpp', about[:start]+welcome+about[end:])
version=read('app/packaging/windows/version.h').replace('2,2,0,0','2,2,1,0').replace('"2.2.0.0\\0"','"2.2.1.0\\0"').replace('"2.2.0 Alpha Professional Editorial\\0"','"2.2.1 Alpha Stability Audio\\0"')
write('app/packaging/windows/version.h',version)
replace('app/widget/projectexplorer/projectexplorer.cpp','Create Proxy Cache','Create Render Cache')
replace('app/widget/projectexplorer/projectexplorer.cpp','Proxy Cache for','Render Cache for')
replace('app/task/precache/precachetask.cpp','Creating proxy cache','Creating render cache')
pt=read('app/ts/pt_BR.ts')
for channels in ('2.1','5.1','7.1'): pt=pt.replace(f'<translation type="unfinished">144p {{{channels}?}}</translation>', f'<translation>{channels}</translation>')
write('app/ts/pt_BR.ts',pt)
print('Applied RB VideoFire 2.2.1 startup and stability corrections')
