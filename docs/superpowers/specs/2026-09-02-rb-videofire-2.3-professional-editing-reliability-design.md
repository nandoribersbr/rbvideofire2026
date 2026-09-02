# RB VideoFire 2.3.0 Professional Editing Reliability Design

## Objetivo
Transformar a base 2.2.1 em uma versão focada em confiabilidade editorial real, priorizando timeline, trim, playback, sincronismo A/V, áudio, proxy/relink e recuperação antes de novos efeitos cosméticos.

## Escopo por marcos

### Marco 1: Timeline, trim e playback
- Conectar o estado profissional de trim a operações reais da timeline.
- Garantir nudge frame a frame previsível em ripple e roll.
- Validar playback em 1x, shuttle e stepping sem drift perceptível.
- Preservar comportamento atual que já funciona.

### Marco 2: Sincronismo A/V e monitoramento de áudio
- Detectar e evitar drift entre áudio e vídeo durante reprodução longa.
- Validar seleção de dispositivo e comportamento do monitor de áudio.
- Expor medição de nível confiável e estado de clipping.
- Manter canais estéreo e layouts multicanal coerentes.

### Marco 3: Proxy e relink
- Separar semanticamente render cache de proxy editorial.
- Manter caminho do original intacto.
- Permitir alternância proxy/original sem quebrar a timeline.
- Preparar relink explícito de mídia offline.

### Marco 4: Recovery e estabilidade
- Autosave mínimo de 1 minuto e retenção padrão de 50 snapshots.
- Recuperação segura após encerramento inesperado.
- Evitar corrupção do projeto e perda silenciosa de alterações.

## Arquitetura
A implementação deve permanecer modular e cirúrgica. A lógica editorial profissional fica isolada em app/professional e se integra aos módulos existentes por interfaces pequenas. Nenhum recurso existente deve ser reescrito sem necessidade direta. O código deve favorecer testes unitários de estado e testes de integração dos fluxos de timeline, áudio e recovery.

## Critérios de aceitação
- Compilação Windows concluída no GitHub Actions.
- Testes existentes continuam passando.
- Novos testes cobrem trim, playback quality, proxy state, recovery e A/V sync policy.
- Nenhum prompt de console antes da interface no Windows.
- Instalador gerado com nome RB VideoFire Setup 2.3.0 Alpha Professional Editing Reliability.exe.
- Auditoria final do artefato antes de distribuição.

## Fora do escopo desta versão
- Pacotes grandes de efeitos novos.
- IA generativa.
- Color grading avançado novo.
- Motion graphics complexos.
- Refatorações amplas não relacionadas à confiabilidade editorial.
