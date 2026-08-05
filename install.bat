@echo off
title Rust Wipe Bot Installer

echo ========================================
echo        Rust Wipe Bot Installer
echo ========================================
echo.

:: Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed.
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit
)

:: Create virtual environment
echo Creating virtual environment...
py -m venv venv

echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

echo.

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

echo.

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.

:: Create .env automatically if it doesn't exist
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo Created .env from .env.example
)

echo.
echo ========================================
echo       Installation Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Open the .env file.
echo 2. Paste your Discord Bot Token.
echo 3. Save the file.
echo 4. Double-click start.bat
echo.
pause