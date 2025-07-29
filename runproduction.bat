@echo off
SETLOCAL ENABLEEXTENSIONS

REM === Unique window title for this CMD ===
set "TITLE=PO_MONITORING_SERVER"

REM === Check if this CMD window is already running ===
echo [CHECK] Checking if server is already running...
tasklist /v | findstr /i "%TITLE%" >nul
if %ERRORLEVEL%==0 (
    echo [INFO] Server is already running. Exiting launcher.
    goto :eof
)

REM === Set the window title to lock it ===
echo [INIT] Setting CMD window title...
title %TITLE%

REM === Activate virtual environment ===
echo [ENV] Activating virtual environment...
call ..\env\Scripts\activate.bat

REM === Git reset ===
echo [GIT] Resetting local changes...
git reset --hard

REM === Git pull ===
echo [GIT] Pulling latest changes from remote...
git pull

REM === Collect static files (interactive) ===
echo [DJANGO] Collecting static files...
python manage.py collectstatic

REM === Skip makemigrations in prod (optional) ===
REM echo [DJANGO] Making migrations...
REM python manage.py makemigrations

REM === Apply database migrations ===
echo [DJANGO] Applying database migrations...
python manage.py migrate

REM === Final info ===
echo.
echo =====================================================
echo [DONE] The server has been updated and is running!
echo.
echo Access it at: 192.168.1.10
echo.
echo DO NOT close this window unless stopping the server.
echo Just minimize and continue using the app.
echo =====================================================
echo.

REM === Start Waitress server ===
echo [SERVER] Launching production server with Waitress...
..\env\Scripts\waitress-serve --host=0.0.0.0 --port=80 mabuhaypowers_pom.wsgi:application
