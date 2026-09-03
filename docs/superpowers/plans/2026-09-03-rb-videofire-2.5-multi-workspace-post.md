# RB VideoFire 2.5.0 Multi-Workspace Post Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir uma pós-produção integrada com cinco workspaces inferiores, estado editorial compartilhado e uma camada transversal de desempenho com proxy, mídia otimizada, pré-render e cache inteligente.

**Architecture:** Um `WorkspaceManager` coordena layouts especializados sobre o mesmo projeto, sequência, seleção e playhead. Edição reutiliza o NLE existente; Áudio conecta mixer/medidores ao motor de áudio existente; Cor adiciona grading por nodes; Efeitos adiciona composição por camadas; Entrega encapsula exportação/fila. Proxy, mídia otimizada e caches são serviços independentes, nunca representações autoritativas do projeto.

**Tech Stack:** C++17, Qt Widgets, CMake, CTest, FFmpeg/motor de mídia existente, OpenGL/render existente, NSIS, GitHub Actions Windows.

**Spec:** `docs/superpowers/specs/2026-09-03-rb-videofire-2.5-multi-workspace-post-design.md`

## Global Constraints

- Versão: `RB VideoFire 2.5.0 Alpha Multi-Workspace Post`.
- Barra inferior fixa: `Edição | Áudio | Cor | Efeitos | Entrega`.
- Troca de workspace preserva projeto, sequência, playhead, seleção e In/Out.
- Não criar cinco motores independentes nem duplicar a timeline editorial.
- Áudio deve consumir o pipeline existente.
- Cor usa nodes; Efeitos usa camadas.
- Proxy, mídia otimizada e Render Cache são conceitos separados.
- Exportação final usa mídia original salvo configuração explícita.
- PT-BR usa `Inspetor` consistentemente.
- Windows deve iniciar sem console e preservar abertura/salvamento de projetos.

---

## File Structure

Como o repositório atual distribui mudanças nativas por patches cumulativos, os caminhos finais devem seguir os componentes reais encontrados no source extraído. As novas unidades lógicas são:

- `app/workspace/workspacemanager.{h,cpp}`: seleção, persistência e restauração de workspaces.
- `app/workspace/workspacebar.{h,cpp}`: barra inferior e ações/atalhos.
- `app/audio/mixer/*`: estado e UI do mixer conectados ao motor existente.
- `app/color/*`: graph de grading, parâmetros e scopes.
- `app/effects/composition/*`: composição por camadas/keyframes.
- `app/export/renderqueue/*`: jobs e fila de entrega.
- `app/media/proxy/*`: vínculo original/proxy.
- `app/media/optimized/*`: mídia otimizada.
- `app/render/prerender/*`: pré-render e invalidação por intervalo.
- `app/render/backgroundcache/*`: cache inteligente em segundo plano.
- Testes devem acompanhar cada unidade e ser integrados ao CTest.

Se os nomes de diretório existentes no source diferirem, manter a convenção real do projeto sem juntar responsabilidades em arquivos globais.

---

### Task 1: Contrato de versão e infraestrutura de workspaces

**Files:**
- Create: `app/workspace/workspacemanager.h`
- Create: `app/workspace/workspacemanager.cpp`
- Create: `app/workspace/workspacebar.h`
- Create: `app/workspace/workspacebar.cpp`
- Modify: arquivo real da janela principal e CMake correspondente
- Test: novo teste CTest de workspace

**Interfaces:**
- Produces: `enum class WorkspaceId { Edit, Audio, Color, Effects, Deliver };`
- Produces: `WorkspaceId WorkspaceManager::current() const`
- Produces: `bool WorkspaceManager::activate(WorkspaceId id)`
- Produces: sinais `workspaceAboutToChange` e `workspaceChanged`.

- [ ] **Step 1: Escrever teste RED** que instancia o manager, ativa `Audio` e comprova que um `ProjectContext` sentinela mantém sequence id, playhead e seleção.
- [ ] **Step 2: Executar apenas o teste de workspace** e confirmar falha por ausência de `WorkspaceManager`.
- [ ] **Step 3: Implementar `WorkspaceManager` mínimo** sem copiar projeto ou timeline; ele só muda a composição de painéis.
- [ ] **Step 4: Implementar `WorkspaceBar` inferior** com cinco ações exclusivas na ordem aprovada e destaque da ativa.
- [ ] **Step 5: Integrar a barra à janela principal** preservando docks e estado atual.
- [ ] **Step 6: Adicionar atalhos configuráveis** para os cinco workspaces usando o sistema de comandos existente.
- [ ] **Step 7: Rodar CTest e teste de startup**; confirmar troca repetida sem alterar o contexto editorial.
- [ ] **Step 8: Commit** `feat: add shared multi-workspace shell`.

