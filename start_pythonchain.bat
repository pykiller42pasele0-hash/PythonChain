@echo off
title PythonChain Master Console
color 0A

echo Checking environment...
if not exist venv (
    echo [!] venv not found. Please run: python -m venv venv
    pause
    exit
)

echo Starting PythonChain Node A on Port 5000...
start cmd /k "venv\Scripts\activate && python app.py"

echo Opening Developer Dashboard...
timeout /t 3
start frontend/index.html

echo.
echo ========================================
echo PythonChain is now running dezentralized!
echo ========================================
pause