@echo off
echo ========================================
echo Anshul Parate AI Portfolio Assistant
echo Fast Chatbot with LangGraph
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating template .env file...
    echo GOOGLE_API_KEY=your_api_key_here > .env
    echo.
    echo Please edit .env file and add your Google Gemini API key
    echo Get your key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo.

REM Run the server
echo ========================================
echo Starting FastAPI Server...
echo ========================================
echo.
echo Server will start at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
