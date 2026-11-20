# Controle de versões da monografia

A fonte única de escolha da base é `docs/assistencia_monografia/versao_vigente.json`.
O campo `vigente` aponta para uma entrada com caminho, SHA256, versão anterior,
responsável, resumo, validação declarada, evidências e pendências. O histórico
começa na importação da versão FASOFT conferida; não inventa numeração das revisões
anteriores, que continuam preservadas em seus caminhos históricos.

## Regra para todos os chats e modelos neste projeto

1. Antes de ler, revisar, auditar ou preparar uma apresentação da monografia,
   executar `python Scripts/versao_monografia.py atual --json`. Usar o caminho
   retornado e registrar ID e hash no trabalho. Não selecionar por data do arquivo,
   nome “final”, memória do chat ou posição de uma pasta.
2. O snapshot em `reports/monografia/versoes/` é preservado: não editar diretamente.
   Usar `preparar` para uma cópia de trabalho com registro de sua origem.
3. Concluir a edição e fazer as verificações pertinentes (Word: texto, tabelas,
   referências, renderização e inspeção visual). Descrever precisamente validações
   incompletas e pendências, sem atribuir aprovação acadêmica.
4. Registrar a nova cópia com `registrar --base vNNN`. A ferramenta só promove
   uma revisão que partiu da vigente; se outro chat já promoveu outra, rejeita a
   base antiga. Comparar e conciliar as mudanças antes de tentar novamente.
5. Confirmar `atual --json` e entregar o caminho numerado registrado. Relatórios
   sem alteração do Word não incrementam a versão; devem citar ID/hash auditados.

Uma instrução explícita do autor pode solicitar trabalhar em versão histórica.
Nesse caso, identificar a exceção e não promovê-la silenciosamente à vigente.
Nunca apresentar “conferida” como aprovação do orientador/banca ou garantia total.

## Comandos

No terminal da raiz ESNAUTO, usando Python 3:

```powershell
python Scripts/versao_monografia.py atual --json
python Scripts/versao_monografia.py historico
python Scripts/versao_monografia.py verificar --todos

python Scripts/versao_monografia.py preparar --destino reports/monografia/trabalho/revisao_citacoes.docx

python Scripts/versao_monografia.py registrar --arquivo reports/monografia/trabalho/revisao_citacoes.docx --base v001 --responsavel "Nome do autor ou identificação do chat" --resumo "Descrever alterações e pendências resolvidas" --estado em_revisao --validacao "Descrever conferências realizadas e pendências" --evidencia reports/caminho_do_relatorio.md
```

O exemplo usa v001; conferir e substituir pelo ID retornado no começo do trabalho.
Se `python` não estiver disponível, usar o executável Python do ambiente instalado.
O script usa somente a biblioteca padrão. A cópia de trabalho recebe um arquivo
`.docx.origem.json` com seu ID base; guardá-lo durante a revisão.

Pendências são herdadas por padrão. `--pendencia` repetido fornece uma nova lista
completa; só remover um item quando sua resolução estiver documentada no resumo
e na evidência. Para registrar ausência de pendências, usar uma declaração explícita
como `--pendencia "Nenhuma pendência conhecida no escopo da revisão registrada"`,
sem transformar isso em certificação universal.

`registrar` torna o documento a última versão de trabalho mesmo quando seu estado
é `em_revisao`. “Mais recente” e “integralmente validada” são informações distintas.
Se a tarefa for interrompida antes do registro, a cópia de trabalho é um rascunho
não promovido; o próximo chat deve retomar pela vigente e examinar o rascunho
se isso fizer parte do pedido. Não publicar snapshots parciais automaticamente.

## Proteções e limites

- O script confere a estrutura ZIP/DOCX e a identidade por SHA256; não julga o texto.
- Cópias numeradas não são sobrescritas pelo script; alteração externa é detectada.
- Bloqueio exclusivo e atualização do registro por substituição evitam duas
  promoções simultâneas no mesmo checkout. Uma base antiga é recusada.
- Um bloqueio abandonado após encerramento abrupto exige verificar se há processo
  ativo antes de remover o arquivo `.lock`. Não ignorar ou contornar o bloqueio.
- O mecanismo é local a este projeto. Chats sem acesso à pasta/instruções não
  consultam o registro automaticamente. Ao iniciar fora do projeto, anexar ou
  indicar a versão vigente e estas instruções.
- Git pode preservar scripts, registro e snapshots em commits. Não foi criado
  commit ou enviado material a serviço externo na implantação deste controle.
  Cópias locais e hashes não substituem backup em outro dispositivo/serviço.
- Checkouts/worktrees separados precisam de sincronização e conciliação antes de
  promover versões. Não há trava distribuída nem mesclagem automática de DOCX.
- Datas são metadados; a ordem válida é a cadeia numerada do registro. Horários de
  registro são armazenados explicitamente em UTC, sem inferir data da revisão.

O catálogo `fontes.json` aponta para este registro como autoridade editorial.
Relatórios antigos permanecem ligados aos arquivos/hashes que examinaram.
