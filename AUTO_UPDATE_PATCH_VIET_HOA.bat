@echo off
setlocal enabledelayedexpansion
title CAP NHAT AUTOMATIC PATCH VIET HOA - ANGELS CLINIC VI

set "REPO_ZIP_URL=https://github.com/shimakazevn/angels-clinic-vi/archive/refs/heads/master.zip"

echo ===========================================================================
echo   ANGELIC CLINIC - TU DONG TAI VA CAP NHAT PATCH VIET HOA
echo   Repo: https://github.com/shimakazevn/angels-clinic-vi
echo ===========================================================================
echo.

REM --- 1. Dinh vi thu muc Game (Banquyen / Repack / Game.exe in subfolders) ---
set "GAME_DIR=."
if not exist "Game.exe" (
    if exist "Game\Game.exe" set "GAME_DIR=Game"
    if exist "www\index.html" set "GAME_DIR=www"
    if exist "app\index.html" set "GAME_DIR=app"
)

REM Truong hop game co data.dts & SRPG_Unpacker.exe (Banan / Repack)
if exist "data.dts" if exist "SRPG_Unpacker.exe" (
    if not exist "data" (
        echo [+] Phat hien file data.dts va SRPG_Unpacker.exe, dang giai nen...
        SRPG_Unpacker.exe -o "data" "data.dts" >nul 2>&1
    )
)

if not exist "%GAME_DIR%\index.html" if not exist "%GAME_DIR%\data\System.json" if not exist "%GAME_DIR%\Game.exe" goto :NO_GAME

echo [+] Da dinh vi xong thu muc Game: %GAME_DIR%
echo [+] Dang tai goi Viet Hoa moi nhat tu GitHub...
echo.

REM --- 2. Tai goi patch qua curl hoac powershell ---
if exist "%SystemRoot%\System32\curl.exe" (
    echo [+] Dang su dung curl sieu toc...
    curl.exe -L --progress-bar -o "patch_latest.zip" "%REPO_ZIP_URL%"
) else (
    echo [+] Dang su dung PowerShell...
    powershell -Command "$ProgressPreference = 'SilentlyContinue'; [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%REPO_ZIP_URL%' -OutFile 'patch_latest.zip'"
)

if not exist "patch_latest.zip" goto :NO_ZIP

echo.
echo [+] Dang giai nen va ap dung Viet Hoa vao game...
if exist "temp_patch" rmdir /s /q "temp_patch"
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path 'patch_latest.zip' -DestinationPath 'temp_patch' -Force"

set "EXTRACTED_DIR=temp_patch"
for /d %%D in (temp_patch\*) do set "EXTRACTED_DIR=%%D"

REM Copy patch vao thu muc game
if exist "%EXTRACTED_DIR%\patch\data" xcopy "%EXTRACTED_DIR%\patch\data" "%GAME_DIR%\data" /E /I /Y /Q >nul 2>&1
if exist "%EXTRACTED_DIR%\patch\js" xcopy "%EXTRACTED_DIR%\patch\js" "%GAME_DIR%\js" /E /I /Y /Q >nul 2>&1
if exist "%EXTRACTED_DIR%\patch\img" xcopy "%EXTRACTED_DIR%\patch\img" "%GAME_DIR%\img" /E /I /Y /Q >nul 2>&1

if exist "%EXTRACTED_DIR%\data" xcopy "%EXTRACTED_DIR%\data" "%GAME_DIR%\data" /E /I /Y /Q >nul 2>&1
if exist "%EXTRACTED_DIR%\js" xcopy "%EXTRACTED_DIR%\js" "%GAME_DIR%\js" /E /I /Y /Q >nul 2>&1
if exist "%EXTRACTED_DIR%\img" xcopy "%EXTRACTED_DIR%\img" "%GAME_DIR%\img" /E /I /Y /Q >nul 2>&1

REM Truong hop game unpack dong goi lai data.dts
if exist "data.dts" if exist "SRPG_Unpacker.exe" (
    echo [+] Dang dong goi lai data.dts...
    SRPG_Unpacker.exe -o "data.dts" "data" >nul 2>&1
)

rmdir /s /q "temp_patch" >nul 2>&1
del /f /q "patch_latest.zip" >nul 2>&1

echo.
echo ===========================================================================
echo   TU DONG CAP NHAT PATCH VIET HOA HOAN TAT!
echo ===========================================================================
echo.
echo Bam phim bat ky de MO GAME...
pause >nul

if exist "%GAME_DIR%\Game.exe" start "" "%GAME_DIR%\Game.exe"
exit /b 0

:NO_GAME
echo [LOI] Khong tim thay thu muc Game hop le!
echo Vui long dat file .bat nay vao thu muc chua Game.exe hoac thu muc root cua Game.
echo.
pause
exit /b 1

:NO_ZIP
echo [LOI] Khong the tai goi patch tu GitHub! Vui long kiem tra ket noi mang.
pause
exit /b 1
