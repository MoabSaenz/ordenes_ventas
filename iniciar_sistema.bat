@echo off
cd /d "%~dp0"

call .venv\Scripts\activate

start "Sistema de Ordenes" cmd /k "waitress-serve --host=0.0.0.0 --port=8000 sistema.wsgi:application"

timeout /t 3 /nobreak >nul

start "" http://192.168.100.20:8000