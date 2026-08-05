@echo off
title Rust Wipe Bot

if not exist "venv\Scripts\python.exe" (
    echo ========================================
    echo Rust Wipe Bot is not installed.
    echo Please run install.bat first.
    echo ========================================
    pause
    exit
)

call venv\Scripts\activate

echo ========================================
echo Starting Rust Wipe Bot...
echo ========================================
echo.

python main.py

echo.
echo ========================================
echo Bot has stopped.
echo Press any key to close...
echo ========================================
pause