### Task 2: Workspace Edição e persistência de layout

**Files:**
- Modify: componentes reais de dock/layout da janela principal
- Create: `app/workspace/workspacelayoutstore.{h,cpp}`
- Test: teste CTest de persistência

**Interfaces:**
- Consumes: `WorkspaceId`, `WorkspaceManager`.
- Produces: `saveLayout(WorkspaceId, QByteArray)` e `restoreLayout(WorkspaceId)`.

- [ ] **Step 1: Escrever teste RED** salvando dois layouts diferentes para Edit e Audio e verificando restauração independente.
- [ ] **Step 2: Executar o teste** e confirmar falha.
- [ ] **Step 3: Implementar armazenamento por workspace** usando o mecanismo Qt de geometria/docks já empregado pelo aplicativo.
- [ ] **Step 4: Configurar Edição** com Source + Inspetor à esquerda, Program Monitor prioritário, Projeto/Efeitos/Histórico embaixo à esquerda, Timeline ampla e Audio Monitor à direita.
- [ ] **Step 5: Implementar `Restaurar workspace`** sem tocar no estado editorial.
- [ ] **Step 6: Rodar teste e smoke test manual automatizável** abrindo projeto, mudando layout, trocando abas e voltando à Edição.
- [ ] **Step 7: Commit** `feat: add persistent edit workspace layout`.

### Task 3: Workspace Áudio e monitoramento real

**Files:**
- Create/modify: componentes de mixer seguindo o caminho real do motor de áudio
- Modify: Audio Monitor existente
- Test: teste CTest de meter/mixer

**Interfaces:**
- Consumes: níveis do pipeline de áudio existente.
- Produces: `TrackMixState { gain, pan, mute, solo }` e `AudioMeterFrame` estéreo inicialmente.

- [ ] **Step 1: Localizar no source o ponto único onde níveis de playback já são calculados** e documentar a conexão no código.
- [ ] **Step 2: Escrever teste RED** para conversão real `20 * log10(linear)` com floor definido em -60 dBFS e clipping em `>= 0 dBFS`.
- [ ] **Step 3: Executar teste** e confirmar falha.
- [ ] **Step 4: Implementar medição dBFS correta**, peak hold e clipping sem criar segundo pipeline.
- [ ] **Step 5: Escrever teste RED do mixer** provando que mute/solo/gain/pan alteram o estado usado pelo motor existente.
- [ ] **Step 6: Implementar mixer por track e master bus**, com fader, pan, mute, solo e meter; EQ/compressor/limiter entram somente por APIs DSP reais disponíveis.
- [ ] **Step 7: Integrar layout Áudio** com tracks ampliadas e mixer dominante.
- [ ] **Step 8: Rodar playback com áudio estéreo, CTest e verificação de ausência de bloqueio da UI**.
- [ ] **Step 9: Commit** `feat: add integrated audio workspace and mixer`.

### Task 4: Workspace Cor baseado em nodes

**Files:**
- Create: `app/color/colorgraph.{h,cpp}`
- Create: `app/color/colornode.{h,cpp}`
- Create: widgets de grading/scopes nos diretórios reais de UI
- Test: testes CTest de graph e processamento

**Interfaces:**
- Produces: `ColorGraph`, `ColorNodeId`, `connect(from,to)`, `evaluate(frame)`.
- Graph mínimo: `MediaIn -> serial correction nodes -> MediaOut`.

- [ ] **Step 1: Escrever teste RED** para graph serial que altera um frame de teste e mantém ordem determinística.
- [ ] **Step 2: Executar teste** e confirmar falha.
- [ ] **Step 3: Implementar graph mínimo não destrutivo** ligado ao item de grading do projeto.
- [ ] **Step 4: Implementar node primário** com exposição, contraste, saturação, temperatura/tint e Lift/Gamma/Gain conforme APIs de cor disponíveis.
- [ ] **Step 5: Integrar viewer grande e scopes reais** (waveform, RGB parade, vectorscope) consumindo o frame processado.
- [ ] **Step 6: Adicionar LUT, curvas, before/after e persistência do graph no projeto**.
- [ ] **Step 7: Testar save/reopen e verificar que o grading permanece e modifica imagem**.
- [ ] **Step 8: Commit** `feat: add node based color workspace`.

