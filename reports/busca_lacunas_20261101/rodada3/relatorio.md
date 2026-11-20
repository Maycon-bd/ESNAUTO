# Pesquisa das lacunas — rodada 3

Base: **v010**, SHA256 `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.

Foram ampliadas as evidências de 11 células em seis fontes. Foram recuperados o material de origem de Gjika, o CSV e dois Rmd originais do OSF. Nenhuma nova substituição foi sustentada. A matriz permanece com 38 informações insuficientes. Word, imagens da monografia e resultados experimentais não foram alterados.

## Achados

### Abebe e Goshu (2024) — P3

**Leitura nesta rodada:** PDF 9, 11, 13, 14.

**Cobertura anterior:** PDF integral já registrado no lote 14, com limitação da extração de fórmulas. Nesta rodada foram consultados também HTML oficial, Gjika/RPubs e arquivos originais do OSF.

A referência Cyber/heart failure está trocada entre as chamadas 44/45 do artigo. A página de Gjika explicitamente substitui zeros por 0.01 para ajuste da variável avg.report.length; não foi demonstrado que Abebe aplicou essa regra. O link OSF de Gjika aponta a uma figura, cujo projeto público contém o CSV original e dois Rmd. O CSV tem 366 semanas e três zeros. Retirar zeros e dividir por 100 produz 363 valores com Q1=3.985, mediana=5.1 e Q3=6.545, iguais à Tabela 5. A média calculada é 5.381322, contra 5.3810 publicado, e os momentos padronizados consultados não coincidem com os coeficientes da tabela. Essa concordância parcial não comprova uma receita histórica única. Rmd de terceiros foi apenas lido; nenhum modelo foi executado.

**Decisão:** Manter P3 como ?. Há evidência nova concreta sobre a origem e hipóteses de preparação; falta atribuir com segurança o procedimento realmente usado na amostra de 363 valores. Não contar tratamento de Gjika/Bakdash como operação executada por Abebe.

### Araújo et al. (2025) — P1, P4

**Leitura nesta rodada:** PDF 10, 11, 12, 13, 14, 15, 16, 17.

**Cobertura anterior:** PDF 1–9 lido na rodada 2; leitura integral histórica documentada no lote 6, com o mesmo hash.

As tabelas 1–4 comparam cinco famílias e fitness MAE/RMSE da ESN. A prosa e o fluxograma não ligam individualmente uma lei à geração dos elementos de Win/W. Não há contraste numérico com LSTM/GRU/Transformer nas tabelas e discussão. A referência 6 sobre GA-LSTM não é uma experiência apresentada no capítulo.

**Decisão:** Manter P1/P4 como ?. A leitura foi ampliada sem preencher informação que a prova local não explicita.

### Timbó et al. (2016) — P4

**Leitura nesta rodada:** PDF 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11.

**Cobertura anterior:** O lote 10 já documentava leitura integral deste mesmo PDF; esta rodada fez releitura sequencial.

O método usa regressão linear múltipla por mínimos quadrados. A função da Figura 2 é linear. A comparação da Figura 3 é previsão versus observado. A discussão compara ARIMA, fuzzy, AG e uma ANN não individualizada como arquitetura qualificadora; não apresenta comparação quantitativa com LSTM/GRU/Transformer. Não converter a sigla ANN em LSTM por hipótese.

**Decisão:** Manter P4 como ?.

### Zhang et al. (2021) — P1, P2, P4

**Leitura nesta rodada:** PDF 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15.

**Cobertura anterior:** PDF 6–9 foi lido na rodada 2; o lote 13 já documentava as 15 páginas do mesmo PDF.

As Figuras 2 e 5 inicializam Win/W sem especificar família ou procedimento de seleção. O algoritmo OMP escolhe átomos para reconstrução; os experimentos fixam parâmetros e compressão de 50%, sem escolher esse valor por busca ou sensibilidade descrita. As tabelas 2/3 e os gráficos comparam ESN versus CS-ESN. Z-score/min-max são preparação dos dados; matriz gaussiana de medição e reescala de estados não são lei dos pesos.

**Decisão:** Manter três ?. Nenhum código qualificador localizado nos canais consultados; a busca negativa não prova inexistência universal.

### Vishwas, Usha e Sangeetha (2025) — P1, P4

**Leitura nesta rodada:** PDF 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26.

**Cobertura anterior:** Páginas 1 e 17 lidas integralmente na rodada 2; os blocos desta rodada completam o texto das 26 páginas. A Figura 1 e a Tabela 5 foram abertas visualmente.

As sugestões de pyESN/EsnTorch são possibilidades de implementação, sem vincular uma versão/código do estudo revisto à lei de Win/W. A taxonomia não contém resultados numéricos. Além dos 72%/90% já investigados, foi rastreada a afirmação de ganho de até 18% por HQNN (p.5,18,24) à referência 9. O resumo oficial indexado de Gandhudi descreve rede quântica híbrida com AG e conclui que a influência dos tweets é limitada; não confirma o ganho de 18% nem que se trate de um contraste quantitativo LSTM. Abertura direta da página retornou 403; esta conferência da fonte de apoio é parcial, sem leitura integral certificada.

**Decisão:** Manter P1/P4 como ?. Não aproveitar o percentual não confirmado apenas para eliminar a célula.

### Millea (2014) — P3, P5

**Leitura nesta rodada:** PDF 84, 85, 86, 87, 88, 89, 90.

**Cobertura anterior:** Registro histórico do lote 21 lista leitura do corpo PDF 1–83. Houve nova leitura dirigida de método/resultados nas rodadas anteriores; esta rodada lê a bibliografia restante sem truncamento.

A bibliografia inclui Maciel et al. sobre câmbio, mas não identifica um ativo/par de moedas analisado pela própria dissertação. O resumo menciona Forex, enquanto o corpo examinado trabalha com MSO, Mackey-Glass, Sunspots e Laser. O artigo de Sarsa-ESN no site do autor é outra obra. Sua identificação de EURUSD não pode ser atribuída automaticamente à dissertação. As transformações da matriz e o ruído de estado não individualizam preparação da série.

**Decisão:** Manter P3/P5 como ?. Não trocar a dissertação por artigo distinto sem registrar mudança de corpus.

## Conciliação de evidências existentes

Os registros anteriores já documentavam leituras amplas de vários artigos. Foram vinculados registros das 22 fontes que ainda possuem “?” aos respectivos PDFs, com conferência dos hashes. Este índice identifica evidências existentes; não é prova automática de leitura integral nem dispensa conferir o alcance declarado. Não repetir a leitura de um PDF apenas porque um relatório de outra rodada se limitou a passagens dirigidas.

## Alternativas externas

- [Abebe e Goshu (2024)](https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/10.3389/fams.2024.1398137/full): Seção 8.2.1, Tabela 5 e referências 44/45 consultadas. A inconsistência das chamadas existe também no HTML oficial.
- [Gjika (2021)](https://rpubs.com/Eraldagjika/715261): Página e documento incorporado recuperados por HTTP público e arquivados por hash. Foram lidos início, importação, resumos, gráficos descritos e tratamento de zeros; feita busca dirigida no restante. Não se afirma leitura integral de todas as saídas de ajuste ou imagens. Nenhum R executado.
- [OSF — dados e análises originais](https://osf.io/rq82a/): Identidade do projeto recuperada pela API pública a partir do arquivo aj7vr. CSV e dois Rmd arquivados com procedência. Foram lidos o CSV por completo e os blocos de importação/preparação dos Rmd, sem executar os modelos. A aritmética descritiva de conferência foi registrada separadamente como reconstrução atual.
- [Zhang (2021)](https://www.sciencedirect.com/science/article/pii/S1007570421001696): Resultado oficial indexado consultado; abertura direta falhou. Conteúdo analisado provém do PDF local completo. Não foi recuperado suplemento qualificador na busca por título/DOI/código.
- [Araújo (2025)](https://link.springer.com/chapter/10.1007/978-3-031-77738-7_26): Página oficial consultada; não substitui a leitura da versão publicada integral pela prova local. Resultados genéricos de repositórios com MAE no nome não foram atribuídos aos autores.
- [Timbó (2016)](https://aircconline.com/ijaia/V7N1/7116ijaia03.pdf): PDF oficial localizado na busca; não há conteúdo novo recuperado que substitua a cópia local.
- [Gandhudi et al. (2024)](https://www.sciencedirect.com/science/article/pii/S0045790624002301): Resumo e prévia indexados da página da editora consultados na busca. Abertura da variante /abs/ retornou 403. Não foi obtido texto integral; a suposta melhora de 18% não foi confirmada. Fonte de apoio, sem ampliar o portfólio de 34.
- [Millea — alternativa de versão](https://m3t4n01a.github.io/rl_esn.pdf): Busca por versão alternativa da dissertação em Groningen e pelo título/Forex retornou também artigo distinto. Não há prova de que seja capítulo faltante da dissertação; não transportar seus ativos ou operações.

## O que permanece aberto

A informação não localizada não pode ser substituída por uma experiência de outro artigo nem pela configuração presumida de uma biblioteca. Parte das células descreve temas que a obra não documenta suficientemente, e não experiências que faltam executar nesta monografia. As leituras desta rodada não eliminam os 38 sinais nem demonstram conclusão da busca integral.

As rotas ainda úteis são verificar material complementar específico e esclarecer ambiguidades documentais. Em Abebe, a origem agora foi recuperada: falta comprovar o procedimento que resultou nos 363 valores e seus coeficientes publicados, não localizar novamente o CSV. A hipótese de excluir três zeros e dividir por 100 é parcialmente compatível, sem provar o protocolo. Continuar código/protocolo de origem para as leis de pesos e escolhas de hiperparâmetros ainda não declaradas. Não solicitar treinamento ou experimento novo para preencher a matriz bibliográfica. Não contactar autores sem instrução explícita do usuário.

## Verificação

- Identidade da v010 conferida por SHA256; sem nova versão Word por esta auditoria.
- Os 22 PDFs das células restantes continuam com os hashes do inventário.
- Oito páginas de fontes foram renderizadas e abertas: Abebe 11; Araújo 9; Timbó 7/9; Zhang 4/5; Vishwas 9/18.
- A triagem de links em todos os PDFs está em `triagem_suplementos.json`. Busca lexical serve para localizar canais, sem substituir leitura.
- Sem treinamento, busca genética, teste DM ou execução de códigos de terceiros.
