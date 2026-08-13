@echo off
chcp 65001 >nul
title Patch Viet Hoa - Thien Su Clinic

echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║       PATCH VIET HOA - Thien Su no Hayarou Clinic    ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

REM Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [CANH BAO] Khong tim thay Python!
    echo.
    echo  Vui long tai Python tai: https://www.python.org/downloads/
    echo  Chon "Add Python to PATH" khi cai dat.
    echo.

    REM Thu dung xcopy thay the
    echo  Dang thu phuong phap du phong ^(khong can Python^)...
    goto FALLBACK
)

REM Chay Python patcher
python "%~dp0tools\apply_patch.py" %*
goto END

:FALLBACK
REM Phuong phap du phong: dung xcopy thuan tuy, hoi duong dan bang set /p
echo.
set /p GAMEDIR="  Nhap duong dan thu muc game (vi du: C:\Games\TienSuClinic): "

if not exist "%GAMEDIR%\data\System.json" (
    echo.
    echo  [LOI] Khong tim thay game RPG Maker MZ tai: %GAMEDIR%
    echo  Hay kiem tra lai duong dan.
    pause
    exit /b 1
)

echo.
echo  Dang ap patch...

REM Backup + copy data
if exist "%~dp0patch\data" (
    for %%f in ("%~dp0patch\data\*.json") do (
        if exist "%GAMEDIR%\data\%%~nxf" (
            copy /Y "%GAMEDIR%\data\%%~nxf" "%GAMEDIR%\data\%%~nf.bak%%~xf" >nul
        )
    )
    xcopy /Y /S /E "%~dp0patch\data\*" "%GAMEDIR%\data\" >nul
    echo  [OK] Da patch file text (JSON)
)

REM Backup + copy img
if exist "%~dp0patch\img" (
    xcopy /Y /S /E "%~dp0patch\img\*" "%GAMEDIR%\img\" >nul
    echo  [OK] Da patch anh UI
)

echo.
echo  ==========================================
echo   PATCH THANH CONG!
echo   Mo thu muc game va chay Game.exe de choi.
echo  ==========================================
echo.

:END
pause