### Task 5: Workspace Efeitos por camadas

**Files:**
- Create: `app/effects/composition/composition.{h,cpp}`
- Create: `app/effects/composition/layer.{h,cpp}`
- Create: `app/effects/composition/keyframe.{h,cpp}`
- Create: UI da timeline de composição
- Test: testes CTest de composição/keyframe

**Interfaces:**
- Produces: `Composition`, `Layer`, `KeyframeTrack`.
- Produces: composição vinculável a um item da sequência sem substituir a mídia original.

- [ ] **Step 1: Escrever teste RED** com duas camadas e keyframes de opacidade/posição avaliados em frames conhecidos.
- [ ] **Step 2: Executar teste** e confirmar falha.
- [ ] **Step 3: Implementar modelo de composição** com ordem de camadas e propriedades Transform/Opacity.
- [ ] **Step 4: Implementar interpolação de keyframes** usando tipos já suportados pelo motor quando disponíveis.
- [ ] **Step 5: Criar timeline de composição por camadas** distinta da timeline editorial.
- [ ] **Step 6: Integrar `Abrir em Efeitos`** a partir do item selecionado e retorno à Edição com resultado atualizado.
- [ ] **Step 7: Adicionar máscaras, blend modes, texto e chroma key somente através de operadores reais do render graph**.
- [ ] **Step 8: Testar save/reopen e render de composição**.
- [ ] **Step 9: Commit** `feat: add layer based effects workspace`.

### Task 6: Workspace Entrega e fila de renderização

**Files:**
- Create: `app/export/renderqueue/renderjob.{h,cpp}`
- Create: `app/export/renderqueue/renderqueue.{h,cpp}`
- Modify: exportador existente
- Test: testes CTest de fila

**Interfaces:**
- Produces: `RenderJob`, `RenderQueue::enqueue`, `start`, `cancel`.
- Jobs referenciam sequência + snapshot de configurações, não cópia do projeto inteiro.

- [ ] **Step 1: Escrever teste RED** enfileirando dois jobs e verificando ordem, progresso e cancelamento seguro.
- [ ] **Step 2: Executar teste** e confirmar falha.
- [ ] **Step 3: Implementar fila sobre o exportador existente**, sem segundo encoder.
- [ ] **Step 4: Criar presets YouTube, Instagram, TikTok, Master e Personalizado** mapeados apenas a codecs realmente disponíveis.
- [ ] **Step 5: Implementar sequência inteira/In-Out, resolução, FPS, bitrate e áudio**.
- [ ] **Step 6: Garantir resolução de mídia original na exportação** quando proxy/otimizada estiver ativa.
- [ ] **Step 7: Exportar arquivo de teste e validar que o arquivo produzido é legível**.
- [ ] **Step 8: Commit** `feat: add deliver workspace render queue`.

### Task 7: Proxy e mídia otimizada

**Files:**
- Create: `app/media/proxy/proxylink.{h,cpp}`
- Create: `app/media/proxy/proxymanager.{h,cpp}`
- Create: `app/media/optimized/optimizedmediamanager.{h,cpp}`
- Test: testes CTest de vínculo/relink

**Interfaces:**
- Produces: associação estável `original -> proxy` e `original -> optimized`.
- Nunca consome Render Cache como fonte de reconexão.

- [ ] **Step 1: Escrever teste RED** criando vínculo proxy, alternando proxy/original e reconectando original sem alterar identidade do asset.
- [ ] **Step 2: Executar teste** e confirmar falha.
- [ ] **Step 3: Implementar ProxyManager** com geração, status, enable/disable e relink.
- [ ] **Step 4: Escrever teste RED** demonstrando que mídia otimizada é uma representação separada do proxy.
- [ ] **Step 5: Implementar OptimizedMediaManager** e seleção de representação para playback.
- [ ] **Step 6: Integrar comandos e indicadores na UI** e qualidade `Completa / 1/2 / 1/4 / Proxy` no Program Monitor.
- [ ] **Step 7: Testar exportação usando original** apesar de playback em proxy.
- [ ] **Step 8: Commit** `feat: separate proxy and optimized media workflows`.

