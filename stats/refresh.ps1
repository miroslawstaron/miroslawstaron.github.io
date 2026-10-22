# Nightly job (lazythought Task Scheduler): refresh stats/data.js from GitHub and publish it
# to www.staron.nu by pushing to miroslawstaron.github.io. Lives in <site repo>\stats\.
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$log = Join-Path $PSScriptRoot 'refresh.log'

function Run([string] $what, [scriptblock] $cmd) {
    & $cmd
    if ($LASTEXITCODE -ne 0) { throw "$what failed with exit code $LASTEXITCODE" }
}

Start-Transcript -Path $log -Append | Out-Null
try {
    Set-Location $repo
    Run 'git pull' { git pull --rebase --quiet }
    Run 'fetch' { python stats\fetch_stats.py --since 2013-09-01 --hide-private --out stats\data.js }
    git add stats/data.js
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        Run 'git commit' { git commit --quiet -m "Refresh GitHub stats" }
        Run 'git push' { git push --quiet }
        'Published new stats.'
    } else {
        'No changes.'
    }
} finally {
    Stop-Transcript | Out-Null
}
