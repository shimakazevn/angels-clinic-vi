#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
apply_images.py — Copy ảnh đã chỉnh sửa từ edited/ ngược vào thư mục game
Game: The Angelic PE Treatment Clinic (RJ01644040)

Cách dùng:
    python tools/apply_images.py

Input:  translation/ui_images/edited/  (ảnh đã dịch, cùng tên file với original/)
Output: Copy vào đúng vị trí trong game

Script đọc image_list.csv để biết ảnh nào cần copy đi đâu.
"""

import shutil
import csv
import sys
from pathlib import Path

# ---- Cấu hình đường dẫn ----
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
GAME_DIR = ROOT_DIR / "天使の早漏治療クリニック" / "Game"
IMG_DIR = GAME_DIR / "img"
TRANS_DIR = ROOT_DIR / "translation"
EDITED_DIR = TRANS_DIR / "ui_images" / "edited"
LIST_CSV = TRANS_DIR / "ui_images" / "image_list.csv"

# ========== Main ==========

def main():
    print("=" * 60)
    print("RPG Maker MZ — Apply Edited Images to Game")
    print(f"Edited dir: {EDITED_DIR}")
    print(f"Game dir:   {GAME_DIR}")
    print("=" * 60)

    if not LIST_CSV.exists():
        print(f"❌ Không tìm thấy: {LIST_CSV}")
        print("   Hãy chạy export_images.py trước!")
        sys.exit(1)

    # Load CSV
    image_list = []
    with open(LIST_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_list.append(row)

    applied = []
    not_found = []
    skipped = []

    for row in image_list:
        export_name = row["export_name"]
        original_path = row["original_path"]  # relative to GAME_DIR

        edited_src = EDITED_DIR / export_name
        game_dest = GAME_DIR / original_path

        if not edited_src.exists():
            not_found.append(export_name)
            continue

        # Backup ảnh gốc nếu chưa có backup
        backup = game_dest.with_suffix(".bak" + game_dest.suffix)
        if not backup.exists() and game_dest.exists():
            shutil.copy2(game_dest, backup)

        shutil.copy2(edited_src, game_dest)
        applied.append(export_name)
        print(f"  ✅ {export_name} → {original_path}")

    print(f"\n{'='*60}")
    print(f"Applied:   {len(applied)} ảnh")
    if not_found:
        print(f"Not found: {len(not_found)} ảnh (chưa chỉnh sửa):")
        for f in not_found:
            print(f"     {f}")
    if skipped:
        print(f"Skipped:   {len(skipped)}")

    if applied:
        print(f"\n🎮 Chạy game để kiểm tra: {GAME_DIR / 'Game.exe'}")
        print(f"\n💡 Ảnh gốc được backup với đuôi .bak.png tại vị trí cũ.")
        print(f"   Để khôi phục: chạy restore_images.py (hoặc đổi tay .bak.png → .png)")

if __name__ == "__main__":
    main()
