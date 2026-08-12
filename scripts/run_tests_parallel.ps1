# Ejecuta la suite de tests en dos procesos paralelos (motor + app)
# para reducir el tiempo de 6 min a ~3-4 min sin instalar nada.
# Uso (cwd = raíz del repo):  powershell -ExecutionPolicy Bypass -File scripts\run_tests_parallel.ps1

$ErrorActionPreference = "Continue"

$py = ".venv\Scripts\python.exe"
$appTests = @(
    "tests/test_maxo.py", "tests/test_reputation_resources.py",
    "tests/test_interchanges.py", "tests/test_forms_bp_comprehensive.py",
    "tests/test_vhv_bp_comprehensive.py", "tests/test_voting.py",
    "tests/test_guide.py", "tests/test_admin_crud_mutations.py",
    "tests/test_validador_conceptual.py",
    "tests/test_users.py", "tests/test_utils.py",
    "tests/test_maxo_edgecases.py", "tests/test_maxo_edgecases_comprehensive.py"
)

$motorTests = Get-ChildItem "tests\test_maxocontracts" -Filter "*.py" | ForEach-Object { $_.FullName }

$appArgs = @("-m", "pytest", "-q") + $appTests
$motorArgs = @("-m", "pytest", "-q") + $motorTests

$p1 = Start-Process -FilePath $py -ArgumentList $appArgs -PassThru -NoNewWindow -RedirectStandardOutput "$env:TEMP\mc_app_tests.log" -RedirectStandardError "$env:TEMP\mc_app_tests_err.log"
$p2 = Start-Process -FilePath $py -ArgumentList $motorArgs -PassThru -NoNewWindow -RedirectStandardOutput "$env:TEMP\mc_motor_tests.log" -RedirectStandardError "$env:TEMP\mc_motor_tests_err.log"

Wait-Process -Id $p1.Id, $p2.Id -ErrorAction SilentlyContinue

Write-Host "`n=== APP (tests de aplicacion) ==="
Get-Content "$env:TEMP\mc_app_tests.log" -Tail 5
if ((Get-Item "$env:TEMP\mc_app_tests_err.log").Length -gt 0) {
    Write-Host "--- stderr app ---"
    Get-Content "$env:TEMP\mc_app_tests_err.log" -Tail 5
}

Write-Host "`n=== MOTOR (maxocontracts) ==="
Get-Content "$env:TEMP\mc_motor_tests.log" -Tail 5
if ((Get-Item "$env:TEMP\mc_motor_tests_err.log").Length -gt 0) {
    Write-Host "--- stderr motor ---"
    Get-Content "$env:TEMP\mc_motor_tests_err.log" -Tail 5
}

Write-Host "`nExit codes: app=$($p1.ExitCode) motor=$($p2.ExitCode)"
if ($p1.ExitCode -ne 0 -or $p2.ExitCode -ne 0) { exit 1 }
