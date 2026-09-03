# RB VideoFire 2.4.0 Professional Workspace Design

## Objective
Transformar o workspace da linha 2.3 em uma estação de edição mais profissional, legível e própria do RB VideoFire, preservando o núcleo nativo já funcional.

## Scope
- Priorizar Program Monitor e Timeline no workspace padrão.
- Manter Source Monitor e Inspector/Parameter Editor acessíveis sem dominar a tela.
- Node Editor deixa de ocupar o workspace editorial padrão e permanece acessível pelo menu.
- Audio Monitor deve apresentar medição dBFS útil, peak hold e indicação de clipping, sem bloquear playback.
- Project Bin deve manter lista e thumbnails e tornar importação e metadados mais claros.
- Tools deve receber nomes/tooltips e atalhos compreensíveis.
- Padronizar o workspace padrão em PT-BR, sem remover suporte aos demais idiomas.
- Preservar abertura Windows sem console e identidade RB VideoFire.

## Layout
Topo: menus e acesso aos workspaces.
Superior esquerdo: Source Monitor e Inspector.
Superior centro/direita: Program Monitor com prioridade de espaço.
Inferior esquerdo: Projeto, Efeitos e Histórico.
Inferior centro: Timeline como maior área operacional.
Direita: Audio Monitor e futuro Audio Mixer.

## Audio Monitor
O monitor deve consumir os níveis de áudio já calculados pelo motor existente, evitando criar um segundo pipeline de áudio. A apresentação visual deve trabalhar em dBFS, indicar clipping no máximo digital e manter peak hold. Estéreo é o primeiro contrato obrigatório; layouts multicanal existentes não podem regredir.

## Editing UX
Timeline deve tornar tracks e controles editoriais mais legíveis. Tools devem expor Selection, Ripple Trim, Roll Trim, Razor, Slip, Slide, Hand e Zoom com tooltip/atalho quando já houver comando correspondente. Nenhum motor de edição paralelo será criado apenas para a interface.

## Identity
A versão será exibida como `RB VideoFire 2.4.0 Alpha Professional Workspace`. A atualização deve reduzir elementos visuais herdados que prejudiquem a identidade própria, sem reescrever componentes funcionais apenas por cosmética.

## Validation
A build Windows deve passar testes CMake/CTest, validação de identidade, startup smoke test sem console, teste do contrato do Audio Monitor e auditoria do instalador. Nome final: `RB VideoFire Setup 2.4.0 Alpha Professional Workspace.exe`.
