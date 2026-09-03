# RB VideoFire 2.5.0 Multi-Workspace Post Design

## Objective
Evoluir o RB VideoFire para um ambiente de pós-produção integrado baseado em cinco workspaces especializados, acessíveis por uma barra fixa na parte inferior da interface, preservando o mesmo projeto, sequência, playhead, seleção e estado editorial ao alternar entre eles.

A versão desta arquitetura será identificada como `RB VideoFire 2.5.0 Alpha Multi-Workspace Post`.

## Workspaces inferiores
A barra inferior será fixa e exibirá, nesta ordem:

`Edição | Áudio | Cor | Efeitos | Entrega`

A troca de workspace não recarrega o projeto, não recria a sequência e não duplica o motor de edição. Cada workspace é uma composição de painéis e ferramentas sobre o mesmo estado de projeto.

A aba ativa deve ter destaque visual claro. A arquitetura deve permitir atalhos de teclado para alternar entre workspaces e preservar customizações de layout.

## Estado compartilhado
Os workspaces compartilham um único contexto de projeto contendo, no mínimo:
- projeto atual;
- sequência ativa;
- clipe ou item selecionado;
- posição do playhead;
- In/Out;
- estado de mídia original/proxy/otimizada;
- cache e pré-render válidos;
- alterações pendentes e histórico/undo quando aplicável.

Trocar de workspace muda a disposição e as ferramentas, não o conteúdo editorial.

## Workspace Edição
O workspace Edição mantém o fluxo NLE principal.

Layout recomendado:
- superior esquerdo: Source Monitor e Inspetor;
- superior centro/direita: Program Monitor com maior prioridade de espaço;
- inferior esquerdo: Projeto, Efeitos e Histórico;
- inferior centro: Timeline como principal área operacional;
- direita: Audio Monitor compacto;
- barra inferior: seletor de workspaces.

O Source Monitor e o Program Monitor permanecem simultaneamente disponíveis. A Timeline deve continuar usando o motor editorial existente e expor Selection, Ripple Trim, Roll Trim, Razor, Slip, Slide, Hand e Zoom quando já houver comandos equivalentes.

## Workspace Áudio
O workspace Áudio será uma estação de pós-produção de som integrada, semelhante em capacidade a uma DAW enxuta, sem criar uma timeline ou projeto paralelo.

Recursos previstos:
- timeline com tracks de áudio ampliadas;
- mixer por track e master bus;
- medidores em dBFS;
- peak hold e clipping;
- fader;
- pan;
- mute e solo;
- ganho;
- EQ;
- compressor;
- limiter;
- automação de parâmetros;
- monitoramento estéreo como primeiro contrato obrigatório;
- evolução posterior para layouts multicanal sem regressão.

O Audio Monitor deve consumir níveis já calculados pelo motor de áudio existente. Não deve existir um segundo pipeline de áudio apenas para alimentar a interface.

## Workspace Cor
O workspace Cor será baseado em nodes desde a primeira versão funcional.

Fluxo conceitual mínimo:
`Media In -> Nodes de correção -> Media Out`

Recursos previstos:
- viewer grande;
- waveform;
- parade RGB;
- vectorscope;
- histogram quando tecnicamente adequado;
- Lift, Gamma e Gain;
- exposição;
- contraste;
- saturação;
- temperatura e tint;
- curvas RGB/HSL;
- LUTs;
- comparação antes/depois;
- máscaras;
- qualifiers;
- tracking;
- nodes seriais;
- preparação arquitetural para nodes paralelos, layer mixer e correções compartilhadas.

As operações devem ser não destrutivas e vinculadas ao clipe, evento ou contexto de grading definido pelo projeto.

## Workspace Efeitos
O workspace Efeitos usará composição baseada em camadas, e não nodes, como paradigma principal de interface.

O fluxo deve lembrar a lógica operacional de um compositor por camadas, mantendo arquitetura e identidade próprias do RB VideoFire.

Recursos previstos:
- composição vinculada a um clipe, trecho ou item gráfico da sequência;
- pilha de camadas;
- timeline de composição própria para animação, distinta visualmente da timeline editorial;
- propriedades expansíveis;
- keyframes;
- posição;
- escala;
- rotação;
- opacidade;
- máscaras;
- modos de mesclagem;
- texto e títulos;
- chroma key;
- tracking;
- estabilização;
- efeitos de transformação;
- preparação arquitetural para partículas e recursos avançados.

Fluxo editorial esperado:
`Edição -> Abrir em Efeitos -> Composição -> Retorno à Edição com resultado atualizado`

A composição deve permanecer não destrutiva e referenciar a mídia/projeto original sempre que possível.

## Workspace Entrega
O workspace Entrega centraliza exportação e renderização.

