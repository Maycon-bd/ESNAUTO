param([ValidateSet('map','final','base','decl')][string]$Stage='map')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$taskRoot='C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\declaracao_ia_reescrita_20261102'
$taskFile='C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\monografia\trabalho\declaracao_ia_reescrita_20261102.docx'
if($Stage -eq 'base'){$taskFile='C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\monografia\versoes\v011\MayconGarciaSilva_monografia_v011.docx'}
if($Stage -eq 'decl'){$taskFile=Join-Path $taskRoot 'entrega\Declaracao_responsabilidade_coletiva_Maycon_reescrita.docx'}
$taskTarget=Join-Path $taskRoot ('word_'+$Stage)
New-Item -ItemType Directory -Path $taskTarget -Force|Out-Null
$taskWord=New-Object -ComObject Word.Application
$taskWord.Visible=$false;$taskWord.DisplayAlerts=0
try {
 $taskWord.WordBasic.FilePrintSetup('Microsoft Print to PDF',0,0,1)
 $taskDoc=$taskWord.Documents.Open($taskFile,$false,$true,$false)
 $taskDoc.ActiveWindow.View.Type=3;$taskDoc.Repaginate()
 $taskCount=$taskDoc.ComputeStatistics(2)
 Write-Output ('Paginas '+$taskCount+'; etapa '+$Stage)
 $taskItems=@()
 if($Stage -in @('map','final')) {
  foreach($taskP in $taskDoc.Paragraphs) {
   $taskText=$taskP.Range.Text.Trim([char]13,[char]7,[char]12).Trim()
   $taskStyle=$taskP.Style.NameLocal
   if($taskStyle -in @('TITULO TCC','SEÇÃO TCC','SUBÇÃO 2') -or ($taskText -match '^(Figura|Quadro|Tabela)\s+\d+\s*[–-]' -and $taskStyle -notlike 'toc*') -or $taskText -eq 'ANEXO' -or $taskText -like 'ANEXO A *' -or ($taskText -eq 'REFERÊNCIAS')) {
    $taskRange=$taskP.Range.Duplicate;$taskRange.Collapse(1)
    $taskItems+=@{title=$taskText;style=$taskStyle;number=$taskP.Range.ListFormat.ListString;page=$taskRange.Information(1);physicalPage=$taskRange.Information(3)}
   }
  }
  @{items=$taskItems;pages=$taskCount;file=$taskFile}|ConvertTo-Json -Depth 6|Set-Content (Join-Path $taskRoot ('mapa_'+$Stage+'.json')) -Encoding utf8
  Write-Output ('Localizadores '+$taskItems.Count)
 }
 if($Stage -ne 'map') {
  $taskPages=$taskDoc.ActiveWindow.Panes.Item(1).Pages
  for($taskI=1;$taskI -le $taskPages.Count;$taskI++) {
   [byte[]]$taskBytes=$taskPages.Item($taskI).EnhMetaFileBits
   $taskStream=New-Object IO.MemoryStream(,$taskBytes);$taskImage=[Drawing.Image]::FromStream($taskStream)
   $taskBmp=New-Object Drawing.Bitmap(1240,1754);$taskG=[Drawing.Graphics]::FromImage($taskBmp)
   $taskG.Clear([Drawing.Color]::White);$taskG.DrawImage($taskImage,0,0,1240,1754)
   $taskBmp.Save((Join-Path $taskTarget ('page-'+$taskI+'.png')),[Drawing.Imaging.ImageFormat]::Png)
   $taskG.Dispose();$taskBmp.Dispose();$taskImage.Dispose();$taskStream.Dispose()
   if($taskI % 10 -eq 0 -or $taskI -eq $taskPages.Count){Write-Output ('Renderizadas '+$taskI+' paginas')}
  }
 }
 $taskSave=[object]0;$taskDoc.Close([ref]$taskSave)
} finally {$taskSave=[object]0;$taskWord.Quit([ref]$taskSave);[Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord)|Out-Null}
