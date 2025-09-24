@echo off
echo ========================================
echo Dashboard Analyse Diabete - Redis
echo ========================================
echo.

echo Verification de Redis...
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Redis n'est pas accessible
    echo Veuillez demarrer Redis Stack avec: redis-stack-server
    echo.
    pause
    exit /b 1
)

echo Redis OK - Demarrage du dashboard...
echo URL: http://localhost:5000
echo Appuyez sur Ctrl+C pour arreter
echo.

python start_dashboard.py

pause