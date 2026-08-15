#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_release.py - Cong cu tu dong dong goi va upload Release len GitHub cho tat ca cac nen tang:
  1. Cap nhat Game Title voi phien ban va Git Commit SHA
  2. Dong bo hoa du lieu sang PC, Android va iOS
  3. Tao file ZIP Full Game PC (Giai nen la choi ngay tren Windows)
  4. Bien dich Android APK (Cai dat truc tiep tren Android)
  5. Bien dich iOS IPA (Cai dat qua TrollStore / Sideloadly / Scarlet tren iOS)
  6. Upload tat ca len GitHub Release qua GitHub CLI (`gh release create`)
"""

import os
import sys
import io
import json
import shutil
import zipfile
import subprocess
import argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR
GAME_TEST_DIR = REPO_ROOT.parent / "天使の早漏治療クリニック - TEST" / "Game"
PATCH_DIR = REPO_ROOT / "patch"
ANDROID_DIR = REPO_ROOT / "android"
IOS_DIR = REPO_ROOT / "ios"
RELEASE_OUT = REPO_ROOT / "release_dist"

def run_cmd(cmd, cwd=None):
    print(f"[EXEC] {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        print(f"[ERR] Command failed with returncode {res.returncode}:")
        print(res.stderr)
        return False, res.stdout, res.stderr
    return True, res.stdout, res.stderr

def get_git_commit():
    ok, out, _ = run_cmd(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT)
    if ok and out.strip():
        return out.strip()
    return "dev"

def update_game_title(version, commit_sha):
    title_suffix = f"[{version}-{commit_sha}]"
    base_title = "Phòng Khám Thiên Sứ: Chuyên Trị Xuất Tinh Sớm"
    full_title = f"{base_title} {title_suffix}"
    
    print(f"\n[+] Cap nhat Game Title thanh: '{full_title}'")
    
    # 1. Update TEST game System.json
    sys_file = GAME_TEST_DIR / "data" / "System.json"
    if sys_file.exists():
        data = json.loads(sys_file.read_text(encoding="utf-8"))
        data["gameTitle"] = full_title
        sys_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("  [OK] Updated TEST Game System.json")
        
    # 2. Update TEST game package.json
    pkg_file = GAME_TEST_DIR / "package.json"
    if pkg_file.exists():
        pkg = json.loads(pkg_file.read_text(encoding="utf-8"))
        if "window" not in pkg:
            pkg["window"] = {}
        pkg["window"]["title"] = full_title
        pkg["version"] = version.lstrip("v")
        pkg_file.write_text(json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8")
        print("  [OK] Updated TEST Game package.json")
        
    # 3. Sync to patch/ directory
    patch_sys = PATCH_DIR / "data" / "System.json"
    if sys_file.exists():
        patch_sys.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sys_file, patch_sys)
        print("  [OK] Synced to patch/data/System.json")
        
    patch_pkg = PATCH_DIR / "package.json"
    if pkg_file.exists():
        shutil.copy2(pkg_file, patch_pkg)
        print("  [OK] Synced to patch/package.json")

    # 4. Sync all latest data/*.json to patch/
    for json_f in (GAME_TEST_DIR / "data").glob("*.json"):
        shutil.copy2(json_f, PATCH_DIR / "data" / json_f.name)
    print("  [OK] Synced all data/*.json to patch/data/")

    # 5. Sync to Android assets
    android_assets = ANDROID_DIR / "template" / "app" / "src" / "main" / "assets"
    if android_assets.exists():
        for json_f in (GAME_TEST_DIR / "data").glob("*.json"):
            dst = android_assets / "data" / json_f.name
            if dst.exists():
                shutil.copy2(json_f, dst)
        print("  [OK] Synced data/*.json to Android assets")

    return full_title

def build_pc_game_zip(version):
    print("\n" + "="*50)
    print("    DONG GOI FULL GAME PC (STANDALONE)")
    print("="*50)
    
    zip_name = f"ThienSuClinic-PC-{version}.zip"
    zip_path = RELEASE_OUT / zip_name
    RELEASE_OUT.mkdir(parents=True, exist_ok=True)
    
    if zip_path.exists():
        zip_path.unlink()
        
    root_folder_name = f"ThienSuClinic-PC-{version}"
    
    print(f"[+] Dang nen thu muc game: {GAME_TEST_DIR} -> {zip_name}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(GAME_TEST_DIR):
            for f in files:
                full_p = Path(root) / f
                rel_p = full_p.relative_to(GAME_TEST_DIR)
                
                # Exclude developer temporary save states (file*.rmmzsave)
                if rel_p.parts and rel_p.parts[0] == "save" and f.startswith("file") and f.endswith(".rmmzsave"):
                    continue
                # Exclude unnecessary temporary logs/backups
                if f.endswith(".tmp") or f.endswith(".bak"):
                    continue
                    
                arc_p = Path(root_folder_name) / rel_p
                zf.write(full_p, arc_p)
                
    print(f"[OK] Da tao file Full Game PC ZIP: {zip_path} ({zip_path.stat().st_size / (1024*1024):.2f} MB)")
    
    # Also copy to F: for quick local access
    f_drive = Path(r"F:\ThienSuClinic-PC.zip")
    if f_drive.parent.exists():
        shutil.copy2(zip_path, f_drive)
        print(f"  [+] Da cap nhat sang {f_drive}")
        
    return zip_path

def build_android_apk(version):
    print("\n" + "="*50)
    print("    BIEN DICH ANDROID APK")
    print("="*50)
    
    cmd = [
        sys.executable,
        str(ANDROID_DIR / "build_apk.py"),
        "--game-dir", str(GAME_TEST_DIR)
    ]
    ok, out, err = run_cmd(cmd, cwd=ANDROID_DIR)
    if not ok:
        print("[ERR] Build Android APK that bai!")
        print(err)
        return None
        
    src_apk = ANDROID_DIR / "output" / "viet-hoa-thiensu.apk"
    if not src_apk.exists():
        print("[ERR] Khong tim thay file APK sau khi build!")
        return None
        
    dst_apk = RELEASE_OUT / f"ThienSuClinic-Android-{version}.apk"
    shutil.copy2(src_apk, dst_apk)
    print(f"[OK] Android APK da duoc tao: {dst_apk} ({dst_apk.stat().st_size / (1024*1024):.2f} MB)")
    
    f_drive = Path(r"F:\ThienSuClinic-Android.apk")
    if f_drive.parent.exists():
        shutil.copy2(dst_apk, f_drive)
        print(f"  [+] Da cap nhat sang {f_drive}")
        
    return dst_apk

def build_ios_ipa(version):
    print("\n" + "="*50)
    print("    BIEN DICH IOS IPA")
    print("="*50)
    
    cmd = [
        sys.executable,
        str(IOS_DIR / "inject_game_ios.py")
    ]
    ok, out, err = run_cmd(cmd, cwd=IOS_DIR)
    if not ok:
        print("[ERR] Build iOS IPA that bai!")
        print(err)
        return None
        
    src_ipa = IOS_DIR / "output" / "ThienSuClinic-VietHoa.ipa"
    if not src_ipa.exists():
        print("[ERR] Khong tim thay file IPA sau khi build!")
        return None
        
    dst_ipa = RELEASE_OUT / f"ThienSuClinic-iOS-{version}.ipa"
    shutil.copy2(src_ipa, dst_ipa)
    print(f"[OK] iOS IPA da duoc tao: {dst_ipa} ({dst_ipa.stat().st_size / (1024*1024):.2f} MB)")
    
    # Also copy to F: for quick local access
    f_drive = Path(r"F:\ThienSuClinic-VietHoa.ipa")
    if f_drive.parent.exists():
        shutil.copy2(src_ipa, f_drive)
        print(f"  [+] Da cap nhat sang {f_drive}")
        
    return dst_ipa

def publish_github_release(version, commit_sha, assets):
    print("\n" + "="*50)
    print(f"    PUBLISH GITHUB RELEASE: {version}")
    print("="*50)
    
    release_notes = f"""## 🌸 Bản Dịch Việt Hóa: Thiên Sứ Trị Liệu Xuất Tinh Sớm ({version})
