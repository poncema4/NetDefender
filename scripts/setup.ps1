$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# NetDefender local setup for Windows PowerShell.
# Core development does not require VMware, Kali, Metasploitable, or tshark.

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

Write-Host "`n== NetDefender setup =="
Write-Host "Repository: $RootDir`n"

function Find-Python {
    $candidates = @('py', 'python')
    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($null -eq $command) { continue }

        try {
            $versionText = & $candidate -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
            $parts = $versionText.Trim().Split('.') | ForEach-Object { [int]$_ }
            if ($parts[0] -gt 3 -or ($parts[0] -eq 3 -and $parts[1] -ge 11)) {
                return $candidate
            }
        }
        catch {
            continue
        }
    }

    throw 'Python 3.11+ is required but was not found.'
}

$Python = Find-Python
& $Python --version

if (-not (Test-Path '.venv')) {
    Write-Host 'Creating .venv...'
    & $Python -m venv .venv
}

$VenvPython = Join-Path $RootDir '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython)) {
    throw "Expected virtual-environment Python at $VenvPython"
}

Write-Host 'Upgrading pip...'
& $VenvPython -m pip install --upgrade pip

Write-Host 'Installing NetDefender and test dependencies...'
& $VenvPython -m pip install -e '.[test]'

Write-Host 'Running complete automated test suite...'
& $VenvPython -m pytest

Write-Host 'Running deterministic CLI smoke test...'
& $VenvPython -m netdefender.cli data/samples/syn-scan.json --html local-report.html

if (-not (Test-Path 'local-report.html') -or ((Get-Item 'local-report.html').Length -le 0)) {
    throw 'CLI completed but local-report.html was not created or is empty.'
}

Write-Host 'Checking optional tshark availability...'
$tshark = Get-Command tshark -ErrorAction SilentlyContinue
if ($null -ne $tshark) {
    & tshark --version | Select-Object -First 1
    Write-Host 'tshark: available'
}
else {
    Write-Host 'tshark: not installed (optional until real PCAP analysis)'
}

Write-Host @"

Setup complete.

Activate the environment with:
  .\.venv\Scripts\Activate.ps1

Run tests with:
  python -m pytest

Run the sample with:
  python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
"@
