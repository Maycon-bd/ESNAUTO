import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from 'file:///C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const root=process.cwd();
const base=path.join(root,'reports/defesa_20261028');
const out=path.join(base,'entrega');
const skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1025.11240/skills/presentations';
await fs.mkdir(out,{recursive:true});
await fs.mkdir(path.join(base,'build/previews_sem_demo'),{recursive:true});
const data=JSON.parse(await fs.readFile(path.join(base,'build/conteudo_sem_demo.json'),'utf8'));
const total=data.reduce((a,b)=>a+b.seconds,0);
data[data.length-1].seconds-=total-1500;
const p=Presentation.create({slideSize:{width:1280,height:720}});
const ink='#16343C', green='#087E72', gray='#53666C', pale='#F7F8F5';
function text(s,txt,x,y,w,h,size=30,color=ink,bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=txt; sh.text.style={typeface:'Arial',fontSize:size,color,bold};return sh;
}
function table(s,d){
 const vals=[d.headers,...d.rows];
 const widths=d.headers.length===2?[280,856]:d.headers.length===3?[300,650,186]:[500,212,212,212];
 const tb=s.tables.add({rows:vals.length,columns:d.headers.length,left:72,top:185,width:1136,height:365,columnWidths:widths,values:vals});
 for(let r=0;r<vals.length;r++)for(let c=0;c<d.headers.length;c++){
   const cell=tb.getCell(r,c);cell.fill=r===0?ink:(r%2?'#FFFFFF':'#EEF2EF');
   cell.text.style={typeface:'Arial',fontSize:d.headers.length===4?25:27,color:r===0?'#FFFFFF':ink,bold:r===0};
 }
 tb.borders.assign({fill:'#FFFFFF',width:2,style:'solid'});
}
let elapsed=0;let md='# Roteiro do vídeo de apresentação da monografia\n\nMaycon Garcia Silva · Engenharia de Software · UniRV\n\n**Duração planejada: 25 minutos, dedicados à exposição da pesquisa.** Os tempos são metas de ensaio, não uma garantia da duração da leitura. O roteiro fornece a fala principal. Use o tempo restante de cada slide para explicar os dados apontados, fazer pausas e avançar os slides. Ensaiar com cronômetro antes da gravação.\n\nEste roteiro se destina ao vídeo e não inclui demonstração do aplicativo. A demonstração do sistema ficará para a defesa, conforme a orientação do autor.\n\n';
const tm=n=>`${Math.floor(n/60).toString().padStart(2,'0')}:${(n%60).toString().padStart(2,'0')}`;
for(const [i,d] of data.entries()){
 const s=p.slides.add();s.background.fill=i===0?ink:pale;
 if(i===0){
 text(s,'DEFESA DE MONOGRAFIA',72,55,1100,45,24,'#77D9C1',true);
 text(s,d.title,72,145,1120,270,48,'#FFFFFF',true);
 text(s,d.body.join('\n'),72,463,1136,180,25,'#FFFFFF');
 }else{
 text(s,d.title,72,58,1136,102,43,ink,true);
 text(s,String(i+1).padStart(2,'0'),1180,655,50,25,19,gray);
 if(d.kind==='table') table(s,d);
 else if(d.kind==='chart'){
   const ch=s.charts.add('bar',{position:{left:90,top:177,width:1090,height:380},categories:['ESN','GRU','LSTM'],series:[{name:'MAE',values:[0.328850012455254,0.418175291762921,0.466612261009447],fill:green},{name:'RMSE',values:[0.498452314212457,0.592452440069539,0.635287229246294],fill:'#8AACC0'}],barOptions:{direction:'column',grouping:'clustered',gapWidth:140},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:23}},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.000',textStyle:{fontSize:23}},xAxis:{textStyle:{fontSize:26}},yAxis:{min:0,max:0.75,majorUnit:0.25,numberFormatCode:'0.00',textStyle:{fontSize:20},title:'Erro na escala do preço ajustado',majorGridlines:{fill:'#D6DEDA',width:1}}});
   const {applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);applyPresentationChartFont(ch,{fontFamily:'Arial'});
 }else if(d.kind==='big'){
   d.numbers.forEach(([n,label],j)=>{text(s,n,72+j*585,190,535,115,78,green,true);text(s,label,72+j*585,325,525,150,31,ink);});
 }else{
   const lines=d.body??[];const step=lines.length<=3?118:94;
   lines.forEach((line,j)=>text(s,line,85,185+j*step,1090,step-12,31,j===0?green:ink,j===0));
 }
 if(d.callout)text(s,d.callout,72,590,1115,55,23,gray);
 }
 const timing=`${tm(elapsed)}–${tm(elapsed+d.seconds)} (${d.seconds} s)`;
 s.speakerNotes.text=`SLIDE ${i+1} · ${timing}\n\n${d.notes}\n\nFONTES\n${d.source}\nDocumento principal: reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx.`;
 md+=`## Slide ${i+1} — ${d.title}\n\n**Tempo: ${timing}**\n\n${d.notes}\n\n`;
 elapsed+=d.seconds;
 const png=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(base,`build/previews_sem_demo/slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 console.log(`Slide ${i+1} renderizado`);
}
md+='## Perguntas prováveis da banca\n\n**O título permite atribuir ganho ao Fator de Ajuste?**\nO fator integra o pré-processamento. Sem ablação com e sem ajuste, a pesquisa não isola sua contribuição causal para o erro.\n\n**Por que usar ESN?**\nEla permite ajustar a saída por Ridge mantendo o reservatório fixo. O protocolo investigou se essa arquitetura, depois de configurada, produziria erro competitivo com baixo custo de ajuste.\n\n**Os p-valores se aplicam às 45 execuções históricas?**\nNão. Os testes usam exclusivamente a rodada controlada com novas matrizes, semente 20260926 e 1.298 datas comuns.\n\n**O GA torna injusta a comparação com GRU e LSTM?**\nO orçamento de otimização foi assimétrico. A evidência vale para as configurações estudadas, sem provar superioridade arquitetural sob orçamento igual. Uma continuação deve controlar esse orçamento.\n\n**LHS e cataclismo melhoraram o resultado?**\nForam implementados, mas não houve ablação para medir seu efeito isolado. O mecanismo é inspirado no CHC e não corresponde à implementação integral do algoritmo.\n\n**Qual a diferença entre 1.299 e 1.298 previsões?**\nO teste completo contém 1.299 previsões por modelo. A janela DM previamente definida usa 1.298 datas comuns, de 30/09/2015 a 30/12/2020.\n\n**O resultado produz lucro?**\nNão houve avaliação de estratégia, retorno líquido ou custos de transação. As métricas descrevem erro de previsão de preços.\n\n**Qual a referência simples que falta ampliar?**\nA comparação sistemática com persistência é uma continuação importante, especialmente porque preços em nível têm forte dependência temporal.\n\n**O sistema é o resultado principal?**\nO resultado central é a avaliação experimental descrita na monografia. O ESNAUTO é a contribuição de software que organiza e automatiza esse processo.\n\n## Referências para consulta durante o ensaio\n\n- Silva, Maycon Garcia. Monografia PETR4 padronizada FASOFT, 2026, capítulos 1, 3–6.\n- Jaeger, H. Echo state network. Scholarpedia, 2007. Referência conceitual citada na monografia.\n- Diebold, F. X.; Mariano, R. S. Comparing Predictive Accuracy. Journal of Business & Economic Statistics, 1995. Método citado na monografia.\n- Registros primários da rodada controlada: manifesto, métricas da janela DM, previsões datadas e resultados DM, semente 20260926.\n\n## Procedência dos números\n\nOs resultados históricos dos slides 7 e 9–12 seguem a consolidação da monografia e os documentos das ondas. O CSV histórico atual não contém as 45 execuções, portanto não foi possível reconferir integralmente essa consolidação em registros primários. Os slides 13–15 usam os arquivos preservados da rodada controlada. Nenhum experimento foi reexecutado para preparar esta apresentação. As fontes específicas também estão nas notas de cada slide.\n';
await fs.writeFile(path.join(out,'MayconGarciaSilva_Roteiro_Video_sem_demonstracao.md'),md);
await fs.writeFile(path.join(base,'build/cronograma_sem_demo.json'),JSON.stringify(data.map((d,i)=>({slide:i+1,seconds:d.seconds,title:d.title})),null,2));
const draft=path.join(base,'build/candidate_sem_demo.pptx');await(await PresentationFile.exportPptx(p)).save(draft);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
await finalizePresentation({workspaceDir:root,candidatePath:draft,finalPath:path.join(out,'MayconGarciaSilva_Apresentacao_sem_demonstracao.pptx'),pythonExecutable:'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...[6,7,9,15,16].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:19,requiredNativeTableOwnerSlides:[6,7,9,15,16],requiredNativeChartOwnerSlides:[14],fontPolicy:{basis:'design',families:['Arial']},materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:path.join(base,'build/validacao_sem_demo.json')});
console.log('PPTX finalizado. Tempo total:',elapsed);



