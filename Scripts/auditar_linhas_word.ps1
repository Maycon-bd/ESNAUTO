param([string]$InputPath,[string]$OutputPath)
$ErrorActionPreference='Stop'
$w=$null; $d=$null; $own=$false
try {
 $w=New-Object -ComObject Word.Application
 if($w.Documents.Count -ne 0){throw 'Instância ocupada; preservar documentos existentes.'}
 $own=$true; $w.Visible=$false; $w.DisplayAlerts=0; $w.AutomationSecurity=3
 $d=$w.Documents.Open((Resolve-Path -LiteralPath $InputPath).Path,$false,$true,$false)
 $d.Repaginate()
 $result=@();$i=0
 foreach($p in $d.Paragraphs){
  $i++;$r=$p.Range;$t=$r.Text.Trim([char]13,[char]7)
  if($t.Length -eq 0){continue}
  $result += [pscustomobject]@{index=$i;text=$t;style=$r.Style.NameLocal;lines=$r.ComputeStatistics(1);page=$r.Information(1);table=$r.Information(12);start=$r.Start}
 }
 $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
 Write-Output ('Parágrafos registrados: '+$result.Count)
} finally {
 if($null -ne $d){$d.Close(0);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($d)}
 if($own -and $null -ne $w -and $w.Documents.Count -eq 0){$w.Quit()}
 if($null -ne $w){[void][Runtime.InteropServices.Marshal]::ReleaseComObject($w)}
}
