$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & python scripts/validate.py
    if ($LASTEXITCODE -ne 0) { throw 'Local contract validation failed.' }

    foreach ($phase in 1..8) {
        & python scripts/phase_check.py $phase
        if ($LASTEXITCODE -ne 0) { throw "Phase $phase evidence check failed." }
    }

    & python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Unit tests failed.' }

    foreach ($environment in @('dev', 'prod')) {
        & python scripts/plan.py --environment $environment
        if ($LASTEXITCODE -ne 0) { throw "Local plan failed for $environment." }
    }
}
finally {
    Pop-Location
}
