"""Setas, contornos e rótulos discretos sobre a demonstração gravada."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CUES = [
    {'start': 650.2, 'end': 656.0, 'text': '1 · Dados da ação\ne divisão temporal',
     'label': [1000, 550, 430, 90], 'rect': [110, 350, 770, 160], 'arrow': [1000, 550, 880, 510]},
    {'start': 664.0, 'end': 667.0, 'text': '2 · Escolha das\ndistribuições',
     'label': [35, 405, 315, 100], 'rect': [425, 445, 920, 135], 'arrow': [350, 455, 425, 505]},
    {'start': 672.4, 'end': 675.8, 'text': '3 · Cataclismo\nAtivação opcional',
     'label': [35, 430, 315, 100], 'rect': [422, 447, 900, 47], 'arrow': [350, 480, 422, 470]},
    {'start': 677.1, 'end': 680.4, 'text': '4 · Perfil de treino\nGRU e LSTM',
     'label': [35, 600, 315, 100], 'rect': [406, 594, 680, 202], 'arrow': [350, 650, 406, 694]},
    {'start': 681.4, 'end': 683.5, 'text': '5 · Iniciar\nbenchmark',
     'label': [1540, 800, 330, 100], 'rect': [1260, 896, 238, 73], 'arrow': [1540, 850, 1498, 929]},
    {'start': 690.0, 'end': 697.4, 'text': '6 · Resumo\nÚltima execução',
     'label': [35, 575, 315, 100], 'rect': [405, 442, 1090, 307], 'arrow': [350, 625, 405, 625]},
]

def timestamp(t):
    cs = round(t*100)
    return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'

def create(path, time_map=lambda t:t):
    lines = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080',
        'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Default,Segoe UI,28,&H00FFFFFF,&H00FFFFFF,&H000F2818,&H000F2818,-1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1',
        '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    for cue in CUES:
        start,end = timestamp(time_map(cue['start'])),timestamp(time_map(cue['end']))
        def event(layer, text):
            lines.append(f'Dialogue: {layer},{start},{end},Default,,0,0,0,,{text}')
        x,y,w,h = cue['label']
        event(1, f'{{\\an7\\pos({x},{y})\\fad(140,140)\\p1\\1c&H332015&\\1a&H08&}}m 0 0 l {w} 0 {w} {h} 0 {h}')
        event(2, f'{{\\an7\\pos({x},{y})\\fad(140,140)\\p1\\1c&HA8B710&}}m 0 0 l 5 0 5 {h} 0 {h}')
        text=cue['text'].replace('\n','\\N')
        event(3, f'{{\\an7\\pos({x+18},{y+12})\\fad(140,140)\\fs28\\1c&HFFFFFF&\\p0}}{text}')
        rx,ry,rw,rh=cue['rect']
        event(1, f'{{\\an7\\pos({rx},{ry})\\fad(140,140)\\p1\\1a&HFF&\\3a&H00&\\3c&HA8B710&\\bord3}}m 0 0 l {rw} 0 {rw} {rh} 0 {rh} 0 0')
        ax,ay,bx,by=cue['arrow']
        dx,dy=bx-ax,by-ay
        length=math.hypot(dx,dy)
        ux,uy=dx/length,dy/length
        nx,ny=-uy,ux
        points=[(ax+nx*2.5,ay+ny*2.5),(bx-ux*17+nx*2.5,by-uy*17+ny*2.5),
                (bx-ux*17+nx*9,by-uy*17+ny*9),(bx,by),
                (bx-ux*17-nx*9,by-uy*17-ny*9),(bx-ux*17-nx*2.5,by-uy*17-ny*2.5),
                (ax-nx*2.5,ay-ny*2.5)]
        vector='m '+' l '.join(f'{px:.1f} {py:.1f}' for px,py in points)
        event(2,f'{{\\an7\\pos(0,0)\\fad(140,140)\\p1\\1c&HA8B710&}}{vector}')
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')

if __name__=='__main__':
    create(ROOT/'orientacoes_base.ass')
    (ROOT/'orientacoes_base.json').write_text(json.dumps(CUES,ensure_ascii=False,indent=2),encoding='utf-8')
