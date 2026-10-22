@echo off
REM ---- edit these two lines if your setup differs ----
set ADB_DIR=C:\Program Files\Netease\MuMuPlayer\nx_device\12.0\shell
set DEVICE=127.0.0.1:16384
REM ----------------------------------------------------
set PATH=%PATH%;%ADB_DIR%
cd /d "%~dp0"
adb connect %DEVICE%
python like_loop.py
pause
