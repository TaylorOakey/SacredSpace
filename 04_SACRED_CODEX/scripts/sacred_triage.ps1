# SacredSpace Security Triage
# Run from PowerShell as USER
# Scans Downloads, moves sensitive files, generates report

$DOWNLOADS = "C:\Users\USER\Downloads"
$SECURE_VAULT = "C:\Users\USER\SACRED_SECURE"
$REPORT_PATH = "C:\Users\USER\SACRED_SECURE\security_report.txt"

# ─── CREATE SECURE VAULT ──────────────────────────────────────────────────────
if (-not (Test-Path $SECURE_VAULT)) {
    New-Item -ItemType Directory -Path $SECURE_VAULT -Force | Out-Null
    Write-Host "`n[CREATED] Secure vault: $SECURE_VAULT" -ForegroundColor Green
}

# ─── DEFINE SENSITIVE FILE PATTERNS ───────────────────────────────────────────
$MOVE_PATTERNS = @(
    # GitHub / Auth recovery
    "github-recovery-codes*",
    "Mozilla-Recovery-Key*",
    # Environment / secrets
    ".env*",
    "*.env",
    "*secret*",
    "*credentials*",
    "*api_key*",
    "*authkey*",
    "tskey-*",
    # Personal documents
    "proof_of_enrollment*",
    # Audit configs that may contain paths/keys
    "*audit_config*",
    # Drive manifests (contain file IDs and paths)
    "drive_manifest*"
)

# ─── MOVE SENSITIVE FILES ─────────────────────────────────────────────────────
Write-Host "`n══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 1: MOVING SENSITIVE FILES" -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════" -ForegroundColor Cyan

$moved = @()
$failed = @()

foreach ($pattern in $MOVE_PATTERNS) {
    $files = Get-ChildItem -Path $DOWNLOADS -Filter $pattern -File -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $dest = Join-Path $SECURE_VAULT $file.Name
        try {
            Move-Item -Path $file.FullName -Destination $dest -Force
            Write-Host "  [MOVED] $($file.Name)" -ForegroundColor Yellow
            $moved += $file.Name
        } catch {
            Write-Host "  [FAILED] $($file.Name): $_" -ForegroundColor Red
            $failed += $file.Name
        }
    }
}

if ($moved.Count -eq 0) {
    Write-Host "  No sensitive files matched patterns (may already be moved)" -ForegroundColor Gray
}

# ─── DEEP SCAN ────────────────────────────────────────────────────────────────
Write-Host "`n══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 2: DEEP SCAN — RISK ASSESSMENT" -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════" -ForegroundColor Cyan

$allFiles = Get-ChildItem -Path $DOWNLOADS -Recurse -File -ErrorAction SilentlyContinue

# Scan categories
$risk_critical  = @()  # Must move now
$risk_high      = @()  # Review and likely move
$risk_medium    = @()  # Personal but not secret
$risk_low       = @()  # SacredSpace project files (safe, should go to OS)
$risk_clean     = @()  # Installers, zips, screenshots

foreach ($file in $allFiles) {
    $n = $file.Name.ToLower()
    $ext = $file.Extension.ToLower()

    # CRITICAL — auth, keys, secrets
    if ($n -match "recovery.code|recovery.key|\.env|secret|credential|api.key|authkey|tskey|\.pem|\.key|\.p12|\.pfx|\.cert") {
        $risk_critical += $file.FullName
    }
    # HIGH — personal identity documents
    elseif ($n -match "proof.of.enrollment|insurance|enrollment|mozilla.recovery|drive.manifest|audit.config") {
        $risk_high += $file.FullName
    }
    # MEDIUM — personal but not secret
    elseif ($ext -in @(".pdf",".docx",".doc") -and $n -notmatch "sacredspace|sacred|codex|sski|grama|py101") {
        $risk_medium += $file.FullName
    }
    # LOW — SacredSpace project files that belong in the OS
    elseif ($n -match "sacred|sski|genesis|protocol.router|srpe|sigil|neural.forest|codex|grama|obsidian|sacredspace") {
        $risk_low += $file.FullName
    }
    # CLEAN — installers, zips, screenshots, media
    elseif ($ext -in @(".exe",".zip",".png",".jpg",".mp4",".gz",".part",".lnk",".crdownload",".pdf") -and $n -notmatch "proof|insurance|recovery|mozilla") {
        $risk_clean += $file.FullName
    }
}

# ─── PRINT REPORT ─────────────────────────────────────────────────────────────

function Print-Section($title, $items, $color) {
    Write-Host "`n  [$title] — $($items.Count) files" -ForegroundColor $color
    foreach ($item in $items) {
        $short = $item.Replace($DOWNLOADS, "~\Downloads")
        Write-Host "    $short" -ForegroundColor $color
    }
}

Print-Section "CRITICAL — MOVE NOW"   $risk_critical  "Red"
Print-Section "HIGH — REVIEW/MOVE"    $risk_high      "Magenta"
Print-Section "MEDIUM — PERSONAL"     $risk_medium    "Yellow"
Print-Section "LOW — SACREDSPACE OS FILES (relocate to OS)" $risk_low "Cyan"
Print-Section "CLEAN"                 $risk_clean     "Gray"

# ─── WRITE REPORT FILE ────────────────────────────────────────────────────────
$report = @"
SACREDSPACE SECURITY TRIAGE REPORT
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
Downloads Path: $DOWNLOADS
Secure Vault:   $SECURE_VAULT

═══════════════════════════════════════
FILES MOVED TO SECURE VAULT ($($moved.Count))
═══════════════════════════════════════
$($moved -join "`n")

═══════════════════════════════════════
CRITICAL RISK — REMAINING ($($risk_critical.Count))
═══════════════════════════════════════
$($risk_critical -join "`n")

═══════════════════════════════════════
HIGH RISK — PERSONAL DOCUMENTS ($($risk_high.Count))
═══════════════════════════════════════
$($risk_high -join "`n")

═══════════════════════════════════════
MEDIUM — PERSONAL FILES ($($risk_medium.Count))
═══════════════════════════════════════
$($risk_medium -join "`n")

═══════════════════════════════════════
SACREDSPACE OS FILES IN DOWNLOADS ($($risk_low.Count))
(these should be moved to C:\SacredSpace_OS\)
═══════════════════════════════════════
$($risk_low -join "`n")

═══════════════════════════════════════
TOTALS
═══════════════════════════════════════
Total files scanned: $($allFiles.Count)
Moved to secure:     $($moved.Count)
Still critical:      $($risk_critical.Count)
High risk:           $($risk_high.Count)
SacredSpace files:   $($risk_low.Count)
"@

[System.IO.File]::WriteAllText($REPORT_PATH, $report)

Write-Host "`n══════════════════════════════════════════" -ForegroundColor Green
Write-Host "  DONE" -ForegroundColor Green
Write-Host "══════════════════════════════════════════" -ForegroundColor Green
Write-Host "  Secure vault:  $SECURE_VAULT" -ForegroundColor Green
Write-Host "  Report saved:  $REPORT_PATH" -ForegroundColor Green
Write-Host "`n  NEXT: Open $SECURE_VAULT and verify files landed safely." -ForegroundColor White
Write-Host "  Then move your SACRED_SECURE folder off Downloads." -ForegroundColor White
