@echo off
setlocal
set PGPASSWORD=pass123

REM Extract date parts from "Day MM/DD/YYYY"
for /f "tokens=2-4 delims=/ " %%a in ("%date%") do (
    set month=%%a
    set day=%%b
    set year=%%c
)

REM Extract hour and minute from time
for /f "tokens=1-2 delims=:" %%a in ("%time%") do (
    set hour=%%a
    set min=%%b
)

REM Remove leading space from hour (if any)
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%

REM Combine date and time
set datestr=%year%-%month%-%day%_%hour%%min%
set filename=mbpom_backup_%datestr%.backup

REM Optional: Show full path
echo Backing up to: C:\psql_backups\%filename%

REM Ensure backup folder exists
if not exist "C:\psql_backups" mkdir "C:\psql_backups"

REM Run the backup
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -U aaronmart -h localhost -p 5432 -F c -b -v -f "C:\psql_backups\%filename%" mabuhaypowers_pom

REM Check result
if %errorlevel% neq 0 (
  echo Backup failed!
) else (
  echo Backup successful!
)

endlocal
