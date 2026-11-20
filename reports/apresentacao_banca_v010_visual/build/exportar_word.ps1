$ErrorActionPreference='Stop'
$taskRoot='C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\apresentacao_banca_v010_visual'
$taskLog=Join-Path $taskRoot 'build\word_export.log'
function taskNote($s) { ((Get-Date -Format o)+' '+$s) | Add-Content $taskLog; Write-Output $s }
taskNote 'Criando Word para exportacao'
$taskWord=New-Object -ComObject Word.Application
taskNote 'Word criado'
$taskWord.Visible=$false
$taskWord.DisplayAlerts=0
$taskOriginalPrinter=$taskWord.ActivePrinter
taskNote ('Impressora original '+$taskOriginalPrinter)
$taskWord.WordBasic.FilePrintSetup('Microsoft Print to PDF',0,0,1)
taskNote ('Impressora de exportacao '+$taskWord.ActivePrinter)
$taskWord.Options.PrintBackground=$false
$taskWord.Options.UpdateFieldsAtPrint=$false
$taskWord.Options.UpdateLinksAtPrint=$false
try {
    taskNote 'Abrindo roteiro em leitura'
    $taskDoc=$taskWord.Documents.Open((Join-Path $taskRoot 'entrega\Roteiro_video_ESNAUTO_25min_v010.docx'),$false,$true,$false)
    taskNote 'Roteiro aberto'
    $taskDoc.ExportAsFixedFormat((Join-Path $taskRoot 'build\roteiro_word.pdf'),17)
    taskNote ('PDF exportado. Paginas '+$taskDoc.ComputeStatistics(2))
    $taskDoc.Close(0)
} finally {
    $taskWord.Quit(0)
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) | Out-Null
}
