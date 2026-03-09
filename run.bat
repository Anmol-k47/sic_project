@echo off
echo ============================================
echo   WorkMatch Pro v3 — Quick Start (Windows)
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

:: Create virtual env if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

:: Download spaCy model
python -m spacy download en_core_web_sm -q 2>nul

:: Run the app
echo.
echo Starting WorkMatch Pro v3...
echo.
python app.py

pause
