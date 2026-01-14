# Django Command Helper Script
# Ensures commands run from correct directory with manage.py validation

param(
    [Parameter(Mandatory=$true)]
    [string]$Command   # Django command to execute (e.g., "check", "migrate", "runserver")
)

# Define paths
$backendRoot = "D:\platform\hrm\backend"
$managePy = Join-Path $backendRoot "manage.py"

# Validate manage.py exists
if (-Not (Test-Path $managePy)) {
    Write-Error "❌ manage.py not found at $managePy"
    Write-Error "Please verify the Django backend is properly installed"
    exit 1
}

Write-Host "✅ manage.py found at $managePy" -ForegroundColor Green

# Change to backend directory
Push-Location $backendRoot
Write-Host "📁 Changed to: $(Get-Location)" -ForegroundColor Cyan

# Execute Django command
Write-Host "🚀 Running: python manage.py $Command" -ForegroundColor Yellow
try {
    python $managePy $Command
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host "✅ Command completed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Command failed with exit code: $exitCode" -ForegroundColor Red
    }
}
catch {
    Write-Error "❌ Error executing Django command: $($_.Exception.Message)"
    $exitCode = 1
}
finally {
    # Return to original directory
    Pop-Location
    Write-Host "📁 Returned to: $(Get-Location)" -ForegroundColor Cyan
}

exit $exitCode
