import hashlib,json,shutil
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1];folder=root/'reports/fechamento_integral_20261029';p=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest();before=sha(p);assert before=='61fac8da8ab082633bbaa113ed697fd32ccfd7d72c2142f003b18b5b10083e2a'
copy=folder/'antes_edicao_lote57.docx';assert not copy.exists();shutil.copy2(p,copy);doc=Document(p)
changes=[(171,'Também se busca otimizar conjuntamente a taxa de vazamento, o raio espectral, o descarte inicial, o tamanho do reservatório e a regularização Ridge por meio de cromossomo binário de 55 bits.','Também se busca otimizar conjuntamente a taxa de vazamento, o raio espectral, o descarte inicial, o tamanho do reservatório e a regularização Ridge. A implementação atual utiliza um cromossomo binário de 55 bits para esses parâmetros.'),(459,'O cromossomo binário de 55 bits codifica','Na implementação atual, o cromossomo binário de 55 bits codifica')]
for i,old,new in changes:
 par=doc.paragraphs[i];assert par.text.count(old)==1
 found=[r for r in par.runs if old in r.text];assert len(found)==1,(i,[(r.text) for r in par.runs]);found[0].text=found[0].text.replace(old,new)
doc.save(p);after=sha(p);assert after!=before
record={'sha_antes':before,'sha_depois':after,'paragrafos':[i for i,_,_ in changes],'motivo':'Distinguir o motor atual da codificação efetivamente utilizada nas execuções históricas; não há alteração de resultados.','backup':str(copy.relative_to(root)),'alteracoes':[{'antes':a,'depois':b} for _,a,b in changes]};(folder/'edicao_lote57.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(after)
