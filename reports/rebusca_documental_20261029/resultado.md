# Rebusca das cinco pendências documentais

Em 29/10/2026, o autor informou: “Tudo está aqui nesse projeto”. A declaração foi tratada como orientação para ampliar a busca local, sem presumir que os documentos já estivessem identificados.

Base examinada: **v002**, SHA256 `d41a33359e19f974dfd48eb322cb2a3877ba3cbbac20c9db941a19985076a093`, resolvida e conferida por `Scripts/versao_monografia.py atual --json`. Nenhuma edição do Word nesta etapa.

## Escopo executado

- Inventário de 3.228 arquivos da árvore de trabalho, incluindo arquivos ocultos e ignorados pelo Git, com exclusão das pastas de dependências listadas no manifesto.
- Inspeção de 52 contêineres ZIP, contando cópias e ZIPs internos, inclusive quatro objetos ZIP alcançáveis no histórico Git. Não são 52 acervos independentes.
- Inventário dos membros dos ZIPs e busca textual em membros compatíveis; consulta aos nomes de objetos históricos CSV, XLS/XLSX, PDF, BIB/RIS e SQL.
- Conferência dos históricos GA atuais e dos CSV contidos nos pacotes Git, sem restaurar ou modificar resultados.
- Leitura dos cabeçalhos de scripts legados e consulta ao histórico de commits dos componentes.

Evidências: `inventario_e_busca.json` e `historicos_conferidos.json`. Procedimento principal reproduzível em `Scripts/rebuscar_pendencias_documentais.py`.

## Resultado por pendência

| Pendência | Material localizado | O que ainda não foi comprovado |
|---|---|---|
| Origem do ajuste PETR4 | `Scripts/data/PETR4_close com factor_2000-2020.txt`; CSV correspondente com datas; `acoes-petr4 brutos com factor v2.8.1.1 para Maycon Garcia Silva.R`; `ESN Acoes-petr4 v2.8.1.2 Maycon G Silva.R`; artigo BovDB em `Artigos citados` | Os scripts leem os preços já ajustados. O caminho de trabalho contendo nome do orientador é indício de procedência, não identificação suficiente de quem calculou o fator. Não foi identificada nesta busca uma consulta/exportação ou rotina que reconstrua a transformação original a partir dos eventos. |
| Onda 5, GA_RUN_0053–0067 | `docs/09_onda_5_ajustes_empiricos_easyfit.md` contém os 15 resultados compilados. `Scripts/onda5_easyfit_simulations.R` contém o executor e `Scripts/empacotar_onda5_orientador.py` prevê o filtro dos IDs | Nos pacotes históricos, o CSV contém GA_RUN_0001–0048; o CSV atual contém GA_RUN_0001–0007. Nenhum contém os 15 IDs procurados. A existência do empacotador não comprova a existência do pacote gerado. Não executar o empacotador: ele altera pastas e não recupera os registros perdidos. |
| Cardoso, RBras 2022a | `Artigos citados/Cardoso -  A data set of stock prices of all companies in B3from 1995 to 2020.pdf`; `reports/tese_Fabian_Correa_Cardoso.pdf` | São o artigo BovDB e a tese, respectivamente. O original procurado tem título “Echo state network e sua aplicação na ação PETR4 da B3 para predição do preço de fechamento”, autores Cardoso/Berri/Mattos, referência aos anais da 66ª RBras, 2022, p. 197–206. Não foi identificado como documento independente no inventário ou nos nomes dos membros dos ZIPs. A menção em outra obra não substitui a conferência do original. |
| Exportações e planilhas bibliográficas | `reports/bibliometria_reconstrucao/artigos_reconstruidos.bib`, base JSON reconstruída, documentos e scripts de reconstrução | Não foram localizadas planilhas XLS/XLSX de pesquisa na árvore inventariada, nem membros correspondentes nos ZIPs examinados. As ocorrências de `methodi_ordinatio` e `extracao_completa` são menções no texto, scripts e relatórios. O BIB reconstruído não é a exportação original de busca/triagem/ranking. |
| Autoria/adaptação de código | Dois scripts legados na raiz; componentes em `app/utils`; commits de inclusão/modificação associados às contas do autor | O Git documenta inclusão e modificações no repositório. Não comprova sozinho autoria original de cada rotina importada. Os cabeçalhos com diretórios pessoais de terceiros também não comprovam autoria ou licença. A contribuição de integração continua documentada; a atribuição integral do código legado permanece não estabelecida. |

## Conclusão limitada

A informação do autor motivou uma busca ampliada, mas a localização exata de todos os documentos ainda não foi estabelecida nesta cópia do projeto. O acervo contém materiais relevantes para as cinco perguntas; isso não equivale ao fechamento das cinco cadeias de evidência. Foi solicitado apenas o caminho da subpasta ou de outra cópia do projeto para direcionar a próxima conferência, sem pedir novamente o envio dos cinco conjuntos.

Não há nova versão Word, novos experimentos, reexecução de GA, treinamento ou DM. Os snapshots, relatórios assinados por hash e arquivos experimentais anteriores foram preservados. Esta busca lexical não certifica ausência de documentos: não inclui OCR de todos os PDFs, conteúdo integral de arquivos binários ou objetos Git não alcançáveis. “Não identificado” significa somente não localizado no escopo registrado.
