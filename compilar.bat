@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
where pwsh.exe >nul 2>nul
if errorlevel 1 (
  echo Instale o PowerShell 7 para compilar e testar o pacote.
  pause
  exit /b 1
)
set "RB_VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if not exist "%RB_VSWHERE%" (
  echo Instale o Visual Studio Build Tools 2022 com Desenvolvimento para desktop com C++.
  pause
  exit /b 1
)
for /f "usebackq tokens=*" %%i in (`"%RB_VSWHERE%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "RB_VS=%%i"
if not defined RB_VS (
  echo As ferramentas C++ x64 do Visual Studio nao foram encontradas.
  pause
  exit /b 1
)
call "%RB_VS%\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
if errorlevel 1 exit /b 1
pwsh.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\build-rb-windows.ps1"
set "RB_RESULT=%ERRORLEVEL%"
if not "%RB_RESULT%"=="0" echo A compilacao falhou. Consulte a mensagem acima.
pause
exit /b %RB_RESULT%
