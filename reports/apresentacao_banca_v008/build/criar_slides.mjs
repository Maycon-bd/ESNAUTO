import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from 'file:///C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import { finalizePresentation, applyPresentationChartFont } from 'file:///C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations/container_tools/artifact_tool_utils.mjs';

const build=path.dirname(fileURLToPath(import.meta.url));
process.env.RUNTIME_NODE_MODULES='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const workspaceDir=path.dirname(build);
const skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations';
const data=JSON.parse(await fs.readFile(path.join(build,'conteudo.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={paper:'#FAFAF7',ink:'#142B3B',muted:'#536575',accent:'#087E83',white:'#FFFFFF',line:'#D4DCDF',pale:'#EEF3F2'};
function txt(s,text,x,y,w,h,size=30,color=C.ink,bold=false){
 const a=s.shapes.add({geometry:'textbox',name:`text-${s.shapes.items.length}`,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 a.text=text;
 a.text.style={typeface:'Arial',fontSize:size,color,bold,alignment:'left',verticalAlignment:'top',insets:{left:0,right:0,top:0,bottom:0},wrap:'square'};
 return a;
}
function table(s,values,y=210,widths){
 const rows=values.length,cols=values[0].length;
 const height=Math.min(370,rows*64);
 const t=s.tables.add({rows,columns:cols,left:76,top:y,width:1128,height,columnWidths:widths??Array(cols).fill(1128/cols),values});
 t.borders.assign({style:'solid',fill:C.line,width:1});
 for(let r=0;r<rows;r++){
  t.rows[r].height=height/rows;
  for(let c=0;c<cols;c++){
   const cell=t.getCell(r,c);cell.fill=r===0?C.ink:(r%2===0?C.pale:C.white);
   cell.text.style={typeface:'Arial',fontSize:25,color:r===0?C.white:C.ink,bold:r===0,verticalAlignment:'middle',alignment:c===0?'left':'center',insets:{left:14,right:14,top:9,bottom:8}};
  }
 }
 return t;
}
function chart(s,title,x,values,max){
 const c=s.charts.add('bar',{
  position:{left:x,top:235,width:535,height:305},
  categories:['ESN','GRU','LSTM'],
  series:[{name:title,values,fill:C.accent,points:[{idx:1,fill:'#708596'},{idx:2,fill:'#A1ADB6'}]}],
  hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:110},
  chartFill:C.paper,plotAreaFill:C.paper,
  xAxis:{textStyle:{fontSize:23,fill:C.ink},line:{fill:C.line,width:1}},
  yAxis:{min:0,max,majorUnit:0.2,numberFormatCode:'0.0',textStyle:{fontSize:20,fill:C.muted},majorGridlines:{fill:C.line,width:1}},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.000000',textStyle:{fontSize:21,fill:C.ink}},
 });
 applyPresentationChartFont(c,{fontFamily:'Arial'});
 txt(s,title+' (R$)',x+40,183,440,40,27,C.ink,true);
 return c;
}
for(const d of data){
 const s=p.slides.add();s.background.fill=C.paper;
 const dark=d.kind==='cover'||d.number===23;
 if(dark)s.background.fill=C.ink;
 const fg=dark?C.white:C.ink;
 if(d.kind==='cover'){
  txt(s,'ESNAUTO',76,58,1000,48,30,'#83D8D2',true);
  txt(s,d.title,76,155,1100,150,58,C.white,true);
  txt(s,d.body[0],76,340,1060,90,37,'#CFE1E8');
  txt(s,d.body[1]+'\n'+d.body[2],76,512,1100,86,26,C.white);
  txt(s,d.body[3],76,637,1100,35,21,'#CFE1E8');
 }else{
  txt(s,d.title,76,52,1128,105,44,fg,true);
  if(d.kind==='table'){
   txt(s,d.body[0],76,157,1128,49,27,C.accent,true);
   const widths=d.number===8?[125,800,203]:d.number===12?[470,220,220,218]:[450,320,358];
   table(s,d.table,d.number===8?225:225,widths);
   const rest=d.body.slice(1);
   if(rest.length)txt(s,rest.join('\n'),76,rowsBottom(d.table)+24,1120,75,23,C.muted);
  }else if(d.kind==='split'){
   txt(s,d.body[0],76,161,1128,45,29,C.accent,true);
   table(s,d.table,240,[210,200,718]);
   txt(s,d.body.slice(1).join('\n'),76,550,1120,90,26,C.muted);
  }else if(d.kind==='charts'){
   txt(s,d.body[0],76,151,1100,40,28,C.accent,true);
   chart(s,'MAE',60,[0.328850,0.418175,0.466612],0.6);
   chart(s,'RMSE',675,[0.498452,0.592452,0.635287],0.8);
   txt(s,d.body[1],76,590,1128,50,28,C.ink,true);
  }else if(d.kind==='image'){
   const b=await fs.readFile(path.join(build,d.image));
   s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',alt:'Figura 6 da monografia: série observada e prevista, com detalhe dos últimos 100 pregões',fit:'contain',position:{left:160,top:143,width:960,height:500}});
   txt(s,'GED × Uniforme · lote ilustrativo de 200 gerações, separado do histórico e do DM',76,648,1128,28,20,C.muted);
  }else if(d.kind==='comparison'){
   txt(s,'Menor MAE histórico',76,175,490,42,27,C.muted);
   txt(s,'0,327224',76,237,560,95,78,C.accent,true);
   txt(s,'Laplace × Normal',76,345,500,45,31,C.ink,true);
   txt(s,'Referência Normal × Normal',710,188,480,80,28,C.muted);
   txt(s,'0,328365',710,278,480,75,56,C.ink,true);
   txt(s,'Redução observada: 0,347%',76,470,1128,55,33,C.ink,true);
   txt(s,d.body[3],76,552,1128,50,28,C.muted);
  }else{
   let y=179;const n=d.body.length;const step=n===5?85:105;
   d.body.forEach((b,i)=>{
    txt(s,String(i+1).padStart(2,'0'),76,y+4,65,45,27,dark?'#83D8D2':C.accent,true);
    txt(s,b,171,y,1015,n===5?77:90,n===5?30:33,fg,false);
    y+=step;
   });
  }
  const visibleSource=d.number===4?'Fonte: monografia v008, cap. 2 e seção 3.8.3':d.number===14?'Fonte: monografia v008, Figura 6':`Fonte: monografia v008${d.number>=15&&d.number<=17?' e registros PETR4-DM':''}`;
  txt(s,visibleSource,76,684,1050,23,17,dark?'#CFE1E8':C.muted);
 }
 txt(s,String(d.number).padStart(2,'0'),1195,681,45,26,19,dark?'#CFE1E8':C.muted);
 s.speakerNotes.text=`${d.window} | Duração planejada: ${d.seconds} segundos\n\n${d.speech}\n\nFonte e rastreabilidade: ${d.source}\nBase: v008, SHA256 0daacd3ea1753bca97619df025923b92a44a047b5c1252a4677f802dfe870dad. ${d.proposed?'As propostas complementares são possibilidades de continuidade, não resultados realizados.':''}`;
}
function rowsBottom(values){return 225+Math.min(370,values.length*64);}
await fs.mkdir(path.join(build,'previews'),{recursive:true});
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];
 const png=await p.export({slide,format:'png',scale:1});
 await fs.writeFile(path.join(build,'previews',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 console.log('Render',i+1);
}
await fs.writeFile(path.join(build,'presentation.json'),JSON.stringify(p.toProto()));
const draft=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(draft);
const result=await finalizePresentation({
 workspaceDir,candidatePath:draft,finalPath:path.join(workspaceDir,'entrega/Apresentacao_ESNAUTO_banca_v008.pptx'),
 pythonExecutable:'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[5,8,12,17].flatMap(n=>['--require-native-table-slide',String(n)])],
 explicitTotalSlideCount:23,requiredNativeTableOwnerSlides:[5,8,12,17],requiredNativeChartOwnerSlides:[16],
 materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,
 receiptPath:path.join(build,'validacao_slides.json')
});
console.log(JSON.stringify(result));
