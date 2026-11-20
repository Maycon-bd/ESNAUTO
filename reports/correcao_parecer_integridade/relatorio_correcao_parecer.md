# Correção do parecer de citações e integridade — ESNAUTO

Revisão de Maycon Garcia Silva. Este relatório documenta a aplicação das correções de F01–F25 e R01–R13 do parecer de 28/10/2026. A base foi v001, cópia exata do Word auditado, SHA256 `2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa`. O original e as evidências históricas foram preservados.

A revisão contém correções substanciais de fidelidade, metodologia, síntese bibliográfica, metadados e apresentação. Há lacunas documentais que não podem ser resolvidas pela redação. Por isso, o estado editorial indicado para o registro é **em revisão**, sem certificação de coerência integral, ausência de plágio ou aprovação acadêmica.

## Documento preparado

Título: **Previsão do preço de fechamento ajustado da PETR4 com redes neurais de estados de eco e otimização genética**.

A cópia candidata recebeu a atualização nativa de listas, sumário e campos no Word. O PDF correspondente tem 76 páginas. A versão numerada vigente deve ser consultada em `docs/assistencia_monografia/versao_vigente.json`; os nomes de candidatas identificam etapas de preparação, não versões oficiais concorrentes.

## Correções principais

- Corrigidas atribuições de F1, sentimento de notícias, tolerância de preço, janelas de treino, simulações e resultados de comparadores. Removidas garantias gerais de estabilidade, eficiência, significância e efeito causal que as evidências consultadas não sustentavam.
- Separadas distribuições dos elementos de Win/W, topologia do reservatório e distribuições usadas na busca de hiperparâmetros. A matriz dos 34 documentos foi recodificada em 170 células e refletida na tabela, no quadro, na Figura 1 e nas sínteses.
- O texto distingue evidência direta, tratamento secundário/contextual, informação insuficiente e dimensão não aplicável. As 43 células insuficientes permanecem explícitas: não são prova de ausência do assunto na obra nem contagem de defeitos da monografia.
- A coleção bibliográfica é descrita como reconstruída. Contagens históricas de busca e seleção não são apresentadas como exportações originais ou ranking independentemente reproduzido; não foi inventada planilha substituta.
- O ajuste corporativo passou a ser descrito como condição dos arquivos recebidos. A redação não atribui sua transformação original ao autor nem estima ganho causal do fator sem comparação correspondente.
- H4 não é tratada como demonstrada pela presença de LHS/cataclismo. H5 distingue dispersão entre configurações de variabilidade entre sementes. A interpretação da H1 não transforma falta de significância em equivalência.
- Preservada a separação entre 45 execuções históricas, rodada controlada com semente 20260926 e lote ilustrativo de 200 gerações. Nenhum treinamento, busca genética ou teste de Diebold–Mariano foi reexecutado para esta correção editorial.
- Retirada da comparação quantitativa a linha de Cardoso (2022a), cujo original não foi conferido. Os mínimos de Lampugnani foram conferidos diretamente em 24 linhas de resultados. A comparação entre estudos continua descritiva.
- Reconciliados nomes e versões bibliográficas; as referências anteriormente sem chamada passaram a sustentar conteúdo pertinente. O Quadro 6 delimita antecedentes, integração experimental e procedência ainda não recuperada do código.
- Corrigidos título, siglas, destaques dos trechos reescritos, paginação e listas. A tabela curta de síntese foi mantida inteira; páginas com apenas duas linhas de continuação foram eliminadas.

## Verificações e alcance

As 45 verificações de `verificacao_candidata06.json` passaram: preservação do texto do corpo/tabelas e das mídias durante o salvamento nativo, margens e A4, extensão dos resumos, tamanhos de fonte específicos, títulos, 60 entradas de listas/sumário, paginação e limites de texto no PDF. Isso não constitui certificação universal de formatação.

A cobertura visual foi registrada por inspeção e comparação de páginas rasterizadas. Na aplicação final, 70 páginas mantiveram todos os pixels fora da região do número no cabeçalho idênticos à aplicação anterior examinada; as seis diferentes foram abertas novamente. As versões anteriores desse encadeamento têm cobertura global registrada. A numeração foi conferida separadamente. Não foram identificados recortes ou sobreposições nessa verificação. As imagens e relatórios permitem conferir seu alcance.

O cruzamento nominal reconheceu **151 ocorrências autor–ano e 50 referências**, sem chamadas reconhecidas órfãs ou referências sem chamada reconhecida. O método não detecta universalmente todo formato e não comprova, sozinho, sustentação científica.

A triagem textual da candidata utilizou 39 fontes locais, incluindo os 34 PDFs, e encontrou seis janelas de oito palavras, agrupadas em três blocos: nomenclatura/autores de arquiteturas, expansão de RNN e denominação de AIC. A leitura dos contextos não demonstrou apropriação indevida nesses blocos. Na comparação adicional de 38.958 pares de parágrafos com Lampugnani, nenhum atingiu a razão heurística de tokens 0,40. **Esses números não são percentual de plágio ou escore de originalidade.**

