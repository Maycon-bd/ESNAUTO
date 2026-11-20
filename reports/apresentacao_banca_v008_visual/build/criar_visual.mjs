import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from 'file:///C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import {applyPresentationChartFont} from 'file:///C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations/container_tools/artifact_tool_utils.mjs';
const build=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(await fs.readFile(path.join(build,'conteudo.json'),'utf8'));
const monthly=JSON.parse(await fs.readFile(path.join(build,'serie_mensal.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={paper:'#FAFAF7',ink:'#142B3B',muted:'#536575',accent:'#087E83',gold:'#C48A32',white:'#FFFFFF',line:'#D4DCDF',pale:'#EEF3F2'};
function txt(s,text,x,y,w,h,size=30,color=C.ink,bold=false,name){
 let a=s.shapes.add({geometry:'textbox',name:name??`text-${s.shapes.items.length}`,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 a.text=text;a.text.style={typeface:'Arial',fontSize:size,color,bold,insets:0,wrap:'square'};return a;
}
function nav(s,label,target,x,y,w=90,dark=false){
 const a=s.shapes.add({geometry:'rect',name:`nav-${target}-${s.shapes.items.length}`,position:{left:x,top:y,width:w,height:32},fill:dark?'#25485B':C.pale,line:{fill:'none',width:0}});
 a.text=label;a.text.style={typeface:'Arial',fontSize:17,color:dark?C.white:C.accent,bold:true,insets:{left:9,right:9,top:5,bottom:4},alignment:'center'};return a;
}
function bars(s,categories,values,{x=76,y=195,w=1128,h=355,max=1,unit=.2,format='0.000000',horizontal=false,colors=true,seriesName='Valor',labelSize=24}={}){
 const c=s.charts.add('bar',{position:{left:x,top:y,width:w,height:h},categories,
  series:[{name:seriesName,values,fill:C.accent,...(colors?{points:values.map((_,idx)=>({idx,fill:[C.accent,'#708596','#A1ADB6',C.gold,'#5AA8A2'][idx%5]}))}:{})}],
  hasLegend:false,barOptions:{direction:horizontal?'bar':'column',grouping:'clustered',gapWidth:75},chartFill:C.paper,plotAreaFill:C.paper,
  xAxis:{textStyle:{fontSize:labelSize,fill:C.ink},line:{fill:C.line,width:1}},
  yAxis:{min:0,max,majorUnit:unit,numberFormatCode:format==='0'?'0':'0.0',textStyle:{fontSize:20,fill:C.muted},majorGridlines:{fill:C.line,width:1}},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:format,textStyle:{fontSize:25,fill:C.ink}}});
 applyPresentationChartFont(c,{fontFamily:'Arial'});return c;
}
function nativeTable(s,values,widths,y=210){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:76,top:y,width:1128,height:values.length*65,columnWidths:widths,values});
 t.borders.assign({fill:C.line,width:1,style:'solid'});
 values.forEach((row,r)=>{t.rows[r].height=65;row.forEach((_,c)=>{const z=t.getCell(r,c);z.fill=r===0?C.ink:r%2===0?C.pale:C.white;z.text.style={typeface:'Arial',fontSize:25,color:r===0?C.white:C.ink,bold:r===0,alignment:c===0?'left':'center',verticalAlignment:'middle',insets:12};});});return t;
}
for(const d of data){
 const s=p.slides.add();s.background.fill=C.paper;
 const dark=d.number===1||d.number===23;if(dark)s.background.fill=C.ink;
 if(d.number===1){
  txt(s,'ESNAUTO',76,52,1100,45,31,'#83D8D2',true);
  txt(s,d.title,76,145,1128,150,58,C.white,true);
  txt(s,d.body[0],76,330,1100,90,37,'#CFE1E8');
  txt(s,d.body[1]+'\n'+d.body[2],76,485,1100,80,26,C.white);
  txt(s,d.body[3],76,590,1100,34,22,'#CFE1E8');
  [['Problema',2],['Método',5],['Resultados',12],['Conclusão',23]].forEach(([l,n],i)=>nav(s,l,n,76+i*215,650,190,true));
 }else{
  txt(s,d.title,76,48,1128,100,44,dark?C.white:C.ink,true);
  switch(d.number){
   case 2:{
    txt(s,'PETR4 · fechamento ajustado',76,150,850,45,28,C.accent,true);
    const c=s.charts.add('line',{position:{left:65,top:215,width:1140,height:335},categories:monthly.map(x=>x[0].endsWith('-12-30')?x[0].slice(0,4):x[0].slice(0,4)),series:[{name:'Fechamento ajustado (R$)',values:monthly.map(x=>x[1]),line:{fill:C.accent,width:3},marker:{symbol:'none'}}],hasLegend:false,chartFill:C.paper,plotAreaFill:C.paper,xAxis:{textStyle:{fontSize:18,fill:C.muted},line:{fill:C.line,width:1}},yAxis:{min:0,numberFormatCode:'0',title:{text:'R$',textStyle:{fontSize:20}},textStyle:{fontSize:20},majorGridlines:{fill:C.line,width:1}}});applyPresentationChartFont(c,{fontFamily:'Arial'});
    txt(s,'Prever o próximo fechamento e avaliar erro e custo',76,578,1128,60,31,C.ink,true);
    txt(s,'Visualização: último fechamento disponível de cada mês, 2000–2020',76,635,1128,30,20,C.muted);break;
   }
   case 3:{
    txt(s,'Investigar ESNs otimizadas na previsão da PETR4',76,155,1128,75,35,C.accent,true);
    [['H1','Desempenho',16],['H2','Custo de ajuste',18],['H3','Inicialização',13],['H4','Exploração evolutiva',7],['H5','Ajuste empírico',8]].forEach(([h,l,n],i)=>{
     const y=260+i*70;nav(s,h,n,76,y,65);txt(s,l,175,y,1000,50,30);
    });break;
   }
   case 4:{
    bars(s,['Documentos da coleção','Com palavras-chave'],[34,24],{max:40,unit:10,format:'0',x:70,y:205,w:685,h:360,labelSize:21});
    txt(s,'34',830,205,340,95,84,C.accent,true);txt(s,'documentos recuperados',830,310,360,85,30);
    txt(s,'Buscas complementares\nCobertura delimitada',830,440,360,115,26,C.muted);
    txt(s,'Fundamentos: ESN, otimização e séries ajustadas',76,605,1128,45,30,C.ink,true);break;
   }
   case 5:{
    txt(s,'5.198',76,150,600,100,87,C.accent,true);txt(s,'observações em ordem cronológica',460,185,730,50,31);
    const c=s.charts.add('bar',{position:{left:65,top:285,width:1140,height:200},categories:['Série PETR4'],series:[{name:'Treino',values:[2600],fill:C.accent},{name:'Validação',values:[1299],fill:'#708596'},{name:'Teste',values:[1299],fill:C.gold}],barOptions:{direction:'bar',grouping:'stacked',overlap:100,gapWidth:45},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:24}},chartFill:C.paper,plotAreaFill:C.paper,xAxis:{visible:false},yAxis:{visible:false,min:0,max:5198},dataLabels:{showValue:true,position:'center',numberFormatCode:'#,##0',textStyle:{fontSize:30,fill:C.white}}});applyPresentationChartFont(c,{fontFamily:'Arial'});
    [['Treino','03/01/2000 a 01/07/2010'],['Validação','02/07/2010 a 28/09/2015'],['Teste','29/09/2015 a 30/12/2020']].forEach(([a,b],i)=>{txt(s,a,76+i*385,505,365,40,28,C.ink,true);txt(s,b,76+i*385,553,365,65,23,C.muted);});
    txt(s,'Dados recebidos já ajustados pelo orientador',76,630,1128,35,23,C.muted);break;
   }
   case 6:{
    [['Win','Entrada','Transforma a série recebida'],['W','Reservatório','Mantém a dinâmica recorrente'],['Wout','Saída','Estima o valor previsto']].forEach(([a,b,c],i)=>{const x=76+i*385;txt(s,a,x,180,350,105,80,C.accent,true);txt(s,b,x,325,350,50,32,C.ink,true);txt(s,c,x,402,350,100,29,C.muted);});
    txt(s,'Win e W fixas no ajuste · Wout estimada por Ridge',76,585,1128,65,32,C.ink,true);break;
   }
   case 7:{
    txt(s,'Cromossomo de 55 bits',76,150,1128,55,34,C.accent,true);
    bars(s,['Vazamento','Raio espectral','Descarte inicial','Reservatório','Ridge'],[17,17,7,5,9],{x:70,y:240,w:1140,h:315,max:20,unit:5,format:'0',labelSize:22,seriesName:'Bits'});
    txt(s,'Cinco hiperparâmetros · LHS e mecanismo cataclísmico no motor atual',76,595,1128,65,28,C.ink,true);break;
   }
   case 8:{
    bars(s,['Caudas\npesadas','Choques e\nassimetria','Esparsidade','Controles','Ajustes\nempíricos'],[9,9,6,6,15],{y:225,h:345,max:18,unit:3,format:'0',labelSize:23,seriesName:'Execuções'});
    txt(s,'45 execuções históricas em cinco ondas',76,150,1128,48,32,C.accent,true);
    txt(s,'A × B identifica as distribuições de Win e W, nessa ordem',76,610,1128,45,26,C.muted);break;
   }
   case 9:{
    [['45','Histórico','Cinco ondas, comparação descritiva',12],['DM','Complementar','Novos pesos e semente fixa',15],['200','Ilustrativo','Gerações no lote legado, fora das 45',14]].forEach(([a,b,c,n],i)=>{const x=76+i*385;txt(s,a,x,175,350,112,85,C.accent,true);nav(s,b,n,x,335,330);txt(s,c,x,410,350,135,29,C.muted);});
    txt(s,'Cada bloco conserva seu protocolo e seus resultados',76,605,1128,48,31,C.ink,true);break;
   }
   case 10:{
    txt(s,'ESNAUTO',76,170,1128,110,88,C.accent,true);
    txt(s,'Configuração e execução dos modelos',76,330,1128,60,34,C.ink,true);
    txt(s,'Métricas, histórico e visualizações',76,415,1128,60,34,C.ink,true);
    txt(s,'Adaptação das rotinas recebidas e desenvolvimento da interface',76,555,1128,85,30,C.muted);break;
   }
   case 11:{
    [['MAE','Média dos erros em módulo'],['RMSE','Maior peso para desvios elevados'],['R²','Aderência global da previsão']].forEach(([a,b],i)=>{txt(s,a,76,170+i*130,260,80,62,C.accent,true);txt(s,b,390,190+i*130,800,65,33);});
    txt(s,'Tempo de busca e tempo de ajuste avaliados separadamente',76,605,1128,50,28,C.muted);break;
   }
   case 12:{
    txt(s,'MAE histórico (R$)',76,150,1128,48,32,C.accent,true);
    bars(s,['ESN Laplace × Normal','GRU','LSTM'],[.327224,.356600,.452100],{y:225,h:340,max:.6,unit:.2,labelSize:25});
    txt(s,'44 de 45 ESNs com MAE menor que os comparadores documentados',76,598,1128,50,28,C.ink,true);
    txt(s,'Comparação descritiva · orçamentos de otimização distintos',76,643,1128,28,20,C.muted);break;
   }
   case 13:{
    bars(s,['Normal × Normal','Laplace × Normal'],[.328365,.327224],{x:65,y:220,w:750,h:345,max:.4,unit:.1,labelSize:24});
    txt(s,'0,347%',860,245,350,95,65,C.accent,true);txt(s,'redução observada\nno MAE histórico',860,360,350,90,29);
    txt(s,'Laplace × Cauchy: menor RMSE histórico, 0,495386',76,610,1128,45,28,C.muted);break;
   }
   case 14:{
    const bytes=await fs.readFile(path.join(build,'fig_p401.png'));s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:'Preços observados e previstos do lote ilustrativo preservado',fit:'contain',position:{left:160,top:143,width:960,height:500}});
    txt(s,'GED × Uniforme · lote ilustrativo de 200 gerações, separado do histórico e do DM',76,645,1128,30,20,C.muted);break;
   }
   case 15:{
    txt(s,'1.298',76,180,670,125,110,C.accent,true);txt(s,'datas comuns para comparação',76,335,660,90,37,C.ink,true);
    txt(s,'30/09/2015 a 30/12/2020',76,455,650,55,28,C.muted);
    txt(s,'Semente 20260926\nNovos pesos\n1.299 previsões por modelo',800,205,405,205,29);
    txt(s,'Alvos de treino e continuidade temporal verificados',76,605,1128,55,30,C.ink,true);break;
   }
   case 16:{
    for(const [x,title,vals,max] of [[65,'MAE (R$)',[.328850,.418175,.466612],.6],[675,'RMSE (R$)',[.498452,.592452,.635287],.8]]){txt(s,title,x+30,175,500,45,29,C.ink,true);bars(s,['ESN','GRU','LSTM'],vals,{x,y:235,w:535,h:320,max,unit:.2,labelSize:25});}
    txt(s,'Menor erro para a ESN nesta execução controlada',76,605,1128,55,31,C.accent,true);break;
   }
   case 17:{
    nativeTable(s,d.table,[450,320,358],200);
    txt(s,'Menor perda média para a ESN nos quatro contrastes',76,555,1128,50,30,C.accent,true);
    txt(s,'Uma semente · α individual de 5% · sem ajuste de multiplicidade',76,615,1128,45,25,C.muted);break;
   }
   case 18:{
    txt(s,'Ajuste do modelo selecionado (s)',76,155,775,50,30,C.ink,true);
    bars(s,['ESN','GRU','LSTM'],[.05,28.8,35.4],{x:65,y:235,w:730,h:315,max:40,unit:10,format:'0.00',labelSize:25});
    txt(s,'37,9 h',850,215,360,95,64,C.gold,true);txt(s,'nas 45 buscas\ngenéticas',850,330,360,100,31);
    txt(s,'Busca por cenário\n21 a 102 minutos',850,475,360,110,26,C.muted);
    txt(s,'O baixo custo de ajuste ocorre após a busca da configuração',76,615,1128,50,28,C.ink,true);break;
   }
   case 19:{
    [['H1','Apoio descritivo e inferencial complementar',16],['H2','Apoio para o custo de ajuste selecionado',18],['H3','Apoio pontual nas configurações observadas',13],['H4','Efeito de exploração não demonstrado',7],['H5','Baixa dispersão descritiva, sem estabilidade entre sementes demonstrada',8]].forEach(([h,t,n],i)=>{const y=175+i*92;nav(s,h,n,76,y,65);txt(s,t,175,y,1000,85,30,i<3?C.accent:C.muted,i<3);});break;
   }
   case 20:{
    txt(s,'Contribuição experimental',76,175,1128,55,37,C.accent,true);txt(s,'Avaliação documentada das configurações para a PETR4',76,250,1128,70,31);
    txt(s,'Contribuição de Engenharia de Software',76,385,1128,60,37,C.accent,true);txt(s,'Adaptação, interface e organização dos artefatos',76,460,1128,70,31);
    txt(s,'Atribuições e limites documentados na monografia',76,610,1128,50,26,C.muted);break;
   }
   case 22:{
    txt(s,'Próximos experimentos',76,170,1128,55,37,C.accent,true);txt(s,'Persistência, sementes e ablações\nOrçamentos comparáveis entre arquiteturas',76,245,1128,125,32);
    txt(s,'JANUS',76,430,540,90,65,C.ink,true);txt(s,'Evolução do software',76,535,540,55,30,C.muted);
    txt(s,'VALE3',735,430,480,90,65,C.ink,true);txt(s,'Continuidade experimental',735,535,480,65,30,C.muted);break;
   }
   default:{
    let y=180;const n=d.body.length;d.body.forEach((b,i)=>{txt(s,String(i+1).padStart(2,'0'),76,y+5,65,45,27,dark?'#83D8D2':C.accent,true);txt(s,b,171,y,1015,n===5?78:95,n===5?30:33,dark?C.white:C.ink);y+=n===5?85:105;});
   }
  }
  txt(s,`Fonte: monografia v008${[15,16,17].includes(d.number)?' e registros PETR4-DM':''}`,76,687,800,23,16,dark?'#CFE1E8':C.muted);
  nav(s,'Início',1,895,678,90,dark);
  if(d.number>1)nav(s,'Anterior',d.number-1,992,678,98,dark);
  if(d.number<23)nav(s,'Próximo',d.number+1,1097,678,98,dark);
 }
 txt(s,String(d.number).padStart(2,'0'),1220,683,40,25,18,dark?'#CFE1E8':C.muted);
 s.speakerNotes.text=`${d.window} | Duração planejada ${d.seconds} s\n\n${d.speech}\n\nFonte e rastreabilidade: ${d.source}\nBase v008 SHA256 0daacd3ea1753bca97619df025923b92a44a047b5c1252a4677f802dfe870dad.\nOperação: transição por clique. A navegação e os atalhos H1–H5 funcionam no modo Apresentação de Slides. Para a gravação de 25 minutos, seguir a ordem numérica sem usar atalhos.`;
}
await fs.mkdir(path.join(build,'previews'),{recursive:true});
for(let i=0;i<p.slides.items.length;i++){
 const png=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(build,'previews',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
await (await PresentationFile.exportPptx(p)).save(path.join(build,'visual_sem_efeitos.pptx'));
await fs.writeFile(path.join(build,'presentation.json'),JSON.stringify(p.toProto()));
console.log('23 slides exportados com 11 gráficos nativos');
