$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$taskRoot='C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\declaracao_ia_20261102'
$taskTarget=Join-Path $taskRoot 'word_paginas'
New-Item -ItemType Directory -Path $taskTarget -Force | Out-Null
$taskWord=New-Object -ComObject Word.Application
$taskWord.Visible=$false; $taskWord.DisplayAlerts=0
try {
 $taskWord.WordBasic.FilePrintSetup('Microsoft Print to PDF',0,0,1)
 $taskDoc=$taskWord.Documents.Open((Join-Path $taskRoot 'entrega\Declaracao_responsabilidade_coletiva_Maycon_MINUTA.docx'),$false,$true,$false)
 Write-Output 'Documento aberto para renderizacao direta'
 $taskDoc.ActiveWindow.View.Type=3
 $taskDoc.Repaginate()
 Write-Output 'Paginacao concluida'
 $taskPages=$taskDoc.ActiveWindow.Panes.Item(1).Pages
 Write-Output ('Paginas '+$taskPages.Count)
 for ($taskI=1;$taskI -le $taskPages.Count;$taskI++) {
   [byte[]]$taskBytes=$taskPages.Item($taskI).EnhMetaFileBits
   [IO.File]::WriteAllBytes((Join-Path $taskTarget ('page-'+$taskI+'.emf')),$taskBytes)
   $taskStream=New-Object IO.MemoryStream(,$taskBytes)
   $taskImage=[Drawing.Image]::FromStream($taskStream)
   $taskBmp=New-Object Drawing.Bitmap(1240,1754)
   $taskG=[Drawing.Graphics]::FromImage($taskBmp)
   $taskG.Clear([Drawing.Color]::White)
   $taskG.DrawImage($taskImage,0,0,1240,1754)
   $taskBmp.Save((Join-Path $taskTarget ('page-'+$taskI+'.png')),[Drawing.Imaging.ImageFormat]::Png)
   $taskG.Dispose();$taskBmp.Dispose();$taskImage.Dispose();$taskStream.Dispose()
   Write-Output ('Renderizada pagina '+$taskI)
 }
 $taskSave=[object]0
 $taskDoc.Close([ref]$taskSave)
} finally {
 $taskSave=[object]0
 $taskWord.Quit([ref]$taskSave)
 [Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord)|Out-Null
}
