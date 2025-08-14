@echo off
echo 🎤 Setting up AI Interview Note Taker...
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python %python_version% detected

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 🔧 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your OpenAI API key
) else (
    echo ✅ .env file already exists
)

REM Create templates directory if it doesn't exist
if not exist "templates" (
    echo 🔧 Creating templates directory...
    mkdir templates
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Activate virtual environment: venv\Scripts\activate.bat
echo 3. Run the application: python app.py
echo 4. Open http://localhost:5000 in your browser
echo.
echo For more information, see README.md
pause