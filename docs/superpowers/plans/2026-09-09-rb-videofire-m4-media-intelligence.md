# RB VideoFire M4 Media Intelligence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar gerenciamento profissional de mídia com bins, metadados editáveis, estados Original/Proxy/Offline, archive/consolidate e relink persistente, sem criar um segundo pipeline de mídia.

**Architecture:** Estender Project/Footage/ProjectPanel e serialização existentes. `MediaState` será metadata do item importado, enquanto playback continua resolvendo a fonte pelo caminho nativo. Proxy será um caminho alternativo associado ao mesmo item; relink apenas troca a resolução de origem/proxy, nunca duplica o clip ou a timeline.

**Tech Stack:** C++17, Qt, CMake, CTest, Python contract tests, GitHub Actions Windows, NSIS.

**Spec:** `docs/superpowers/specs/2026-09-09-rb-videofire-resolve-class-professional-suite-design.md`

## Global Constraints
- Base: RB VideoFire 2.4.0 M3 Editorial Precision aprovado no CI.
- Branch de execução: `rb-videofire-2.4.0-m4-media-intelligence`.
- Sem segundo decoder, segundo Project Bin ou cache usado como proxy falso.
- Projeto antigo precisa abrir sem novas propriedades.
- Estados desconhecidos precisam cair de forma segura em `Original`.
- Toda alteração persistente deve sobreviver a save/reopen.
- Relink e archive não podem alterar conteúdo temporal da timeline.

---

### Task 1: Mapear Project/Footage e criar contrato RED
**Files:**
- Create: `.github/scripts/test-rbvf-m4-media-contract.py`
- Create: `docs/superpowers/notes/2026-09-09-rbvf-m4-media-map.md`
- Inspect: `app/node/project/`, `app/node/media/`, `app/panel/project/`, serializers existentes.

**Interfaces:**
- Produces: mapa exato de classes para media item, path, metadata, project tree, serialization e import.

- [ ] Criar teste que exige marcadores de integração `MediaState`, `ProxyPath`, `Relink`, `Archive`, `SmartBin` e metadata editável.
- [ ] Rodar `python .github/scripts/test-rbvf-m4-media-contract.py <source-root>` antes da implementação e confirmar RED.
- [ ] Documentar arquivos/classes reais e caminho de serialização.
- [ ] Commit `test(media): add M4 RED contract and native map`.

### Task 2: Estado Original/Proxy/Offline
**Files:**
- Create: `app/media/rbmediastate.h`
- Modify: classe real de Footage/Media identificada na Task 1.
- Modify: serializer correspondente.

**Interfaces:**
```cpp
enum class RBMediaState { kOriginal, kProxy, kOffline };
struct RBMediaSourceState {
  QString original_path;
  QString proxy_path;
  RBMediaState preferred_state;
};
```
- `QString ResolvePlaybackPath(const RBMediaSourceState &state)` retorna proxy somente quando `preferred_state == kProxy` e o arquivo existe; caso contrário tenta original; se nenhum existe, retorna vazio.

- [ ] Escrever CTest/contract RED para original existente, proxy existente, proxy ausente e offline.
- [ ] Implementar tipos e resolução mínima.
- [ ] Serializar `original_path`, `proxy_path`, `preferred_state` com versão.
- [ ] GREEN + save/reopen.
- [ ] Commit `feat(media): add original proxy offline source state`.

### Task 3: Project Bin profissional e metadados
**Files:**
- Modify: `app/panel/project/` e model/view reais identificados na Task 1.
- Create: `app/media/rbmediametadata.h` se o modelo atual não tiver estrutura extensível.

**Interfaces:**
```cpp
struct RBMediaMetadata {
  QString reel;
  QString scene;
  QString take;
  QString camera;
  QString notes;
  QString label;
  bool favorite;
};
```
- [ ] RED para edição round-trip de reel/scene/take/camera/notes/label/favorite.
- [ ] Implementar colunas editáveis no modo lista e preservar miniaturas existentes.
- [ ] Implementar navegação Enter/Tab entre células editáveis.
- [ ] Adicionar pesquisa por nome + campos de metadata.
- [ ] GREEN + save/reopen.
- [ ] Commit `feat(media): add editable metadata and professional bin list`.

### Task 4: Bins, Smart Bins e favoritos
**Files:**
- Create: `app/media/rbsmartbin.h`
- Modify: Project tree/model e serializer.

**Interfaces:**
```cpp
enum class RBSmartBinField { kName, kReel, kScene, kTake, kCamera, kLabel, kFavorite, kState };
enum class RBSmartBinOp { kContains, kEquals, kNotEquals };
struct RBSmartBinRule { RBSmartBinField field; RBSmartBinOp op; QString value; };
```
- [ ] RED para regra por nome, camera, label, favorite e state.
- [ ] Implementar avaliação determinística das regras sobre os itens existentes.
- [ ] Smart Bin não move nem duplica media; apenas referencia resultados.
- [ ] Persistir regras no projeto.
- [ ] GREEN + save/reopen.
- [ ] Commit `feat(media): add bins smart bins labels and favorites`.

