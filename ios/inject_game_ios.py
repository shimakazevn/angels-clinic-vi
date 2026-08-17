#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ tự động tiêm (inject) dữ liệu Game RPG Maker MZ Việt Hóa vào file iOS .IPA Shell
Tự động tiêm đầy đủ Icons, Plist, Game Assets, Audio ASCII Aliases, và VorbisDecoder WebAssembly / Non-fatal Audio Guards cho iOS WebKit.
"""

import os
import sys
import io
import re
import json
import shutil
import hashlib
import zipfile
import argparse
import plistlib
from pathlib import Path
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
DEFAULT_GAME_DIR = REPO_ROOT.parent / "天使の早漏治療クリニック - TEST" / "Game"
OUTPUT_DIR = BASE_DIR / "output"

def print_banner():
    print("=" * 60)
    print("    CONG CU TIEM DU LIEU GAME VA ICONS VAO FILE IOS .IPA")
    print("=" * 60)

def find_shell_ipa():
    candidates = [
        BASE_DIR / "ThienSuClinic-shell.ipa",
        BASE_DIR / "ThienSuClinic.ipa",
        REPO_ROOT / "ThienSuClinic-shell.ipa",
        OUTPUT_DIR / "ThienSuClinic-shell.ipa"
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    
    for p in REPO_ROOT.rglob("*.ipa"):
        if "shell" in p.name.lower():
            return p
    return None

def generate_and_inject_icons(app_dir: Path, game_dir: Path):
    """Tạo và nhúng trực tiếp icon tràn viền (Full-bleed) vào Payload/*.app"""
    src_icon_path = game_dir / "icon" / "icon.png"
    if not src_icon_path.exists():
        src_icon_path = REPO_ROOT.parent / "天使の早漏治療クリニック" / "Game" / "icon" / "icon.png"

    if src_icon_path.exists():
        try:
            src_img = Image.open(src_icon_path).convert("RGB")
            master_1024 = src_img.resize((1024, 1024), Image.Resampling.LANCZOS)

            icon_map = {
                "AppIcon60x60@2x.png": 120,
                "AppIcon60x60@3x.png": 180,
                "AppIcon76x76@2x~ipad.png": 152,
                "AppIcon76x76~ipad.png": 76,
                "AppIcon83.5x83.5@2x~ipad.png": 167,
                "AppIcon.png": 120,
                "icon.png": 120,
                "iTunesArtwork": 512,
                "iTunesArtwork@2x": 1024
            }

            for name, sz in icon_map.items():
                target_f = app_dir / name
                img_res = master_1024.resize((sz, sz), Image.Resampling.LANCZOS)
                img_res.save(target_f, format="PNG")

            print("  [OK] Đã tạo và nhúng bộ Icon tràn viền iOS (không viền đen)")
        except Exception as e:
            print(f"  [!] Cảnh báo tạo icon: {e}")

    # Patch Info.plist để khai báo CFBundleIcons rõ ràng
    plist_path = app_dir / "Info.plist"
    if plist_path.exists():
        try:
            with open(plist_path, 'rb') as fp:
                pl = plistlib.load(fp)
            
            icon_files = ["AppIcon60x60", "AppIcon76x76", "AppIcon", "icon"]
            pl["CFBundleIcons"] = {
                "CFBundlePrimaryIcon": {
                    "CFBundleIconFiles": icon_files,
                    "CFBundleIconName": "AppIcon"
                }
            }
            pl["CFBundleIcons~ipad"] = {
                "CFBundlePrimaryIcon": {
                    "CFBundleIconFiles": icon_files,
                    "CFBundleIconName": "AppIcon"
                }
            }
            pl["CFBundleIconFiles"] = icon_files
            pl["GCSupportsGameMode"] = True
            pl["GCSupportedGameControllers"] = [
                {"ProfileName": "ExtendedGamepad"},
                {"ProfileName": "DirectionalGamepad"}
            ]
            pl["GCSupportsControllerUserInteraction"] = True
            pl["UIRequiresFullScreen"] = True
            pl["UIViewControllerBasedStatusBarAppearance"] = True
            pl["UIStatusBarHidden"] = True
            pl["CADisableMinimumFrameDurationOnPhone"] = True

            with open(plist_path, 'wb') as fp:
                plistlib.dump(pl, fp)
            print("  [OK] Đã cập nhật Info.plist với CFBundleIcons, Game Mode & Hiding Home Bar")
        except Exception as e:
            print(f"  [!] Cảnh báo patch Info.plist: {e}")


def setup_ios_audio_aliases_and_mapping(temp_www: Path):
    """Tạo bản sao ASCII an toàn cho toàn bộ file Audio có ký tự tiếng Nhật và sinh plugin map"""
    audio_dir = temp_www / "audio"
    if not audio_dir.exists():
        return
    
    audio_map = {}
    copied = 0

    for folder in ["bgm", "bgs", "me", "se"]:
        f_dir = audio_dir / folder
        if not f_dir.exists():
            continue
        
        idx = 0
        for p in sorted(f_dir.glob("*.ogg")):
            stem = p.stem
            try:
                stem.encode("ascii")
            except UnicodeEncodeError:
                idx += 1
                h = hashlib.md5(stem.encode("utf-8")).hexdigest()[:6]
                safe_name = f"{folder}_{idx:03d}_{h}"
                
                safe_file = f_dir / f"{safe_name}.ogg"
                shutil.copy2(p, safe_file)
                copied += 1
                
                audio_map[f"{folder}/{stem}"] = safe_name
                audio_map[stem] = safe_name

    # Sinh plugin FixIOSAudioMapping.js kèm WebAudio Vorbis Safety
    plugin_js = f"""//=============================================================================
// FixIOSAudioMapping.js
// Maps all Japanese/Unicode audio filenames to safe ASCII aliases & protects WebAudio for iOS WebKit.
//=============================================================================
(() => {{
    const AUDIO_MAP = {json.dumps(audio_map, ensure_ascii=False, indent=2)};

    const _AudioManager_createBuffer = AudioManager.createBuffer;
    AudioManager.createBuffer = function(folder, name) {{
        const cleanFolder = folder.replace(/\\/$/, "");
        const key = cleanFolder + "/" + name;
        let targetName = name;
        if (AUDIO_MAP[key]) {{
            targetName = AUDIO_MAP[key];
        }} else if (AUDIO_MAP[name]) {{
            targetName = AUDIO_MAP[name];
        }}
        const ext = this.audioFileExt();
        const url = this._path + folder + Utils.encodeURI(targetName) + ext;
        const buffer = new WebAudio(url);
        buffer.autoPlay = true;
        return buffer;
    }};

    // Chặn lỗi AudioManager.checkErrors làm dừng màn hình trên iOS
    AudioManager.checkErrors = function() {{
        const buffers = [this._bgmBuffer, this._bgsBuffer, this._meBuffer];
        buffers.push(...this._staticBuffers);
        for (const buffer of buffers) {{
            if (buffer && buffer.isError()) {{
                console.warn("[AudioManager] Non-fatal audio load error suppressed:", buffer.url);
                buffer._isError = false;
                buffer._isLoaded = true;
            }}
        }}
    }};
}})();
"""
    
    plugin_file = temp_www / "js" / "plugins" / "FixIOSAudioMapping.js"
    plugin_file.write_text(plugin_js, encoding="utf-8")
    
    # Đăng ký vào plugins.js
    plugins_js_path = temp_www / "js" / "plugins.js"
    if plugins_js_path.exists():
        content = plugins_js_path.read_text(encoding="utf-8")
        if "FixIOSAudioMapping" not in content:
            idx = content.rfind("]")
            if idx != -1:
                entry = ',\n{"name":"FixIOSAudioMapping","status":true,"description":"Fixes iOS non-ASCII audio loading & safety","parameters":{}}\n'
                new_content = content[:idx].rstrip() + entry + content[idx:]
                plugins_js_path.write_text(new_content, encoding="utf-8")

    print(f"  [OK] Đã tạo {copied} file alias ASCII cho Audio và kích hoạt FixIOSAudioMapping.js")

def patch_web_assets_for_ios(temp_www: Path):
    """Patch các file JavaScript để tối ưu cho iOS WebKit WKWebView"""
    js_dir = temp_www / "js"
    
    # 1. Patch rmmz_core.js (VorbisDecoder & WebAudio Safety)
    core_file = js_dir / "rmmz_core.js"
    if core_file.exists():
        content = core_file.read_text(encoding="utf-8")
        # Fix Nwjs
        content = re.sub(r'Utils\.isNwjs\s*=\s*function\(\)\s*\{[^}]*\}',
                         'Utils.isNwjs = function() { return typeof nw === "object"; }',
                         content)
        
        # Ép buộc dùng VorbisDecoder cho OGG trên iOS WebKit
        vorbis_patch = "WebAudio.prototype._shouldUseDecoder = function() {\n    return typeof VorbisDecoder === 'function';\n};"
        content = re.sub(r'WebAudio\.prototype\._shouldUseDecoder\s*=\s*function\(\)\s*\{[\s\S]*?^\s*\};',
                         vorbis_patch, content, flags=re.MULTILINE)

        # Tránh crash khi decodeAudioData lỗi
        decode_patch = """WebAudio.prototype._decodeAudioData = function(arrayBuffer) {
    if (this._shouldUseDecoder()) {
        if (this._decoder) {
            this._decoder.send(arrayBuffer, this._isLoaded);
        }
    } else {
        WebAudio._context
            .decodeAudioData(arrayBuffer.slice())
            .then(buffer => this._onDecode(buffer))
            .catch(err => {
                if (typeof VorbisDecoder === "function") {
                    this._destroyDecoder();
                    this._createDecoder();
                    if (this._decoder) {
                        this._decoder.send(arrayBuffer, this._isLoaded);
                        return;
                    }
                }
                console.warn("Audio decode failed, skipping gracefully:", this._url, err);
                this._onLoad();
            });
    }
};"""
        content = re.sub(r'WebAudio\.prototype\._decodeAudioData\s*=\s*function\(arrayBuffer\)\s*\{[\s\S]*?^\s*\};',
                         decode_patch, content, flags=re.MULTILINE)

        content = content.replace("preferQueryMode: false", "preferQueryMode: false, powerPreference: 'high-performance'")
        core_file.write_text(content, encoding="utf-8")
        print("  [OK] Patch rmmz_core.js (VorbisDecoder & WebAudio Safety)")

    # 2. Patch rmmz_managers.js
    mgr_file = js_dir / "rmmz_managers.js"
    if mgr_file.exists():
        content = mgr_file.read_text(encoding="utf-8")
        content = re.sub(
            r'SceneManager\.isGameActive\s*=\s*function\(\)\s*\{[\s\S]*?^\s*\};',
            'SceneManager.isGameActive = function() {\n    return true;\n};',
            content,
            flags=re.MULTILINE
        )
        mgr_file.write_text(content, encoding="utf-8")
        print("  [OK] Patch rmmz_managers.js (luôn active)")

    # 3. Patch index.html
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
        print("\nBUOC 1: Giai nen file IPA shell...")
        with zipfile.ZipFile(shell_ipa, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

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

        print("\nBUOC 2: Sao chep du lieu game (~700 MB)...")
        subdirs = ["audio", "css", "data", "effects", "fonts", "img", "js"]
        for sub in subdirs:
            src_sub = game_dir / sub
            if src_sub.exists():
                dst_sub = target_www / sub
                shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)
                file_count = sum(1 for _ in dst_sub.rglob("*") if _.is_file())
                print(f"  [OK] {sub}/ ({file_count} files)")

        for fn in ["index.html", "package.json"]:
            src_f = game_dir / fn
            if src_f.exists():
                shutil.copy2(src_f, target_www / fn)
                print(f"  [OK] {fn}")

        print("\nBUOC 3: Patch ma nguon cho iOS WebKit, Audio Aliases & Nhúng Icon...")
        patch_web_assets_for_ios(target_www)
        setup_ios_audio_aliases_and_mapping(target_www)
        generate_and_inject_icons(app_dir, game_dir)

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
        print("    TIEM DU LIEU GAME VA ICONS VAO FILE IOS .IPA THANH CONG!")
        print(f"    File IPA: {output_ipa}")
        print(f"    Dung luong: {final_size_mb:.1f} MB")
        print("=" * 60)
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

    if args.ipa:
        shell_ipa = Path(args.ipa).resolve()
    else:
        shell_ipa = find_shell_ipa()
        if not shell_ipa:
            print("[-] Chua tim thay file 'ThienSuClinic-shell.ipa' trong thu muc 'ios/'.")
            return

    if args.game_dir:
        game_dir = Path(args.game_dir).resolve()
    else:
        game_dir = DEFAULT_GAME_DIR

    if args.output:
        output_ipa = Path(args.output).resolve()
    else:
        output_ipa = OUTPUT_DIR / "ThienSuClinic-VietHoa.ipa"

    inject_game(shell_ipa, game_dir, output_ipa)

if __name__ == "__main__":
    main()