A comparação lexical não cobre traduções dependentes, paráfrases sem correspondência literal, documentos privados, todo o conteúdo publicado ou procedência do código. Nelson é escaneado e não possui texto indexável na extração usada; a consulta visual anterior à obra serviu à fidelidade conceitual, sem produzir OCR integral. As fontes eletrônicas adicionais não foram incorporadas automaticamente ao corpus local. Não foram usados Turnitin, iThenticate ou detectores de IA como prova.

A conferência científica tem localizadores e escopos de leitura registrados. Não se declara leitura integral de todas as páginas de todas as obras nem conferência de uma edição final paga quando só foi lida a prova ou o preprint.

## Estado dos 38 itens

A coluna de estado distingue correção do texto e comprovação documental. Os localizadores P no log e na matriz de resolução pertencem à base v001; inserções e exclusões alteraram os índices da revisão.

| ID | Achado ou risco | Situação |
|---|---|---|
| F01 | F1 de uma amostra de ações atribuído especificamente à PETR4 | Corrigido no escopo do achado |
| F02 | Sentimento de notícias confundido com direção do índice | Corrigido no escopo do achado |
| F03 | Janelas de treinamento apresentadas como horizonte de previsão | Corrigido no escopo do achado |
| F04 | Distribuição da busca de hiperparâmetros confundida com distribuição dos pesos | Recodificado; incerteza explícita |
| F05 | A lista dos cinco trabalhos omite uma fonte explicitamente pertinente | Recodificado; incerteza explícita |
| F06 | Taxa de acerto por tolerância confundida com acerto direcional | Corrigido no escopo do achado |
| F07 | Recomendação de redes recorrentes atribuída além do que a fonte diz | Corrigido no escopo do achado |
| F08 | Uso de fechamento ajustado em Sun não está demonstrado | Corrigido no escopo do achado |
| F09 | Seddik exige distinção entre série simulada e preços observados | Corrigido no escopo do achado |
| F10 | Resultados conservadores em Liu não demonstram imunidade a mudanças de regime | Corrigido no escopo do achado |
| F11 | Definição de AG atribuída a Millea sem apoio localizado | Corrigido no escopo do achado |
| F12 | Versão de Soltani e conclusões de lacuna precisam ser distinguidas | Corrigido no escopo do achado |
| F13 | Eficiência e estabilidade apresentadas como garantias gerais | Corrigido no escopo do achado |
| F14 | Comparações e linguagem causal mais fortes que a evidência localizada | Corrigido no escopo do achado |
| F15 | A matriz P1–P5 tem marcas incompatíveis com suas definições | Recodificado; incerteza explícita |
| F16 | Lacunas científicas e palavras de abrangência não estão sustentadas pelas contagens atuais | Recodificado; incerteza explícita |
| F17 | Ajuste corporativo tem apoio, mas a lista detalhada contém interpretação adicional | Corrigido no escopo do achado |
| F18 | Fórmula e execução de Methodi Ordinatio não podem ser certificadas | Texto corrigido; documento pendente |
| F19 | Comparação com Cardoso 2022a depende do original | Original ainda necessário |
| F20 | Metadados não estão integralmente reconciliados | Resolvido no escopo do achado |
| F21 | Duas referências não têm chamada autor–ano localizada | Resolvido no escopo do achado |
| F22 | Resultados de Nelson apoiam a parametrização, não uma necessidade de pesos GED | Corrigido no escopo do achado |
| F23 | Duttilo 2023 reúne afirmações de fontes distintas | Corrigido no escopo do achado |
| F24 | H1 ainda define comparabilidade por não significância | Corrigido no escopo do achado |
| F25 | A introdução teórica exclui modelos estatísticos de forma indevida | Corrigido no escopo do achado |
| R01 | “Como a revisão foi sistemática se não há trilha de seleção/ranking?” | Texto corrigido; documento pendente |
| R02 | “Por que as contagens de cobertura contêm estudos mal classificados?” | Recodificado; incerteza explícita |
| R03 | “Quem aplicou o Fator de Ajuste e onde está a transformação?” | Texto corrigido; documento pendente |
| R04 | “A ordem cronológica garante sozinha ausência de vazamento?” | Limitação conferida no texto |
| R05 | “Foram preservadas as matrizes campeãs?” | Limitação conferida no texto |
| R06 | “O teste foi usado para escolher o campeão?” | Limitação conferida no texto |
| R07 | “Qual o efeito específico de LHS/cataclismo?” | Limitação explicitada |
| R08 | “Baixa variação entre configurações é estabilidade entre repetições?” | Texto corrigido; documento pendente |
| R09 | “A comparação favorece a ESN pelo orçamento de otimização?” | Limitação conferida no texto |
| R10 | “DM comprova equivalência, generalização ou todas as sementes?” | Escopo controlado conferido |
| R11 | “R² alto demonstra utilidade financeira ou valor além da persistência?” | Limitação explicitada |
| R12 | “O título atribui ao fator uma contribuição que não foi isolada?” | Corrigido no escopo do achado |
| R13 | “Qual a contribuição própria frente a Araújo, Lampugnani e Cardoso?” | Texto corrigido; documento pendente |

