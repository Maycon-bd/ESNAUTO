"""Atribuição aos trabalhos de Cardoso e correção da comparação de métricas."""
import hashlib,json,shutil
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from incorporar_fechamento_integral_lote1 import NS,visible,replace_text,format_revised_prose

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='bdb37cc278346de7b0da09ea09e349acec749b46d2614609b5afa5216b3efd88'
backup=out/'antes_lote29.docx'; assert not backup.exists(); shutil.copy2(doc,backup)
with ZipFile(doc) as z: infos=z.infolist(); parts={i.filename:z.read(i.filename) for i in infos}
before=dict(parts); tree=etree.fromstring(parts['word/document.xml'])
p=[p for p in tree.xpath('//w:p',namespaces=NS) if visible(p).startswith('Araújo et al. (2025) e Lampugnani (2026) já investigaram')]
assert len(p)==1; p=p[0]; old=visible(p)
original='Naqueles estudos de caso, ARMA-EGARCH apresentou melhor desempenho, ressaltando a dependência entre método, dados e desfecho.'
corrected='Nas comparações da tese, o ARMA-EGARCH obteve menor RMSE nas duas ações, enquanto a ESN apresentou menor MAE para PETR4.'
assert old.count(original)==1; new=old.replace(original,corrected); assert len(new)<=700
replace_text(p,new); format_revised_prose(p,0)
parts['word/document.xml']=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
assert [x for x in parts if parts[x]!=before[x]]==['word/document.xml']
tmp=doc.with_suffix('.tmp.docx')
with ZipFile(tmp,'w') as z:
 for i in infos:z.writestr(i,parts[i.filename])
tmp.replace(doc)
inv=out.parent/'bibliometria_reconstrucao/referencias_graficas'
sources=[]
for label in ['ENMC','KBS']:
 info=json.loads((inv/(label+'_inventario.json')).read_text(encoding='utf8')); path=Path(info['arquivo']); assert path.exists()
 sources.append({'id':label,'arquivo':str(path),'sha256':sha(path),'paginas_pdf_examinadas':([6,8] if label=='ENMC' else [6,7]),'alcance':'Conferência dirigida de figuras e trechos; não é leitura integral.'})
report={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho_antes':sha(backup),'sha256_rascunho_apos_edicao':sha(doc),
 'tese':{'arquivo':'reports/tese_Fabian_Correa_Cardoso.pdf','sha256':sha(root/'reports/tese_Fabian_Correa_Cardoso.pdf'),'alcance':'Resumo e comparações nas Tabelas 16 e 32; leitura dirigida, não integral.',
 'pontos':[{'localizacao':'Tabela 16, p. 84 impressa / p. 87 PDF (ITSA4)','arma_egarch_mae':'0,000013794','arma_egarch_rmse':'0,000036582','esn_mae':'0,000017793','esn_rmse':'0,000040582'},
 {'localizacao':'Tabela 32, p. 101 impressa / p. 104 PDF (PETR4)','arma_egarch_mae':'0,000022638','arma_egarch_rmse':'0,000107948','esn_mae':'0,000016448','esn_rmse':'0,000110424'}],
 'diagnostico':'A tese resume ARMA-EGARCH como melhor nos estudos de caso, mas a Tabela 32 mostra menor MAE da ESN na PETR4; redação agora especifica RMSE e ressalva a exceção por MAE. Dados e desfecho de volatilidade diferem da monografia.'},
 'fontes_visuais':sources,'diagnostico_figuras':'ENMC Figura 2 apresenta frequência de palavras-chave e Figura 7 expressões de títulos; KBS Figura 1 mostra frequência de palavras-chave e Figura 2 bigramas de resumos. Sustentam o uso como referências visuais em sentido amplo, sem confundir suas amostras com a coleção da monografia.',
 'similaridade':'Figuras e números dos artigos não foram reproduzidos como dados da monografia; a comparação pontual não certifica ausência global de plágio.',
 'texto_antes':old,'texto_depois':new,'estado':'pendente_exportacao_validacao_e_inspecao'}
(out/'conferencia_cardoso_lote29.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Comparação corrigida e evidências registradas; pendente inspeção.')
