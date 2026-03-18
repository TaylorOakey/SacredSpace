param(
    [string]$RepoName = "SacredSpace_Repo",
    [string]$TargetRoot = "."
)

$ErrorActionPreference = "Stop"
$repoPath = Join-Path $TargetRoot $RepoName
if (-not (Test-Path $repoPath)) {
    New-Item -ItemType Directory -Path $repoPath -Force | Out-Null
}

$paths = @(
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "docs/canon",
    "docs/governance",
    "agents",
    "templates",
    "scripts/powershell",
    "scripts/bash",
    "config/labels"
)

foreach ($p in $paths) {
    $full = Join-Path $repoPath $p
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        Write-Host "Created: $full"
    }
}

if (-not (Test-Path (Join-Path $repoPath ".git"))) {
    git -C $repoPath init | Out-Null
    Write-Host "Initialized git repo at $repoPath"
}
else {
    Write-Host "Git already initialized at $repoPath"
}
