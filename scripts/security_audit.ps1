# security_audit.ps1 - Auditoria de vulnerabilidades de dependencias.
# Ejecutar desde la raiz del repo:
#   powershell -ExecutionPolicy Bypass -File scripts\security_audit.ps1
# Fuentes: npm audit (frontend) + pip-audit (backend, venv del proyecto).
# Plan canonico: docs/architecture/PLAN_ENDURECIMIENTO_SEGURIDAD.md

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot

Write-Host "=== pip-audit (backend) ===" -ForegroundColor Cyan
& "$root\.venv\Scripts\python.exe" -m pip_audit -r "$root\requirements.txt" --progress-spinner off
if ($LASTEXITCODE -ne 0) { Write-Host "pip-audit: se hallaron vulnerabilidades" -ForegroundColor Yellow }

Write-Host "`n=== npm audit (frontend, solo produccion) ===" -ForegroundColor Cyan
Push-Location "$root\frontend"
try {
    npm audit --omit=dev
    if ($LASTEXITCODE -ne 0) { Write-Host "npm audit: se hallaron vulnerabilidades" -ForegroundColor Yellow }
} finally {
    Pop-Location
}

Write-Host "`nAuditoria terminada. 0 vulnerabilidades = salida limpia." -ForegroundColor Green
