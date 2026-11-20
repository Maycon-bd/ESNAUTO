"""Registra decisões humanas da nova auditoria; não modifica a monografia."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
A=json.loads((OUT/'estrutura.json').read_text(encoding='utf-8'))
C=json.loads((OUT/'conferencia.json').read_text(encoding='utf-8'))
prior=json.loads((ROOT/'reports/fechamento_integral_20261029/matriz_guia_decisoes_lote162.json').read_text(encoding='utf-8'))
assert C['contagem']['falhas']==0
# Decisões desta leitura. Não se copiam aprovações da v006 para a v010.
decisions={
 'G01':('conforme','Seis seçõesA4;78páginasPDFmedidas.'),
 'G02':('conforme','Seis seções:1701twips no alto/esquerda,1134na direita/base; textoPDFdentro da mancha, tolerância1,2pt.'),
 'G03':('conforme','248parágrafos de corpo/896runs emTimesNewRoman12; exceções de11/10conferidas separadamente.'),
 'G04':('conforme_no_escopo','Sem cor textual divergente identificada no corpo ou na inspeção das78páginas; cores das figuras permitidas.'),
 'G05':('conforme','248parágrafos do corpo justificados; referências e pré-textuais respeitam exceções.'),
 'G06':('conforme','Corpo1,5e primeira linha709twips; alíneas possuem deslocamento específico.'),
 'G07':('conforme','Página física18exibe17; capa não contada; páginas1–17sem número visível; sequência até77.'),
 'G08':('conforme_no_escopo','Números no alto à direita, tamanho12na representaçãoWord/PDFinspecionada.'),
 'G09':('conforme','Pré-textuais distintos; referências começam em página própria. Continuação de listas/sumário não é elemento novo.'),
 'G10':('conforme','Introdução18; revisão21; métodos42; resultados55; discussão68; conclusão71; referências74(páginasfísicas).'),
 'G11':('conforme_no_escopo','41títulos comkeepNext;78páginas examinadas, sem título isolado/corte observado. Nas239medições de parágrafo, nenhuma quebra deixou fragmento de uma linha;9casos não medidos automaticamente.'),
 'G12':('conforme','Primárias maiúsculas/negrito; secundárias maiúsculas regulares; quatroterciárias com inicialmaiúscula/negrito. Somente três níveis empregados.'),
 'G13':('conforme','Numeração arábica até o terceiro nível; sequência conferida visualmente e no sumário.'),
 'G14':('conforme','Títulos numerados justificados,12e1,5; espaços antes/depois coerentes com modelo.'),
 'G15':('conforme','Títulos pré-textuais eREFERÊNCIAS centralizados,negrito12; dedicatória/epígrafe semtítulo.'),
 'G16':('conforme','Introdução em15parágrafos de texto corrido; sem estilos de subtítulo ou objetos.'),
 'G17':('conforme_no_escopo','Introdução lida nas páginas18–20: sem citaçõesautor-data, tabelas,figuras/equações destacadas ou apresentação de resultados numéricos experimentais.'),
 'G18':('estrutura_presente','Introdução apresenta contexto,problema,objetivos,hipóteses,justificativa e roteiro; mérito científico não reavaliado.'),
 'G19':('conforme','Introdução ocupa três páginas18–20; última contém apenas roteiro, o que não infringe extensão recomendada.'),
 'G20':('conforme','Somente níveisprimário/secundário/terciário.'),
 'G21':('observacao_editorial','Confirmados17parágrafos com8–10linhas entre239medidos;9dos248não medidos automaticamente. A faixa4–7é recomendação, não infração automática; alíneas não recebem alongamento artificial.'),
 'G22':('estrutura_presente_com_pendencia_institucional','Elementos da monografia presentes, mas fichaCIPé espaço reservado e aprovação incompleta pela etapa.'),
 'G23':('conforme','Capa,rosto,ficha,aprovação,dedicatória,agradecimentos,epígrafe,resumos,listas,sumário nessa ordem.'),
 'G24':('fora_do_escopo_cientifico','Seções2.7/2.8presentes; esta auditoria não reabre cobertura bibliográfica ou fidelidade das afirmações.'),
 'G25':('fora_do_escopo_cientifico','Capítulo3presente; resultados,protocolo e mérito da metodologia não reavaliados.'),
 'G26':('conforme','Capa com instituição,curso,autor,título,RioVerde/GOe2026; página1inspecionada.'),
 'G27':('conforme_no_escopo','Composição/legibilidade da capa conferidas; modelo não é sobreposição de pixels com o exemplo.'),
 'G28':('conforme','Rosto comautor,título,natureza,objetivo,instituição,área,orientador,localeano.'),
 'G29':('conforme','Bloconatureza/orientador11,simples; recuo4536twips(~8cm); justificado.'),
 'G30':('pendencia_institucional','Folha reservada apósrosto, sem ficha bibliográfica emitida pela biblioteca. Não considerar o quadro vazio como ficha concluída.'),
 'G31':('conforme_apenas_reserva','Caixa7087×4252twips(~12,5×7,5cm),cabeçalhos11; conteúdoCIPnão preenchido.'),
 'G32':('conforme_no_escopo','Aprovação contémidentificação,natureza,área,banca e instituições; nomes/titulações institucionais não foram confirmados externamente.'),
 'G33':('conforme_com_ambiguidade','Fontes/disposição conferidas. Texto da natureza mantido regular pela divergência interna entre balão e exemplo doGuia40.'),
 'G34':('etapa_posterior','Data definitiva e assinaturas dependem da aprovação, conformeGuia21.'),
 'G35':('conforme','Dedicatória semtítulo, bloco direito inferior,p5.'),
 'G36':('conforme','Agradecimentos comtítulo12negrito ecorpo12/1,5,p6.'),
 'G37':('conforme_no_escopo','Epígrafe12itálico,recuo~8cm,simples; autoria11àdireita,p7. Posição vertical é aproximada noGuia.'),
 'G38':('identificacao_presente','Epígrafe identificaGleick1987/parágrafo1e referência correspondente; fonteoriginal não reaberta nesta auditoria.'),
 'G39':('conforme','Resumo331palavras/umparágrafo;abstract273palavras/umparágrafo.'),
 'G40':('conforme','Resumo12simples,justificado,semrecuo.'),
 'G41':('conforme_no_escopo','Siglas principais apresentadas por extenso no resumo; nomes próprios/identificadorPETR4preservados.'),
 'G42':('conforme','Cinco palavras-chave emPT/EN; separadas por ponto e vírgula, encerradas por ponto;PETR4é identificador próprio.'),
 'G43':('formato_conforme_fidelidade_nao_reauditada','Abstract12simples,justificado,semrecuo,mesmascinco palavras-chave; não houve nova auditoria linguística ou semântica integral.'),
 'G44':('conforme','Listas próprias defiguras,quadros,tabelas,siglas e símbolos presentes.'),
 'G45':('conforme','19entradas deelementos conciliadas comtítulos/páginas; ordem e pontilhado inspecionados.'),
 'G46':('conforme_no_escopo','Lista deabreviaturas/siglas alfabética presente emduaspáginas; não repetida auditoria semântica de cada expansão.'),
 'G47':('conforme','Sumário contém apenaspartestextuais/póstextuais; pré-textuais excluídos.'),
 'G48':('conforme','41entradas do sumário conciliadas com os títulos e páginas; hierarquia/realce conferidos.'),
 'G49':('nao_aplicavel','Cronograma/orçamento não incluídos; opcionais nesta monografia.'),
 'G50':('nao_aplicavel_no_escopo_declarado','Pesquisa documental/computacional; nenhum instrumento novo com participantes foi acrescentado nesta revisão.'),
 'G51':('fora_do_escopo_cientifico','Resultados/discussão presentes; fidelidade/inferências não reabertas nesta auditoria de formatação.'),
 'G52':('conforme_no_escopo','Setetabelasquantitativas e seisquadros de organização/síntese; matrizdeestados é quadrodescritivo.'),
 'G53':('conforme_no_escopo','Sequências1–6figuras/quadros e1–7tabelas; chamadas observadas na leitura, sem elemento visual solto identificado.'),
 'G54':('conforme','19títulos acima,10simples,sem ponto final.'),
 'G55':('conforme_no_escopo','Títulos identificamobjetos; abrangência temporal explícita quando pertinente, sem exigir mesma fórmula emelementos conceituais.'),
 'G56':('conforme','19fontes abaixo,10simples,anoeponto final.'),
 'G57':('conforme_no_escopo','Tabela7indicaAdaptadode; figuras5/6identificam referência deapresentação e dados próprios, sem falsa autoria dedados de terceiros.'),
 'G58':('ambiguidade_a_avaliar','Tabela7temduaslinhasdedados+umcabeçalho. Guia32–33indica mínimo3linhas, sem esclarecer contagem do cabeçalho; não inventar terceira observação.'),
 'G59':('conforme','Setetabelas com11simples,cabeçalho negrito,sem laterais/grade interna no corpo. Divisórias verticais restritas ao cabeçalho, permitidas pelo modelo53.'),
 'G60':('conforme','Seisquadros com11simples,largura9071twips(~16cm),fechamento lateral,sem grade no corpo; divisórias no cabeçalho seguem anotação do modelo54.'),
 'G61':('conforme','19títulos sem siglas técnicas desnecessárias; nomes próprios preservados.'),
 'G62':('conforme_no_escopo','78páginas examinadas; elementos próximos daschamadas,semcortes/sobreposições observados. Famíliafonte dos pixels das seisfiguras não certificável só pela rasterização.'),
 'G63':('fora_do_escopo_cientifico','Conclusão presente; resposta científica aobjetivos/hipóteses não reauditada.'),
 'G64':('conforme_no_escopo','51referências em12simples,àesquerda,com separação entre entradas e itálico nos veículos/obras. Ordem por primeiroautorconferida; não reaberta normalização bibliográfica integral.'),
 'G65':('fora_do_escopo_desta_rodada','Correspondência completa de todasaschamadas/fontes não reauditada; 51referências preservadas. Não somar aprovação histórica como teste novo.'),
 'G66':('nao_aplicavel','Semglossário.'),
 'G67':('nao_aplicavel','Semapêndices/anexos.'),
 'G68':('conforme_no_escopo','Seisalíneas naSeção4.7comintrodução por dois-pontos,a)–f),minúsculas,ponto-e-vírgula e ponto final na última; recuo/deslocamento visualmente coerentes.'),
 'G69':('nao_aplicavel_no_escopo','Não identificadas notas explicativas ou blocos de citação longa no corpo; epígrafe tratada separadamente.'),
 'G70':('fora_do_escopo_linguistico','Não feita nova revisão integral de português/inglês.'),
 'G71':('fora_do_escopo_semantico','Contextualização de cada termo técnico não reauditada nesta rodada.'),
 'G72':('verificacao_tipografica_parcial','Itálicos inspecionados naspáginas; não repetida classificação lexical integral dos estrangeirismos. Não inventar regra de italicizar todo nome de pacote/autor.'),
 'G73':('verificacao_tipografica','Ocorrências etal.visualmente emitálico; conferir suporte automático emcontrole complementar.'),
 'G74':('fora_do_escopo_semantico','Primeira ocorrência de cadasigla não reauditada integralmente; auditoria anterior não tratada como nova aprovação.'),
 'G75':('verificacao_tipografica_parcial','Grafia de siglas naslistas/títulos inspecionada; sem certificação universal de convenções especializadas.'),
 'G76':('verificacao_tipografica','Win/Woutitálicos eíndices visíveis naspáginas; notação matemática preservada.'),
 'G77':('orientacao_nao_limite','Capítulos emextensões diversas; não existe tamanho obrigatório uniforme. Observação deparágrafos tratada emG21.'),
 'G78':('nao_verificavel_no_digital','Papel,gramatura,número decópias everso físico dependem da entrega impressa.'),
 'G79':('nao_aplicavel','Nenhum quarto/quinto nível empregado; divergênciaGuia12/50não afeta os títulos atuais.'),
 'G80':('ambiguidade_preservada','Natureza da aprovação regular conforme exemplo40; balão pede caixa/negrito distintos, semcoincidência normativa única.'),
 'G81':('conforme','Auditoria somente leitura; DOCX/hash preservado; nenhum treino,GA,DM ou alteração de resultados.'),
}
assert len(decisions)==81
matrix=[]
for r in prior['requisitos']:
 state,evidence=decisions[r['id']]
 matrix.append({k:r[k] for k in ['id','pagina_guia','requisito','natureza']}|{'estado_nesta_auditoria':state,'evidencia_e_alcance':evidence})
(OUT/'matriz_guia81.json').write_text(json.dumps({'base':'v010','sha256_docx':A['sha256'],'requisitos':matrix,'limite':'Não são81aprovações: há verificações parciais,exclusões deescopo,condicionais eambiguidades explícitas.'},ensure_ascii=False,indent=2),encoding='utf-8')
longs=[p for p in C['paragrafos_medidos'] if p.get('linhas',0)>7]
rows=['# Parágrafos acima da recomendação de quatro a sete linhas','',
 'GuiaPDF14: recomendação editorial. Não é erro obrigatório nem autorização para alongar/encurtar texto artificialmente. Medição em239dos248parágrafos de corpo; nove não localizados com segurança pelo extrator. As seisalíneas estão separadas dessa recomendação.','',
 '| Índice XML (basezero) | Página física / impressa | Linhas | Início |','|---:|---|---:|---|']
for p in longs:
 pp=', '.join(f"{x}/{int(x)-1}" for x in p['por_pagina_pdf'])
 rows.append(f"| {p['indice_xml']} | {pp} | {p['linhas']} | {p['inicio']}… |")
(OUT/'paragrafos_recomendacao.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
visual={'base':'v010','sha256_docx':A['sha256'],'pdf_sha256':C['pdf_sha256'],'tipo':'Nova rasterização e nova inspeção de78páginas da exportaçãoWord anterior vinculada por hashes à mesma versão; não nova exportaçãoWord bem-sucedida.', 'paginas_inspecionadas':list(range(1,79)), 'guia_imagens_inspecionadas':[38,40,43,44,50,53,54,60], 'resultado':'Nenhum corte,sobreposição,título isolado ou página branca indevida observado. Tabela7possui duaslinhas de dados; restante conforme no alcance visual.', 'limite':'Não certifica fontes de pixels rasterizados,impressão física ou mérito científico.'}
(OUT/'inspecao_visual.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2),encoding='utf-8')
assert hashlib.sha256((ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx').read_bytes()).hexdigest()==A['sha256']
print(json.dumps({'controles_estruturais':C['contagem'],'requisitos_classificados':len(matrix),'paginas_inspecionadas':78,'paragrafos_longos_confirmados':len(longs),'word_alterado':False}))