**Commit ID:** `{commit_sha}`

### 📌 Các tính năng & nội dung cập nhật:
- **Việt hóa 100% cốt truyện chính, thoại nhân vật Sera, các đợt trị liệu và Aftercare**.
- **Hiển thị phiên bản & Git Commit ID ngay trên tiêu đề game PC** (`[{version}-{commit_sha}]`) giúp dễ dàng kiểm tra phiên bản.
- **Bản PC Full Game đóng gói sẵn**: Chỉ cần giải nén và mở `Game.exe` là chơi được ngay, không cần game gốc.
- **Bản Android APK tích hợp sẵn**: Cài đặt và chơi mượt mà trên điện thoại/máy tính bảng Android.
- **Khắc phục trọn vẹn âm thanh trên iOS Safari/WebKit** qua bộ giải mã WebAudio VorbisDecoder WASM chuyên dụng.
- **Sửa toàn bộ các lỗi hiển thị, từ nối, kính ngữ và đồng bộ thoại - voice audio**.

---

### 📦 Tải về theo nền tảng:
1. **Windows PC (Full Game)**: Tải file `ThienSuClinic-PC-{version}.zip`, giải nén và chạy `Game.exe` để chơi ngay.
2. **Android**: Tải và cài đặt trực tiếp `ThienSuClinic-Android-{version}.apk`.
3. **iOS (iPhone / iPad)**: Tải file `ThienSuClinic-iOS-{version}.ipa` và cài qua TrollStore, Scarlet, Sideloadly hoặc AltStore.
"""
    
    notes_file = RELEASE_OUT / "RELEASE_NOTES.md"
    notes_file.write_text(release_notes, encoding="utf-8")
    
    cmd = [
        "gh", "release", "create", version,
        "--title", f"Bản Dịch Việt Hóa {version} [{commit_sha}]",
        "--notes-file", str(notes_file)
    ]
    for asset in assets:
        if asset and Path(asset).exists():
            cmd.append(str(asset))
            
    print(f"[EXEC] Dang upload len GitHub Release...")
    ok, out, err = run_cmd(cmd, cwd=REPO_ROOT)
    if ok:
        print("\n" + "="*60)
        print("  🎉 PUBLISH RELEASE LEN GITHUB THANH CONG!")
        print("  Link:", out.strip())
        print("="*60)
        return True
    else:
        print(f"[NOTE] Thu cap nhat assets voi gh release upload:")
        up_cmd = ["gh", "release", "upload", version, "--clobber"] + [str(a) for a in assets if a and Path(a).exists()]
        ok2, out2, err2 = run_cmd(up_cmd, cwd=REPO_ROOT)
        if ok2:
            print("[OK] Da upload/cap nhat assets len GitHub Release thanh cong!")
            return True
        else:
            print("[ERR] Upload that bai:", err, err2)
            return False

def main():
    parser = argparse.ArgumentParser(description="Tao va publish Release da nen tang len GitHub")
    parser.add_argument("--version", default="v1.0.0", help="Phien ban release (vi du: v1.0.0)")
    parser.add_argument("--skip-upload", action="store_true", help="Chi dong goi tai cho ma khong upload")
    args = parser.parse_args()
    
    version = args.version
    commit_sha = get_git_commit()
    print(f"[+] Bat dau quy trinh Release cho phien ban: {version} (Commit: {commit_sha})")
    
    # 1. Update Game Title
    update_game_title(version, commit_sha)
    
    # 2. Git commit version change
    run_cmd(["git", "add", "."], cwd=REPO_ROOT)
    run_cmd(["git", "commit", "-m", f"chore(release): bump version to {version} [{commit_sha}]"], cwd=REPO_ROOT)
    commit_sha = get_git_commit() # Refresh commit sha after bump commit
    
    # 3. Package Full PC Game Zip
    pc_zip = build_pc_game_zip(version)
    
    # 4. Build Android APK
    apk_file = build_android_apk(version)
    
    # 5. Build iOS IPA
    ipa_file = build_ios_ipa(version)
    
    # 6. Publish to GitHub Release (if not skip-upload)
    if not args.skip_upload:
        assets = [pc_zip, apk_file, ipa_file]
        publish_github_release(version, commit_sha, assets)
    else:
        print("\n[OK] Bo qua buoc upload len GitHub (theo yeu cau --skip-upload).")
        
    # Push git commits and tags
    run_cmd(["git", "push", "origin", "ios-build"], cwd=REPO_ROOT)
    run_cmd(["git", "push", "--tags", "origin"], cwd=REPO_ROOT)

if __name__ == "__main__":
    main()
