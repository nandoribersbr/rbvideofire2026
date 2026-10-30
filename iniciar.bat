@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0RBVideofire.exe" (
  start "RB Videofire" "%~dp0RBVideofire.exe" %*
  exit /b 0
)
echo RBVideofire.exe nao encontrado nesta pasta.
echo Se voce baixou o codigo-fonte, use compilar.bat.
pause
exit /b 1
