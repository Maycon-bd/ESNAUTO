"""Revalida contextos modificados e liga ocorrências a evidências disponíveis."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(doc)=='61fac8da8ab082633bbaa113ed697fd32ccfd7d72c2142f003b18b5b10083e2a';index=json.loads((out/'indice_citacoes_atuais_lote50.json').read_text(encoding='utf8'));refs={r['id']:r for r in index['registros']}
supp={'R06':'reports/fontes_drive_20261029/Cardoso_RBras_2022_completo.pdf','R10':'reports/tese_Fabian_Correa_Cardoso.pdf','R27':'reports/fechamento_integral_20261029/fontes_suplementares/Jaeger_2001_errata_2010.pdf','R30':'MatheusTeixeiraLampugnani_monografia (1).docx'}
items=[
 ('R02','P_atual0319','PDF 8–9, prova de autor','55 bits e cinco hiperparâmetros; fonte não divide os bits. A redação atual identifica a alocação como pertencente ao motor atual.'),
 ('R06','P_atual0319','p. 203 impressa, PDF 7','Raio espectral 1,25, vazamento 0,2 e regularização 10⁻⁸; texto foi alterado em outra frase, preservando a atribuição.'),
 ('R02','P_atual0330','PDF 7–8 e código atual ga_engine.R 293–296','Ponderação de 40% treino e 60% validação; texto agora atribui a função concreta ao motor atual, sem provar seu uso por todas as rodadas.'),
 ('R47','P_atual0208','PDF 5–8, Tabela 1 e Figuras 6–7','Após correção, melhor comparador é indicado por horizonte; artigo descreve Lasso em um passo e LSTM em quatro/dez.'),
 ('R02','P_atual0321','PDF 8–9 e quadro atual','Prova descreve cromossomo de 55 bits e cinco parâmetros; as faixas e os blocos do quadro foram conferidos no código, não imputados à prova.'),
 ('R06','P_atual0321','p. 203 impressa, PDF 7','Fonte descreve parâmetros fixos de ESN; a codificação e as faixas do quadro são do código atual.'),
 ('R28','P_atual0321','PDF 1–5, Scholarpedia','Fonte descreve ESN, reservatório e treinamento; a alocação dos bits é informação do código atual, não afirmação de Jaeger.'),
 ('R28','P_atual0299','PDF 1–5, Scholarpedia; ga_engine.R e esn_core.R','Fundamentos ESN são coerentes. O código e a adaptação são sustentados pelos artefatos e pela declaração do autor.'),
 ('R28','P_atual0322','PDF 2–5, Scholarpedia; app/utils/esn_core.R 27–41','Fonte discute tanh, dinâmica de reservatório e treinamento da saída. Equação de implementação e regressão regularizada precisam também do código; ele inclui fallback por pseudoinversa.'),
 ('R02','P_atual0498','PDF 7–9, prova de autor; Quadro 6','ESN, AG, 55 bits e distribuições são antecedentes; não equivale a atribuição de autoria da integração atual.'),
 ('R27','P_atual0498','relatório Jaeger 2001 com errata 2010, PDF 3 e seções de treinamento','Reservatório recorrente e ajuste da saída fundamentam o quadro; a contribuição própria do projeto é avaliada em fontes separadas.'),
 ('R28','P_atual0498','PDF 1–5, Scholarpedia','Descrição de reservatório fixo e saída treinável sustenta a atribuição de fundamento ESN no quadro.'),
 ('R07','P_atual0302','BovDB PDF 5 e 7; declaração do autor e comparação dos arquivos locais','O artigo descreve base da B3 e fatores de eventos. O recebimento de série já ajustada é declaração do autor; a cadeia original do ajuste não é inferida do artigo.'),
 ('R07','P_atual0312','BovDB PDF 5 e 7; declaração do autor','Fonte da tabela foi corrigida para identificar a série recebida e citar Cardoso como contexto, sem atribuir execução comprovada do ajuste ao artigo.'),
 ('R10','T_atual13/L2/C1/P0','tese Cardoso, resumo e capítulos metodológicos','A tese discute ESN, AG e distribuições. Os demais autores no mesmo quadro exigem evidências separadas.'),
 ('R02','T_atual13/L2/C1/P0','prova Araújo PDF 7–10','ESN, AG e distribuições são abordadas na fonte; não significa que o antecedente é idêntico ao protocolo atual.'),
 ('R27','T_atual13/L1/C1/P0','relatório Jaeger 2001/errata, resumo e treinamento','Reservatório recorrente e treinamento de saída são fundamentos anteriores.'),
 ('R28','T_atual13/L1/C1/P0','Scholarpedia PDF 1–5','Reservatório e treinamento da saída são fundamentos anteriores.'),
 ('R30','T_atual13/L2/C1/P0','monografia Lampugnani, parágrafos 397, 435 e tabelas 9–12','ESN, AG e distribuições em PETR4 são antecedentes; protocolos não são iguais.'),
 ('R30','T_atual12/L1/C0/P0','tabelas 9–12 da monografia Lampugnani','Linha identifica o estudo; mínimos por métrica e combinações foram recontados em afirmacoes_lampugnani_lote42.json.'),
 ('R30','P_atual0067','Tabela 7 e sua fonte','Entrada de lista corresponde à tabela de comparação descritiva, cujos valores foram conferidos no lote 42.'),
 ('R15','T_atual1/L4/C2/P0','Deng PDF 20, Tabela 6','O artigo atribui valores LSTM e outros comparadores à referência 36; o quadro classifica como comparação secundária.'),
 ('R31','T_atual1/L4/C2/P0','Liu B. PDF 15, Tabela 6','O artigo utiliza resultados comparadores provenientes de estudo anterior; o quadro distingue comparação secundária.')]
rows=[]
for rid,loc,place,ev in items:
 ref=refs[rid];hits=[o for o in ref['ocorrencias'] if o['local']==loc];assert len(hits)==1,(rid,loc,len(hits));o=hits[0];path=supp.get(rid,ref.get('arquivo_fonte'));assert path and (root/path).exists();expected=ref.get('sha256_fonte');assert expected is None or sha(root/path)==expected
 rows.append({'referencia':rid,'ancora':loc,'texto_atual':o['contexto'],'chamada':o['chamada'],'arquivo_fonte':path,'sha256_fonte':sha(root/path),'localizador':place,'evidencia':ev,'diagnostico':'condizente no escopo delimitado; procedência local apenas quando expressamente documentada'})
f=out/'afirmacoes_ocorrencias_lote52.json';assert not f.exists();f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'registros':rows,'limites':'Fontes, trechos e condições do alcance são descritos individualmente; não prova a totalidade de cada parágrafo. Quadro 3 e atribuições do código baseiam-se também nos arquivos e relato do autor; resultados históricos não foram reexecutados.','acao':'Nenhuma edição adicional.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8');s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Atualizar cobertura e confrontar citações restantes, inclusive fontes não acessadas integralmente.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(len(rows),'relações revalidadas ou vinculadas.')
