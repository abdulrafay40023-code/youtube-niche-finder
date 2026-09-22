@echo off
echo ====================================
echo   YouTube Niche Finder - Starting
echo ====================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python install nahi hai!
    echo Download karo: https://python.org
    pause
    exit
)

:: Install requirements
echo [1/2] Libraries install ho rahi hain...
pip install -r requirements.txt -q

echo [2/2] Server start ho raha hai...
echo.
echo  Browser mein yeh URL kholo:
echo  >> http://localhost:5000 <<
echo.
python app.py

pause
