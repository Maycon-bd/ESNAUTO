$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\apresentacao_banca_v008'
$taskDoc = Join-Path $taskRoot 'entrega\Roteiro_video_ESNAUTO_25min_v008.docx'
$taskPdf = Join-Path $taskRoot 'build\roteiro_word.pdf'
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
try {
    $taskOpened = $taskWord.Documents.Open($taskDoc, $false, $true)
    $taskOpened.ExportAsFixedFormat($taskPdf, 17)
    $taskOpened.Close(0)
} finally {
    $taskWord.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) | Out-Null
}
Write-Output 'PDF de conferência exportado do roteiro em leitura'
