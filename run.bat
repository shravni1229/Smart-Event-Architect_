@echo off
title Smart Event Architect & Recommendation System
color 0D

echo ================================================================
echo   Smart Event Architect ^& Recommendation System
echo   BCA Mini Project (Python, Flask, SQLite / MySQL Workbench)
echo   Theme: Purple, Pink ^& White
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.10+ from https://www.python.org/ and check 'Add to PATH'.
    pause
    exit /b
)

echo [2/3] Initializing SQLite database and sample records...
python init_db.py

echo [3/3] Starting Flask Development Server...
echo.
echo ================================================================
echo   Open your browser and navigate to:
echo   http://127.0.0.1:5000
echo.
echo   Default Admin: admin@eventarchitect.com  ^|  admin123
echo   Default User:  rohit@example.com          ^|  user123
echo ================================================================
echo.
echo Press Ctrl+C in this window to stop the server.
echo.

python app.py
pause