### Task 8: Pré-render e cache inteligente

**Files:**
- Create: `app/render/prerender/prerendermanager.{h,cpp}`
- Create: `app/render/backgroundcache/backgroundcachemanager.{h,cpp}`
- Modify: timeline para indicador de cache
- Test: testes CTest de invalidação/background

**Interfaces:**
- Produces: `invalidate(TimeRange)`, `request(TimeRange)`, `status(TimeRange)`.
- Cache nunca substitui a fonte autoritativa do projeto.

- [ ] **Step 1: Escrever teste RED** pré-renderizando intervalo A, alterando intervalo B e provando que A continua válido.
- [ ] **Step 2: Executar teste** e confirmar falha.
- [ ] **Step 3: Implementar invalidação por intervalo/dependência**.
- [ ] **Step 4: Adicionar estados visuais de timeline** pendente/processando/pronto.
- [ ] **Step 5: Escrever teste RED** do background cache provando que trabalho interativo suspende/reduz processamento conforme prioridade.
- [ ] **Step 6: Implementar scheduler de baixa prioridade** com ativação, diretório, limite de armazenamento e limpeza segura.
- [ ] **Step 7: Testar playback durante cache e alteração de efeitos durante pré-render**.
- [ ] **Step 8: Commit** `feat: add timeline prerender and smart background cache`.

### Task 9: PT-BR, identidade e integração completa

**Files:**
- Modify: traduções PT-BR e recursos de identidade
- Modify: About/version/installer
- Test: validador de release

**Interfaces:**
- Consumes todos os workspaces.

- [ ] **Step 1: Escrever validação RED** para versão 2.5.0, cinco labels inferiores e terminologia `Inspetor`.
- [ ] **Step 2: Executar validação** e confirmar falha antes do patch final.
- [ ] **Step 3: Corrigir strings restantes** como Window/History/Tools e remover inconsistências visíveis no PT-BR.
- [ ] **Step 4: Aplicar identidade** `RB VideoFire 2.5.0 Alpha Multi-Workspace Post` em CMake, About, version resource e NSIS.
- [ ] **Step 5: Rodar todos os CTest** e validator.
- [ ] **Step 6: Commit** `chore: finalize 2.5 multi-workspace identity`.

### Task 10: Build Windows e regressão profissional

**Files:**
- Modify: `.github/workflows/build-windows.yml`
- Modify/Create: validadores de CI necessários

**Interfaces:**
- Produces: `RB VideoFire Setup 2.5.0 Alpha Multi-Workspace Post.exe`.

- [ ] **Step 1: Atualizar workflow** para aplicar patches cumulativos na ordem, executar validators RED/GREEN, CMake Release e CTest.
- [ ] **Step 2: Compilar Windows x64** e corrigir apenas falhas relacionadas a esta linha de desenvolvimento.
- [ ] **Step 3: Executar startup smoke test** comprovando ausência de console e abertura da janela principal.
- [ ] **Step 4: Executar regressão**: importar mídia, playback A/V, editar, undo/redo, salvar/reabrir, alternar cinco workspaces, grading, composição, proxy, pré-render e exportar.
- [ ] **Step 5: Gerar instalador NSIS** com nome exato `RB VideoFire Setup 2.5.0 Alpha Multi-Workspace Post.exe`.
- [ ] **Step 6: Calcular SHA-256 do EXE**, publicar artifact e verificar tamanho/PE válido.
- [ ] **Step 7: Commit** `build: package RB VideoFire 2.5.0 multi-workspace post`.

---

## Self-Review

- Cobertura: todos os requisitos da especificação estão associados às Tasks 1-10.
- Isolamento: workspaces compartilham contexto e serviços, sem cinco motores.
- Áudio: exige integração ao pipeline existente e dBFS matematicamente correto.
- Cor: nodes são funcionais e persistentes, não mockups.
- Efeitos: camadas/keyframes são funcionais e não substituem a timeline editorial.
- Entrega: reutiliza exportador real e força resolução de original conforme configuração.
- Desempenho: proxy, otimizada, pré-render e cache possuem responsabilidades separadas.
- Release: só é considerada entregável após CTest, smoke, regressão e artifact Windows válidos.
