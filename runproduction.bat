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

call pg_backup.bat

REM === Activate virtual environment ===
echo [ENV] Activating virtual environment...
call ..\env\Scripts\activate.bat

REM === Installing and updating dependencies ===
echo [PYTHON] Installing and updating dependencies...
pip install -r requirements.txt

REM === Git reset ===
echo [GIT] Resetting local changes...
REM git reset --hard

REM === Git pull ===
echo [GIT] Pulling latest changes from remote...
REM git pull

REM === Collect static files (interactive) ===
echo [DJANGO] Collecting static files...
REM python manage.py collectstatic --noinput

REM === Apply database migrations ===
echo [DJANGO] Applying database migrations...
REM python manage.py migrate

cls

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=1 delims= " %%b in ("%%a") do (
        set "MYIP=%%b"
    )
)

REM === Final info ===
echo.
echo =====================================================
echo [DONE] The server has been updated and is running!
echo.
echo You can access it anytime at link: %MYIP%
echo.
echo DO NOT close this window unless you want to shutdown or restart server.
echo Please minimize and continue using the link in browser.
echo Please make sure internet access is available.
echo =====================================================
echo.
echo.

REM === Start Waitress server ===
echo [SERVER] Launching production server with Waitress...
waitress-serve --host=0.0.0.0 --port=80 mabuhaypowers_pom.wsgi:application

