@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
	echo No se encontro el entorno virtual en .venv.
	pause
	exit /b 1
)

start "Sistema de Ordenes" cmd /k ""%~dp0.venv\Scripts\python.exe" -m waitress --host=0.0.0.0 --port=8000 sistema.wsgi:application"

timeout /t 3 /nobreak >nul

start "" http://127.0.0.1:8000