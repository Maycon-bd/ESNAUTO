"""Primeiro lote editorial rastreável; preserva partes OOXML não alteradas."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from difflib import SequenceMatcher
from copy import deepcopy
import hashlib,json,re,io,struct

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reports/monografia/versoes/v001/MayconGarciaSilva_monografia_v001.docx'
DEST=ROOT/'reports/monografia/trabalho/revisao_parecer_integridade.docx'
OUT=ROOT/'reports/correcao_parecer_integridade';OUT.mkdir(exist_ok=True)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
XMLSPACE='{http://www.w3.org/XML/1998/namespace}space'
registry=json.loads((ROOT/'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf8'))
assert registry['vigente']=='v001','A versão vigente mudou; conciliar antes de reconstruir a cópia.'
assert hashlib.sha256(BASE.read_bytes()).hexdigest()=='2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa'
previous_log=OUT/'lote1_alteracoes.json'
if DEST.exists() and previous_log.exists():
    assert hashlib.sha256(DEST.read_bytes()).hexdigest()==json.loads(previous_log.read_text(encoding='utf8'))['sha256_trabalho'],'Rascunho modificado fora do construtor; preservar e conciliar antes de continuar.'

# Índices da extração do parecer: parágrafos do corpo, depois parágrafos das tabelas.
with ZipFile(BASE) as basezip:
    base_paragraphs=etree.fromstring(basezip.read('word/document.xml')).find('w:body',NS).findall('w:p',NS)
def base_text(index):return ''.join(base_paragraphs[index].xpath('.//w:t/text()',namespaces=NS))
TITLE='PREVISÃO DO PREÇO DE FECHAMENTO AJUSTADO DA PETR4 COM REDES NEURAIS DE ESTADOS DE ECO E OTIMIZAÇÃO GENÉTICA'
edits={
3:('R12',TITLE,'Título alinhado ao desfecho efetivamente avaliado e à otimização ESN. O estudo não isola ganho causal do fator; evita atribuir ao ajuste a contribuição experimental principal.'),
7:('R12',TITLE,'Mesma alteração de título na folha de rosto, preservando estilo e demais elementos.'),
18:('R12',TITLE,'Mesma alteração de título na folha de aprovação, sem preencher nomes, datas ou aprovação inexistentes.'),
41:('R03',base_text(41).replace('O Fator de Ajuste foi aplicado como etapa fixa de pré-processamento para reduzir descontinuidades associadas a eventos corporativos, sem atribuição causal isolada de ganho de acurácia ao procedimento.','Os modelos receberam arquivos identificados como previamente ajustados por eventos corporativos. A documentação preservada não identifica a autoria da transformação original, e o efeito causal isolado do ajuste não foi estimado.'),'Resumo: correção pontual de procedência, sem alterar resultados numéricos. Mantido parágrafo único e extensão de resumo; não se aplica o limite editorial de 700 caracteres a este elemento.'),
44:('R03',base_text(44).replace('The Adjustment Factor was applied as a fixed preprocessing step to reduce discontinuities associated with corporate events, without attributing an isolated causal accuracy gain to the procedure.','The models received files identified as previously adjusted for corporate events. The preserved documentation does not identify who performed the original transformation, and the isolated causal effect of the adjustment was not estimated.'),'Abstract: mesma limitação de procedência do resumo; alteração pontual, sem mudar números nem tratar o texto inglês inteiro como estrangeirismo em português.'),
158:('R08','4.4DISPERSÃO ENTRE CONFIGURAÇÕES E GENERALIZAÇÃO57','Título do sumário harmonizado à seção 4.4; tabulações preservadas. Página será atualizada ao final.'),
179:('R08',base_text(179).replace('exame da estabilidade das execuções','exame da dispersão entre configurações'),'Objetivo de avaliação delimitado ao dado efetivamente compilado, sem pressupor repetições de sementes por configuração.'),
243:('F17','Cardoso et al. (2022b) propõem o BovDB como base de cotações e eventos de ações negociadas na B3. O esquema inclui fatores associados a eventos e um fator acumulado por registro de preço. Essa estrutura permite representar o tratamento de descontinuidades corporativas na base, mas não comprova, por si só, quais eventos foram aplicados aos arquivos locais desta pesquisa nem identifica a autoria de sua transformação.','BovDB PDF 5–7, esquema e seção 4.1; separa proposta da base da cadeia não recuperada dos arquivos PETR4.'),
244:('F17','Na definição do BovDB, o fator isolado é a razão entre o fechamento do dia anterior e a abertura do dia do evento, e os fatores acumulados são calculados regressivamente. O campo EventPrice.applied distingue os registros considerados no ajuste. A interpretação de cada tipo de evento e a reprodução da transformação exigem esses registros; uma lista de descrições, isoladamente, não demonstra como o preço local foi corrigido (Cardoso et al., 2022b).','BovDB PDF 5, EventPrice.applied, e PDF 7, equações 1–2. Retiradas exceções por evento sem respaldo primário específico.'),
309:('R03','A pesquisa utiliza arquivos locais da série PETR4, identificados como preços de fechamento com Fator de Ajuste e cuja procedência é atribuída ao BovDB (Cardoso et al., 2022b). O ativo é a ação preferencial da Petróleo Brasileiro S.A. (PETROBRAS PN). A documentação do BovDB fundamenta o tratamento de eventos corporativos; a procedência da base e a autoria da transformação dos arquivos utilizados são questões distintas.','Arquivos Scripts/data/PETR4_close com factor_2000-2020.txt e CSV com datas; executor 01_prepare_data.R; cadeia da transformação não recuperada.'),
310:('R03/F19','A variável-alvo foi o preço de fechamento disponibilizado como ajustado, de 3 de janeiro de 2000 a 30 de dezembro de 2020, totalizando 5.198 observações diárias. Os arquivos fornecidos aos modelos preservam os valores e as datas dessa série. A coincidência de ativo ou intervalo entre estudos não demonstra equivalência dos respectivos tratamentos, partições e protocolos de previsão.','Executor controlado 01_prepare_data.R verifica valores, datas e 5.198 observações. Retira afirmação de mesmo período de Cardoso RBras sem original e de equivalência entre protocolos.'),
311:('R03/F17','Os executores consultados importam os valores dos arquivos PETR4_close com factor_2000-2020.txt e PETR4_close com factor_2000-2020_com data.csv. Não foi recuperado um registro completo que ligue as cotações e os eventos originais do BovDB à geração desses dois arquivos, incluindo quem realizou a transformação. Por isso, o procedimento de modelagem é descrito a partir da série recebida como previamente ajustada, sem atribuir a aplicação original do fator ao autor.','Scripts/diebold_mariano/01_prepare_data.R, linhas 4–18; ausência de cadeia completa documentada no parecer e na inspeção local, sem declarar inexistência histórica da transformação.'),
312:('R03/F17','A ausência dessa cadeia limita a auditoria retrospectiva do ajuste corporativo, ainda que os valores e as datas de entrada possam ser identificados por seus arquivos. A descrição das equações do BovDB oferece a referência metodológica, mas não substitui o registro dos eventos aplicados nem prova que cada exceção descrita na literatura tenha sido implementada na série local.','BovDB PDF 5–7 e arquivos locais de entrada. Removidas atribuições de aplicação/isenção de tipos de eventos que os executores de modelagem não comprovam.'),
316:('R03/R04','A ESN recebeu os valores da série já disponibilizada como ajustada, sem normalização adicional para [−1, 1]. Na rodada controlada, LSTM e GRU usaram Min-Max calculado exclusivamente sobre as 2.600 observações de treino e reutilizado na validação e no teste. Esse procedimento de escalonamento foi verificado no protocolo controlado; sua confirmação para cada execução histórica depende dos artefatos preservados. A ordem cronológica, isoladamente, não demonstra ausência de vazamento.','Scripts/diebold_mariano/01_prepare_data.R e 02_esn_controlled.R; distinção entre evidência controlada e histórico, sem inferir verificação universal de dias sem negociação.'),
325:('R08',base_text(325).replace('tanto desempenho quanto estabilidade','tanto desempenho quanto dispersão dos erros entre configurações'),'Discussão da Onda 5 delimitada à comparação entre configurações; não alterar hipótese inicial nem afirmar variabilidade entre sementes.'),
333:('R07','O motor de busca disponibilizado incorpora um mecanismo de mutação cataclísmica inspirado no CHC (Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation), de Eshelman (1991). Após estagnação, o mecanismo aumenta a mutação para ampliar a exploração. Essa finalidade de implementação não demonstra manutenção de diversidade: não foram produzidas medidas populacionais específicas nem uma ablação que isolasse o efeito do LHS e do operador. O mecanismo não corresponde ao CHC completo.','app/utils/ga_engine.R, inicializador LHS e mutação 0,12/0,40; implementação atual não é prova de eficácia em todas as execuções históricas. Fonte original Eshelman permanece em conferência.'),
348:('R07/R08','A análise das hipóteses distinguiu resultados e limites de avaliação. H1 comparou ESNs, GRU e LSTM; H2 separou ajuste e busca; H3 descreveu configurações não gaussianas frente a Normal × Normal. Para H4, verificou-se a integração do LHS e do operador cataclísmico, sem medida de diversidade ou ablação. H5 foi examinada pelos erros e pela dispersão entre configurações da Onda 5, sem estimar a variabilidade de repetidas sementes para uma mesma configuração.','Parecer R07/R08; documentação histórica agrega combinações, não estudo de diversidade ou repetições controladas por configuração.'),
416:('R08','DISPERSÃO ENTRE CONFIGURAÇÕES E GENERALIZAÇÃO','Título descreve a análise realizada; não apresenta dispersão entre configurações como estabilidade entre sementes.'),
419:('R08','Nas métricas compiladas da Onda 5, as 15 configurações apresentaram MAE entre aproximadamente 0,328395 e 0,328398, amplitude de 0,000003, e amplitude de RMSE próxima de 0,000002. Essa concentração descreve diferenças entre as configurações avaliadas. Não estima a variabilidade de repetir cada configuração com novas sementes nem comprova robustez a outros períodos. As distribuições ajustadas não produziram o menor erro global.','docs/09_onda_5_ajustes_empiricos_easyfit.md, tabela de GA_RUN_0053–0067; CSV agregado atual não contém esses IDs, portanto valores tratados como compilados, sem alegar revalidação primária nesta etapa.'),
456:('R07/R08','Para H3, variantes não gaussianas produziram os menores erros observados, com ganhos inferiores a 1% frente a Normal × Normal. Para H4, a integração do LHS e do operador cataclísmico foi documentada, mas a diversidade não foi mensurada e seus efeitos não foram isolados por ablação. Para H5, observou-se baixa dispersão entre configurações da Onda 5, sem menor erro global; esse resultado não demonstra redução da variabilidade entre repetições de uma mesma configuração.','Síntese do alcance das hipóteses; preserva números históricos como descrição e não promove integração a confirmação de H4.'),
458:('R03/F19','Esta pesquisa avaliou cinco ondas de distribuições e integrou LHS e um mecanismo antiestagnação inspirado no CHC ao processo experimental. Os modelos receberam a série identificada como previamente ajustada por eventos corporativos. Como os estudos diferem em mais de um componente metodológico e a cadeia original do ajuste local não foi recuperada, diferenças de erro não são interpretadas como efeito causal do fator nem como teste de superioridade entre protocolos equivalentes.','Registros do protocolo e importação da série ajustada; fonte Cardoso RBras 2022a não localizada, comparação numérica ainda pendente no parecer.'),
478:('R08',base_text(478).replace('elevada estabilidade','baixa dispersão dos erros entre configurações'),'Discussão: substituir estabilidade geral por dispersão efetivamente observada, mantendo a interpretação conjunta dos fatores.'),
493:('R03','Foram investigadas famílias probabilísticas em Win e W, selecionados hiperparâmetros por AG e comparados resultados com ESN Normal × Normal, LSTM e GRU. O ESNAUTO organizou o processo e suas saídas, e H1 recebeu uma análise inferencial complementar pelo teste de Diebold-Mariano. A modelagem utilizou arquivos identificados como previamente ajustados; a autoria e a cadeia da transformação original não foram recuperadas. As limitações de procedência, comparação e preservação dos artefatos integram o alcance dos resultados.','Produtos experimentais e importação de dados; não declarar a aplicação do fator como objetivo demonstradamente executado pelo autor, nem certificar todas as comparações externas.'),
494:('R03','O emprego de preços disponibilizados como ajustados delimita a entrada do protocolo. Não houve uma comparação, sob condições idênticas, entre a série bruta e essa série ajustada. Assim, não se quantificou um ganho causal isolado do Fator de Ajuste. A coincidência da base declarada com a de outro estudo tampouco demonstra identidade de transformação, partição ou orçamento de otimização.','Ausência de ablação bruto/ajustado e cadeia de transformação não recuperada. Retira contraste categórico com procedimento de Lampugnani sem comprovação equivalente de execução.'),
497:('R08',base_text(497).replace('elevada estabilidade','baixa dispersão dos erros entre configurações'),'Conclusão: mesma delimitação descritiva da Onda 5, sem inferir estabilidade entre sementes.'),
499:('R07/R08','H2 recebeu apoio para o custo de ajuste do modelo selecionado, sem estender essa conclusão ao custo total da busca; H3 teve apoio pontual nos melhores erros observados. H4 não foi demonstrada: a integração dos mecanismos não foi acompanhada de medida de diversidade nem de ablação. H5 teve apenas evidência descritiva de baixa dispersão entre configurações, sem demonstrar menor variabilidade entre repetições ou superioridade de erro. Esses limites separam funcionamento do software, observação de resultados e efeitos não testados.','Parecer R07/R08; hipóteses H4/H5 originais preservadas em P0184–P0185, sem reformulá-las retrospectivamente para coincidir com o resultado.'),
273:('F15/F16','Fonte: Elaborado pelo autor (2026), a partir da recodificação do portfólio. D: evidência direta; S: tratamento secundário/contextual; ?: informação insuficiente; —: não aplicável.','Legenda dos quatro estados imediatamente abaixo da Tabela 1, sem depender da legenda do Quadro 1 em outra página.'),
47:('F15/F16','Figura 1 – Documentação localizada nas cinco dimensões analíticas35','Título da lista de figuras harmonizado a P0279; tabulação preservada. Número de página será atualizado na etapa final.'),
263:('F13/F16','A literatura examinada apresenta aplicações de ESNs em problemas financeiros e comparações com LSTM ou GRU, como em Sun (2021), Kumar (2025) e Hassaan et al. (2025). Os resultados dependem dos dados, configurações, métricas e comparadores de cada estudo. Essas aplicações fundamentam a avaliação da ESN no protocolo desta pesquisa, incluindo seu custo de ajuste, sem demonstrar que uma arquitetura seja universalmente mais eficiente ou que o custo das redes profundas seja sempre proibitivo.','Sun PDF 6–8; Kumar PDF 16–17; Hassaan PDF 11–13. Limites das métricas e condições preservados.'),
267:('F16/R13','Araújo et al. (2024) e a monografia correlata de Lampugnani (2026) são referências próximas para situar a investigação de distribuições e otimização em ESNs. O recorte desta pesquisa é a avaliação da PETR4 no protocolo documentado e a organização dos experimentos na infraestrutura ESNAUTO. A motivação não depende de quantificar uma escassez de estudos que a coleção reconstruída não permite estimar. A descrição do tratamento dos eventos corporativos segue a procedência dos dados, com seus limites explicitados.','Araújo PDF 7–11; Lampugnani permanece referência correlata fora do corpus34. Retira lacunas quantitativas não sustentadas, sem certificar comparação integral com a monografia externa.'),
268:('F16/R03/R13','A pesquisa utiliza a série da PETR4 disponibilizada como ajustada por eventos corporativos, seleciona cinco hiperparâmetros por AG e compara configurações probabilísticas aplicadas a Win e W. O ESNAUTO integra inicialização populacional por LHS, operador antiestagnação inspirado no CHC e organização de 45 execuções em cinco ondas. Essa aplicação e sua documentação compõem a contribuição experimental e de software, sem atribuir ganho causal isolado ao Fator de Ajuste ou declarar a transformação dos arquivos como etapa executada nesta pesquisa.','Scripts/diebold_mariano/01_prepare_data.R importa série com factor; acervo histórico de 45 execuções. Cadeia original da transformação não recuperada; reconhecimento metodológico não substitui quadro de atribuição de código ainda pendente.'),
271:('F15/F16','Lampugnani (2026) é discutido separadamente e não integra os 34 documentos da matriz. As dimensões são: P1 lei probabilística ligada à geração de Win ou W; P2 procedimento de seleção de hiperparâmetros de ESN/RC; P3 preparação concreta de séries temporais, incluindo transformações e construção de atributos ou janelas; P4 comparação quantitativa de previsão com LSTM, GRU ou Transformer; e P5 mercado e ativo identificados. A codificação distingue aplicações próprias de tratamentos secundários e registra informação insuficiente, sem pressupor que todos os temas sejam aplicáveis a cada fonte.','criterios_matriz_p1_p5.md e matriz_recodificada.json: cinco objetos uniformes, 34 documentos, 170 células; Transformer não é chamado de recorrente.'),
274:('F15/F16','O Quadro 1 apresenta a codificação por documento: D indica evidência direta localizada na aplicação da própria fonte; S indica tratamento secundário ou contextual; ? indica informação insuficiente no escopo consultado; e — indica dimensão não aplicável ao objeto estudado. A marca ? não demonstra que o assunto inexista na obra. A presença de uma informação também não representa reprodução independente, aprovação da qualidade do estudo ou equivalência entre os protocolos comparados.','Definições operacionais e evidência por célula em criterios_matriz_p1_p5.md e matriz_recodificada.json; não confundir recodificação com validação integral das fontes.'),
276:('F15/F16','Fonte: Elaborado pelo autor (2026). D: evidência direta; S: tratamento secundário/contextual; ?: informação insuficiente; —: não aplicável.','Legenda do Quadro 1, compatível com as 170 células recodificadas.'),
277:('F15/F16','A distinção entre D e S evita somar uma revisão e o experimento por ela descrito como duas execuções independentes. Os códigos ? e — também têm sentidos diferentes: o primeiro conserva uma incerteza de leitura ou de especificação; o segundo delimita o objeto da fonte. Assim, as frequências desta coleção descrevem a documentação localizada segundo os critérios adotados, sem estimar a prevalência de métodos em toda a literatura nem comprovar, isoladamente, uma lacuna científica.','Interpretação dos quatro estados, sem as antigas contagens de oito estudos completos ou 30/34 aplicações financeiras indiferenciadas.'),
278:('F15/F16/F18','A caracterização da coleção é complementada pelas Figuras 1 a 4. A cobertura temática utiliza a codificação do Quadro 1, enquanto as demais representações utilizam metadados reconstruídos dos documentos. Esses materiais descrevem o acervo recuperado e não substituem exportações bibliográficas originais ou registros de seleção. O procedimento e seus limites de procedência são apresentados na Seção 3.8.3.','Matriz recodificada e base_reconstruida.json; separa codificação temática de metadados bibliométricos e de exportação original ausente.'),
279:('F15/F16','Figura 1 – Documentação localizada nas cinco dimensões analíticas','Legenda harmonizada ao gráfico de quatro estados e ao Quadro 1.'),
282:('F15/F16','Nota: P1: distribuição de Win/W; P2: seleção de hiperparâmetros ESN/RC; P3: preparação das séries; P4: comparação com LSTM/GRU/Transformer; P5: mercado e ativo. Cada barra distribui os 34 documentos entre D, S, ? e não aplicável, conforme a legenda do Quadro 1. Informação insuficiente não é prova de ausência.','Gráfico deriva das 170 células; cada dimensão conserva denominador 34 e a separação de tipos de evidência.'),
283:('F15/F16','A Figura 1 registra evidência direta de preparação de séries em 25 documentos e de mercado/ativo em 25; comparações com LSTM, GRU ou Transformer e seleção de hiperparâmetros aparecem diretamente em dez documentos cada. A distribuição de Win/W tem cinco registros diretos segundo o critério de identificação da matriz e de sua lei. Tratamentos secundários, informação insuficiente e itens não aplicáveis são exibidos separadamente. Esses números não demonstram que apenas essas fontes tratem dos temas nem que as escolhas documentadas sejam superiores.','Contagens D por P1–P5: 5,10,25,10,25; S: 0,4,2,2,3; ?:13,5,7,16,2; não aplicável:16,15,0,6,4. Validar concordância em cada construção.'),
214:('F14','Ribeiro et al. (2021) combinaram o modelo autorregressivo heterogêneo (Heterogeneous Autoregressive – HAR), PSO e ESN no HAR-PSO-ESN. O estudo previu volatilidades realizadas diárias de CAT, EBAY e MSFT, construídas a partir de retornos intradiários de cinco minutos. Foram avaliados horizontes de um, cinco e 21 dias, com ARIMA, HAR, MLP e variantes ESN como comparadores. Esses experimentos oferecem uma aplicação financeira da combinação, sem demonstrar vantagem universal nem transformar volatilidade observada em comprovação de caos.','Ribeiro PDF 6–8, seções 4.1–4.4 e Tabelas 3–5; a volatilidade prevista é diária, embora derivada de retornos intradiários.'),
239:('F04/F05/F16','Os estudos consultados descrevem diferentes objetos de inicialização. Ribeiro et al. (2021) informam distribuição Uniforme para pesos de entrada, recorrentes e de realimentação. Hariharan et al. (2025) especificam Uniforme(-1,1) para as entradas não nulas de Win, enquanto Wang et al. (2021) distinguem a geração de Win da topologia de W. Identificar a matriz é necessário à comparação: conectividade e reescalonamento espectral, isoladamente, não especificam a distribuição probabilística de seus elementos.','Ribeiro PDF 4, seção 3.2.4; Hariharan PDF 4; Wang W. PDF 7. Retira contagem de cinco não sustentada e separa matrizes.'),
240:('F04/F14','Hassaan et al. (2025) estudaram sequências caóticas normalizadas para gerar Win e Wres e adotaram controles He e Xavier. Nas Equações 9a e 9b, He usa amostras Gaussianas e Xavier usa amostras Uniformes reescaladas. A descrição de Xavier no texto da seção seguinte não coincide com essa fórmula, o que exige cautela na interpretação. Além disso, uma regra de geração por trajetória caótica não equivale, por si só, à identificação de uma família probabilística ajustada aos dados financeiros.','Hassaan PDF 7, equações 9a–9b; PDF 8, seção 3.3, descreve Xavier como similar à Gaussiana; PDF 12, Algoritmo 1.'),
241:('F04/F05/F16','Araújo et al. (2024) compararam ESNs associadas a cinco famílias: Normal, Uniforme, t de Student, GED e t assimétrica. Essa fonte é pertinente à investigação de distribuições, embora a descrição consultada não individualize completamente sua aplicação em Win e W. Sharma (2025), por outro lado, apresenta Uniforme e Log Uniforme como distribuições de amostragem de hiperparâmetros na busca TPE. Essas informações não devem ser reunidas como se descrevessem, com o mesmo grau de detalhe, a geração dos pesos de entrada.','Araújo PDF 7–11; Sharma PDF 7–8, Tabela 1 e Hyperparameter Selection. Informação pertinente não implica descrição inequívoca de cada matriz.'),
509:('F20','BEHERA, S.; NAYAK, S. C.; KUMAR, A. V. S. P. A Comprehensive Survey on Higher Order Neural Networks and Evolutionary Optimization Learning Algorithms in Financial Time Series Forecasting. Archives of Computational Methods in Engineering, v. 30, p. 4401-4448, 2023. DOI: 10.1007/s11831-023-09942-9.','Behera PDF 1: Sudersan Behera; Sarat Chandra Nayak; A. V. S. Pavan Kumar.'),
152:('F18/R01','3.8.3Procedimento de revisão bibliográfica49','Harmonização do título do sumário com P0364; tabs e estilo preservados. Número de página ainda depende da atualização final.'),
248:('F18/R01','Esta seção discute trabalhos relacionados a ESNs, otimização, inicialização probabilística e aplicações financeiras, a partir dos documentos recuperados no acervo da pesquisa. A organização permite situar as escolhas metodológicas deste estudo, sem apresentar a coleção disponível como cobertura exaustiva da literatura. A procedência da seleção e os limites da reconstrução bibliográfica são descritos na Seção 3.8.3.','Parecer F18; limites dos registros de busca e seleção. Harmonização com P0365–P0369; remove afirmação não demonstrada de revisão sistemática reproduzível.'),
364:('F18/R01','Procedimento de revisão bibliográfica','Título harmonizado ao alcance verificável da revisão e da reconstrução; não muda numeração hierárquica.'),
369:('F18/R01','Referências anteriores a 2021 e trabalhos de outros domínios foram utilizados como apoio conceitual, metodológico ou histórico. A coleção descritiva de 34 documentos, apresentada na Tabela 1, no Quadro 1 e nas Figuras 1 a 4, reúne essas fontes com estudos financeiros recentes. Seu tamanho corresponde ao material recuperado para análise, sem representar a quantidade de estudos que teria atendido a todos os critérios da busca originalmente relatada.','Conferência do escopo da coleção LIT-34; não há lista original que permita separar com segurança elegíveis e complementares para recuperar as etapas da seleção.'),
227:('F12','Soltani et al. (2022), na versão preliminar consultada, revisaram 74 estudos sobre otimização de ESNs. A Tabela 5 relaciona PSO a 16 trabalhos e AG a dez, além de outras técnicas bio-inspiradas e não bio-inspiradas. Essas frequências descrevem o emprego dos métodos na coleção dos autores; não constituem uma classificação de eficácia. A revisão discute custos, parâmetros e topologias, sem sustentar uma lacuna específica sobre distribuições de inicialização em aplicações financeiras.','Soltani preprint v1, PDF 1, 6, 8 e 13, DOI 10.21203/rs.3.rs-1909702/v1; distingue versão local de publicação final não examinada.'),
236:('F12/F16','Dewick (2022) discute a modelagem de distribuições financeiras e sua relação com séries temporais. Essa discussão pertence à representação estatística dos dados, enquanto Soltani et al. (2022) examinam estratégias de otimização de ESNs. As duas frentes oferecem contexto para esta pesquisa, mas não demonstram, em conjunto, que uma distribuição de pesos deva reproduzir a distribuição dos retornos. A comparação entre inicializações é uma escolha experimental do presente trabalho.','Dewick PDF 1–3, escopo e distribuições financeiras; Soltani PDF 4 e 13, questões e discussão de otimização.'),
265:('F12/F16','A literatura examinada apresenta diferentes estratégias de seleção de hiperparâmetros: AG em Deng et al. (2022), SSA em Tian (2024) e otimização Bayesiana em Sharma (2025). Soltani et al. (2022) também registram diversidade de técnicas em sua revisão. Esse conjunto fundamenta investigar a busca de configurações, mas não estabelece consenso sobre um otimizador universalmente superior nem garante a eliminação de mínimos locais ou de instabilidades em toda ESN.','Deng PDF 10; Tian PDF 4–6; Sharma PDF 7–8; Soltani PDF 8 e 13. Evitar confundir frequência de uso, eficácia e garantia de convergência.'),
266:('F12/F16','A questão desta pesquisa é examinar o desempenho de configurações de ESN que combinam distribuições de inicialização e hiperparâmetros na previsão da PETR4 ajustada. Trabalhos próximos, como Araújo et al. (2024), já investigaram distribuições alternativas em séries financeiras. A motivação reside na aplicação e na avaliação documentada dessas configurações no protocolo adotado, sem pressupor que o tema esteja ausente da literatura ou que a comparação isole causalmente o efeito da distribuição.','Araújo PDF 3, 7–9; limites dos protocolos PETR4-HIST e PETR4-DM. Remove alegação de maioria/lacuna atribuída indevidamente a Millea e Soltani.'),
545:('F12','SOLTANI, R.; BENMOHAMED, E.; LTIFI, H. Echo State Network Optimization: A Systematic Literature Review. Research Square, versão 1, 4 ago. 2022. Preprint. DOI: 10.21203/rs.3.rs-1909702/v1.','Folha de rosto do PDF local: Posted Date August 4th 2022 e DOI da versão 1; substitui referência final de 2023 não consultada.'),
213:('F14','Wang et al. (2021) avaliaram modelos de RC em sete índices internacionais e compararam suas previsões com RNRs, LSTM e modelos de outros estudos. O desempenho relativo variou conforme o índice e a métrica, sem domínio de uma arquitetura em todas as condições. Os autores exploraram topologias aleatórias, livres de escala e de pequeno mundo, juntamente com diferentes tamanhos de reservatório, janelas e taxas de aprendizado. Essa análise motiva examinar configurações de reservatório, sem isolar a topologia como causa preponderante do ganho preditivo.','Wang W. PDF 7 e 11, seções 4.3 e 5 e Tabela 8. Os totais de vitórias diferem entre essas seções; a redação não escolhe um total contraditório.'),
218:('F14','Hariharan et al. (2025) propuseram ESNs com reservatórios divididos em grupos para séries multivariadas, incluindo dados do NIFTYBEES. Cada variável foi direcionada a um grupo, mantendo conexões entre grupos segundo a topologia examinada. Os erros e a sensibilidade à conectividade variaram entre as estruturas. O estudo apoia investigar a organização do reservatório, sem demonstrar que todo intercâmbio entre variáveis seja prejudicial ou que uma topologia domine em qualquer tarefa.','Hariharan PDF 4, 6–7 e 11–12: Win por grupo, conexões intergrupos e sensibilidade com 50 realizações.'),
224:('F14','Tian (2024) empregou o Sparrow Search Algorithm (SSA) para otimizar uma ESN na previsão de dez ações dos Estados Unidos e dez da China. O estudo comparou SSA-ESN com ESN, LSTM e redes BP e Elman, reportando menores erros para o modelo proposto nas condições examinadas. ESN e SSA-ESN utilizaram as mesmas matrizes Win e W. Essa evidência motiva a seleção de hiperparâmetros, mas não garante evitar mínimos locais nem demonstra significância estatística apenas pela comparação de RMSE e MAPE.','Tian PDF 5–7, seções 3.3, 4 e 5, Tabelas 3–5; a fonte reporta comparação de erros, não prova universal de otimização.'),
225:('F14','Deng et al. (2022) aplicaram AG à seleção do escalonamento de entrada, raio espectral e taxa de vazamento de ESNs empilhadas para prever degradação de células de combustível de membrana de troca de prótons (Proton Exchange Membrane Fuel Cells – PEMFCs). A Tabela 6 compara os erros obtidos com valores de LSTM e outros métodos provenientes de um estudo anterior. Os resultados apoiam a estratégia nessa aplicação, sem estabelecer superioridade geral frente a LSTM nem identificar uma fragilidade principal de toda a literatura de ESNs.','Deng PDF 10, seção 3.2, e PDF 20, Tabela 6: comparadores LSTM, ARIMA e Fusion marcados [36].'),
226:('F14','Ecer (2020) comparou Perceptrons Multicamadas (MLP) ajustados por AG e PSO para o índice BIST 100, examinando funções de saída e tamanhos de população. O modelo estudado não é uma ESN, e os resultados não garantem estabilidade de qualquer rede. Behera (2023) revisou redes de ordem superior e otimização evolucionária em séries financeiras. Essa revisão amplia o contexto das combinações entre redes e otimizadores, sem estabelecer um consenso de superioridade universal de AG ou PSO.','Ecer PDF 1 e métodos/resultados; Behera PDF 3 e Tabela 2, PDF 30: domínio HONN e técnicas evolucionárias.'),
230:('F11/F16','A inicialização dos pesos participa da construção da dinâmica de uma ESN e deve ser descrita de forma que permita examinar a configuração utilizada. Millea (2014) investigou matrizes aleatórias e ortonormais em problemas de osciladores sobrepostos. Esse trabalho oferece evidência sobre condições específicas de inicialização, sem quantificar a proporção de estudos financeiros que adotam cada distribuição. A frequência dessas escolhas no portfólio depende de critérios explícitos de extração.','Millea seção 3.3, PDF 28–31; não extrapolar experimento não financeiro para frequência em toda a literatura.'),
231:('F22','A ocorrência de caudas pesadas em retornos financeiros motiva o exame de distribuições além da Normal (Nelson, 1991). Entretanto, a distribuição dos retornos observados e a lei usada para gerar pesos de uma ESN são objetos distintos. A adoção de distribuições alternativas nos pesos constitui uma hipótese de modelagem desta pesquisa; sua pertinência deve ser avaliada pelos resultados preditivos e não decorre automaticamente da semelhança entre suas caudas e as dos dados.','Nelson PDF 7–8, páginas impressas 352–353; fonte trata inovações/modelo de volatilidade, não pesos ESN.'),
232:('F22','Nelson (1991) empregou a Distribuição Generalizada de Erro (Generalized Error Distribution – GED) na modelagem de retornos com heterocedasticidade condicional, no contexto do modelo exponencial autorregressivo de heterocedasticidade condicional generalizada (Exponential Generalized Autoregressive Conditional Heteroskedasticity – EGARCH). A família permite representar caudas mais pesadas ou mais leves que as da Normal. Essa aplicação fundamenta sua flexibilidade em finanças, sem estabelecer prioridade histórica absoluta nem validar sua transferência para os pesos de ESNs.','Nelson PDF 7–8, impressas 352–353; PDF 7 atribui a família também a Harvey (1981) e Box e Tiao (1973).'),
234:('F23','Duttilo e Gattone (2022) ajustaram misturas de duas GED a retornos diários do DJIA entre 2016 e 2022 e compararam-nas com misturas Gaussianas e Gaussiana-Laplace. A preferência pelo modelo GED foi avaliada por razões de verossimilhança e critérios de informação: de Akaike (Akaike Information Criterion – AIC), bayesiano (Bayesian Information Criterion – BIC) e de Hannan–Quinn (Hannan–Quinn Information Criterion – HQIC). Esses critérios comparam modelos ajustados; não constituem, isoladamente, testes de normalidade.','Duttilo e Gattone 2022, PDF 4–5, seção 3 e Tabela 1; não atribuir aplicação da conferência à tese de 2023.'),
365:('F18/R01','A revisão bibliográfica utiliza uma coleção de 34 documentos disponíveis no acervo da pesquisa, reconstruída para permitir a conferência das fontes. A documentação anterior menciona buscas em Scopus e Springer Nature Link em 23 de março de 2026, com 41 e 59 registros, respectivamente. Sem as exportações e planilhas originais, esses números permanecem como relato do processo anterior, e não como contagens independentemente verificadas. A síntese apresentada tem caráter descritivo do material recuperado.','Parecer F18; reports/bibliometria_reconstrucao/base_reconstruida.json; ausência dos registros originais não autoriza negar execução histórica.'),
366:('F18/R01','A documentação anterior descreve uma busca voltada a revisões de ESNs e Computação de Reservatório em finanças, com preferência por textos completos em inglês ou português publicados entre 2021 e 2026. O conjunto recuperado também inclui estudos anteriores, fundamentos teóricos e aplicações de outros domínios. Portanto, esses critérios não caracterizam de modo uniforme os 34 documentos utilizados, e não se apresenta a coleção reconstruída como resultado integralmente reproduzível de uma revisão sistemática.','Coleção LIT-34 contém Nelson 1991, Millea 2014, Timbó 2016, Ecer 2020 e Deng PEMFC; confronto com critérios originais P0366–P0367.'),
367:('F18/R01','O Methodi Ordinatio (Pagani; Kovaleski; Resende, 2015) foi indicado na documentação anterior como referência para organizar a seleção. Contudo, não foram recuperados os valores individuais dos indicadores, as datas de coleta de citações ou a planilha de pontuação que permitiriam recalcular a ordenação. Assim, a análise atual não utiliza uma pontuação InOrdinatio como evidência verificada de seleção ou relevância dos 34 documentos. A reconstrução bibliográfica preserva essa limitação de procedência.','Parecer F18 e fontes.json; a fórmula com citações/100 do original não foi validada e foi retirada, sem fabricar ranking substituto.'),
505:('F20','ABEBE, T. N.; GOSHU, A. T. Asymmetric generalized error distribution with its properties and applications. Frontiers in Applied Mathematics and Statistics, v. 10, art. 1398137, 2024. DOI: 10.3389/fams.2024.1398137.','Abebe PDF 1: Tayu Nigusie Abebe e Ayele Taye Goshu.'),
181:('F24','H1 - desempenho: a ESN otimizada apresentará menor perda preditiva que os modelos LSTM e GRU definidos no protocolo. A comparação histórica será descritiva; na rodada controlada complementar, a avaliação considerará a diferença de acurácia pelo teste bilateral de Diebold-Mariano e a direção do diferencial médio de perda. A ausência de significância será interpretada como evidência insuficiente de diferença, sem demonstrar equivalência entre os modelos.','Esclarecimento editorial autorizado; documentação primária forecast::dm.test, hipótese nula e alternativa bilateral; não representa pré-registro retrospectivo.'),
193:('F25','Modelos lineares, como o autorregressivo integrado de médias móveis (Autoregressive Integrated Moving Average – ARIMA) e a regressão linear, podem apresentar limitações na representação de dependências não lineares e mudanças de regime. Isso não impede seu emprego como modelos de referência. A diferenciação em ARIMA permite tratar determinadas formas de não estacionariedade, e a adequação de cada abordagem deve ser avaliada para a série e a tarefa consideradas.','Ribeiro PDF 3; Kumar PDF 4 e 9–10; Timbó métodos.'),
194:('F06','Timbó et al. (2016) aplicaram regressão linear à previsão do fechamento da PETR4 e selecionaram indicadores com apoio da correlação de Pearson. O estudo avaliou o acerto das previsões por uma tolerância absoluta de 0,50 em relação ao fechamento observado. Esse critério mede proximidade de preços e não deve ser interpretado como taxa de acerto da direção da variação do ativo.','Timbó PDF 5 e 7–8; leitura dos critérios e da discussão.'),
195:('F01/F07','Costa e Lunkes (2025) combinaram indicadores técnicos e fundamentalistas em um modelo de classificação com máquina de vetores de suporte (Support Vector Machine – SVM). O modelo híbrido apresentou F1-score de aproximadamente 72,7% na amostra de ações brasileiras analisada, sem atribuição desse valor especificamente à PETR4. Os autores recomendaram investigar outros algoritmos, incluindo redes neurais e métodos de conjunto; a escolha de arquiteturas recorrentes constitui uma decisão da presente pesquisa.','Costa/Lunkes PDF 12, 15, 17 e 19.'),
196:('F02','Liu H. (2025) integrou indicadores técnicos, modelos temporais e análise de sentimentos com modelos de linguagem de grande escala (Large Language Models – LLMs), incluindo FinBERT e GPT-2, em estratégias associadas ao índice Standard and Poor’s (S&P) 500. O FinBERT atingiu 75,56% de acurácia na classificação de sentimento das notícias da Benzinga. Esse resultado pertence à tarefa de Processamento de Linguagem Natural (Natural Language Processing – NLP) e não representa acerto da direção do índice.','Liu H. PDF 1, 21 e 28; Tabela 1 distinta da Tabela 2.'),
211:('F13','O reservatório transforma a sequência de entrada em estados dos quais a camada de saída extrai informação preditiva. O ajuste apenas dessa camada reduz o conjunto de pesos treináveis em comparação com o treinamento de toda a rede. Essa organização pode reduzir o custo de ajuste, mas não garante estabilidade numérica nem uma razão universal de tempos frente à retropropagação através do tempo. O condicionamento da regressão, a dinâmica do reservatório e a regularização continuam relevantes (Jaeger, 2007).','Jaeger PDF 1–5; readout, regularização e dinâmica.'),
212:('F08','Sun (2021) comparou uma ESN com uma LSTM simplificada na previsão do fechamento das ações da Kweichow Moutai e reportou menores erros nas configurações examinadas. A fonte lista fechamento e fechamento ajustado como campos distintos, mas descreve os experimentos com preços de fechamento. Por isso, esse estudo não é tomado aqui como comprovação inequívoca de uso do fechamento ajustado nem como demonstração de superioridade sobre qualquer configuração LSTM.','Sun PDF 5–6 e 8–9; comparação e colunas da base.'),
216:('F10','Liu (2022) investigou um sistema de Computação de Reservatório nanofotônico para índices de mercados chineses, norte-americano e britânico. Os autores observaram previsões conservadoras, mas também maiores erros nos pontos de flutuação intensa, discutidos como efeito de ancoragem nos dados históricos. Os resultados caracterizam as condições do sistema estudado e não demonstram imunidade a mudanças de regime nem superioridade geral sobre implementações de software em tempo real.','Liu B. PDF 6–8, 10 e 14.'),
219:('F09/F14','Hassaan et al. (2025) compararam ESN e GRU com inicializações caóticas e controles Xavier e He em seis conjuntos financeiros. Seddik (2023), por sua vez, investigou uma ESN em trajetórias simuladas pelo sistema de Lorenz, com condições iniciais associadas a valores de Bitcoin. As métricas desse segundo estudo avaliam as trajetórias geradas, não previsões fora da amostra de uma série observada de preços. Seus resultados não isolam o efeito da distribuição dos pesos iniciais da ESN.','Hassaan PDF 1, 7–8 e 12–13; Seddik PDF 4–7.'),
220:('F03','Sharma (2025) avaliou ESNs para preços de Bitcoin, com XGBoost e previsão pelo último valor como comparadores. A análise relacionou o erro preditivo ao grau de caos estimado por expoentes de Lyapunov. Os testes de Mann–Whitney discutidos no estudo compararam ESN e XGBoost em condições específicas de caos e tamanho de janela; esse resultado não demonstra superioridade estatística geral da ESN sobre ARIMA ou sobre todos os períodos.','Sharma PDF 8–12; contrastes e condições.'),
223:('F11','Millea (2014) investigou matrizes ortonormais e matrizes aleatórias reescaladas em ESNs aplicadas ao problema de múltiplos osciladores sobrepostos. Os experimentos mostraram que conectividade, tamanho da rede e inicialização alteram o espaço de soluções. A significância das diferenças dependeu do limiar de erro avaliado. Esses resultados motivam documentar a inicialização, sem demonstrar uma vantagem universal das matrizes ortonormais em séries financeiras.','Millea seção 3.3, PDF 28–31: localizadores corrigidos em relação ao parecer preliminar.'),
245:('F08','O uso de séries ajustadas também aparece fora do mercado brasileiro. Cortesi et al. (2026) descrevem dados do Center for Research in Security Prices (CRSP) com fatores de ajuste para eventos corporativos na análise de ações do S&P 500. Essa procedência documentada permite discutir a preparação dos dados sem inferir o uso de fechamento ajustado apenas da existência dessa coluna em uma base.','Cortesi PDF 16–18; Sun PDF 5–6.'),
246:('F07/F17','Costa e Lunkes (2025) informam o uso de preços ajustados a desdobramentos e dividendos na construção de indicadores e da variável de classificação. O tratamento de eventos corporativos é relevante quando suas descontinuidades afetam a variável e a tarefa investigadas. A necessidade e a forma do ajuste dependem do objeto da modelagem; seu emprego, isoladamente, não garante resultados confiáveis para qualquer modelo.','Costa/Lunkes PDF 12; limites de inferência explicitados.'),
260:('F03/F04','Sharma (2025) empregou otimização Bayesiana via Tree Parzen Estimator (TPE) na seleção de hiperparâmetros da ESN. A Tabela 1 do estudo apresenta as distribuições de amostragem dos hiperparâmetros, que não equivalem à lei de geração dos elementos de Win ou W. A avaliação usou janelas de treino de 15, 30 e 60 observações, teste de dez pontos e avanço de um ponto. Assim, esses tamanhos de treino não representam horizontes de previsão de 15, 30 e 60 dias.','Sharma PDF 7–8, Tabela 1 e seção 5.'),
252:('R05/R13','Araújo et al. (2024) investigaram ESNs com Algoritmos Genéticos e diferentes distribuições probabilísticas em séries da B3. Essa combinação constitui uma referência metodológica próxima desta pesquisa. O ESNAUTO organiza a investigação da PETR4 ajustada em cinco ondas e integra LHS e um operador antiestagnação inspirado no CHC. A infraestrutura dispõe de mecanismos de preservação de matrizes, mas o acervo histórico não contém as matrizes e previsões de todas as execuções, conforme a Seção 3.8.','Araújo PDF 4–9; docs/10_diebold_mariano_tfc.md, seção 2.'),
264:('F13','O ajuste da camada de saída, mantendo fixos os pesos do reservatório, distingue a ESN das arquiteturas treinadas integralmente por BPTT (Jaeger, 2007). Essa diferença pode reduzir o custo de ajuste, mas não elimina problemas de condicionamento numérico ou de dinâmica do reservatório. Os desafios computacionais discutidos por Vishwas et al. (2025) motivam comparar custos sob condições explícitas, distinguindo treinamento do modelo e busca de hiperparâmetros.','Jaeger PDF 3–5; Vishwas discussão de custo e escalabilidade.'),
314:('R04','A série foi organizada em blocos cronológicos, sem embaralhar as datas entre treino, validação e teste. Essa organização é necessária à avaliação temporal, mas não demonstra, isoladamente, ausência de vazamento de informação. Na rodada controlada complementar, a fronteira dos alvos de treino e a propagação contínua dos estados foram verificadas explicitamente; nos resultados históricos, a identificação do comportamento de cada execução depende dos artefatos preservados.','Scripts/diebold_mariano/02_esn_controlled.R, targets e frozen; docs/10_diebold_mariano_tfc.md.'),
315:('R06','A divisão estática 50%/25%/25% reuniu 2.600 observações de treino, de 03/01/2000 a 01/07/2010; 1.299 de validação, de 02/07/2010 a 28/09/2015; e 1.299 de teste, de 29/09/2015 a 30/12/2020. A função de aptidão da busca combinou erros de treino e validação. Os recordes de erro de teste apresentados nos resultados constituem comparações descritivas posteriores e não equivalem a uma seleção prospectiva de configuração para uma nova amostra.','Partições descritas no manifesto controlado; protocolo do fitness e distinção de recordes de teste do parecer.'),
330:('R04/F13','Em cada variante, Win e W foram geradas conforme a combinação probabilística da onda, e W foi reescalonada por sr/|λmax(W)|, em que λmax representa o autovalor de maior módulo. Esse procedimento controla o raio espectral, sem constituir garantia geral da propriedade de estado de eco. Durante o ajuste de cada ESN, Win e W permaneceram fixas, e Wout foi estimada por regressão Ridge. As comparações avaliam configurações que combinam inicialização, hiperparâmetros e realização estocástica, sem isolar causalmente a distribuição.','Jaeger PDF 3–5; comparação das configurações e executor controlado.'),
337:('R05/R13','A função de aptidão combinou erros de treino e validação: fitness = −(0,4 · MAEtreino + 0,6 · MAEvalidação). O sinal negativo converteu a minimização em maximização para o pacote GA. A ponderação atribuiu maior peso à validação e segue a combinação descrita por Araújo et al. (2024). O software dispõe de serialização dos pesos e hiperparâmetros associados a recordes; contudo, esse mecanismo não resultou na preservação integral de todas as saídas históricas.','Araújo PDF 7; docs/10_diebold_mariano_tfc.md seção 2; capacidade versus acervo efetivo.'),
338:('R05','As combinações de Win e W foram exploradas no mesmo espaço de hiperparâmetros. A reinjeção de uma configuração depende da disponibilidade de suas matrizes e parâmetros. Como não foram recuperados todos os artefatos históricos, a reprodução exata de cada execução não é garantida. Os resultados representam realizações documentadas de reservatórios estocásticos, sem estimar uma distribuição completa de desempenho para cada configuração.','Limites de preservação em docs/10_diebold_mariano_tfc.md; registros do parecer.'),
368:('F18/R01','A documentação da pesquisa menciona as planilhas methodi_ordinatio.xlsx e extracao_completa.xlsx como registros intermediários de seleção e extração bibliográfica. Esses arquivos não foram localizados no acervo examinado, o que limita a auditoria retrospectiva do processo. A coleção reconstruída a partir dos documentos disponíveis apoia a síntese descritiva, mas não substitui os registros originais de busca, triagem e ordenação.','Busca local por nomes de arquivos e fontes.json; indisponibilidade não implica inexistência histórica.'),
}
edits.update({
197:('F14','Xiao (2024) comparou LSTM, GRU e Transformer na previsão de preços da Tesla, sem investigar arquiteturas de reservatório. O artigo descreve preparação dos dados, mas sua Tabela 2 registra ausência de valores faltantes; esse relato não comprova uma avaliação de imputação. A diversidade de propostas com SVM, Aprendizado Profundo e processamento de linguagem natural contextualiza a escolha das ESNs nesta pesquisa, cuja eficiência deve ser examinada no protocolo adotado.','Xiao, PDF4, seção3.1 e Tabela2 (Missing Values: None); PDF5, Tabela3. Retirada atribuição de tratamento multivariado de ausentes como evidência experimental.'),
204:('F14','Xiao (2024) apresenta uma comparação de LSTM, GRU e Transformer para a Tesla. A Tabela 3 contém valores de MSE e RMSE que não são coerentes entre si para todos os modelos, o que limita a interpretação quantitativa desses resultados. O artigo não demonstra, por ablação, o efeito isolado de incorporar informações do mercado. Cortesi et al. (2026) mostram que otimizadores podem produzir erros escalares idênticos de NMSE e funções de previsão distintas; a métrica agregada, isoladamente, não descreve todo o comportamento preditivo.','Xiao PDF5, Tabela3: MSE260,8710984 versus RMSE26,0917386 para LSTM e MSE360,2837729 versus RMSE16,3973472 para Transformer. Cortesi: afirmação sobre NMSE mantida com linguagem delimitada, pendente da conferência global de seus usos.'),
210:('F21/F13','As ESNs integram o paradigma da Computação de Reservatório (Reservoir Computing – RC). Jaeger (2001) apresenta uma abordagem em que a rede recorrente fornece estados e o treinamento ajusta as conexões de saída por regressão. Na configuração usual descrita por Jaeger (2007), os pesos internos são inicializados aleatoriamente e permanecem fixos durante o ajuste da saída. Essa separação entre dinâmica recorrente e leitura fundamenta a arquitetura utilizada nesta pesquisa.','Jaeger2001, versão com errata26/01/2010 disponibilizada pelo autor: PDF4 introdução, PDF12–13 seção3 e preparação aleatória; definição geral apenas, sem reutilizar teorema corrigido de ESP. Jaeger2007 PDF1–3.'),
215:('F14','Wang et al. (2025) avaliaram um sistema óptico de Computação de Reservatório com ponderação de atributos em sete índices acionários, integrando dados de mercado e indicadores macroeconômicos e técnicos. O protocolo inclui modelos de aprendizado de máquina, entre eles LSTM, e seleciona o melhor comparador para cada índice. Os autores relatam ganhos nos horizontes de um, quatro e dez passos. A análise de atraso em trajetórias específicas não demonstra que a ponderação elimine atrasos em qualquer regime de mercado.','WangF PDF2–3: índices e seleção do melhor ML; PDF5 protocolo; PDF8 atraso do melhor ML, não LSTM em todas as condições; PDF12–13 horizontes1/4/10.'),
217:('F14','Zhang et al. (2021) propuseram a CS-ESN, que acrescenta sensoriamento compressivo à representação dos estados do reservatório. Foram examinadas uma sequência logística e séries acionárias, comparando a ESN original à variante com compressão. Os autores relatam menores erros nas configurações estudadas. A redução da representação do reservatório não demonstra uma propriedade geral de preservação de picos ou da estrutura caótica de séries financeiras.','Zhang PDF2: objetivo de reduzir representação do reservatório; PDF6–7 mecanismo; PDF13–14: compressão50% e Tabela3. Retirada confusão entre compressão de estados e custo de amostragem da série.'),
254:('F14','Ribeiro et al. (2021) propuseram o HAR-PSO-ESN para prever volatilidade realizada de três ações da Nasdaq, combinando atributos do modelo HAR, ESN e seleção de hiperparâmetros por PSO. Os pesos de entrada, recorrentes e de realimentação foram inicializados com distribuição Uniforme. O modelo apresentou melhores resultados na maioria dos casos estudados, com comparações por Friedman e Nemenyi. Essa evidência se refere à combinação avaliada, sem estabelecer superioridade universal ou isolar o efeito de leis alternativas de inicialização.','Ribeiro PDF1 resumo: maioria dos casos, HAR-PSO-ESN, Friedman/Nemenyi; PDF4: Uniforme nas três matrizes; PDF11 conclusão. Não reduzir o modelo híbrido à ESN otimizada nem declarar ausência geral de justificativa.'),
267:('F21/R13','Araújo et al. (2025) e Lampugnani (2026) já investigaram distribuições e otimização em ESNs. Cardoso (2025) estudou a combinação ARIMA-ESN com Algoritmo Genético, incluindo ITSA4 e PETR4 e distribuições alternativas de pesos. Naqueles estudos de caso, ARMA-EGARCH apresentou melhor desempenho, ressaltando a dependência entre método, dados e desfecho. A avaliação de volatilidade da tese pertence a outro protocolo e não fornece um comparador numérico para este experimento. A contribuição desta pesquisa é delimitada pela aplicação e organização dos experimentos no ESNAUTO, sem reivindicar a criação da ESN ou da combinação ESN-AG.','Cardoso_tese PDF6, resumo: combinação, ativos, distribuições e resultado desfavorável frente a ARMA-EGARCH nos estudos de caso. Uso substantivo para delimitar contribuição; não transportar métricas/protocolos.'),
306:('R13','Os executores de ESN preservados foram escritos em R, com atualização dos estados e cálculo da saída explicitados no código. Essa implementação utiliza fundamentos descritos por Jaeger (2007); a existência dos arquivos não demonstra autoria integral das rotinas legadas. Foram empregados GA na busca genética; PerformanceAnalytics nas medidas descritivas; fGarch, PearsonDS e StockDistFit nas distribuições; fitdistrplus e MASS no ajuste; pracma na medição de tempo; e ggplot2 na visualização. O Quadro 6 delimita as contribuições e lacunas de procedência.','Código R preservado e dependências dos executores; não converter implementação manual ou nome do arquivo em prova de autoria. Sem execução dos scripts científicos.'),
500:('R13','A contribuição de Engenharia de Software documentada no ESNAUTO reúne preparação de dados, execução de ESN, otimização genética, baselines LSTM/GRU, métricas, histórico, visualização e mecanismos de preservação e reinjeção de configurações. O Quadro 6 distingue fundamentos anteriores, integração experimental e limites de procedência. Essa organização do protocolo não implica autoria original das técnicas combinadas nem comprova a origem de cada rotina legada.','Artefatos existentes, distinção entre integração documentada e criação original dos componentes; quadro de atribuições com lacunas explícitas.'),
531:('F21/F20','JAEGER, H. The “echo state” approach to analysing and training recurrent neural networks – with an Erratum note. GMD Report 148. Sankt Augustin: GMD Forschungszentrum Informationstechnik, 2001. Versão com errata de 26 jan. 2010. DOI: 10.24406/publica-fhg-291111. Disponível em: https://www.ai.rug.nl/minds/uploads/EchoStatesTechRep.pdf. Acesso em: 28 out. 2026.','PDF primário ligado na página de publicações do autor em Groningen,47 páginas; capa distingue relatório2001 e correção2010. Consultadas introdução e preparação/treino, não leitura integral.'),
})
edits.update({
66:('F19','Tabela 7 – Comparação descritiva com Lampugnani (2026)62','Lista: título alinhado à retirada do comparador sem fonte primária; paginação será atualizada na conferência final.'),
457:('F19','Os resultados foram contextualizados pela monografia de Lampugnani (2026), que investigou ESNs com Algoritmo Genético na PETR4 e apresentou erros de teste para diferentes combinações de distribuições. A Tabela 7 reúne os menores erros documentados em cada trabalho. Trata-se de comparação entre estudos, sem execução de ambos sob um protocolo comum.','Lampugnani, tabelas XML 9–12: 24 registros de teste; menores MAE 0,378706 e RMSE 0,568178. Retiradas alegações não verificadas de Cardoso 2022a.'),
459:('F19','Tabela 7 – Comparação descritiva com Lampugnani (2026)','Comparador Cardoso 2022a retirado por falta de conferência primária; não se declara incorreto seu resultado.'),
460:('F19','Fonte: Elaborado pelo autor (2026), com base nas tabelas de resultados de Lampugnani (2026) e nos resultados desta pesquisa. Os mínimos de MAE e RMSE podem corresponder a configurações distintas.','Conferência direta das tabelas XML 9–12 de Lampugnani. Não tratar dois mínimos como uma mesma execução.'),
461:('F19','Os menores MAE e RMSE documentados nesta pesquisa são numericamente inferiores aos mínimos apresentados por Lampugnani (2026). Essa comparação descritiva não demonstra superioridade sob condições equivalentes: não foi executado um contraste conjunto com os mesmos dados de entrada, pesos, sementes e orçamento de otimização. As diferenças entre os estudos não identificam o efeito de um componente isolado.','Mínimos lidos diretamente nas 24 linhas de resultados de Lampugnani; ausência de comparação experimental conjunta.'),
462:('F19/R03','Lampugnani (2026) declara não realizar tratamento adicional dos dados. Essa declaração não comprova que os valores recebidos fossem desprovidos de ajuste corporativo. Nesta pesquisa, os modelos também receberam arquivos identificados como previamente ajustados. Sem a cadeia de preparação de ambas as séries e uma comparação controlada, não se atribui a diferença de erro ao Fator de Ajuste, ao LHS ou ao mecanismo cataclísmico.','Lampugnani P0408; distinção entre não tratar adicionalmente e série não ajustada; cadeias e ablações indisponíveis.'),
477:('F19','Entre as configurações avaliadas, Laplace × Normal apresentou o menor MAE, enquanto Laplace × Cauchy apresentou o menor RMSE e o maior R². Na maior parte das execuções documentadas, as ESNs obtiveram MAE menor que os baselines LSTM e GRU definidos no protocolo. A comparação documental com Lampugnani (2026) contextualizou os erros, sem transformar protocolos distintos em um experimento comum.','Preservadas combinações e ordem dos resultados internos; removida retomada da comparação Cardoso 2022a não verificada.'),
496:('F19/R10','Os quatro testes de Diebold-Mariano rejeitaram a hipótese de igualdade de acurácia preditiva a 5%, sempre com menor perda média para a ESN na rodada controlada. Essa inferência não se estende aos resultados históricos de outras sementes. A comparação com Lampugnani (2026) permaneceu descritiva, sem tratar protocolos distintos como equivalentes.','Preservados quatro contrastes da rodada controlada; retirada a retomada Cardoso 2022a sem original.'),
})
finding,text,evidence=edits[41]
edits[41]=(finding,text.replace('o menor raiz do erro quadrático médio','a menor raiz do erro quadrático médio'),evidence+' Correção de concordância, sem alteração numérica.')
edits[476]=('R11','O valor elevado de R² exige cautela porque o objeto previsto é o preço da ação em nível, com forte persistência temporal. MAE e RMSE descrevem os erros, mas não demonstram, por si sós, vantagem sobre a previsão que repete o último preço observado. Esse comparador não integra os quatro contrastes da rodada controlada com GRU e LSTM. Assim, a evidência apresentada não estabelece ganho sobre a persistência nem utilidade econômica; uma comparação futura com esse referencial deverá usar a mesma janela e escala.','R11: quatro contrastes do manifesto controlado são ESN×GRU/LSTM sob perdas absoluta/quadrática; ausência do contraste de persistência não permite afirmar ganho. Sem executar experimento adicional ou transferir resultados VALE3.')
edits.update({
186:('QA/R12','O texto apresenta revisão da literatura, material e métodos, resultados, discussão das limitações e conclusão. A revisão fundamenta os modelos; a metodologia distingue os blocos experimentais; os capítulos finais avaliam os resultados e seu alcance. Os resultados principais se restringem à PETR4.','Síntese organizacional condensada para evitar uma página quase vazia ao fim da introdução, sem alterar escopo experimental.'),
490:('QA/R10','A extensão à VALE3 permanece como continuidade experimental, fora dos resultados desta monografia. Ela deverá avaliar preparação da série, distribuições, repetições e comparadores sob partições temporalmente auditáveis. Os parâmetros das distribuições deverão ser ajustados ao treino ou ter sua transferência entre ativos explicitada. As execuções exploratórias preservadas são material preliminar.','Condensação do parágrafo de continuidade para evitar página com duas linhas; preserva separação VALE3 e exigência de treino sem repetir experimentos.'),
305:('F14/F18/R01','Quanto aos objetivos, a pesquisa foi exploratória e comparativa: examinou configurações de ESNs que combinam distribuições de inicialização e seleção de hiperparâmetros por AG, com a série recebida como ajustada. Essa classificação descreve o propósito do experimento e não pressupõe que a combinação seja inédita ou pouco estudada. Quanto aos procedimentos, foi experimental, com comparações computacionais sob o protocolo descrito. O alcance das inferências depende dos controles e dos artefatos efetivamente preservados.','Retirada alegação de combinação pouco estudada sem pesquisa exaustiva demonstrada; preservadas classificação e natureza do protocolo, com distinção de procedência.'),
228:('F14/R03/R13','Araújo et al. (2025) investigaram a combinação de AG, ESN e distribuições probabilísticas em séries da B3. Essa combinação é um antecedente metodológico próximo. Nesta pesquisa, o ESNAUTO organiza cinco ondas de configurações para Win e W, integra LHS e um operador antiestagnação inspirado no CHC e recebe a série identificada como previamente ajustada. Essa integração não comprova novidade de cada componente nem isola o efeito causal da distribuição ou do ajuste.','Araújo PDF4–9; harmonização com P0252/P0267 e limites da procedência. Retirada retomada que atribuía aplicação do fator ao autor ou causalidade isolada à inicialização.'),
251:('F17/R03','O ajuste de eventos corporativos pode reduzir descontinuidades que afetam a interpretação dos preços históricos. A presente pesquisa utiliza arquivos cuja procedência é atribuída ao BovDB e que foram disponibilizados como previamente ajustados. Essa condição de entrada não demonstra que o autor tenha executado a transformação, nem permite avaliar seu efeito isolado sobre a previsão sem a cadeia de processamento e a comparação correspondentes.','BovDB PDF7–8 e identificação dos arquivos de entrada. Retirada expressão obrigatória de pré-processamento como ação comprovadamente executada nesta pesquisa.'),
256:('F14','Os resultados de Wang et al. (2021) mostram que modelos de RC podem ser competitivos com LSTM e RNR nas tarefas examinadas. A melhor topologia variou entre os índices. A análise constitui uma referência para comparar configurações de reservatório; ela não identifica uma distribuição de pesos universalmente adequada nem demonstra que a lei dos pesos deva coincidir com a distribuição dos retornos financeiros.','WangW PDF7 e10/Tabela8; resumo derivado delimitado às condições do estudo, sem generalizar desempenho.'),
257:('F14','Tian e Pei (2024) avaliaram uma ESN otimizada por SSA em dez ações dos Estados Unidos e dez da China. O estudo apresenta comparações com ESN, LSTM e redes BP e Elman. Os resultados de erro favorecem o modelo proposto nas condições examinadas, mas não estabelecem uma garantia geral de superioridade nem isolam o efeito de uma família probabilística dos pesos. A geração aleatória das matrizes não deve ser confundida com sua especificação estatística completa.','Tian PDF5–7, seções3.3/4/5 e Tabelas3–5; harmonização com P0224. Removido superlativo consistente geral e inclusão indiscriminada de todas métricas.'),
258:('F14','Hassaan et al. (2025) estudaram inicializações por sequências caóticas para ESN e GRU em seis conjuntos financeiros, incluindo índices acionários e pares cambiais. O protocolo compara sistemas como Lorenz, Chen, oscilador de Chen perturbado e Mackey–Glass, além dos controles He e Xavier. Os resultados pertencem às séries, arquiteturas e condições de avaliação adotadas pelos autores.','Hassaan PDF1/resumo e seção3.1/PDF5–7; seis conjuntos. Removida descrição parcial usada como fundamento de conclusão causal abrangente.'),
259:('F14','Os erros reportados por Hassaan et al. (2025) motivam investigar regras de inicialização. Contudo, diferenças numéricas de erro não constituem, por si sós, evidência de significância estatística ou de efeito independente dos demais componentes. A inicialização por uma trajetória caótica também difere da escolha de uma família probabilística dos pesos. A interpretação dos controles deve observar a divergência entre a fórmula e a descrição textual de Xavier, apresentada na Seção 2.5.','Hassaan equações9a/9b e contexto de validação; cautela já documentada na recodificação. Retirado ganho significativo sem teste identificado e classificação como abordagem ortogonal.'),
261:('F14/R01','O conjunto examinado apresenta aplicações de ESNs, métodos de seleção de hiperparâmetros e regras de inicialização em diferentes tarefas. Ele fundamenta escolhas experimentais desta pesquisa, sem demonstrar cobertura exaustiva do campo. O estudo organiza uma avaliação de distribuições canônicas, de caudas pesadas, assimétricas, esparsas e ajustadas empiricamente para a PETR4. A coleção reconstruída não permite estimar a dimensão de uma lacuna na literatura nem reivindicar ineditismo dessa combinação.','Síntese coerente com coleção descritiva e P0266/P0267; retirada retomada de lacuna não quantificada e conclusão universal.'),
})
finding,text,evidence=edits[197]
edits[197]=(finding,text.replace('Aprendizado Profundo e','Aprendizado Profundo (Deep Learning – DL) e'),evidence+' Preservada a definição de DL no trecho.')
edits[204]=('F14','Na comparação de Xiao (2024), a Tabela 3 contém valores de erro quadrático médio (Mean Squared Error – MSE) e RMSE incoerentes entre si para alguns modelos, limitando sua interpretação. O artigo não demonstra o efeito isolado de incorporar informações de mercado. Cortesi et al. (2026), na previsão de volatilidade de ações do S&P 500, mostram que valores idênticos de erro quadrático médio normalizado (Normalized Mean Squared Error – NMSE) podem corresponder a funções de previsão distintas conforme o otimizador. A métrica agregada, isoladamente, não descreve todo o comportamento preditivo.','Xiao PDF5 Tabela3; Cortesi PDF1 resumo e discussão da volatilidade S&P500. Preservadas definições na primeira ocorrência textual de MSE/NMSE.')
edits[208]=('F14','Behera (2023) revisa redes neurais de ordem superior (Higher Order Neural Networks – HONNs) e otimização evolucionária em previsão financeira. O levantamento examina modelos, seleção de hiperparâmetros e métodos como AG e otimização por enxame de partículas (Particle Swarm Optimization – PSO). Trata-se de síntese de estudos com tarefas e protocolos distintos; os ganhos relatados não constituem uma comparação experimental própria nem demonstram que a associação a uma metaheurística melhore qualquer rede ou série.','Behera PDF1, objetivo declarado de survey e limites das comparações secundárias; seção de métodos evolucionários. Retirada conclusão de aumento substancial geral de precisão; mantida definição inicial de PSO.')
edits[255]=('F14','Wang et al. (2021) avaliaram RC, LSTM e RNR em sete índices acionários, com topologias aleatórias, de pequeno mundo e livres de escala. A distribuição Uniforme foi usada nos pesos de entrada, enquanto a matriz do reservatório foi definida pela conectividade da rede gerada. A camada de saída foi ajustada por um otimizador iterativo, o que distingue esse protocolo da leitura Ridge empregada nesta pesquisa. O desempenho relativo variou entre índices e configurações; não se estabelece uma hierarquia geral das topologias.','WangW PDF7: geração das matrizes e ajuste de Wout por RMSProp; PDF10 Tabela8: melhor topologia depende do índice. Retirado superlativo bibliográfico não demonstrado; distribuição de Win não transferida automaticamente a W.' )
finding,text,evidence=edits[217]
edits[217]=(finding,text.replace('propuseram a CS-ESN, que acrescenta sensoriamento compressivo à representação dos estados do reservatório.','acrescentaram sensoriamento compressivo (Compressed Sensing – CS) à representação dos estados do reservatório, originando a CS-ESN.'),evidence+' Definição inicial de CS preservada.')
finding,text,evidence=edits[217]
edits[217]=(finding,text.replace('acrescentaram sensoriamento compressivo (Compressed Sensing – CS) à representação dos estados do reservatório, originando a CS-ESN.','propuseram uma ESN com sensoriamento compressivo (Compressed Sensing Echo State Network – CS-ESN), aplicada à representação dos estados do reservatório.'),evidence+' Extenso alinhado à entrada CS-ESN da lista, sem criar sigla CS isolada usada uma só vez.')
finding,text,evidence=edits[224]
edits[224]=(finding,text.replace('redes BP e Elman','redes de retropropagação (Backpropagation – BP) e Elman'),evidence+' Definição de BP restaurada na primeira ocorrência textual.')
# A remoção é deliberadamente estrutural: não deixar uma linha com números não
# verificados nem reindexar as demais edições, que usam a tabela da base v001.
table_rows_to_remove={(12,1):('F19','Comparador Cardoso 2022a sem original conferido; RMSE 0,4987 e descrição do protocolo retirados, sem declarar o resultado falso.')}
table_edits={
    (12,2,3,0):('F19/R03','ESN com Algoritmo Genético; distribuições alternativas; declaração de ausência de tratamento adicional dos dados.','Lampugnani P0408 e tabelas XML 9–12. Não equiparar ausência de tratamento adicional a dados sem ajuste.'),
    (12,3,3,0):('F19/R03','Série recebida como ajustada; Algoritmo Genético, LHS, cinco ondas e mecanismo antiestagnação inspirado no CHC.','Capacidade implementada e protocolo; a aplicação original do ajuste não é atribuída ao autor.'),
    (8,9,4,0):('R08','Baixa dispersão da Onda 5','Nota de grupo, não alegação de estabilidade da configuração entre sementes.'),
    (8,10,4,0):('R08','Baixa dispersão da Onda 5','Nota de grupo, não alegação de estabilidade da configuração entre sementes.'),
    (11,4,1,0):('R07','LHS e operador cataclísmico integrados; diversidade não mensurada e ausência de ablação.','Limites da avaliação de H4; hipótese original mantida.'),
    (11,4,2,0):('R07','Efeito não demonstrado.','Presença dos mecanismos no código não demonstra manutenção de diversidade ou ganho de busca.'),
    (11,5,1,0):('R08','Baixa dispersão entre as 15 configurações da Onda 5; sem avaliação de repetidas sementes por configuração.','Dados agregados da Onda 5, não estudo de repetibilidade estocástica.'),
    (11,5,2,0):('R08','Evidência descritiva; estabilidade estocástica não demonstrada.','Não converter amplitude pequena entre configurações em confirmação de H5.'),
    (2,24,0,0):('F12','Soltani et al. (2022)','Folha de rosto do preprint v1 local, PDF 1. A recodificação das cinco dimensões desta linha permanece pendente.')
}
edits[506]=('F20','ARAÚJO, H. V.; CARDOSO, F. C.; MATTOS, V. L. D.; BORGES, E. N.; LUCCA, G.; DALMAZO, B. L.; BERRI, R. A. Comparing MAE and RMSE as fitness of genetic algorithm for optimizing echo state network hyperparameters with different probabilistic distributions. In: JULIAN, V. et al. (ed.). Intelligent Data Engineering and Automated Learning – IDEAL 2024. Cham: Springer, 2025. p. 315-327. (LNCS, v. 15347). DOI: 10.1007/978-3-031-77738-7_26.','Springer, página oficial do DOI: Cite this paper usa 2025; pp.315–327; publicação online 14/11/2024. Metadados reconciliados sem alegar leitura do texto final pago.')
finding,text,evidence=edits[252]
edits[252]=(finding,text+' Foi consultada a prova de autor; os metadados da edição final foram conferidos no editor.',evidence+' Distinção entre prova local e metadados finais Springer.')
citation_year=re.compile(r'(Araújo(?:\s+et al\.)?(?:\s*\(|,\s*))2024',re.I)
for i,p in enumerate(base_paragraphs):
    finding,text,evidence=edits.get(i,('F20',base_text(i),'Atualização exclusiva da chamada autor–ano de Araújo, conforme citação recomendada pela Springer.'))
    updated=citation_year.sub(r'\g<1>2025',text)
    if updated!=text:edits[i]=(finding+'/F20' if finding!='F20' else finding,updated,evidence+' Ano bibliográfico 2025, distinto da publicação online em 2024.')
table_edits[(2,2,0,0)]=('F20','Araújo et al. (2025)','Springer DOI10.1007/978-3-031-77738-7_26, ano recomendado 2025; o mesmo PDF local foi usado na recodificação.')
matrix=json.loads((OUT/'matriz_recodificada.json').read_text(encoding='utf8'))
assert matrix['n_fontes']==34 and matrix['n_celulas']==170
assert matrix['recodificacao_registrada_para_todas_as_celulas']
by_id={}
for cell in matrix['decisoes']:by_id.setdefault(cell['id'],{})[cell['dimensao']]=cell['codigo']
expected_counts=[{'D':5,'S':0,'?':13,'-':16},{'D':10,'S':4,'?':5,'-':15},
                 {'D':25,'S':2,'?':7,'-':0},{'D':10,'S':2,'?':16,'-':6},
                 {'D':25,'S':3,'?':2,'-':4}]
for dim,expected in enumerate(expected_counts,1):
    assert {k:sum(v[f'P{dim}']==k for v in by_id.values()) for k in 'DS?-'}==expected,'Rever os números da prosa após mudança na matriz.'
# Ordem real do quadro: tese/conferência Duttilo e Liu B./Liu H. são invertidos
# relativamente aos IDs da base reconstruída. Não associar apenas pelo índice.
row_ids=[f'D{i:02d}' for i in range(1,35)]
row_ids[9:11]=['D11','D10'];row_ids[16:18]=['D18','D17']
for row,id in enumerate(row_ids,1):
    for col in range(1,6):
        code=by_id[id][f'P{col}'];text='—' if code=='-' else code
        table_edits[(2,row,col,0)]=('F15/F16',text,f'{id}, P{col}: matriz_recodificada.json, localizador, evidência e limite; PDF identificado por SHA256.')
summaries=[
 ('P1 Distribuição de Win/W','Identifica lei e matriz. Topologia, trajetória caótica e distribuição usada na busca são informações distintas.'),
 ('P2 Seleção de hiperparâmetros','AG, PSO, SSA, TPE e sensibilidade são distinguidos de treino de Wout, parâmetros fixos e otimização de MLP.'),
 ('P3 Preparação das séries','Retornos, normalização, imputação, filtragem, ajuste corporativo e atributos/janelas; inclui séries não financeiras.'),
 ('P4 Comparações com modelos','Separa comparação própria de LSTM/GRU/Transformer e números importados, como em Deng e Liu B. (S).'),
 ('P5 Mercado e ativo','Separa o ativo/mercado da análise própria (D) do tratamento contextual ou secundário (S).')]
table_edits[(1,0,1,0)]=('F15/F16','Registros','Cada dimensão tem 34 documentos, distribuídos em quatro estados, sem somar evidência direta e secundária.')
for row,((title,summary),counts) in enumerate(zip(summaries,expected_counts),1):
    for col,text in enumerate((title,f"{counts['D']} D; {counts['S']} S; {counts['?']} ?; {counts['-']} —",summary)):
        table_edits[(1,row,col,0)]=('F15/F16',text,f'Tabela 1, P{row}; contagens e evidência em matriz_recodificada.json e contagens_recodificadas.csv.')

def visible(p):return ''.join(p.xpath('.//w:t/text()',namespaces=NS))

def replace_text(p,new):
    old=visible(p)
    # Aplicar alterações do fim ao início conserva índices da cadeia original.
    for tag,a,b,c,e in reversed(SequenceMatcher(None,old,new,autojunk=False).get_opcodes()):
        if tag=='equal':continue
        nodes=p.xpath('.//w:t',namespaces=NS)
        offsets=[];pos=0
        for node in nodes:
            text=node.text or '';offsets.append((node,pos,pos+len(text)));pos+=len(text)
        replacement=new[c:e]
        if a==b:
            node,start,end=next(((n,s,t) for n,s,t in offsets if s<=a<=t),offsets[-1])
            text=node.text or '';node.text=text[:a-start]+replacement+text[a-start:]
            node.set(XMLSPACE,'preserve')
        else:
            affected=[(n,s,t) for n,s,t in offsets if s<b and t>a]
            for index,(node,start,end) in enumerate(affected):
                text=node.text or ''
                node.text=text[:max(0,a-start)]+(replacement if index==0 else '')+text[min(len(text),b-start):]
                node.set(XMLSPACE,'preserve')
    assert visible(p)==new

ITALIC_PHRASES=(
    'et al.', 'Autoregressive Integrated Moving Average', 'Support Vector Machine',
    'F1-score', 'Large Language Models', 'Natural Language Processing',
    'Sparrow Search Algorithm', 'Proton Exchange Membrane Fuel Cells',
    'Generalized Error Distribution',
    'Exponential Generalized Autoregressive Conditional Heteroskedasticity',
    'Akaike Information Criterion', 'Bayesian Information Criterion',
    'Hannan–Quinn Information Criterion', 'Center for Research in Security Prices',
    'Tree Parzen Estimator', 'fitness', 'Methodi Ordinatio',
    'Heterogeneous Autoregressive',
    'Deep Learning', 'Mean Squared Error', 'Normalized Mean Squared Error',
    'Compressed Sensing', 'Higher Order Neural Networks', 'Particle Swarm Optimization',
    'Reservoir Computing',
    'Compressed Sensing Echo State Network', 'Backpropagation',
    'Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation',
)

def format_revised_prose(p,index):
    """Corrige atributos que a substituição textual pode herdar de outro termo.

    Opera apenas em runs textuais dos parágrafos efetivamente reescritos;
    conserva os demais atributos, bookmarks, estilos e texto visível.
    """
    text=visible(p)
    wanted=[[False,None] for _ in text]
    reference_titles={
        506:('Intelligent Data Engineering and Automated Learning – IDEAL 2024','et al.'),
        531:('The “echo state” approach to analysing and training recurrent neural networks – with an Erratum note',),
        545:('Echo State Network Optimization: A Systematic Literature Review',),
    }
    phrases=reference_titles.get(index,ITALIC_PHRASES)
    for phrase in phrases:
        for match in re.finditer(re.escape(phrase),text):
            for k in range(match.start(),match.end()):wanted[k][0]=True
    if index!=545:
        for match in re.finditer(r'\bW(?:in|out)?\b|λmax|\bsr\b',text):
            token=match.group()
            if token=='W' and text[max(0,match.start()-5):match.start()]=='Wang ' and text[match.end():match.end()+1]=='.':continue
            for k in range(match.start(),match.end()):wanted[k][0]=True
            if token in ('Win','Wout'):
                for k in range(match.start()+1,match.end()):wanted[k][1]='subscript'
            if token=='λmax':
                for k in range(match.start()+1,match.end()):wanted[k]=[False,'subscript']
        for match in re.finditer(r'MAE(treino|validação)',text):
            for k in range(match.start()+3,match.end()):wanted[k][1]='subscript'
    before=[];pos=0
    for run in list(p.findall('w:r',NS)):
        value=''.join(run.xpath('./w:t/text()',namespaces=NS))
        if not value:continue
        assert all(etree.QName(c).localname in ('rPr','t','lastRenderedPageBreak') for c in run),index
        olditalic=run.find('w:rPr/w:i',NS)
        oldscript=run.find('w:rPr/w:vertAlign',NS)
        before.append({'texto':value,'italico':None if olditalic is None else olditalic.get('{'+NS['w']+'}val','1'),'posicao':None if oldscript is None else oldscript.get('{'+NS['w']+'}val')})
        cuts=[0]+[k for k in range(1,len(value)) if wanted[pos+k]!=wanted[pos+k-1]]+[len(value)]
        insertion=p.index(run)
        for a,b in zip(cuts,cuts[1:]):
            newrun=deepcopy(run)
            for t in newrun.findall('w:t',NS):newrun.remove(t)
            if a:
                for marker in newrun.findall('w:lastRenderedPageBreak',NS):newrun.remove(marker)
            props=newrun.find('w:rPr',NS)
            if props is None:props=etree.Element('{'+NS['w']+'}rPr');newrun.insert(0,props)
            italic,script=wanted[pos+a]
            for name,val in [('i','1' if italic else '0'),('iCs','1' if italic else '0'),('vertAlign',script or 'baseline')]:
                node=props.find('w:'+name,NS)
                if node is None:node=etree.SubElement(props,'{'+NS['w']+'}'+name)
                node.set('{'+NS['w']+'}val',val)
            t=etree.SubElement(newrun,'{'+NS['w']+'}t');t.text=value[a:b];t.set(XMLSPACE,'preserve')
            p.insert(insertion,newrun);insertion+=1
        p.remove(run);pos+=len(value)
    assert pos==len(text) and visible(p)==text,index
    return {'paragrafo':f'P{index:04d}','antes_runs':before,'criterio':'Guia FASOFT PDF 71, estrangeirismos e et al.; nomes próprios/siglas em romano; índices matemáticos preservados por seu significado, não por posição antiga.'}

def format_revised_cell(p,ti,ri,ci):
    format_revised_prose(p,1000+ti*1000+ri*10+ci)
    if ti==2 and ci>0:
        for run in p.findall('w:r',NS):
            props=run.find('w:rPr',NS)
            if props is None:props=etree.Element('{'+NS['w']+'}rPr');run.insert(0,props)
            fonts=props.find('w:rFonts',NS)
            if fonts is None:fonts=etree.Element('{'+NS['w']+'}rFonts');props.insert(0,fonts)
            for name in ('ascii','hAnsi','eastAsia','cs'):fonts.set('{'+NS['w']+'}'+name,'Times New Roman')

def widen_study_column(table):
    grid=table.find('w:tblGrid',NS).findall('w:gridCol',NS)
    widths=[int(g.get('{'+NS['w']+'}w')) for g in grid]
    assert len(widths)==6
    updated=[widths[0]+500]+[w-100 for w in widths[1:]]
    assert sum(updated)==sum(widths) and min(updated)>0
    for g,w in zip(grid,updated):g.set('{'+NS['w']+'}w',str(w))
    for row in table.findall('w:tr',NS):
        cells=row.findall('w:tc',NS);assert len(cells)==6
        for cell,w in zip(cells,updated):
            width=cell.find('w:tcPr/w:tcW',NS);assert width is not None
            width.set('{'+NS['w']+'}w',str(w));width.set('{'+NS['w']+'}type','dxa')
    return {'antes_dxa':widths,'depois_dxa':updated,'motivo':'Evitar contato do nome do estudo com o código de P1, preservando a largura total.'}

def keep_summary_table_together(table):
    """Tabela1 é curta; encadear suas linhas evita partir cinco dimensões."""
    paragraphs=table.findall('.//w:p',NS)
    for p in paragraphs[:-1]:
        pr=p.find('w:pPr',NS)
        if pr is None:pr=etree.Element('{'+NS['w']+'}pPr');p.insert(0,pr)
        keep=pr.find('w:keepNext',NS)
        if keep is None:keep=etree.SubElement(pr,'{'+NS['w']+'}keepNext')
        keep.set('{'+NS['w']+'}val','1')

def set_figure_aspect(p,png):
    width,height=struct.unpack('>II',png[16:24])
    changed=[]
    for extent in p.xpath('.//*[local-name()="extent" or local-name()="ext"]'):
        if extent.get('cx') and extent.get('cy'):
            old=int(extent.get('cy'));extent.set('cy',str(round(int(extent.get('cx'))*height/width)))
            changed.append({'antes_cy':old,'depois_cy':int(extent.get('cy'))})
    assert len(changed)==2
    return changed

with ZipFile(BASE) as z:
    infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
original_parts=parts.copy()
root=etree.fromstring(parts['word/document.xml'])
body=root.find('w:body',NS)
ps=body.findall('w:p',NS)
records=[]
formatting=[]
for i,(finding,new,evidence) in edits.items():
    if i in (41,44):
        assert 150<=len(new.split())<=500,(i,len(new.split()))
        assert new!=base_text(i)
        assert re.findall(r'\d+(?:[.,]\d+)*',new)==re.findall(r'\d+(?:[.,]\d+)*',base_text(i)),i
    else:assert len(new)<=700,(i,len(new))
    p=ps[i];old=visible(p)
    assert not p.xpath('.//w:fldChar|.//w:instrText|.//w:drawing|.//w:hyperlink',namespaces=NS),i
    replace_text(p,new)
    if i==158:
        # Sumário: manter número, título e página em campos separados. O diff
        # achatado pode deslocar a tabulação para dentro de uma palavra nova.
        template_props=p.find('w:r/w:rPr',NS)
        template_props=deepcopy(template_props) if template_props is not None else None
        assert not p.xpath('.//w:sectPr',namespaces=NS)
        for child in list(p):
            if child.tag!='{'+NS['w']+'}pPr':p.remove(child)
        for value in ('4.4',None,'DISPERSÃO ENTRE CONFIGURAÇÕES E GENERALIZAÇÃO',None,'57'):
            run=etree.SubElement(p,'{'+NS['w']+'}r')
            if template_props is not None:run.append(deepcopy(template_props))
            node=etree.SubElement(run,'{'+NS['w']+'}'+('tab' if value is None else 't'))
            if value is not None:node.text=value;node.set(XMLSPACE,'preserve')
        assert visible(p)==new
    if i not in (41,44,47,66,152,158,505,509):formatting.append(format_revised_prose(p,i))
    records.append({'paragrafo_origem':f'P{i:04d}','achado':finding,'antes':old,'depois':new,'evidencia':evidence,'alcance':'Trechos pertinentes e contexto consultados; sem declaração de leitura integral de todas as obras.','estado':'incorporado_validacao_visual_pendente'})
tables=body.findall('w:tbl',NS)
table_layout=widen_study_column(tables[2])
keep_summary_table_together(tables[1])
for (ti,ri,ci,pi),(finding,new,evidence) in table_edits.items():
    p=tables[ti].findall('w:tr',NS)[ri].findall('w:tc',NS)[ci].findall('w:p',NS)[pi]
    old=visible(p)
    assert not p.xpath('.//w:fldChar|.//w:instrText|.//w:drawing|.//w:hyperlink',namespaces=NS)
    replace_text(p,new)
    format_revised_cell(p,ti,ri,ci)
    records.append({'paragrafo_origem':f'TabelaXML{ti}/linha{ri}/celula{ci}/paragrafo{pi}','achado':finding,'antes':old,'depois':new,'evidencia':evidence,'alcance':'Recodificação com escopo e incerteza declarados; sem certificação integral das fontes. Tipografia dos segmentos substituídos corrigida.','estado':'incorporado_validacao_visual_pendente'})
removed_rows=[]
for (ti,ri),(finding,evidence) in sorted(table_rows_to_remove.items(),reverse=True):
    row=tables[ti].findall('w:tr',NS)[ri]
    assert not row.xpath('.//w:fldChar|.//w:instrText|.//w:drawing|.//w:hyperlink',namespaces=NS)
    removed_rows.append({'tabela_origem':ti,'linha_origem':ri,'achado':finding,'antes':' | '.join(row.xpath('.//w:t/text()',namespaces=NS)),'evidencia':evidence})
    tables[ti].remove(row)
rels=etree.fromstring(parts['word/_rels/document.xml.rels'])
rid=ps[280].xpath('.//*[local-name()="blip"]/@*[local-name()="embed"]')[0]
target=next(r.get('Target') for r in rels if r.get('Id')==rid)
media_name='word/'+target
assert media_name.endswith('.png')
new_image=(OUT/'figura1_recodificada.png').read_bytes()
assert new_image.startswith(b'\x89PNG\r\n\x1a\n')
parts[media_name]=new_image
aspect_changes=set_figure_aspect(ps[280],new_image)
media_changes=[{'figura':'Figura 1','paragrafo':'P0280','parte':media_name,
                'antes_sha256':hashlib.sha256(original_parts[media_name]).hexdigest(),
                'depois_sha256':hashlib.sha256(new_image).hexdigest(),
                'evidencia':'matriz_recodificada.json; contagens_recodificadas.csv; plotar_cobertura_recodificada.R',
                'dimensoes':aspect_changes,'estado':'inserção e dimensão no Word pendentes de conferência visual'}]
parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
buffer=io.BytesIO()
with ZipFile(buffer,'w') as z:
    for info in infos:z.writestr(info,parts[info.filename])
with ZipFile(io.BytesIO(buffer.getvalue())) as z:
    assert set(z.namelist())==set(parts)
    for name in parts:
        if name not in ('word/document.xml',media_name):assert z.read(name)==original_parts[name]
    assert z.read(media_name)==new_image
    after=etree.fromstring(z.read('word/document.xml'));newps=after.find('w:body',NS).findall('w:p',NS)
    for i,(_,text,_) in edits.items():assert visible(newps[i])==text
    before_root=etree.fromstring(ZipFile(BASE).read('word/document.xml'))
    before_ps=before_root.find('w:body',NS).findall('w:p',NS)
    assert len(before_ps)==len(newps)
    for i,(p,q) in enumerate(zip(before_ps,newps)):
        if i==280:set_figure_aspect(p,new_image)
        if i not in edits:assert etree.tostring(p)==etree.tostring(q),i
    expected_tables=before_root.find('w:body',NS).findall('w:tbl',NS)
    widen_study_column(expected_tables[2])
    keep_summary_table_together(expected_tables[1])
    for (ti,ri,ci,pi),(_,text,_) in table_edits.items():
        p=expected_tables[ti].findall('w:tr',NS)[ri].findall('w:tc',NS)[ci].findall('w:p',NS)[pi]
        replace_text(p,text);format_revised_cell(p,ti,ri,ci)
    for (ti,ri) in sorted(table_rows_to_remove,reverse=True):
        expected_tables[ti].remove(expected_tables[ti].findall('w:tr',NS)[ri])
    assert [etree.tostring(t,method='c14n') for t in expected_tables]==[etree.tostring(t,method='c14n') for t in after.find('w:body',NS).findall('w:tbl',NS)]
# Acrescentar o quadro de atribuições só depois da validação das edições da base.
# A verificação por remoção das inserções prova que nenhum nó anterior foi mudado.
removed_list_entries=[]
for index,label in [(76,'BPNN'),(86,'ER'),(106,'NRMSE'),(107,'PCO'),(118,'SF'),(119,'SJR'),(122,'SW'),(123,'TFC')]:
    p=ps[index]
    assert visible(p).startswith(label+' '),(index,visible(p))
    assert not p.xpath('.//w:sectPr|.//w:fldChar|.//w:instrText|.//w:drawing|.//w:hyperlink',namespaces=NS)
    removed_list_entries.append({'paragrafo_origem':f'P{index:04d}','antes':visible(p),'motivo':'Sigla não utilizada na parte textual/tabelas da revisão; nome por extenso não obriga manter abreviatura sem uso.'})
    body.remove(p)
before_insertions=etree.tostring(root,method='c14n')
def strip_clone_ids(node):
    for child in node.iter():
        for attr in list(child.attrib):
            name=etree.QName(attr).localname
            if name in ('paraId','textId') or name.startswith('rsid'):del child.attrib[attr]
    for child in list(node.xpath('.//w:bookmarkStart|.//w:bookmarkEnd|.//w:proofErr|.//w:lastRenderedPageBreak',namespaces=NS)):
        child.getparent().remove(child)
    return node

def plain_paragraph(template,text,size=20,bold=False):
    p=strip_clone_ids(deepcopy(template))
    for child in list(p):
        if child.tag!='{'+NS['w']+'}pPr':p.remove(child)
    assert not p.xpath('.//w:sectPr',namespaces=NS)
    r=etree.SubElement(p,'{'+NS['w']+'}r');rp=etree.SubElement(r,'{'+NS['w']+'}rPr')
    fonts=etree.SubElement(rp,'{'+NS['w']+'}rFonts')
    for attr in ('ascii','hAnsi','eastAsia','cs'):fonts.set('{'+NS['w']+'}'+attr,'Times New Roman')
    for name,val in [('sz',str(size)),('szCs',str(size)),('b','1' if bold else '0'),('bCs','1' if bold else '0')]:
        e=etree.SubElement(rp,'{'+NS['w']+'}'+name);e.set('{'+NS['w']+'}val',val)
    t=etree.SubElement(r,'{'+NS['w']+'}t');t.set(XMLSPACE,'preserve');t.text=text
    format_revised_prose(p,90000)
    return p

contribution_rows=[
    ['Elemento','Base ou atribuição','Contribuição e limite'],
    ['Fundamentos da ESN','Jaeger (2001, 2007)','Reservatório fixo e ajuste da saída são fundamentos anteriores, não algoritmos originais deste trabalho.'],
    ['ESN, AG e distribuições','Araújo et al. (2025); Cardoso (2025); Lampugnani (2026)','O protocolo combina elementos já investigados. A aplicação à PETR4 não demonstra novidade de cada técnica.'],
    ['LHS e antiestagnação','Implementação do ESNAUTO; Seção 3.4','Integração no motor genético, sem constituir CHC completo nem demonstrar ganho de diversidade por ablação.'],
    ['Organização e auditoria','Artefatos do protocolo; Seção 3.8','Infraestrutura experimental e preservação complementar documentadas; as 45 execuções históricas têm preservação incompleta.'],
    ['Dados e código legado','Arquivos recebidos e scripts preservados','A autoria do ajuste dos preços e a origem de rotinas legadas não foram integralmente reconstruídas. Não se atribui criação integral ao autor.'],
]
new_table=strip_clone_ids(deepcopy(tables[11]))
assert not new_table.xpath('.//w:fldChar|.//w:instrText|.//w:drawing|.//w:hyperlink',namespaces=NS)
widths=[1900,3100,4071]
assert sum(widths)==9071
for g,width in zip(new_table.find('w:tblGrid',NS),widths):g.set('{'+NS['w']+'}w',str(width))
new_rows=new_table.findall('w:tr',NS);assert len(new_rows)==len(contribution_rows)
for ri,(row,texts) in enumerate(zip(new_rows,contribution_rows)):
    trpr=row.find('w:trPr',NS)
    if trpr is None:trpr=etree.Element('{'+NS['w']+'}trPr');row.insert(0,trpr)
    for h in trpr.findall('w:trHeight',NS):trpr.remove(h)
    if trpr.find('w:cantSplit',NS) is None:etree.SubElement(trpr,'{'+NS['w']+'}cantSplit')
    if ri==0 and trpr.find('w:tblHeader',NS) is None:etree.SubElement(trpr,'{'+NS['w']+'}tblHeader')
    for ci,(cell,text,width) in enumerate(zip(row.findall('w:tc',NS),texts,widths)):
        cell.find('w:tcPr/w:tcW',NS).set('{'+NS['w']+'}w',str(width))
        oldps=cell.findall('w:p',NS);assert oldps
        p=plain_paragraph(oldps[0],text,size=22,bold=ri==0)
        for oldp in oldps:cell.remove(oldp)
        cell.append(p)
caption_text='Quadro 6 – Delimitação das contribuições e da procedência'
caption=plain_paragraph(ps[453],caption_text)
source_text='Fonte: Elaborado pelo autor (2026), com base em Jaeger (2001, 2007), Araújo et al. (2025), Cardoso (2025), Lampugnani (2026) e nos artefatos examinados.'
source=plain_paragraph(ps[454],source_text)
list_item=strip_clone_ids(deepcopy(ps[58]))
assert not list_item.xpath('.//w:sectPr|.//w:fldChar|.//w:instrText',namespaces=NS)
# Texto e página são campos separados por tabulação; não usar o diff de texto
# achatado aqui, pois ele pode ancorar um algarismo no lado errado do tab.
list_run_props=ps[58].find('w:r/w:rPr',NS)
for child in list(list_item):
    if child.tag!='{'+NS['w']+'}pPr':list_item.remove(child)
for value in (caption_text,None,'71'):
    run=etree.SubElement(list_item,'{'+NS['w']+'}r')
    if list_run_props is not None:run.append(deepcopy(list_run_props))
    if value is None:etree.SubElement(run,'{'+NS['w']+'}tab')
    else:
        node=etree.SubElement(run,'{'+NS['w']+'}t');node.text=value;node.set(XMLSPACE,'preserve')
assert visible(list_item)==caption_text+'71'
assert len(list_item.findall('w:r/w:tab',NS))==1
body.insert(body.index(ps[58])+1,list_item)
for node in (caption,new_table,source):body.insert(body.index(ps[504]),node)
added=[list_item,caption,new_table,source]
added_indices=sorted(body.index(n) for n in added)
parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
final_buffer=io.BytesIO()
with ZipFile(final_buffer,'w') as z:
    for info in infos:z.writestr(info,parts[info.filename])
with ZipFile(io.BytesIO(final_buffer.getvalue())) as z:
    assert z.testzip() is None
    check=etree.fromstring(z.read('word/document.xml'));check_body=check.find('w:body',NS)
    for idx in reversed(added_indices):check_body.remove(check_body[idx])
    assert etree.tostring(check,method='c14n')==before_insertions,'A inserção alterou nós anteriores.'
    final_root=etree.fromstring(z.read('word/document.xml'))
    assert len(final_root.find('w:body',NS).findall('w:tbl',NS))==14
    assert [visible(p) for p in new_table.findall('.//w:p',NS)]==[text for row in contribution_rows for text in row]
    for name in parts:
        if name not in ('word/document.xml',media_name):assert z.read(name)==original_parts[name]
DEST.write_bytes(final_buffer.getvalue())
log={'base':'v001','sha256_base':hashlib.sha256(BASE.read_bytes()).hexdigest(),'arquivo_trabalho':str(DEST),'sha256_trabalho':hashlib.sha256(DEST.read_bytes()).hexdigest(),'alteracoes':records,'midias':media_changes,'ajuste_larguras_quadro1':table_layout,'validacao':f'{len(edits)} parágrafos do corpo e {len(table_edits)} de tabelas alterados; Figura 1 substituída e redimensionada; Quadro 1 com redistribuição de largura. Demais parágrafos, células e partes OOXML preservados. Renderização e conjunto dos achados ainda pendentes.'}
log['linhas_removidas']=removed_rows
log['entradas_siglas_removidas']=removed_list_entries
log['layout_tabela1']='Parágrafos internos encadeados por keepNext, exceto o último, para manter a síntese de cinco dimensões na mesma página. Texto, fonte e largura preservados; conferência visual necessária.'
log['blocos_inseridos']={'achado':'R13','local':'Após P0058 (lista) e antes de P0504 (fim da conclusão)','legenda':caption_text,'linhas':contribution_rows,'fonte':source_text,'validacao':'Inserções removidas da árvore de conferência restituem exatamente a árvore validada antes da inserção; 11pt corpo, 10pt legenda/fonte, largura9071dxa, cabeçalho repetível, sem altura fixa. Paginação e visual ainda pendentes.'}
log['validacao']+=f' {len(removed_rows)} linha de comparação removida conforme registro específico.'
(OUT/'lote1_alteracoes.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(OUT/'formatacao_trechos_reescritos.json').write_text(json.dumps({'paragrafos':formatting,'sha256_docx':log['sha256_trabalho'],'validacao_visual':'pendente na exportação posterior à correção tipográfica'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'{len(edits)} parágrafos do corpo; {len(table_edits)} células/parágrafos de tabelas; Figura 1 substituída. Cópia salva e invariantes conferidos.')
