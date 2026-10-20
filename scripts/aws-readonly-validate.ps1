param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('dev', 'prod')]
    [string]$Environment,
    [string]$Profile,
    [switch]$ExplicitAwsAuthorization
)

$ErrorActionPreference = 'Stop'
if (-not $ExplicitAwsAuthorization) {
    throw 'BLOCKED: AWS access is disabled by default. This repository review forbids AWS commands. Only a separately authorized future operator may pass -ExplicitAwsAuthorization.'
}
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    $null = Get-Command aws -ErrorAction Stop
    $region = 'us-east-1'
    $profileArgs = @()
    if ($Profile) { $profileArgs = @('--profile', $Profile) }

    Write-Host 'Calling only read/validation AWS APIs; no stack or resource changes are requested.'
    & aws sts get-caller-identity --region $region @profileArgs
    if ($LASTEXITCODE -ne 0) { throw 'STS identity check failed.' }

    foreach ($template in @('network', 'registry', 'data', 'app')) {
        $body = "file://templates/$template.json"
        Write-Host "CloudFormation ValidateTemplate: $template.json"
        & aws cloudformation validate-template --template-body $body --region $region @profileArgs
        if ($LASTEXITCODE -ne 0) { throw "CloudFormation ValidateTemplate failed for $template.json." }
    }

    $config = Get-Content -Raw "config/environments/$Environment.json" | ConvertFrom-Json
    if ($config.EnableAuditStack) {
        Write-Host 'CloudFormation ValidateTemplate: audit.json (optional account-level stack)'
        & aws cloudformation validate-template --template-body 'file://templates/audit.json' --region $region @profileArgs
        if ($LASTEXITCODE -ne 0) { throw 'CloudFormation ValidateTemplate failed for audit.json.' }
    }
}
finally {
    Pop-Location
}
