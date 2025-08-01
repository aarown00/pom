cd ..
call env\Scripts\activate.bat
cd pom
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=1 delims= " %%b in ("%%a") do (
        set "MYIP=%%b"
    )
)

python manage.py runserver %MYIP%:8000
