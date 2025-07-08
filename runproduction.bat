@echo off
SETLOCAL ENABLEEXTENSIONS

REM === Unique window title for this CMD ===
set "TITLE=PO_MONITORING_SERVER"

REM === Check if this CMD window is already running ===
tasklist /v | findstr /i "%TITLE%" >nul
if %ERRORLEVEL%==0 (
    echo Server is already running. Opening browser...
    start http://po.monitoring/
    goto :eof
)

REM === Set the window title to lock it ===
title %TITLE%

REM === Activate virtual environment ===
call ..\env\Scripts\activate.bat

REM === Open browser once ===
start http://po.monitoring/

echo.
echo =====================================================
echo The server is already running!
echo.
echo You can access it anytime at:  http://po.monitoring/ 
echo You can access it anytime at:  192.168.1.9 
echo.
echo There's no need to open this file multiple times.
echo As long as this single window is open, the program is accessible at any devices.
echo.
echo Just minimize this window and continue using the site.
echo Do NOT close it unless you want to stop the program.
echo =====================================================
echo.

REM === Run Waitress server ===
..\env\Scripts\waitress-serve --host=0.0.0.0 --port=80 mabuhaypowers_pom.wsgi:application







