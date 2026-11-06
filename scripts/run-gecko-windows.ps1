# Windows Gecko development smoke launcher. Runs Mozilla Firefox, NOT a NOLP-branded browser.
# Requires an existing Firefox installation; never downloads or modifies Firefox.
[CmdletBinding()]
param(
    [string]$FirefoxPath = "",
    [string]$Url = "about:blank"
)
$ErrorActionPreference = "Stop"
if ($Url -ne "about:blank" -and $Url -notmatch '^https://[a-zA-Z0-9]') {
    throw "Only HTTPS URLs or about:blank are supported by this development launcher."
}
if (-not $FirefoxPath) {
    $candidates = @(
        [IO.Path]::Combine($env:ProgramFiles, "Mozilla Firefox", "firefox.exe")
    )
    if (${env:ProgramFiles(x86)}) {
        $candidates += [IO.Path]::Combine(${env:ProgramFiles(x86)}, "Mozilla Firefox", "firefox.exe")
    }
    $FirefoxPath = $candidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
}
if (-not $FirefoxPath -or -not (Test-Path -LiteralPath $FirefoxPath -PathType Leaf)) {
    throw "Firefox executable not found. Supply -FirefoxPath pointing to an installed firefox.exe."
}
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$profile = Join-Path $root ".local\nolp-windows-gecko-smoke"
[IO.Directory]::CreateDirectory($profile) | Out-Null
Write-Host "Launching upstream Firefox with isolated test profile: $profile"
Write-Host "This is a Gecko smoke test, not an integrated NOLP browser."
& $FirefoxPath -no-remote -profile $profile $Url
if ($LASTEXITCODE -ne 0) { throw "Firefox exited with code $LASTEXITCODE" }
