#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
export_images.py — Copy toàn bộ ảnh UI có text ra thư mục để chỉnh sửa
Game: 天使の早漏治療クリニック (RJ01644040) — Bản tiếng Nhật

Cách dùng:
    python tools/export_images.py

Output:
    translation/ui_images/original/   <- ảnh gốc copy ra
    translation/ui_images/image_list.csv  <- danh sách + ghi chú
"""

import shutil
import csv
from pathlib import Path

# ---- Cấu hình đường dẫn ----
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
GAME_DIR = ROOT_DIR / "天使の早漏治療クリニック" / "Game"
IMG_DIR = GAME_DIR / "img"
TRANS_DIR = ROOT_DIR / "translation"
OUT_DIR = TRANS_DIR / "ui_images" / "original"
EDITED_DIR = TRANS_DIR / "ui_images" / "edited"
LIST_CSV = TRANS_DIR / "ui_images" / "image_list.csv"

OUT_DIR.mkdir(parents=True, exist_ok=True)
EDITED_DIR.mkdir(parents=True, exist_ok=True)

# ---- Danh sách ảnh cần export ----
# Format: (source_path_relative_to_IMG_DIR, category, note_vi)
IMAGE_LIST = [
    # Title screen & Clipboard Command Buttons
    ("titles1/タイトル画面.png",
     "Title", "Màn hình tiêu đề game — cần thay tên game"),
    ("titles2/Command_0.png",
     "TitleCommand", "Nút Khám Lần Đầu trên bìa hồ sơ"),
    ("titles2/Command_1.png",
     "TitleCommand", "Nút Tái Khám trên bìa hồ sơ"),
    ("titles2/Command_2.png",
     "TitleCommand", "Nút Tùy Chọn trên bìa hồ sơ"),
    ("spines/UI 戦闘.png",
     "Spine_UI", "Spine Texture Atlas giao diện chiến đấu (Còn / Lượt)"),

    # PC UI (Home screen, menus)
    ("pictures/システム/PC_ホーム画面1.png",
     "PC_UI", "Màn hình chính PC — tab 1"),
    ("pictures/システム/PC_ホーム画面2.png",
     "PC_UI", "Màn hình chính PC — tab 2"),
    ("pictures/システム/PC_ホーム画面3.png",
     "PC_UI", "Màn hình chính PC — tab 3"),
    ("pictures/システム/PC_ホーム画面4.png",
     "PC_UI", "Màn hình chính PC — tab 4"),
    ("pictures/システム/PC_UI 回想1.png",
     "PC_UI", "UI hồi ký — trang 1"),
    ("pictures/システム/PC_UI 回想2.png",
     "PC_UI", "UI hồi ký — trang 2"),
    ("pictures/システム/PC_UI 戦闘.png",
     "PC_UI", "UI chiến đấu"),
    ("pictures/システム/PC_UI 戦闘2.png",
     "PC_UI", "UI chiến đấu — trang 2"),
    ("pictures/システム/PC_UI 編成.png",
     "PC_UI", "UI biên chế đội hình"),
    ("pictures/システム/PC_アフターケア.png",
     "PC_UI", "UI Aftercare (chăm sóc sau)"),
    ("pictures/システム/PC_アフターケアリスト.png",
     "PC_UI", "UI danh sách Aftercare"),
    ("pictures/システム/PC_クリック誘導スチル7.png",
     "PC_UI", "Hướng dẫn click — still 7"),
    ("pictures/システム/PC_買い物.png",
     "PC_UI", "UI mua sắm / shop"),

    # Tutorial images (チュートリアル1 - チュートリアル31)
    *[
        (f"pictures/システム/チュートリアル{i}.png",
         "Tutorial", f"Hình hướng dẫn trang {i}")
        for i in range(1, 32)
        if (IMG_DIR / f"pictures/システム/チュートリアル{i}.png").exists()
    ],
    # Bonus tutorial variants
    ("pictures/システム/チュートリアル23_2.png",
     "Tutorial", "Hình hướng dẫn trang 23 (biến thể 2)"),
    ("pictures/システム/チュートリアル24_2.png",
     "Tutorial", "Hình hướng dẫn trang 24 (biến thể 2)"),

    # HUD / Gauges
    ("pictures/システム/ホイール操作可.png",
     "HUD", "Chỉ dẫn thao tác cuộn chuột (cả 2 chiều)"),
    ("pictures/システム/ホイール操作可_上のみ.png",
     "HUD", "Chỉ dẫn thao tác cuộn chuột (chỉ lên)"),
    ("pictures/システム/射精ゲージ1.png",
     "HUD", "Thanh gauge — loại 1"),
    ("pictures/システム/射精ゲージ2.png",
     "HUD", "Thanh gauge — loại 2"),
    ("pictures/システム/射精ゲージ_スリップダメージ.png",
     "HUD", "Thanh gauge — slip damage"),
    ("pictures/システム/照れゲージ1.png",
     "HUD", "Thanh gauge xấu hổ — loại 1"),
    ("pictures/システム/照れゲージ2.png",
     "HUD", "Thanh gauge xấu hổ — loại 2"),
    ("pictures/システム/スリップダメージ表記.png",
     "HUD", "Hiển thị slip damage"),
]

# ========== Main ==========

def main():
    print("=" * 60)
    print("RPG Maker MZ -- Export UI Images for Editing")
    print(f"Game dir: {GAME_DIR}")
    print(f"Output:   {OUT_DIR}")
    print("=" * 60)

    exported = []
    skipped = []

    for rel_path, category, note in IMAGE_LIST:
        src = IMG_DIR / rel_path
        if not src.exists():
            skipped.append(rel_path)
            continue

        # Flatten tên file: dùng tên gốc, tránh overwrite nếu trùng tên
        dest_name = src.name
        dest = OUT_DIR / dest_name

        # Nếu trùng tên với file khác, thêm prefix category
        if dest.exists() and dest.read_bytes() != src.read_bytes():
            dest_name = f"{category}_{src.name}"
            dest = OUT_DIR / dest_name

        shutil.copy2(src, dest)
        exported.append({
            "original_path": str(src.relative_to(GAME_DIR)),
            "export_name": dest_name,
            "category": category,
            "note": note,
            "status": "pending"  # pending / done
        })
        print(f"  [{category}] {src.name}")

    # Ghi image_list.csv
    fieldnames = ["original_path", "export_name", "category", "note", "status"]
    with open(LIST_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(exported)

    print(f"\n✅ Exported {len(exported)} ảnh → {OUT_DIR}")
    if skipped:
        print(f"⚠️  Bỏ qua {len(skipped)} file không tìm thấy:")
        for s in skipped:
            print(f"     {s}")

    print(f"\n📋 Danh sách ảnh: {LIST_CSV}")
    print(f"\nBước tiếp theo:")
    print(f"  1. Mở ảnh trong thư mục: {OUT_DIR}")
    print(f"  2. Chỉnh sửa text → lưu vào: {EDITED_DIR}")
    print(f"  3. Chạy apply_images.py để copy vào game")

if __name__ == "__main__":
    main()
