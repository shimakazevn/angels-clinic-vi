#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ tự động tiêm (inject) dữ liệu Game RPG Maker MZ Việt Hóa vào file iOS .IPA Shell
Được thiết kế để tạo file .IPA hoàn chỉnh cho iPhone / iPad.
"""

import os
import sys
import io
import re
import shutil
import zipfile
import argparse
from pathlib import Path

# Đảm bảo in UTF-8 trên Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
DEFAULT_GAME_DIR = REPO_ROOT.parent / "天使の早漏治療クリニック - TEST" / "Game"
OUTPUT_DIR = BASE_DIR / "output"

def print_banner():
    print("=" * 60)
    print("    CONG CU TIEM DU LIEU GAME VAO FILE IOS .IPA SHELL")
    print("=" * 60)

def find_shell_ipa():
    # 1. Check in ios/ folder or root
    candidates = [
        BASE_DIR / "ThienSuClinic-shell.ipa",
        BASE_DIR / "ThienSuClinic.ipa",
        REPO_ROOT / "ThienSuClinic-shell.ipa",
        OUTPUT_DIR / "ThienSuClinic-shell.ipa"
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    
    # 2. Search anywhere in repo
    for p in REPO_ROOT.rglob("*.ipa"):
        if "shell" in p.name.lower():
            return p
    return None

def patch_web_assets_for_ios(temp_www: Path):
    """Patch các file JavaScript để tối ưu cho iOS WebKit WKWebView"""
    js_dir = temp_www / "js"
    
    # Patch rmmz_core.js
    core_file = js_dir / "rmmz_core.js"
    if core_file.exists():
        content = core_file.read_text(encoding="utf-8")
        # Fix Nwjs check
        content = re.sub(r'Utils\.isNwjs\s*=\s*function\(\)\s*\{[^}]*\}',
                         'Utils.isNwjs = function() { return typeof nw === "object"; }',
                         content)
        # Fix WebGL auto fallback
        content = content.replace("preferQueryMode: false", "preferQueryMode: false, powerPreference: 'high-performance'")
        core_file.write_text(content, encoding="utf-8")
        print("  [OK] Patch rmmz_core.js cho iOS")

    # Patch rmmz_managers.js: Giữ audio và game active khi mất focus
    mgr_file = js_dir / "rmmz_managers.js"
    if mgr_file.exists():
        content = mgr_file.read_text(encoding="utf-8")
        content = re.sub(r'SceneManager\.isGameActive\s*=\s*function\(\)\s*\{[^}]*\}',
                         'SceneManager.isGameActive = function() { return true; }',
                         content)
        mgr_file.write_text(content, encoding="utf-8")
        print("  [OK] Patch rmmz_managers.js (luôn active)")

    # Patch index.html cho tràn viền tai thỏ / dynamic island
    index_file = temp_www / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        if 'viewport-fit=cover' not in content:
            content = content.replace(
                'content="user-scalable=no">',
                'content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width, height=device-height, viewport-fit=cover">'
            )
            content = content.replace(
                '<body style="background-color: black">',
                '<body style="background-color: black; margin: 0; padding: 0; overflow: hidden; -webkit-user-select: none;">'
            )
            index_file.write_text(content, encoding="utf-8")
            print("  [OK] Patch index.html (viewport-fit=cover)")

def inject_game(shell_ipa: Path, game_dir: Path, output_ipa: Path):
    if not shell_ipa.exists():
        print(f"[-] LOI: Khong tim thay file IPA shell tai: {shell_ipa}")
        print("    Vui long tai file 'ThienSuClinic-shell.ipa' tu GitHub Actions ve dat vao thu muc 'ios/'.")
        return False

    if not (game_dir / "data" / "System.json").exists():
        print(f"[-] LOI: Thu muc game khong hop le: {game_dir}")
        return False

    print(f"\n[+] Su dung IPA Shell: {shell_ipa.name}")
    print(f"[+] Thu muc Game nguon: {game_dir}")
    print(f"[+] File dau ra du kien: {output_ipa}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = BASE_DIR / "_temp_inject"
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Giai nen IPA shell
        print("\nBUOC 1: Giai nen file IPA shell...")
        with zipfile.ZipFile(shell_ipa, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Tim thu muc Payload/*.app
        payload_dir = temp_dir / "Payload"
        if not payload_dir.exists():
            print("[-] LOI: Khong tim thay thu muc Payload trong file IPA!")
            return False

        app_dirs = list(payload_dir.glob("*.app"))
        if not app_dirs:
            print("[-] LOI: Khong tim thay file .app nao trong Payload!")
            return False

        app_dir = app_dirs[0]
        target_www = app_dir / "www"
        if target_www.exists():
            shutil.rmtree(target_www, ignore_errors=True)
        target_www.mkdir(parents=True, exist_ok=True)

        # 2. Copy tai nguyen Game vao www/
        print("\nBUOC 2: Sao chep du lieu game (~700 MB)...")
        subdirs = ["audio", "css", "data", "effects", "fonts", "img", "js"]
        for sub in subdirs:
            src_sub = game_dir / sub
            if src_sub.exists():
                dst_sub = target_www / sub
                shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)
                file_count = sum(1 for _ in dst_sub.rglob("*") if _.is_file())
                print(f"  [OK] {sub}/ ({file_count} files)")

        # Copy single files
        for fn in ["index.html", "package.json"]:
            src_f = game_dir / fn
            if src_f.exists():
                shutil.copy2(src_f, target_www / fn)
                print(f"  [OK] {fn}")

        # 3. Patch JS cho iOS
        print("\nBUOC 3: Patch ma nguon cho iOS WebKit...")
        patch_web_assets_for_ios(target_www)

        # 4. Dong goi lai thanh IPA
        print(f"\nBUOC 4: Dong goi file IPA hoan chinh...")
        if output_ipa.exists():
            try:
                output_ipa.unlink()
            except Exception:
                pass

        with zipfile.ZipFile(output_ipa, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zip_out.write(file_path, arcname)

        final_size_mb = output_ipa.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 60)
        print("    TIEM DU LIEU GAME VAO FILE IOS .IPA THANH CONG!")
        print(f"    File IPA: {output_ipa}")
        print(f"    Dung luong: {final_size_mb:.1f} MB")
        print("=" * 60)
        print("\nHuong dan cai dat len iPhone / iPad:")
        print("1. Cai dat qua AltStore / Sideloadly / Scarlet / TrollStore / LiveContainer.")
        print("2. Chon file: " + str(output_ipa))
        print("3. Sign va cai dat truc tiep vao may.\n")
        return True

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Inject Game Data into iOS Shell IPA")
    parser.add_argument("--ipa", type=str, default=None, help="Duong dan den file IPA shell")
    parser.add_argument("--game-dir", type=str, default=None, help="Thu muc game nguon")
    parser.add_argument("--output", type=str, default=None, help="Duong dan file IPA dau ra")
    args = parser.parse_args()

    # 1. Xac dinh shell IPA
    if args.ipa:
        shell_ipa = Path(args.ipa).resolve()
    else:
        shell_ipa = find_shell_ipa()
        if not shell_ipa:
            print("[-] Chua tim thay file 'ThienSuClinic-shell.ipa' trong thu muc 'ios/'.")
            print("    Vui long copy file IPA shell tai ve tu GitHub Actions vao day:")
            print(f"    {BASE_DIR}")
            return

    # 2. Xac dinh thu muc game
    if args.game_dir:
        game_dir = Path(args.game_dir).resolve()
    else:
        game_dir = DEFAULT_GAME_DIR
        if not game_dir.exists():
            # Thu tim cac thu muc game ben canh
            candidates = [
                REPO_ROOT.parent / "天使の早漏治療クリニック" / "Game",
                REPO_ROOT.parent / "Game"
            ]
            for c in candidates:
                if (c / "data" / "System.json").exists():
                    game_dir = c
                    break

    # 3. Xac dinh file output
    if args.output:
        output_ipa = Path(args.output).resolve()
    else:
        output_ipa = OUTPUT_DIR / "ThienSuClinic-VietHoa.ipa"

    inject_game(shell_ipa, game_dir, output_ipa)

if __name__ == "__main__":
    main()
