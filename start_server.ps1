# Silent Signal AI - Server Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Silent Signal AI - Starting Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\HELLO\Silent-Signal-"

Write-Host "Server will be available at:" -ForegroundColor Green
Write-Host "  - API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "  - Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& ".venv\Scripts\uvicorn.exe" backend.main:app --reload --host 0.0.0.0 --port 8000