O arquivo `resolucao_achados.csv` contém a decisão individual, trechos e limites de cada item. `lote1_alteracoes.json` contém texto anterior, texto aplicado, evidências e mudanças estruturais. A classificação acima não equivale a afirmar que documentos ausentes foram recuperados.

## Informações que ainda preciso do autor

1. **Origem da série ajustada — R03.** Quem gerou `PETR4_close com factor_2000-2020.txt` e `PETR4_close com factor_2000-2020_com data.csv`? É necessário o script, consulta ou exportação que ligue cotações/eventos originais aos arquivos, com responsável e versão. A concordância das 5.198 observações foi conferida; ela não comprova a transformação original.
2. **Registros primários da Onda 5 — R08.** Há uma cópia histórica das execuções `GA_RUN_0053` a `GA_RUN_0067`, com parâmetros, erros e, se existentes, sementes/horários? Esses IDs constam no relatório compilado, mas não no CSV agregado atual examinado. Os números foram preservados como compilados e a interpretação foi limitada. Não é necessário refazer os experimentos para responder.
3. **Trabalho RBras de Cardoso (2022a) — F19.** É necessário o texto original completo ou as páginas que originaram o Quadro 3. A comparação de RMSE foi retirada; a atribuição histórica do quadro foi preservada para não apagar crédito. A tese de 2025 não substitui esse original.
4. **Busca e seleção bibliográfica — F18/R01.** Existem as exportações originais de Scopus/Springer, as strings e filtros usados e as planilhas `methodi_ordinatio.xlsx` e `extracao_completa.xlsx`? Sem esses registros, a redação continua assumindo uma coleção reconstruída, sem alegar reprodução integral do processo histórico.
5. **Código legado — R13.** Quais rotinas foram fornecidas pelo orientador ou adaptadas de Araújo/Lampugnani/outros autores, e quais foram implementadas nesta pesquisa? São úteis os arquivos originais, commits, cabeçalhos de autoria/licença ou confirmação escrita das contribuições. Caminhos e nomes de arquivos não bastam para atribuir autoria.

Se algum material não existir, essa informação permite definir com o autor a manutenção da limitação ou a retirada de uma atribuição ainda não comprovada. Não se deve reconstruir evidência histórica como se fosse original.

## Guia e etapa acadêmica

O título e as conclusões foram alinhados ao que o protocolo demonstra; fontes, limites e versões consultadas ficaram explícitos. A ficha catalográfica emitida pela biblioteca e a folha de aprovação datada/assinada dependem da etapa institucional. Não foram fabricadas.

Os riscos de defesa foram tratados como questões de rigor e sustentação, não como previsão de reprovação. O guia fornecido não estabelece um percentual automático de plágio ou uma tabela completa de penalidades e notas de banca; tais regras não foram inventadas nesta revisão. Uma decisão institucional sobre aprovação ou irregularidade não pode ser substituída por este relatório.

## Evidências principais

- `lote1_alteracoes.json`: alterações rastreáveis, fontes e preservação.
- `resolucao_achados.csv`: 25 achados e 13 riscos, um a um.
- `matriz_recodificada.json` e `revalidacao_matriz_170_atual.json`: 34 fontes, 170 células, critérios e limites; conferência adicional direta na candidata final.
- `verificacao_candidata06.json` e `inspecao_visual_candidata06.json`: estrutura, paginação e cobertura visual.
- `cruzamento_referencias_candidata06.json`: correspondência nominal.
- `integridade_candidata06/triagem.json`, `interpretacao.md` e `pares_lampugnani.json`: corpus, coincidências, interpretação e limites.
- `evidencia_procedencia_h4_h5.json`, `evidencia_comparacao_lampugnani.json`, `evidencia_fidelidade_atribuicoes.json` e registros de metadados: evidências específicas.

Candidata preparada: `reports\monografia\trabalho\revisao_parecer_integridade_candidata06.docx`.

SHA256 DOCX: `d41a33359e19f974dfd48eb322cb2a3877ba3cbbac20c9db941a19985076a093`.

PDF: `reports\correcao_parecer_integridade\candidata06_listas_atualizadas.pdf`.

SHA256 PDF: `46828aeec0502424c41320db72f54ad1941e76f1c3ca5a7bfc94a5a09d99fda4`.
