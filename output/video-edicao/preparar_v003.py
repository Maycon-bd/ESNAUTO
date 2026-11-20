"""Alinha legendas revistas, cortes e orientações à mesma linha de tempo."""
import difflib
import importlib.util
import json
from pathlib import Path
import re
import textwrap
import unicodedata

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v003'
OUT=ROOT/'exportados'
cuts=json.loads((QA/'cortes_v002.json').read_text(encoding='utf-8'))
source=json.loads((QA/'transcricao_automatica.json').read_text(encoding='utf-8'))
review=json.loads((QA/'revisao_legendas.json').read_text(encoding='utf-8'))
assert all(str(s['id']) in review for s in source['segments'])

def remap(t):
    frame=t*30
    return (frame-sum(max(0,min(frame,c['fim_frame_exclusivo'])-c['inicio_frame']) for c in cuts))/30

def normal(word):
    word=unicodedata.normalize('NFKD',word.lower())
    value=''.join(c for c in word if c.isalnum())
    return {'sn':'esn','asn':'esn','dnsn':'esn','petra':'petr4','petro':'petr4',
            'mai':'mae','mike':'mae','may':'mae','rmsi':'rmse','eco':'echo'}.get(value,value)

words=[]
dropped=[]
for segment in source['segments']:
    old=segment['words']
    new=review[str(segment['id'])].split()
    matcher=difflib.SequenceMatcher(None,[normal(w['word']) for w in old],[normal(w) for w in new],autojunk=False)
    aligned=[]
    for tag,a,b,c,d in matcher.get_opcodes():
        if tag=='equal':
            aligned.extend({'word':new[j], 'start':old[i]['start'], 'end':old[i]['end']} for i,j in zip(range(a,b),range(c,d)))
        elif tag in ('replace','insert'):
            if a<b:
                begin,end=old[a]['start'],old[b-1]['end']
            else:
                begin=old[a-1]['end'] if a else segment['start']
                end=old[a]['start'] if a<len(old) else segment['end']
            end=max(end,begin+.04*(d-c))
            for j in range(c,d):
                aligned.append({'word':new[j], 'start':begin+(end-begin)*(j-c)/(d-c),
                                'end':begin+(end-begin)*(j-c+1)/(d-c)})
    for w in aligned:
        start,end=remap(w['start']),remap(w['end'])
        if end-start < .001 and w['end']-w['start']>.001:
            dropped.append({'segmento':segment['id'],**w})
            continue
        words.append({'word':w['word'],'start':start,'end':max(start+.025,end),'segment':segment['id']})

groups=[]
current=[]
for word in words:
    trial=current+[word]
    text=' '.join(w['word'] for w in trial)
    if current and (len(text)>78 or len(textwrap.wrap(text,width=42,break_long_words=False,break_on_hyphens=False))>2 or word['end']-current[0]['start']>6):
        groups.append(current)
        current=[]
    current.append(word)
    text=' '.join(w['word'] for w in current)
    if len(text)>=30 and current[-1]['word'].endswith(('.','?','!')) and current[-1]['end']-current[0]['start']>=1.2:
        groups.append(current)
        current=[]
if current: groups.append(current)

captions=[]
for group in groups:
    text=' '.join(w['word'] for w in group)
    lines=textwrap.wrap(text,width=42,break_long_words=False,break_on_hyphens=False)
    assert len(lines)<=2, (text,lines)
    start=max(0,group[0]['start']-.035)
    end=max(start+.7,group[-1]['end']+.12)
    captions.append({'start':start,'end':end,'text':'\n'.join(lines)})
for i,cue in enumerate(captions):
    if i+1<len(captions):
        cue['end']=min(cue['end'],captions[i+1]['start']-.025)
    assert cue['end']>cue['start'], cue
    assert cue['end']<=remap(source['duration'])+.03

# Ajuste editorial de quebra: mantém o sujeito "o computador" junto ao verbo,
# reduzindo a velocidade de leitura da legenda anterior.
for i,cue in enumerate(captions[:-1]):
    flat=cue['text'].replace('\n',' ')
    if flat.startswith('Além de olhar o erro dessa previsão') and flat.endswith('o computador'):
        cue['text']='\n'.join(textwrap.wrap(flat[:-len('o computador')].rstrip(),width=42))
        captions[i+1]['text']='\n'.join(textwrap.wrap('o computador '+captions[i+1]['text'].replace('\n',' '),width=42))
        cue['end']-=.2
        captions[i+1]['start']=cue['end']+.025

def ts(t):
    ms=round(t*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'

srt='\n\n'.join(f"{i+1}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}" for i,c in enumerate(captions))+'\n'
(OUT/'ESNAUTO_apresentacao_v003.srt').write_text(srt,encoding='utf-8-sig')
(QA/'legendas_alinhadas.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2),encoding='utf-8')
spec=importlib.util.spec_from_file_location('orientacoes',QA/'criar_orientacoes.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.create(QA/'orientacoes_final.ass',remap)
mapped=[{**c,'start_final':remap(c['start']),'end_final':remap(c['end'])} for c in module.CUES]
(QA/'orientacoes_final.json').write_text(json.dumps(mapped,ensure_ascii=False,indent=2),encoding='utf-8')
warnings=[{'index':i+1,'cps':len(c['text'].replace('\n',' '))/(c['end']-c['start']),**c}
          for i,c in enumerate(captions) if len(c['text'].replace('\n',' '))/(c['end']-c['start'])>25]
result={'segmentos_revistos':len(review),'legendas':len(captions),'quadros_previstos':44707-sum(c['fim_frame_exclusivo']-c['inicio_frame'] for c in cuts),
        'segundos_retirados':sum(c['fim_frame_exclusivo']-c['inicio_frame'] for c in cuts)/30,
        'palavras_em_cortes':dropped,'legendas_rapidas_para_exame':warnings,
        'duracao_prevista_s':(44707-sum(c['fim_frame_exclusivo']-c['inicio_frame'] for c in cuts))/30}
(QA/'preparacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
