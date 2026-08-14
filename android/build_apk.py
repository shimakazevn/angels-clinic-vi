#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_apk.py -- Build Android APK tu game RPG Maker MZ da patch Viet hoa

Yeu cau truoc khi chay:
  1. Java JDK 11+ (https://adoptium.net/)
  2. Android SDK Command-line Tools (https://developer.android.com/studio#command-tools)
  3. Da ap patch Viet hoa truoc (chay apply_patch.bat/sh)

Cach dung:
  python android/build_apk.py --game-dir "C:\\Games\\TienSuClinic"
  python android/build_apk.py  (hoi duong dan sau)

Output:
  android/output/viet-hoa-thiensu.apk
"""

import os
import sys
import io
import shutil
import subprocess
import platform
import argparse
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ---- Cau hinh duong dan ----
SCRIPT_DIR   = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "template"
ASSETS_DIR   = TEMPLATE_DIR / "app" / "src" / "main" / "assets"
OUTPUT_DIR   = SCRIPT_DIR / "output"
OUTPUT_APK   = OUTPUT_DIR / "viet-hoa-thiensu.apk"

IS_WINDOWS = platform.system() == "Windows"
GRADLEW = "gradlew.bat" if IS_WINDOWS else "gradlew"

# Cac file/thu muc game can copy vao APK
GAME_INCLUDES = [
    "audio",
    "css",
    "data",
    "effects",
    "fonts",
    "img",
    "js",
    "index.html",
    "package.json",
]

# Cac thu muc/file KHONG copy
GAME_EXCLUDES = {
    # NW.js runtime -- khong can tren Android
    "Game.exe",
    "nw.dll", "nw_elf.dll", "node.dll", "ffmpeg.dll",
    "libEGL.dll", "libGLESv2.dll", "d3dcompiler_47.dll",
    "nw_100_percent.pak", "nw_200_percent.pak",
    "icudtl.dat", "resources.pak", "v8_context_snapshot.bin",
    "notification_helper.exe",
    "credits.html", "read me.txt", ".gitignore",
    # Thu muc khong can
    "locales", "swiftshader", "save", "icon",
    "gameupdate", "GameUpdate.bat", "GameUpdate_linux.sh",
}

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}[OK]{RESET} {msg}")
def warn(msg): print(f"  {YELLOW}[!!]{RESET} {msg}")
def err(msg):  print(f"  {RED}[XX]{RESET} {msg}")
def info(msg): print(f"  {CYAN}[..]{RESET} {msg}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")

# ========== Kiem tra moi truong ==========

def check_java() -> bool:
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True, text=True
        )
        version_line = result.stderr or result.stdout
        ok(f"Java: {version_line.split(chr(10))[0].strip()}")
        return True
    except FileNotFoundError:
        err("Khong tim thay Java!")
        err("  Tai tai: https://adoptium.net/")
        err("  Chon 'Temurin 17' va cai dat")
        return False

def check_android_sdk() -> Path | None:
    """Tim Android SDK trong cac vi tri pho bien."""
    candidates = []

    if os.environ.get("ANDROID_HOME"):
        candidates.append(Path(os.environ["ANDROID_HOME"]))
    if os.environ.get("ANDROID_SDK_ROOT"):
        candidates.append(Path(os.environ["ANDROID_SDK_ROOT"]))

    home = Path.home()
    if IS_WINDOWS:
        candidates += [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk",
            Path(os.environ.get("APPDATA", "")) / "Android" / "Sdk",
            home / "AppData" / "Local" / "Android" / "Sdk",
        ]
    else:
        candidates += [
            home / "Android" / "Sdk",
            home / "Library" / "Android" / "sdk",
            Path("/opt/android-sdk"),
        ]

    for sdk in candidates:
        if sdk.exists() and (sdk / "platforms").exists():
            ok(f"Android SDK: {sdk}")
            return sdk

    err("Khong tim thay Android SDK!")
    err("  Tai command-line tools tai:")
    err("  https://developer.android.com/studio#command-tools")
    err("  Giai nen va dat vao: ~/Android/Sdk/cmdline-tools/latest/")
    err("  Sau do chay: sdkmanager 'platforms;android-34' 'build-tools;34.0.0'")
    return None

def check_gradlew() -> bool:
    gw = TEMPLATE_DIR / GRADLEW
    if not gw.exists():
        err(f"Khong tim thay {GRADLEW} tai {TEMPLATE_DIR}")
        return False
    if not IS_WINDOWS:
        gw.chmod(0o755)
    ok(f"Gradle wrapper: {gw}")
    return True

# ========== Kiem tra game ==========

def validate_game(game_dir: Path) -> bool:
    required = [
        game_dir / "index.html",
        game_dir / "data" / "System.json",
        game_dir / "js" / "rmmz_core.js",
    ]
    for r in required:
        if not r.exists():
            err(f"Khong tim thay: {r.name} -- day khong phai game RPG Maker MZ")
            return False

    ok("Game dir valid: RPG Maker MZ project structure verified.")
    return True

def get_game_size(game_dir: Path) -> int:
    total = 0
    for item in GAME_INCLUDES:
        path = game_dir / item
        if path.is_file():
            total += path.stat().st_size
        elif path.is_dir():
            for f in path.rglob("*"):
                if f.is_file():
                    total += f.stat().st_size
    return total

# ========== Copy game files ==========

def copy_game_to_assets(game_dir: Path):
    header("BUOC 3: Copy game files vao APK")

    if ASSETS_DIR.exists():
        info("Dang xoa assets cu...")
        shutil.rmtree(ASSETS_DIR)
    ASSETS_DIR.mkdir(parents=True)

    total_bytes = 0
    total_files = 0

    for item_name in GAME_INCLUDES:
        src = game_dir / item_name
        dst = ASSETS_DIR / item_name

        if not src.exists():
            warn(f"  Bo qua (khong tim thay): {item_name}")
            continue

        if src.is_file():
            shutil.copy2(src, dst)
            total_files += 1
            total_bytes += src.stat().st_size
            info(f"  {item_name}")
        elif src.is_dir():
            info(f"  {item_name}/ ...")
            n = 0
            for f in src.rglob("*"):
                if not f.is_file():
                    continue
                if f.name in GAME_EXCLUDES:
                    continue
                rel = f.relative_to(src)
                dst_f = dst / rel
                dst_f.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst_f)
                n += 1
                total_bytes += f.stat().st_size
            ok(f"  {item_name}/: {n} files")
            total_files += n

    size_mb = total_bytes / 1024 / 1024
    ok(f"Tong cong: {total_files} files, {size_mb:.1f} MB")
    warn(f"APK cuoi se nang khoang {size_mb * 1.05:.0f} MB (sau khi dong goi)")

# ========== Android WebView Compatibility Patch ==========

def patch_for_android():
    """Patch cac file JS de tuong thich 100% voi Android WebView va fix triet de loi man hinh den."""
    header("BUOC 3.5: Patch JS cho Android WebView")

    # --- Patch 1: rmmz_core.js ---
    core_js = ASSETS_DIR / "js" / "rmmz_core.js"
    if core_js.exists():
        content = core_js.read_text(encoding="utf-8")
        
        # 1.1 Fix Utils.isNwjs
        OLD_NWJS = 'return typeof require === "function" && typeof process === "object";'
        NEW_NWJS = 'return typeof nw === "object"; // Android fix: avoid false positive from vorbisdecoder.js'
        if OLD_NWJS in content:
            content = content.replace(OLD_NWJS, NEW_NWJS, 1)
            ok("  rmmz_core.js: da patch Utils.isNwjs() -> typeof nw === 'object'")

        # 1.2 Robust WebGL context creation for PIXI
        NEW_CREATE_PIXI = (
            "Graphics._createPixiApp = function() {\n"
            "    try {\n"
            "        this._setupPixi();\n"
            "        this._app = new PIXI.Application({\n"
            "            view: this._canvas,\n"
            "            autoStart: false,\n"
            "            powerPreference: 'default',\n"
            "            preserveDrawingBuffer: true\n"
            "        });\n"
            "        this._app.ticker.remove(this._app.render, this._app);\n"
            "        this._app.ticker.add(this._onTick, this);\n"
            "    } catch (e) {\n"
            "        console.error('PIXI App Creation Failed:', e);\n"
            "        this._app = null;\n"
            "    }\n"
            "};"
        )
        content = re.sub(r'Graphics\._createPixiApp\s*=\s*function\(\)\s*\{[\s\S]*?\n\};', NEW_CREATE_PIXI, content)
        ok("  rmmz_core.js: da patch _createPixiApp voi WebGL chuan")

        # 1.3 Fix Effekseer Context creation to NEVER null out this._app
        NEW_EFFEKSEER = (
            "Graphics._createEffekseerContext = function() {\n"
            "    this._effekseer = null;\n"
            "    if (this._app && this._app.renderer && this._app.renderer.gl && window.effekseer && typeof effekseer.createContext === 'function') {\n"
            "        try {\n"
            "            const ctx = effekseer.createContext();\n"
            "            if (ctx) {\n"
            "                ctx.init(this._app.renderer.gl);\n"
            "                ctx.setRestorationOfStatesFlag(false);\n"
            "                this._effekseer = ctx;\n"
            "            }\n"
            "        } catch (e) {\n"
            "            console.warn('Effekseer WebGL init skipped on this device:', e);\n"
            "            this._effekseer = null;\n"
            "        }\n"
            "    }\n"
            "};"
        )
        content = re.sub(r'Graphics\._createEffekseerContext\s*=\s*function\(\)\s*\{[\s\S]*?\n\};', NEW_EFFEKSEER, content)
        ok("  rmmz_core.js: da patch _createEffekseerContext de tranh null _app")

        # 1.4 Clean PIXI setup
        NEW_SETUP = (
            "Graphics._setupPixi = function() {\n"
            "    PIXI.utils.skipHello();\n"
            "    PIXI.settings.GC_MAX_IDLE = 600;\n"
            "};"
        )
        content = re.sub(r'Graphics\._setupPixi\s*=\s*function\(\)\s*\{[\s\S]*?\n\};', NEW_SETUP, content)

        core_js.write_text(content, encoding="utf-8")

    # --- Patch 2: main.js ---
    main_js = ASSETS_DIR / "js" / "main.js"
    if main_js.exists():
        main_content = main_js.read_text(encoding="utf-8")

        # 2.1 Ensure pixi.js is used (NOT pixi-legacy)
        main_content = main_content.replace('"js/libs/pixi-legacy.js"', '"js/libs/pixi.js"')

        # 2.2 Fix isPathRandomized
        OLD_PROCESS = 'typeof process === "object" &&'
        NEW_PROCESS = 'typeof process === "object" && process.mainModule &&'
        if OLD_PROCESS in main_content and NEW_PROCESS not in main_content:
            main_content = main_content.replace(OLD_PROCESS, NEW_PROCESS, 1)

        # 2.3 Fix initEffekseerRuntime with safety timeout so game NEVER gets stuck on black screen
        NEW_EFFEKSEER_RUNTIME = (
            "    initEffekseerRuntime() {\n"
            "        let booted = false;\n"
            "        const bootGame = () => {\n"
            "            if (!booted) {\n"
            "                booted = true;\n"
            "                this.eraseLoadingSpinner();\n"
            "                SceneManager.run(Scene_Boot);\n"
            "            }\n"
            "        };\n"
            "\n"
            "        const timer = setTimeout(() => {\n"
            "            console.warn('[Main] Effekseer wasm load timed out, starting game directly...');\n"
            "            bootGame();\n"
            "        }, 1000);\n"
            "\n"
            "        try {\n"
            "            effekseer.initRuntime(\n"
            "                effekseerWasmUrl,\n"
            "                () => {\n"
            "                    clearTimeout(timer);\n"
            "                    bootGame();\n"
            "                },\n"
            "                () => {\n"
            "                    clearTimeout(timer);\n"
            "                    console.warn('[Main] Effekseer wasm failed to load, starting game without 3D effekseer...');\n"
            "                    bootGame();\n"
            "                }\n"
            "            );\n"
            "        } catch (e) {\n"
            "            clearTimeout(timer);\n"
            "            bootGame();\n"
            "        }\n"
            "    }"
        )
        main_content = re.sub(r'initEffekseerRuntime\(\)\s*\{[\s\S]*?\n    \}', NEW_EFFEKSEER_RUNTIME, main_content)
        ok("  main.js: da patch initEffekseerRuntime voi safety timeout de luon vao duoc game")

        main_js.write_text(main_content, encoding="utf-8")

# ========== Build APK ==========

def build_apk(sdk_dir: Path):
    header("BUOC 4: Build APK (co the mat 5-15 phut lan dau)")

    env = os.environ.copy()
    env["ANDROID_HOME"] = str(sdk_dir)
    env["ANDROID_SDK_ROOT"] = str(sdk_dir)

    gradlew_path = TEMPLATE_DIR / GRADLEW

    info("Dang build... (vui long doi)")
    try:
        result = subprocess.run(
            [str(gradlew_path), "assembleRelease", "--no-daemon"],
            cwd=str(TEMPLATE_DIR),
            env=env,
            capture_output=False,
            text=True,
        )
        if result.returncode != 0:
            err("Build that bai!")
            err("  Xem log phia tren de biet chi tiet.")
            err("  Thu chay: java -version  va  kiem tra ANDROID_HOME")
            return False
        return True
    except FileNotFoundError:
        err(f"Khong chay duoc Gradle: {gradlew_path}")
        return False

def collect_apk():
    apk_locations = list((TEMPLATE_DIR / "app" / "build" / "outputs" / "apk").rglob("*.apk"))
    if not apk_locations:
        err("Khong tim thay APK output!")
        return None

    apk_src = None
    for apk in apk_locations:
        if "release" in str(apk):
            apk_src = apk
            break
    if not apk_src:
        apk_src = apk_locations[0]

    OUTPUT_DIR.mkdir(exist_ok=True)
    shutil.copy2(apk_src, OUTPUT_APK)
    ok(f"APK: {OUTPUT_APK}")
    return OUTPUT_APK

# ========== Main ==========

def main():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║         BUILD ANDROID APK - Thien Su Clinic VN        ║
╚══════════════════════════════════════════════════════╝{RESET}
""")

    parser = argparse.ArgumentParser(description="Build Android APK tu game RMMZ da patch")
    parser.add_argument("--game-dir", type=str, help="Duong dan den thu muc game")
    parser.add_argument("--sdk-dir", type=str, help="Duong dan Android SDK (tu dong tim neu bo trong)")
    args = parser.parse_args()

    # -- Buoc 1: Kiem tra moi truong --
    header("BUOC 1: Kiem tra moi truong")
    java_ok = check_java()
    sdk_dir = Path(args.sdk_dir) if args.sdk_dir else check_android_sdk()
    gradlew_ok = check_gradlew()

    if not java_ok:
        err("\nThieu Java! Xem huong dan cai dat o tren.")
        sys.exit(1)
    if not sdk_dir:
        err("\nThieu Android SDK! Xem ANDROID_GUIDE.md de biet cach cai dat.")
        sys.exit(1)
    if not gradlew_ok:
        sys.exit(1)

    # -- Buoc 2: Chon thu muc game --
    header("BUOC 2: Chon thu muc game")
    if args.game_dir:
        game_dir = Path(args.game_dir)
    else:
        print("  Nhap duong dan den thu muc game (da ap patch Viet hoa).")
        print("  Vi du: C:\\Games\\TienSuClinic")
        try:
            raw = input(f"\n  {BOLD}Duong dan:{RESET} ").strip().strip('"').strip("'")
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        game_dir = Path(raw)

    if not game_dir.exists():
        err(f"Khong tim thay thu muc: {game_dir}")
        sys.exit(1)

    if not validate_game(game_dir):
        sys.exit(1)

    size_bytes = get_game_size(game_dir)
    ok(f"Game dir: {game_dir}")
    ok(f"Dung luong se copy: {size_bytes/1024/1024:.0f} MB")

    # -- Buoc 3: Copy game files --
    copy_game_to_assets(game_dir)

    # -- Buoc 3.5: Patch JS cho Android WebView --
    patch_for_android()

    # -- Buoc 4: Build --
    if not build_apk(sdk_dir):
        sys.exit(1)

    # -- Buoc 5: Lay APK --
    header("BUOC 5: Hoan thanh")
    apk = collect_apk()
    if not apk:
        sys.exit(1)

    apk_size_mb = apk.stat().st_size / 1024 / 1024
    print(f"""
  {GREEN}{BOLD}BUILD THANH CONG!{RESET}

  APK: {BOLD}{apk}{RESET}
  Dung luong: {apk_size_mb:.0f} MB

  {BOLD}Cach cai APK len Android:{RESET}
  1. Copy APK sang dien thoai (USB hoac cloud)
  2. Mo file APK tren Android
  3. Neu hoi "Unknown sources": Bat 'Cai ung dung tu nguon khac'
  4. Cai dat va mo game

  {YELLOW}Luu y Save Game:{RESET}
  - Save game luu trong app. Goi Uninstall se XOA save!
  - Dung chuc nang 'Export Save' trong game truoc khi goi cai.
""")

if __name__ == "__main__":
    main()