### Task 5: Relink profissional
**Files:**
- Create: `app/media/rbrelinkservice.h`
- Create: `app/media/rbrelinkservice.cpp`
- Modify: ProjectPanel context menu/dialog.

**Interfaces:**
```cpp
struct RBRelinkCandidate {
  QString path;
  qint64 size;
  QString reel;
  QString timecode;
};
struct RBRelinkScore { int score; QString reason; };
RBRelinkScore ScoreRelinkCandidate(const MediaItem &, const RBRelinkCandidate &);
```
- Prioridade: nome exato + tamanho > reel/timecode compatível > nome exato > metadata parcial. Nunca escolher automaticamente entre empate de maior score.

- [ ] RED para matches exatos, metadata parcial, empate e nenhum candidato.
- [ ] Implementar scanner de diretório escolhido pelo usuário sem tocar timeline.
- [ ] Preview da decisão antes de aplicar múltiplos relinks.
- [ ] Aplicação atualiza `original_path` e volta a `kOriginal` somente se arquivo validar.
- [ ] GREEN + undo quando integrado como mutação de projeto.
- [ ] Commit `feat(media): add deterministic media relink service`.

### Task 6: Archive/Consolidate
**Files:**
- Create: `app/media/rbarchiveservice.h`
- Create: `app/media/rbarchiveservice.cpp`
- Modify: menu Project/File.

**Interfaces:**
```cpp
struct RBArchiveOptions {
  bool used_media_only;
  bool include_originals;
  bool include_proxies;
  bool include_cache;
  bool include_luts;
};
```
- [ ] RED para manifest contendo exatamente os ativos selecionados.
- [ ] Implementar coleta de mídia usada pelas sequências existentes.
- [ ] Copiar arquivos para `Media/Original`, `Media/Proxy`, `Cache`, `LUTs` e gerar `manifest.json` versionado.
- [ ] Reescrever somente a cópia arquivada do projeto para paths relativos; projeto aberto permanece inalterado.
- [ ] GREEN com archive contendo projeto + manifest + ativos válidos.
- [ ] Commit `feat(media): add archive and consolidate workflow`.

### Task 7: UX de mídia e Source Monitor
**Files:**
- Modify: Source/Footage viewer e ProjectPanel.

**Interfaces:**
- Source Monitor preserva aspect ratio e pixel aspect nativos.
- Badge do item mostra `Original`, `Proxy` ou `Offline`.

- [ ] RED para propriedade de aspect ratio e estado visual conectado ao modelo.
- [ ] Implementar toggle Original/Proxy por item e ação global de playback proxy quando suportada pelo viewer atual.
- [ ] Item offline abre diálogo de relink, não falha silenciosamente.
- [ ] GREEN.
- [ ] Commit `ui(media): add source-state and media intelligence controls`.

### Task 8: Regressão e qualificação Windows M4
**Files:**
- Create: `.github/scripts/apply-rbvf-2.4-m4-media.py`
- Create: `.github/scripts/test-rbvf-2.4-m4-regression.py`
- Create: `.github/workflows/build-m4-media-windows.yml`

**Interfaces:**
- Produces artifact `RB-VideoFire-2.4.0-M4-Media-Intelligence-Installer`.

- [ ] Workflow aplica cumulativamente 2.1 -> 2.4 M1 -> M2 -> M3 -> M4.
- [ ] RED M4 antes do patch e GREEN depois.
- [ ] Rodar CTest, startup smoke, package audit e PE GUI/no-console.
- [ ] Regressão: import -> metadata -> proxy toggle -> offline -> relink -> save/reopen -> archive -> playback -> export path.
- [ ] Empacotar `RB VideoFire Setup 2.4.0 Alpha M4 Media Intelligence.exe`.
- [ ] Publicar installer e portable/symbols; calcular SHA-256 do EXE extraído.
- [ ] Commit `build: qualify RB VideoFire 2.4 M4 Media Intelligence`.

## Self-review
- Cobertura: metadata, bins, smart bins, labels/favorites, Original/Proxy/Offline, relink, archive/consolidate e Source Monitor estão mapeados.
- Sem placeholders: todos os tipos e regras centrais estão definidos.
- Compatibilidade: timeline/playback continuam usando o item nativo; M4 apenas resolve o caminho da mídia e metadata associada.
- Fora de escopo: Color, Composition, Audio Mixer, Delivery, IA e scripting permanecem nos planos M5-M11 e não recebem UI simulada neste marco.