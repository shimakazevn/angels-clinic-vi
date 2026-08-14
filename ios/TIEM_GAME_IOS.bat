@echo off
chcp 65001 >nul
title TIEM DU LIEU GAME VAO FILE IOS IPA
setlocal enabledelayedexpansion

echo ============================================================
echo      CONG CU DONG GOI FILE IOS .IPA - THIEN SU CLINIC
echo ============================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Khong tim thay Python! Vui long cai dat Python 3 de su dung.
    pause
    exit /b 1
)

python inject_game_ios.py

echo.
echo ============================================================
echo  Da hoan tat! Nhan phim bat ky de thoat.
echo ============================================================
pause >nul
