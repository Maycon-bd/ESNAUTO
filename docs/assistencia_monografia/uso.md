# Como usar a assistência da monografia

A assistência reúne instruções locais, catálogo de fontes, extração textual e uma
primeira auditoria. É uma configuração específica para a pesquisa ESNAUTO, com
instruções próprias; não é a instalação integral do Academic Research Skills de
terceiros. Não inclui seus hooks, painel de agentes, verificações automáticas de
citações ou chamadas a outros provedores. A organização por etapas e a separação
de evidências discutidas na conversa foram aplicadas ao acervo deste projeto.

## Entradas principais

- `contexto.md`: escopo, prioridades e decisões da pesquisa.
- `fontes.json`: catálogo de fontes por finalidade e bloco experimental.
- `auditoria_inicial.md`: diagnóstico com localizações e propostas.
- `plano_revisao.md`: sequência por capítulo e critérios de conclusão.
- `.agents/skills/monografia-esnauto/SKILL.md`, na raiz do projeto: instruções
  reutilizáveis para trabalhar no manuscrito.
- `AGENTS.md`, na raiz: encaminhamento para a configuração em tarefas acadêmicas.

O uso de skills locais em `.agents/skills/` segue a
[documentação oficial OpenAI](https://developers.openai.com/blog/skills-agents-sdk).
Se a skill não aparecer na lista da sessão, ainda é possível pedir para ler
explicitamente seu arquivo antes da revisão. A disponibilidade na interface desta
sessão não foi validada por reinicialização do aplicativo.

## Exemplos de pedidos

> Use $monografia-esnauto para revisar a introdução, começando por A01 e A07.

> Use $monografia-esnauto para conferir a origem de todos os números da Tabela 4,
> preservando a separação entre resultados históricos e o DM complementar.

> Use $monografia-esnauto para revisar o capítulo 2 e harmonizar as versões
> bibliográficas apontadas em A02, conferindo os PDFs correspondentes.

> Use $monografia-esnauto para preparar uma versão revisada do Word com as
> alterações identificadas e um registro do que foi modificado.

## Conferência da identidade dos arquivos

Na raiz do projeto, com Python 3.9 ou superior disponível:

```powershell
python Scripts/auditar_base_monografia.py --check
```

O comando compara os arquivos catalogados, os PDFs locais e o texto extraído com
o snapshot. Não escreve nem acessa a rede, não calcula novos testes estatísticos
e não garante validade científica. Se o Word ou outra fonte mudou, leia a diferença
antes de renovar o registro.

Após aceitar uma nova base editorial ou revisar conscientemente o acervo:

```powershell
python Scripts/auditar_base_monografia.py
```

Esse segundo comando atualiza `reports/assistencia_monografia/snapshot_fontes.json`
e `monografia_base_texto.txt`. Não atualiza os achados humanos da auditoria nem
transforma uma auditoria antiga em revisão da nova versão. As localizações Pxxxx
e o hash no relatório antigo devem ser tratados como históricos.

## Limites da configuração

O registro de hashes permite detectar mudanças; ele não autentica a origem dos
experimentos. A extração XML permite conferir texto e tabelas; ela não verifica
layout, equações como imagens, notas ou comentários fora do corpo principal.
Uma entrega em Word exige exportação/renderização e inspeção visual próprias.
Nenhum manuscrito ou dado é enviado a serviços externos pelo script criado aqui.
