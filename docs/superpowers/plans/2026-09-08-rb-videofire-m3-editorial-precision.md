# RB VideoFire M3 Editorial Precision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar a edição de timeline mais precisa e confiável sem substituir o motor editorial nativo.

**Architecture:** Estender as ferramentas, comandos e painéis existentes do Olive/RB VideoFire, mantendo TimeBased, TimelinePanel, ViewerOutput e undo stack como fontes de verdade. As mudanças de UX chamam comandos editoriais existentes ou pequenos adaptadores testáveis; não haverá segunda timeline.

**Tech Stack:** C++17, Qt, KDDockWidgets, CMake, CTest, Python contract tests, GitHub Actions Windows, NSIS.

**Spec:** `docs/superpowers/specs/2026-09-08-rb-videofire-professional-roadmap-design.md`

## Global Constraints
- Base: RB VideoFire 2.4.0 Workspace M2.
- Branch: `rb-videofire-2.4.0-m3-editorial-precision`.
- Preservar Audio Monitor M1 e workspace M2.
- Reutilizar timeline/undo/playback nativos.
- Sem controles decorativos ou comandos sem implementação.
- Build final precisa passar Release, CTest, startup smoke e package audit.

---

### Task 1: Contrato M3 e auditoria dos comandos editoriais
**Files:**
- Create: `.github/scripts/test-rbvf-2.4-m3-editorial.py`
- Inspect/Modify: `app/panel/timeline/*`, `app/widget/timeline/*`, `app/window/mainwindow/*`, atalhos existentes.

**Interfaces:**
- Consumes: ferramentas e comandos editoriais nativos.
- Produces: mapa verificável de Selection/Ripple/Roll/Razor/Slip/Slide, JKL e undo.

- [ ] Escrever teste de contrato exigindo ferramentas existentes e pontos de integração M3.
- [ ] Executar antes da aplicação e confirmar RED para os novos contratos.
- [ ] Mapear classes e ações reais; falhar se algum requisito depender de UI falsa.
- [ ] Commitar teste RED.

### Task 2: Trim e nudge profissional
**Files:**
- Modify: arquivos reais de TimelinePanel/TimelineWidget identificados na Task 1.
- Test: `.github/scripts/test-rbvf-2.4-m3-editorial.py`.

**Interfaces:**
- Consumes: ripple/roll/slip/slide e undo stack nativos.
- Produces: nudge de exatamente 1 frame e trim por lado A/B/ambos.

- [ ] Adicionar casos RED para nudge e trim.
- [ ] Implementar adaptadores mínimos sobre comandos existentes.
- [ ] Validar undo/redo restaura exatamente o estado anterior.
- [ ] Rodar GREEN e commit.

### Task 3: Transporte editorial e comandos de corte
**Files:**
- Modify: ações/shortcuts do MainWindow e TimelinePanel conforme mapa da Task 1.

**Interfaces:**
- Produces: J/K/L, insert, overwrite, lift, extract e go-to in/out somente quando houver implementação real.

- [ ] Testar presença e ligação dos comandos.
- [ ] Implementar/ligar ações reais.
- [ ] Verificar que foco da timeline não quebra transporte.
- [ ] GREEN e commit.

### Task 4: Track targeting, sync e linked A/V
**Files:**
- Modify: track headers/model somente onde a arquitetura nativa suportar os estados.

**Interfaces:**
- Produces: estados persistentes/funcionais de targeting, lock/sync e linked selection; qualquer estado não suportado fica fora do M3 em vez de virar decoração.

- [ ] Criar RED para estados realmente suportados.
- [ ] Implementar controles ligados ao modelo.
- [ ] Testar cortes/ripple com A/V linkado e deslinkado.
- [ ] GREEN e commit.

### Task 5: Markers e legibilidade da Timeline
**Files:**
- Modify: timeline ruler/header e recursos de marker existentes.

**Interfaces:**
- Produces: marker add/remove/navigation e cabeçalhos legíveis V/A sem alterar o timebase.

- [ ] Testar round-trip de marker no projeto.
- [ ] Implementar UI usando modelo existente.
- [ ] Testar save/reopen.
- [ ] GREEN e commit.

### Task 6: Regressão editorial
**Files:**
- Create: `.github/scripts/test-rbvf-2.4-m3-regression.py`.
- Modify: workflow M3 Windows.

**Interfaces:**
- Produces: gate automatizado para M3.

- [ ] Testar import -> timeline -> trim -> undo/redo -> save/reopen em contratos disponíveis.
- [ ] Verificar A/V sync policy permanece válida.
- [ ] Verificar Audio Monitor e workspace M2 continuam aplicados.
- [ ] Commit.

### Task 7: Windows qualification e EXE
**Files:**
- Create/Modify: `.github/workflows/build-m3-editorial-windows.yml`.

**Interfaces:**
- Produces: instalador Windows M3 verificável.

- [ ] Executar RED/GREEN M3 no runner.
- [ ] Configurar e compilar Release.
- [ ] Rodar CTest sem falhas.
- [ ] Fazer deploy runtime e startup smoke.
- [ ] Auditar PE GUI, identidade RB e ausência de console.
- [ ] Empacotar NSIS e publicar artifact.
- [ ] Calcular SHA-256 do EXE extraído antes de entregar.