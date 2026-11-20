$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\busca_lacunas_20261101'
$taskFile = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\monografia\trabalho\busca_lacunas_20261101.docx'
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
$taskTitles = @()
$taskCaptions = @()
$taskInsideBody = $false
try {
    $taskDoc = $taskWord.Documents.Open($taskFile, $false, $true)
    $taskDoc.Repaginate()
    $taskDoc.ExportAsFixedFormat((Join-Path $taskRoot 'candidata.pdf'), 17)
    foreach ($taskParagraph in $taskDoc.Paragraphs) {
        $taskStyle = $taskParagraph.Style.NameLocal
        $taskRange = $taskParagraph.Range
        $taskText = $taskRange.Text.Trim()
        if ($taskStyle -eq 'TITULO TCC' -and $taskText -eq 'INTRODUÇÃO') { $taskInsideBody = $true }
        if ($taskStyle -in @('TITULO TCC','SEÇÃO TCC','SUBÇÃO 2')) {
            $taskTitles += @{title=$taskText;style=$taskStyle;number=$taskRange.ListFormat.ListString;page=$taskRange.Information(1);physicalPage=$taskRange.Information(3)}
        }
        if ($taskInsideBody -and $taskText -match '^(Figura|Quadro|Tabela)\s+\d+\s*[–-]') {
            $taskCaptions += @{title=$taskText;page=$taskRange.Information(1);physicalPage=$taskRange.Information(3)}
        }
    }
    @{titles=$taskTitles;captions=$taskCaptions;pages=$taskDoc.ComputeStatistics(2)} | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $taskRoot 'paginacao_candidata.json') -Encoding utf8
    $taskDoc.Close(0)
    Write-Output ('Conferidos ' + $taskTitles.Count + ' títulos e ' + $taskCaptions.Count + ' legendas')
} finally {
    $taskWord.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) | Out-Null
}