Recursos previstos:
- presets para YouTube, Instagram, TikTok, master e personalizados;
- H.264, H.265 e demais formatos suportados pelo motor existente;
- resolução;
- frame rate;
- bitrate;
- configuração de áudio;
- exportação da sequência inteira ou somente In/Out;
- fila de renderização;
- múltiplas entregas do mesmo projeto;
- progresso;
- tempo restante estimado;
- cancelamento seguro;
- histórico básico da fila quando tecnicamente viável.

A exportação final deve preferir a mídia original de alta qualidade, salvo configuração explícita em contrário.

## Arquitetura de desempenho
Desempenho será tratado como uma camada transversal aos cinco workspaces.

### Proxy
Proxy cria cópias leves para edição e reprodução. O projeto deve manter associação explícita entre original e proxy. A troca entre original e proxy não pode depender do Render Cache.

Comandos mínimos:
- gerar proxies;
- usar proxies;
- revelar status de proxy;
- reconectar originais.

### Mídia otimizada
Mídia otimizada é distinta de proxy e deve permitir transcodificação interna para codecs mais adequados à edição.

O software poderá sugerir mídia otimizada para formatos pesados, alta resolução, codecs de baixa eficiência editorial ou reprodução abaixo do desempenho esperado.

### Pré-render da Timeline
Trechos com efeitos, correção, composição ou processamento pesado poderão ser pré-renderizados.

O cache de pré-render deve ser invalidado somente quando uma alteração afetar o trecho correspondente. A Timeline deve indicar visualmente estados como pendente, processando e pronto.

### Cache inteligente em segundo plano
O RB VideoFire poderá preparar cache automaticamente durante períodos de baixa atividade.

O usuário deverá poder controlar:
- ativação do cache inteligente;
- prioridade de processamento;
- uso máximo ou comportamento de CPU/GPU conforme suporte disponível;
- diretório e limite de armazenamento;
- limpeza segura do cache.

O processamento em segundo plano não deve bloquear a edição nem introduzir uma segunda representação autoritativa do projeto.

### Qualidade de reprodução
O Program Monitor deverá permitir alternância rápida entre qualidades de reprodução, incluindo pelo menos:
- Completa;
- 1/2;
- 1/4;
- Proxy quando disponível.

A qualidade de preview não altera a qualidade da exportação final.

## Persistência de layout
Cada workspace poderá salvar seu próprio arranjo de painéis. Deve existir um comando para restaurar o layout padrão de cada workspace.

O estado dos painéis deve ser independente do estado editorial do projeto.

## Navegação e usabilidade
A barra inferior permanece acessível em todos os workspaces. A troca deve ser rápida e evitar reconstruções custosas de widgets quando o reaproveitamento seguro for possível.

A interface PT-BR deve usar terminologia consistente:
- Edição;
- Áudio;
- Cor;
- Efeitos;
- Entrega;
- Projeto;
- Histórico;
- Ferramentas;
- Inspetor.

## Limites arquiteturais
- não criar cinco motores independentes;
- não duplicar timeline editorial;
- não criar um pipeline de áudio paralelo para o workspace Áudio;
- não tratar proxy, mídia otimizada e Render Cache como sinônimos;
- não usar cache como mecanismo de reconexão de mídia;
- não permitir que a troca de workspace descarte estado de projeto;
- não implementar apenas telas estáticas sem integração funcional.

## Estratégia incremental
A implementação deve ser dividida em fases para reduzir risco:

1. infraestrutura do WorkspaceManager e barra inferior;
2. Edição usando o layout atual reorganizado;
3. Áudio com mixer/monitoramento conectados ao motor existente;
4. Cor com node graph mínimo funcional e scopes;
5. Efeitos com composição por camadas e keyframes;
6. Entrega com fila de renderização;
7. Proxy, mídia otimizada, pré-render e cache inteligente integrados aos cinco ambientes.

Cada fase deve preservar uma build Windows utilizável e testável.

## Validação
Antes de considerar a arquitetura concluída, devem existir testes ou verificações para:
- troca de workspace preservando sequência, seleção e playhead;
- salvamento e restauração de layout;
- ausência de recarga destrutiva de projeto;
- Audio Monitor conectado ao áudio real;
- nodes de Cor modificando efetivamente a imagem;
- keyframes e camadas de Efeitos alterando efetivamente a composição;
- fila de Entrega exportando um arquivo válido;
- proxy voltando ao original sem perder vínculo;
- mídia otimizada sem substituir indevidamente o original;
- pré-render invalidado corretamente após alteração;
- cache em segundo plano sem bloquear playback/interação;
- exportação final usando original quando configurado;
- startup Windows sem console;
- regressão de abrir/salvar/reabrir projeto;
- CMake/CTest e smoke test do executável.

## Critério de sucesso
O RB VideoFire deve permitir que um usuário percorra Edição, Áudio, Cor, Efeitos e Entrega dentro do mesmo projeto, com estado contínuo, e complete uma sequência simples com corte, mixagem, grading, composição e exportação sem precisar sair do aplicativo ou reconstruir o trabalho ao trocar de workspace.
