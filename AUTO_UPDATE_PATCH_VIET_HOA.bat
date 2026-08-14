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

REM --- 4. Tu dong tuong thich ten file Audio (Ban goc Nhat / Ban Kimochi EN Romaji / Mojibake) ---
if exist "%GAME_DIR%audio" (
    echo [+] Dang tu dong kiem tra va dong bo ten file Audio (Tieng Nhat / Romaji Kimochi / Mojibake)...
    powershell -ExecutionPolicy Bypass -NoProfile -Command ^
        "$map = @{ " ^
        "  'ガーデン・シティ_2.ogg' = @('gaaden_shitei_2.ogg', 'K[fEVeB_2.ogg', 'garden_city_2.ogg'); " ^
        "  'ドラマティック・シティ.ogg' = @('doramateikku_shitei.ogg', 'h}eBbNEVeB.ogg', 'dramatic_city.ogg'); " ^
        "  '今日は、気ままなカフェ巡り。.ogg' = @('konnichiha_kimamanakafemeguri.ogg', 'ACJtFB.ogg'); " ^
        "  '優しい心、温かい日.ogg' = @('yasashiikokoro_atatakainichi.ogg', 'DSA.ogg'); " ^
        "  '夏が呼んでいる.ogg' = @('natsugayondeiru.ogg', 'ĂĂł.ogg'); " ^
        "  '夢見る世界(Dreaming_world).ogg' = @('yumemirusekai_dreaming_world.ogg', 'E(Dreaming_world).ogg'); " ^
        "  '奈落への巡行.ogg' = @('narakuhenojunkou.ogg', 's.ogg'); " ^
        "  '月曜日の庭.ogg' = @('getsuyoubinoniwa.ogg', 'j.ogg'); " ^
        "  '波に揺られる.ogg' = @('naminiyurareru.ogg', 'gh.ogg'); " ^
        "  '狼達の行軍.ogg' = @('ookamitoorunokougun.ogg', 'TBsR.ogg'); " ^
        "  '秘境の地.ogg' = @('hikyounochi.ogg', 'n.ogg'); " ^
        "  '霧の中へ.ogg' = @('kirinonakahe.ogg'); " ^
        "  '静かな余韻(Quiet_suggestiveness).ogg' = @('shizukanayoin_quiet_suggestiveness.ogg', ']C(Quiet_suggestiveness).ogg'); " ^
        "  'Lazy_Midnight(深夜にまったり).ogg' = @('lazy_midnight_shinyanimattari.ogg', 'Lazy_Midnight([).ogg'); " ^
        "  'Midnight_Isolation_編集済み.ogg' = @('midnight_isolation_henshuusumi.ogg', 'Midnight_Isolation_W.ogg'); " ^
        "  'ぬるぐちゃ001.ogg' = @('nurugucha001.ogg', '001.ogg'); " ^
        "  'ぬるぐちゃ003.ogg' = @('nurugucha003.ogg', '003.ogg'); " ^
        "  'パイズリ.ogg' = @('paizuri.ogg', 'pCY.ogg'); " ^
        "  'パイズリ2.ogg' = @('paizuri2.ogg', 'pCY2.ogg'); " ^
        "  'パイズリカウベル入り.ogg' = @('paizurikauberuiri.ogg', 'pCYJEx.ogg'); " ^
        "  'パイズリカウベル入り2.ogg' = @('paizurikauberuiri2.ogg', 'pCYJEx2.ogg'); " ^
        "  'ピストン ウェット.ogg' = @('pisuton_wetto.ogg', 'pisuton wetto.ogg', 'sXg EFbg.ogg'); " ^
        "  'フェラＳＥ（中）長.ogg' = @('feraSE_chuu_chou.ogg', 'feraSE_chuu.ogg', 'tFrdij.ogg'); " ^
        "  'フェラＳＥ（強）長.ogg' = @('feraSE_kyou_chou.ogg', 'feraSE_kyou.ogg', 'tFrdij.ogg'); " ^
        "  '手コキ３（低速～中速）.ogg' = @('tekoki3_teisoku_chuusoku.ogg', 'tekoki3.ogg', 'RLRi`j.ogg'); " ^
        "  '手コキ５（中速）.ogg' = @('tekoki5_chuusoku.ogg', 'tekoki5.ogg', 'RLTij.ogg'); " ^
        "  '手コキ６（中速～高速）.ogg' = @('tekoki6_chuusoku_kousoku.ogg', 'tekoki6.ogg', 'RLUi`j.ogg'); " ^
        "  '1.ハードピストン（低速）.ogg' = @('1.haadopisuton_teisoku.ogg', '1.haadopisuton.ogg', '1.n[hsXgij.ogg'); " ^
        "  '2.ハードピストン（低速～中速）08倍速.ogg' = @('2.haadopisuton_teisoku_chuusoku_08baisoku.ogg', '2.haadopisuton.ogg', '2.n[hsXgi`j08{.ogg'); " ^
        "  '3.ハードピストン（中速）.ogg' = @('3.haadopisuton_chuusoku.ogg', '3.haadopisuton.ogg', '3.n[hsXgij.ogg') " ^
        "}; " ^
        "$files = Get-ChildItem -Path '%GAME_DIR%audio' -Recurse -Filter *.ogg; " ^
        "foreach ($jp in $map.Keys) { " ^
        "  $aliases = $map[$jp]; " ^
        "  foreach ($f in $files) { " ^
        "    if ($aliases -contains $f.Name -or $f.Name.ToLower() -eq $jp.ToLower()) { " ^
        "      $target = Join-Path $f.DirectoryName $jp; " ^
        "      if (-not (Test-Path -LiteralPath $target)) { Copy-Item -LiteralPath $f.FullName -Destination $target -Force } " ^
        "    } " ^
        "  } " ^
        "}" >nul 2>&1
)

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
