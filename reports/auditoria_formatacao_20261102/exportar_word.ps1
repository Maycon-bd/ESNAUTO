$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
$taskDocPath = (Resolve-Path (Join-Path $taskRoot '../monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx')).Path
$taskPdfPath = Join-Path $taskRoot 'v010_word.pdf'
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
$taskWord.AutomationSecurity = 3
$taskDoc = $null
try {
    $taskDoc = $taskWord.Documents.Open($taskDocPath, $false, $true, $false)
    $taskDoc.Repaginate()
    $taskDoc.ExportAsFixedFormat($taskPdfPath, 17)
    $taskParagraphs = @()
    for ($taskIndex=1; $taskIndex -le $taskDoc.Paragraphs.Count; $taskIndex++) {
        $taskPara = $taskDoc.Paragraphs.Item($taskIndex)
        $taskRange = $taskPara.Range
        $taskText = $taskRange.Text.Trim([char]13,[char]7)
        if ($taskText.Length -gt 0) {
            $taskParagraphs += [pscustomobject]@{
                indice_word=$taskIndex; texto=$taskText; pagina_fisica=$taskRange.Information(3);
                pagina_exibida=$taskRange.Information(1); linhas=$taskRange.ComputeStatistics(1)
            }
        }
    }
    $taskParagraphs | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskRoot 'paginacao_word.json') -Encoding utf8
    Write-Output "Exportacao Word somente leitura concluida; paginas=$($taskDoc.ComputeStatistics(2))"
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    $taskWord.Quit()
}
