@echo off
set dict=%~dp0
start "Backend" cmd /k "python %dict%backend\run.py"
start "Frontend" cmd /k "cd /d %dict%frontend && npm install && npm run dev"