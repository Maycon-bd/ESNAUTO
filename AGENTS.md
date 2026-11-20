# ESNAUTO

## Trabalho na monografia

Ao redigir, revisar ou conferir a monografia de Maycon Garcia Silva, leia a skill
`.agents/skills/monografia-esnauto/SKILL.md` e o contexto em
`docs/assistencia_monografia/contexto.md`. Não carregue esses materiais para tarefas
de software sem relação com o texto acadêmico.

A base editorial vigente deve ser resolvida exclusivamente pelo registro
`docs/assistencia_monografia/versao_vigente.json`. Antes de qualquer trabalho
acadêmico, execute `python Scripts/versao_monografia.py atual --json` e use o
caminho retornado após conferência do SHA256. Não escolha por nome, data de
modificação ou memória de outro chat. Esta regra prevalece sobre indicações
históricas de base no contexto, catálogo e skill, salvo escolha explícita posterior
do autor.

Siga `docs/assistencia_monografia/controle_versoes.md`: preserve os snapshots,
prepare uma cópia de trabalho, registre a nova revisão com a versão-base e confira
a vigente antes de entregar. Se outro chat já avançou a base, concilie as mudanças;
não sobrescreva a revisão posterior. Auditoria sem edição não cria versão Word.
Relatórios devem identificar versão e hash examinados. Versões PETR4 anteriores,
VALE3 e Word original servem como histórico. “Vigente” não significa aprovação
acadêmica ou validação integral.

Preserve a separação entre as 45 execuções históricas PETR4, a rodada controlada
de Diebold–Mariano e o lote ilustrativo de 200 gerações. VALE3 permanece como
desdobramento. Use os registros primários de cada execução para conferir números.

Resultados e scripts existentes podem conter alterações ainda não versionadas.
Não os restaure nem regenere durante uma revisão editorial. A autorização para
revisar o texto não implica repetir treinamentos, buscas genéticas ou testes DM.

## Fontes e revisão

O mapa de fontes está em `docs/assistencia_monografia/fontes.json`; o diagnóstico
inicial e o roteiro estão no mesmo diretório. O relatório inicial é uma fotografia
da versão auditada, e não uma lista automática de defeitos de futuras versões.
Não transfira números entre protocolos nem apresente metadados reconstruídos como
exportação original de uma base bibliográfica. Confira afirmações nos trabalhos
citados antes de atribuí-las aos autores.
