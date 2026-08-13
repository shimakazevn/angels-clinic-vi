@echo off
chcp 65001 >nul
title CAI DAT PATCH VIET HOA - ANGELIC CLINIC

echo.
echo ===========================================================================
echo   ANGELIC CLINIC (TENSHI NO HAYAROU CLINIC) - PATCH VIET HOA 1-CLICK
echo ===========================================================================
echo.

set "GAME_DIR=."
if not exist "Game.exe" if exist "Game\Game.exe" set "GAME_DIR=Game"

if not exist "%GAME_DIR%\Game.exe" goto :NO_GAME

echo [+] Da tim thay Game.exe tai: %GAME_DIR%

set "PATCH_SRC=patch"
if not exist "%PATCH_SRC%\data" if exist "%~dp0patch\data" set "PATCH_SRC=%~dp0patch"

if not exist "%PATCH_SRC%\data" goto :NO_PATCH

echo [+] Dang tien hanh sao chep file Viet Hoa vao Game...
echo.

if exist "%PATCH_SRC%\data" echo  + Dang cai dat Thoai va Database Tieng Viet (data)...
if exist "%PATCH_SRC%\data" xcopy "%PATCH_SRC%\data" "%GAME_DIR%\data" /E /I /Y /Q >nul 2>&1

if exist "%PATCH_SRC%\js" echo  + Dang cai dat Plugin UI va Font Tieng Viet (js)...
if exist "%PATCH_SRC%\js" xcopy "%PATCH_SRC%\js" "%GAME_DIR%\js" /E /I /Y /Q >nul 2>&1

if exist "%PATCH_SRC%\img" echo  + Dang cai dat Giao dien Hinh anh UI (img)...
if exist "%PATCH_SRC%\img" xcopy "%PATCH_SRC%\img" "%GAME_DIR%\img" /E /I /Y /Q >nul 2>&1

echo.
echo ===========================================================================
echo   HOAN THANH CAI DAT PATCH VIET HOA THANH CONG!
echo ===========================================================================
echo.
echo Bam phim bat ky de MO GAME ngay lap tuc...
pause >nul

start "" "%GAME_DIR%\Game.exe"
exit /b 0

:NO_GAME
echo [LOI] Khong tim thay file Game.exe!
echo Vui long copy file .bat nay va thu muc "patch" vao cung thu muc chua Game.exe!
echo.
pause
exit /b 1

:NO_PATCH
echo [LOI] Khong tim thay thu muc "patch"!
pause
exit /b 1
