@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title CAP NHAT AUTOMATIC PATCH VIET HOA - ANGELS CLINIC VI

set "REPO_ZIP_URL=https://github.com/shimakazevn/angels-clinic-vi/archive/refs/heads/master.zip"
set "WORK_TEMP=%TEMP%\angels_clinic_patch_%RANDOM%"

echo ===========================================================================
echo   ANGELIC CLINIC - TU DONG TAI VA CAP NHAT PATCH VIET HOA
echo   Repo: https://github.com/shimakazevn/angels-clinic-vi
echo ===========================================================================
echo.

REM --- 1. Dinh vi thu muc Game ---
set "GAME_DIR=%~dp0"
if not exist "%GAME_DIR%Game.exe" (
    if exist "%GAME_DIR%Game\Game.exe" set "GAME_DIR=%GAME_DIR%Game\"
    if exist "%GAME_DIR%www\index.html" set "GAME_DIR=%GAME_DIR%www\"
    if exist "%GAME_DIR%app\index.html" set "GAME_DIR=%GAME_DIR%app\"
)

REM Truong hop game co data.dts & SRPG_Unpacker.exe
if exist "%GAME_DIR%data.dts" if exist "%GAME_DIR%SRPG_Unpacker.exe" (
    if not exist "%GAME_DIR%data" (
        echo [+] Phat hien file data.dts va SRPG_Unpacker.exe, dang giai nen...
        cd /d "%GAME_DIR%"
        SRPG_Unpacker.exe -o "data" "data.dts" >nul 2>&1
        cd /d "%~dp0"
    )
)

if not exist "%GAME_DIR%index.html" if not exist "%GAME_DIR%data\System.json" if not exist "%GAME_DIR%Game.exe" goto :NO_GAME

echo [+] Da dinh vi thu muc Game: %GAME_DIR%
echo [+] Dang chuan bi thu muc tam: %WORK_TEMP%
if exist "%WORK_TEMP%" rmdir /s /q "%WORK_TEMP%" >nul 2>&1
mkdir "%WORK_TEMP%" >nul 2>&1

echo [+] Dang tai goi Viet Hoa moi nhat tu GitHub...
echo.

REM --- 2. Tai goi patch qua curl hoac powershell vao thu muc TEMP ---
set "ZIP_FILE=%WORK_TEMP%\patch_latest.zip"

if exist "%SystemRoot%\System32\curl.exe" (
    echo [+] Dang su dung curl sieu toc...
    curl.exe -k -L --progress-bar -o "%ZIP_FILE%" "%REPO_ZIP_URL%"
) else (
    echo [+] Dang su dung PowerShell...
    powershell -ExecutionPolicy Bypass -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('%REPO_ZIP_URL%', '%ZIP_FILE%')"
)

if not exist "%ZIP_FILE%" goto :NO_ZIP

echo.
echo [+] Dang giai nen va ap dung Viet Hoa vao game...

REM --- 3. Giai nen (Uu tien tar.exe -> PowerShell) ---
if exist "%SystemRoot%\System32\tar.exe" (
    tar.exe -xf "%ZIP_FILE%" -C "%WORK_TEMP%" >nul 2>&1
) else (
    powershell -ExecutionPolicy Bypass -NoProfile -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -LiteralPath '%ZIP_FILE%' -DestinationPath '%WORK_TEMP%' -Force"
)

REM Tim thu muc vua giai nen
set "EXTRACTED_DIR="
for /d %%D in ("%WORK_TEMP%\*") do (
    if exist "%%D\patch" set "EXTRACTED_DIR=%%D\patch"
    if exist "%%D\data" if not defined EXTRACTED_DIR set "EXTRACTED_DIR=%%D"
)

if not defined EXTRACTED_DIR set "EXTRACTED_DIR=%WORK_TEMP%"

echo [+] Dang sao chep du lieu Viet Hoa vao: %GAME_DIR%
if exist "%EXTRACTED_DIR%\data" xcopy "%EXTRACTED_DIR%\data" "%GAME_DIR%data" /E /I /Y /Q >nul 2>&1
if exist "%EXTRACTED_DIR%\js" xcopy "%EXTRACTED_DIR%\js" "%GAME_DIR%js" /E /I /Y /Q >nul 2>&1
if exist "%EXTRACTED_DIR%\img" xcopy "%EXTRACTED_DIR%\img" "%GAME_DIR%img" /E /I /Y /Q >nul 2>&1

REM Truong hop game unpack dong goi lai data.dts
if exist "%GAME_DIR%data.dts" if exist "%GAME_DIR%SRPG_Unpacker.exe" (
    echo [+] Dang dong goi lai data.dts...
    cd /d "%GAME_DIR%"
    SRPG_Unpacker.exe -o "data.dts" "data" >nul 2>&1
    cd /d "%~dp0"
)

REM Xoa thu muc tam
if exist "%WORK_TEMP%" rmdir /s /q "%WORK_TEMP%" >nul 2>&1

echo.
echo ===========================================================================
echo   TU DONG CAP NHAT PATCH VIET HOA HOAN TAT!
echo ===========================================================================
echo.
echo Bam phim bat ky de MO GAME...
pause >nul

if exist "%GAME_DIR%Game.exe" start "" "%GAME_DIR%Game.exe"
exit /b 0

:NO_GAME
echo [LOI] Khong tim thay thu muc Game hop le!
echo Vui long dat file .bat nay vao thu muc chua Game.exe hoac thu muc root cua Game.
echo.
pause
exit /b 1

:NO_ZIP
echo [LOI] Khong the tai goi patch tu GitHub! Vui long kiem tra ket noi mang.
if exist "%WORK_TEMP%" rmdir /s /q "%WORK_TEMP%" >nul 2>&1
pause
exit /b 1
