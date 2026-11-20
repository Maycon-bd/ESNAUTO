# Conferência dos materiais recuperados no Drive

O autor indicou a pasta `1wjFkzGUiIAZ2wlYcqG_BLlHnQP2joYml` como acervo documental do TFC. A consulta ao Drive recuperou materiais que não estavam na cópia local: **as duas planilhas originais e o artigo RBras 2022a**. A conclusão anterior sobre não localização aplica-se somente ao acervo local então examinado e foi superada, para esses documentos, por esta recuperação.

Base editorial desta revisão: **v002**, SHA256 `d41a33359e19f974dfd48eb322cb2a3877ba3cbbac20c9db941a19985076a093`. A revisão altera seis parágrafos, identificados em `alteracoes_word_final.json`, e não modifica resultados experimentais.

## Evidências recuperadas

### Planilhas de seleção e extração — F18/R01

- [methodi_ordinatio.xlsx](https://drive.google.com/file/d/15j9btZi2vdhxUs2syjS_y4s657hfbWmm/view): original XLSX preservado localmente, incluindo fórmulas e valores em cache.
- [extracao_completa.xlsx](https://drive.google.com/file/d/118c9JyYZIxbRzjzz7pzn8lmdDvjZRZXC/view): original XLSX com 34 registros, todos marcados `CONCLUIDO`; os 34 nomes correspondem aos PDFs locais.

Na aba `1. Protocolo RSL`, `D7:D10` registra data declarada de busca 23/03/2026, Scopus + Springer Nature Link e alfa 5. A célula `A13`, abaixo do título da string, contém somente espaço. `A23` descreve a fórmula utilizada no arquivo, com divisão das citações por 100. A presença da fórmula documenta a implementação local; não demonstra identidade com a fórmula publicada por Pagani e colaboradores.

Na aba `2. InOrdinatio`, as linhas 4–62 contêm **59 candidatos**: **7 INCLUIR, 4 EXCLUIR e 48 sem decisão** em `R4:R62`. Todos os campos `J4:J62` estão zerados. As fórmulas de pontuação em `N4:N62` usam `J/1000 + 5*(10-(2026-Ano)) + Ci/100`; o ranking está em `O4:O62`. Não houve reexecução ou alteração das fórmulas originais.

O fluxo declarado em `1. Protocolo RSL!A27:E33` exige conciliação: 24 + 35 após triagem somam 59; descontar as 5 duplicatas declaradas produziria 54, enquanto o portfólio seguinte permanece 59. A inclusão final está marcada com `?`. Esses dados não comprovam uma triagem final de 34 estudos.

A aba `Fator de Impacto` tem 33 linhas de registros (3–35), com duplicação do título de Wang W. nas linhas 31 e 33. A coluna de cálculo não contém fórmulas preenchidas. Os valores manuais de SJR, anos e citações não foram aceitos como metadados validados apenas por constarem na planilha.

`extracao_completa.xlsx`, aba `Extração RSL`, linhas 2–35, preserva respostas P1–P5 e datas de processamento. A extração é registro intermediário de interpretação, não fonte primária. Exemplos de respostas históricas não devem substituir as correções científicas já documentadas na v002, como a distinção entre distribuições de pesos e distribuições da busca de hiperparâmetros. A matriz recodificada de 170 células permanece preservada.

**Resultado:** encerrada a lacuna de localização das planilhas. Permanecem a falta de exportações diretas das plataformas no conjunto recuperado nesta etapa, a string vazia, a triagem incompleta e os problemas de conciliação. A descrição da monografia foi atualizada para refletir o material realmente recuperado.

### Original RBras — F19

[Original fornecido no Drive](https://drive.google.com/file/d/120l0dL5DM28bgXuhZeWqSrR9EoPpigQ9/view): recorte de **dez páginas, numeradas 197–206**, título e autores correspondentes à referência Cardoso/Berri/Mattos, 66ª Reunião Anual da RBras, 2022. Trata-se de PDF composto por imagens: a extração textual retornou vazia. As **dez páginas foram renderizadas e lidas visualmente** nesta revisão.

Arquivo completo preservado como `Cardoso_RBras_2022_completo.pdf`, 10.262.978 bytes, SHA256 `286bc9f8f90a8ce41d68605462a4656a0290a9f1685859823ddeff1ea4eb1a07`. O download inicial ficou incompleto; o trecho final foi recuperado por requisição parcial e a cópia completa foi aberta e renderizada com sucesso. O hash identifica os bytes obtidos; o conector não retornou checksum do provedor para uma comparação independente.

Localizadores conferidos:

- **p. 202, metodologia:** PETR4 PN, 2000–2020, **5.197 observações**, séries bruta e ajustada, divisão **75% treino e 25% teste**.
- **p. 203:** raio espectral **1,25**, taxa de vazamento **0,2**, regularização **10⁻⁸**; matrizes geradas aleatoriamente entre −1 e 1. A descrição não informa uma busca genética nesse experimento. Não atribuir a esse artigo as faixas binárias do ESNAUTO.
- **p. 205:** RMSE **11,1785 sem fator** e **0,4987 com fator**, na comparação interna do artigo. O valor 0,4987 não corresponde à série sem ajuste.
- **p. 198:** há menção isolada a VALE3, em contraste com título, resumo, metodologia e figuras que tratam PETR4. Registrar a inconsistência do original, sem converter os resultados em evidência VALE3.

**Resultado:** F19 deixa de ter a fonte original pendente. A revisão explicita que os conceitos de hiperparâmetros são apoiados pela literatura e que as faixas/55 bits são do código local. O RMSE foi contextualizado em prosa com indicação correta do ajuste e das diferenças de protocolo. A Tabela 7 continua dedicada a Lampugnani; não se restituiu uma comparação experimental equivalente que nunca foi executada.

### Série ajustada e código — R03/R13

Na pasta `Scripts` do Drive foram recuperados o script legado, TXT da série e CSV com datas. Os TXT/CSV apresentam **conteúdo textual idêntico** aos arquivos locais após normalização de UTF-8/BOM e quebras de linha; os hashes binários diferem. Conferência em `comparacao_drive_local.json` e `conferencia_planilhas_procedencia.json`.

O script do Drive, `script_legado_drive.R`, preserva uma versão anterior da rotina da raiz. A comparação mostra mudanças em comentários, exportações e configurações entre as cópias; o cabeçalho preserva um diretório pessoal associado ao orientador. Isso reforça a documentação da evolução do código, mas não estabelece sozinho autoria intelectual de cada rotina nem identifica quem calculou o ajuste dos preços. A rotina importa a série já ajustada.

O documento histórico de metodologia foi consultado e preservado como `metodologia_planejada_connector.txt`. Emprega futuro para diversas atividades e descreve experimentos diferentes do protocolo efetivamente executado; não foi usado como prova de aplicação do fator, ablações, sementes ou testes já realizados. A atribuição PETR4 ON nesse planejamento também não substitui a identificação correta de PETR4 PN no manuscrito vigente.

**Resultado:** há novas evidências de procedência do acervo e de evolução de código. A cadeia original da transformação dos preços e a divisão completa de autoria/licenças continuam não estabelecidas pelos arquivos consultados.

### Onda 5 — R08

A pasta `Scripts` do Drive contém quatro pastas de cenários de 10.000 gerações e seus arquivos de matrizes, melhores soluções e resumos. Os nomes identificam Normal/Normal, Uniforme/Uniforme e GED/Uniforme; em uma pasta cujo nome contém GED/Uniforme, o PDF interno indica GED/Normal. O inventário foi preservado e essa divergência impede usar somente o nome da pasta como identidade do experimento.

Esses materiais não foram identificados como os **15 registros GA_RUN_0053–0067**. Não foram assimilados à Onda 5, à rodada DM de seed 20260926 ou ao lote ilustrativo de 200 gerações. Nenhum experimento foi reexecutado. O ZIP do anteprojeto foi inventariado e contém documentos de apresentação/planejamento, sem o histórico dessa onda.

**Resultado:** a documentação compilada da Onda 5 permanece disponível, mas os registros primários dos 15 IDs continuam não identificados nesta consulta. Não se declara inexistência universal no Drive.

## Alcance da revisão

O inventário do Drive está nos arquivos `pasta_*.json`, com IDs, nomes, tipos e datas retornados pelo conector. Foram priorizados materiais pertinentes às cinco pendências; vídeos e subpastas de renderização de slides não foram integralmente examinados. Não foi certificado o conteúdo integral de todos os arquivos da pasta.

Os originais do Drive foram apenas lidos. Nenhum arquivo remoto foi editado, reorganizado ou compartilhado. Os snapshots anteriores e suas evidências registradas por hash permanecem preservados. Não houve treinamento, busca genética ou teste DM.

Esta conferência não representa aprovação acadêmica, validação universal de todas as citações nem certificação de ausência de plágio. A localização das fontes agora permite corrigir as declarações de indisponibilidade e avançar a revisão com evidência concreta.

## Verificação da revisão para registro

A revisão de seis parágrafos manteve **76 páginas**, com **45 verificações estruturais aprovadas**. As 60 entradas das listas/sumário correspondem ao mapa do Word. As 50 referências e 151 ocorrências autor–ano reconhecidas permanecem sem órfãs nos padrões examinados. Texto das tabelas, mídias e conteúdo fora das alterações autorizadas foram preservados no escopo das verificações.

A comparação visual intermediária encontrou 56 páginas idênticas, pixel a pixel, à v002; as outras 20 foram examinadas em quatro folhas de contato. A revisão final teve 75 páginas idênticas à intermediária, com a página 50 aberta integralmente após o último ajuste. As páginas 44 e 63 também foram abertas integralmente para conferir os trechos novos sobre Cardoso. Não foram usados mascaramentos nas comparações. Evidências em `verificacao_final.json`, `inspecao_visual_final.json` e nos dois registros de comparação visual.

A matriz atualizada dos 38 achados está em `resolucao_achados_atualizada.csv`. Ela complementa o relatório histórico da v002 sem modificar seus arquivos de evidência registrados por hash. Os índices dos parágrafos em `alteracoes_word_final.json` referem-se à v002, não à v001 do parecer inicial.
