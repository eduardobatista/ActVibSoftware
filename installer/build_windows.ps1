#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Builds the ActVib and ActVibFlash Windows executables, packages the
    portable ZIP, and compiles the Inno Setup installer.

.DESCRIPTION
    Intended to run on windows-latest GitHub Actions runners (or a local
    Windows machine) with `uv` available. All build artifacts are written
    under installer/output, keeping the repository root `dist/` directory
    (used for the wheel/sdist) untouched.

.EXAMPLE
    pwsh installer/build_windows.ps1
#>

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$InstallerDir = Join-Path $RepoRoot "installer"
$BuildDir = Join-Path $InstallerDir "build"
$StageDir = Join-Path $InstallerDir "dist"
$OutputDir = Join-Path $InstallerDir "output"

function Get-ProjectVersion {
    $pyproject = Get-Content (Join-Path $RepoRoot "pyproject.toml") -Raw
    if ($pyproject -match '(?m)^version\s*=\s*"([^"]+)"') {
        return $Matches[1]
    }
    throw "Could not find project.version in pyproject.toml"
}

$Version = Get-ProjectVersion
Write-Host "Building ActVib $Version for Windows x64"

if ([Environment]::Is64BitOperatingSystem -eq $false -or [Environment]::Is64BitProcess -eq $false) {
    throw "This build script must run on a 64-bit Windows process."
}

Write-Host "Cleaning previous build outputs..."
foreach ($dir in @($BuildDir, $StageDir, $OutputDir)) {
    if (Test-Path $dir) {
        Remove-Item -Recurse -Force $dir
    }
    New-Item -ItemType Directory -Path $dir | Out-Null
}

Push-Location $RepoRoot
try {
    Write-Host "Syncing locked dependencies (including packaging group)..."
    uv sync --locked --group packaging
    if ($LASTEXITCODE -ne 0) { throw "uv sync failed" }

    Write-Host "Running unit tests (offscreen Qt)..."
    $env:QT_QPA_PLATFORM = "offscreen"
    uv run --locked python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Unit tests failed" }

    Write-Host "Building ActVibFlash helper..."
    uv run --locked pyinstaller `
        --noconfirm `
        --distpath $StageDir `
        --workpath $BuildDir `
        (Join-Path $InstallerDir "ActVibFlash.spec")
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed building ActVibFlash" }

    Write-Host "Building ActVib main application..."
    uv run --locked pyinstaller `
        --noconfirm `
        --distpath $StageDir `
        --workpath $BuildDir `
        (Join-Path $InstallerDir "ActVib.spec")
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed building ActVib" }
}
finally {
    Pop-Location
}

$AppDir = Join-Path $StageDir "ActVib"
$FlasherExe = Join-Path $StageDir "ActVibFlash.exe"
$FlasherDestDir = Join-Path $AppDir "flasher"

if (-not (Test-Path $FlasherExe)) {
    throw "ActVibFlash.exe was not produced by PyInstaller at $FlasherExe"
}
New-Item -ItemType Directory -Path $FlasherDestDir -Force | Out-Null
Copy-Item $FlasherExe (Join-Path $FlasherDestDir "ActVibFlash.exe") -Force

Write-Host "Verifying the frozen bundle layout..."
Push-Location $RepoRoot
try {
    uv run --locked python (Join-Path "scripts" "check_windows_bundle.py") $AppDir
    if ($LASTEXITCODE -ne 0) { throw "Windows bundle verification failed" }
}
finally {
    Pop-Location
}

Write-Host "Smoke-testing the frozen application..."
$env:QT_QPA_PLATFORM = "offscreen"
$env:ACTVIB_SMOKE_TEST = "1"
& (Join-Path $AppDir "ActVib.exe")
if ($LASTEXITCODE -ne 0) { throw "ActVib.exe smoke test failed with exit code $LASTEXITCODE" }
Remove-Item Env:\ACTVIB_SMOKE_TEST
Remove-Item Env:\QT_QPA_PLATFORM

Write-Host "Verifying the flasher helper starts..."
& (Join-Path $FlasherDestDir "ActVibFlash.exe") "version"
if ($LASTEXITCODE -ne 0) { throw "ActVibFlash.exe version check failed with exit code $LASTEXITCODE" }

Write-Host "Creating the portable ZIP archive..."
$PortableRootName = "ActVib-$Version-windows-x64"
$PortableStage = Join-Path $StageDir $PortableRootName
Copy-Item $AppDir $PortableStage -Recurse
$PortableZip = Join-Path $OutputDir "$PortableRootName-portable.zip"
Compress-Archive -Path $PortableStage -DestinationPath $PortableZip -Force
Write-Host "Portable ZIP: $PortableZip"

Write-Host "Locating Inno Setup compiler (ISCC.exe)..."
$IsccCommand = Get-Command "ISCC.exe" -ErrorAction SilentlyContinue
if ($IsccCommand) {
    $IsccPath = $IsccCommand.Source
}
else {
    $CandidatePaths = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
    )
    $IsccPath = $CandidatePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $IsccPath) {
        throw "ISCC.exe (Inno Setup) was not found. Install Inno Setup 6 or add it to PATH."
    }
}
Write-Host "Using Inno Setup compiler: $IsccPath"

Write-Host "Compiling the Windows installer..."
& $IsccPath `
    "/DAppVersion=$Version" `
    "/DSourceDir=$AppDir" `
    "/DOutputDir=$OutputDir" `
    (Join-Path $InstallerDir "ActVib.iss")
if ($LASTEXITCODE -ne 0) { throw "Inno Setup compilation failed" }

$SetupExe = Join-Path $OutputDir "ActVib-$Version-windows-x64-setup.exe"
if (-not (Test-Path $SetupExe)) {
    throw "Expected installer was not produced at $SetupExe"
}

Write-Host "Generating checksums..."
$ChecksumFile = Join-Path $OutputDir "ActVib-$Version-SHA256SUMS.txt"
$Artifacts = @($PortableZip, $SetupExe)
$Lines = foreach ($artifact in $Artifacts) {
    $hash = (Get-FileHash -Algorithm SHA256 $artifact).Hash.ToLowerInvariant()
    "$hash  $(Split-Path -Leaf $artifact)"
}
Set-Content -Path $ChecksumFile -Value $Lines -Encoding ascii

Write-Host ""
Write-Host "Build complete. Artifacts in $OutputDir :"
Get-ChildItem $OutputDir | ForEach-Object { Write-Host "  $($_.Name)" }
