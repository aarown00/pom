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
python manage.py collectstatic --noinput

REM === Skip makemigrations in prod (optional) ===
REM echo [DJANGO] Making migrations...
python manage.py makemigrations

REM === Apply database migrations ===
echo [DJANGO] Applying database migrations...
python manage.py migrate

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
echo Ignore the warning below. Server is up if you see this message.
echo =====================================================
echo.
echo.

REM === Start Waitress server ===
echo [SERVER] Launching production server with Waitress...
..\env\Scripts\waitress-serve --host=0.0.0.0 --port=80 mabuhaypowers_pom.wsgi:application

