@echo off
echo ================================
echo Anshul Portfolio Backend Setup
echo Minimal Version for Vercel
echo ================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Python detected
python --version
echo.

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/6] Virtual environment already exists
)
echo.

:: Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate
echo.

:: Install dependencies
echo [4/6] Installing dependencies...
pip install -r requirements.txt
echo.

:: Check for .env file
if not exist ".env" (
    echo [5/6] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit .env file and add your GOOGLE_API_KEY
    echo Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    notepad .env
) else (
    echo [5/6] .env file already exists
)
echo.

:: Start the server
echo [6/6] Starting FastAPI server...
echo.
echo ================================
echo Server will start at:
echo http://localhost:8000
echo.
echo Interactive docs:
echo http://localhost:8000/docs
echo ================================
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
