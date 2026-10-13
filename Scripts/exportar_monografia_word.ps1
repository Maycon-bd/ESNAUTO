param(
  [Parameter(Mandatory=$true)][string]$InputPath,
  [Parameter(Mandatory=$true)][string]$PdfPath,
  [switch]$AtualizarListas,
  [switch]$UsarPaginaAjustada,
  [string]$PageMapPath
)
$ErrorActionPreference = 'Stop'
$inputResolved = (Resolve-Path -LiteralPath $InputPath).Path
$pdfResolved = [System.IO.Path]::GetFullPath($PdfPath)
[System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($pdfResolved)) | Out-Null
$word = $null
$document = $null
$createdEmptyInstance = $false
try {
  $word = New-Object -ComObject Word.Application
  if ($word.Documents.Count -ne 0) { throw 'A instância retornada contém documentos existentes; operação interrompida para preservar a sessão.' }
  $createdEmptyInstance = $true
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $word.AutomationSecurity = 3
  $document = $word.Documents.Open($inputResolved, $false, (-not $AtualizarListas.IsPresent), $false)
  $document.Repaginate()
  $pageMap = @()
  foreach ($paragraph in $document.Paragraphs) {
    $text = $paragraph.Range.Text.Trim([char]13, [char]7)
    $style = [string]$paragraph.Style.NameLocal
    if ($text.Contains("`t")) { continue }
    if ($style -in @('TITULO TCC','SEÇÃO TCC','SUBÇÃO 2','Caption') -or $text -match '^(Tabela|QUADRO|Figura)\s+\d+\s*[–—-]') {
      $tipoInformacao = if ($UsarPaginaAjustada) { 3 } else { 1 }
      $pageMap += [pscustomobject]@{texto=$text; pagina=$paragraph.Range.Information($tipoInformacao); estilo=$style; numero=$paragraph.Range.ListFormat.ListString}
    }
  }
  if ($AtualizarListas) {
    foreach ($paragraph in $document.Paragraphs) {
      $text = $paragraph.Range.Text.Trim([char]13, [char]7)
      if (-not $text.Contains("`t")) { continue }
      if ($text -notmatch "`t\d+\s*$") { continue }
      $parts = $text.Split("`t")
      $title = if ($parts.Length -ge 3) { $parts[$parts.Length-2] } else { $parts[0] }
      $titleNormalized = ($title -replace '\s+',' ').Trim()
      $found = @($pageMap | Where-Object { (($_.texto -replace '\s+',' ').Trim()) -eq $titleNormalized })
      if ($found.Count -gt 1 -and $parts.Length -ge 3) {
        $sectionNumber = $parts[0].Trim()
        $found = @($found | Where-Object { $_.numero -eq $sectionNumber })
      }
      if ($found.Count -eq 1) {
        $match = [regex]::Match($text, '\d+(?=\s*$)')
        $newPage = [string]$found[0].pagina
        if ($match.Value.Trim() -ne $newPage) {
          # Alterar somente os algarismos: o marcador final pode conter uma
          # quebra de seção e não deve ser substituído com Range.Text.
          $digitsRange = $document.Range($paragraph.Range.Start + $match.Index,
                                        $paragraph.Range.Start + $match.Index + $match.Length)
          $digitsRange.Text = $newPage
        }
      }
    }
    $document.Repaginate()
    $document.Fields.Update() | Out-Null
    $document.Save()
  }
  if ($PageMapPath) {
    $pageMap | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $PageMapPath -Encoding utf8
  }
  $document.ExportAsFixedFormat($pdfResolved, 17)
  Write-Output ('Exportado: ' + $pdfResolved)
  Write-Output ('Páginas: ' + $document.ComputeStatistics(2))
} finally {
  if ($document) { $document.Close(0) | Out-Null; [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) | Out-Null }
  if ($word -and $createdEmptyInstance) { $word.Quit(0) | Out-Null }
  if ($word) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null }
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}
