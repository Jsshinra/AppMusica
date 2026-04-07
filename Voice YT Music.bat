@echo off
title Voice YT Music Launcher
color 0A
echo ==================================================
echo         INICIANDO VOICE YT MUSIC...
echo      Cargando IA y motor local del navegador.
echo ==================================================
cd /d "%~dp0"

:: Activar entorno si es necesario, o ejecutar directo
python main.py

:: Si ocurre un error, pausar para mirarlo
pause
