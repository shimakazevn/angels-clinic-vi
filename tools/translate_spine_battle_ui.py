#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate_spine_battle_ui.py — Dịch và dựng lại toàn bộ Texture UI Chiến Đấu (Spine Battle UI) v6 Final Perfect
Sử dụng chính xác kích thước 333x64 & xử lý xoay 90 độ Spine Atlas chuẩn 100%.
Xóa bỏ hoàn toàn 100% các hộp đen, bóng chữ Nhật chìm và lỗi chữ lệch.
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
SPINE_DIR = ROOT_DIR / "天使の早漏治療クリニック" / "Game" / "img" / "spines"
SPINE_IMG = SPINE_DIR / "UI 戦闘.png"
SPINE_BAK = SPINE_DIR / "UI 戦闘.bak.png"
SPINE_ATLAS = SPINE_DIR / "UI 戦闘.atlas"

if SPINE_BAK.exists():
    img_orig = Image.open(SPINE_BAK).convert("RGBA")
else:
    img_orig = Image.open(SPINE_IMG).convert("RGBA")

# Fonts
font_skill = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
font_btn_lg = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
font_turn = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 15)

SKILL_TRANSLATIONS = {
    1: "Đáng Yêu",
    2: "Anh Yêu Em",
    3: "Thích Chị",
    4: "Dịu Dàng",
    5: "Giỏi Quá",
    6: "Ngầu Quá",
    7: "Đáng Tin",
    8: "Giọng Ấm",
    9: "Dâm Táo",
    10: "Khiêu Gợi",
    11: "Chịu Đựng I",
    12: "Chịu Đựng II",
    13: "Chịu Đựng III",
    14: "Điều Hòa Nhịp Thở",
    15: "Hít Thở Sâu",
    16: "Phản Công • Tay",
    17: "Phản Công • Miệng",
    18: "Phản Công • Ngực",
    19: "Phản Công • Chân",
    20: "Phản Công • Cọ Xát",
    21: "Thế Cảnh Giác I",
    22: "Thế Cảnh Giác II",
    23: "Phân Tích I",
    24: "Phân Tích II",
    25: "Luyện Tưởng Tượng I",
    26: "Luyện Tưởng Tượng II",
    27: "Thế Thân I",
    28: "Thế Thân II",
    29: "Tạm Hưu Chiến",
    30: "Không Phòng Thủ",
    31: "Hạ Nhiệt I",
    32: "Hạ Nhiệt II",
    33: "Hạ Nhiệt III",
    34: "Hất Ra",
    35: "Trò Chuyện Hài Hước",
    36: "Hư Cấu",
    37: "Xúc Xắc Giả",
    38: "Nhịp Độ Nhanh"
}

SPECIAL_BTNS = {
    "あきらめる": ("TỪ BỎ", (255, 245, 252, 255), (150, 20, 100, 255)),
    "なすがまま": ("MẶC CHO XỬ LÝ", (255, 245, 252, 255), (150, 20, 110, 255)),
    "オナニーする": ("TỰ SƯỚNG", (255, 245, 252, 255), (150, 20, 100, 255)),
    "拘束おねだり": ("CẦU XIN TRÓI BUỘC", (255, 245, 252, 255), (150, 20, 100, 255))
}

def parse_atlas():
    with open(SPINE_ATLAS, "r", encoding="utf-8") as f:
        lines = f.readlines()
    regions = {}
    current_name = None
    for line in lines:
        l = line.strip()
        if not l or l.endswith(".png") or "size:" in l or "filter:" in l:
            continue
        if ":" not in l:
            current_name = l
            regions[current_name] = {}
        elif current_name and ":" in l:
            k, v = l.split(":", 1)
            regions[current_name][k.strip()] = v.strip()
    return regions

def main():
    print("=" * 60)
    print("Translating Spine Battle UI Atlas v6 Final Perfect (UI 戦闘.png)")
    print("=" * 60)

    regions = parse_atlas()
    arr = np.array(img_orig)

    # 1. 38 Skill Buttons
    for i in range(1, 39):
        reg_name = f"コマンド_{i}"
        if reg_name not in regions:
            continue

        info = regions[reg_name]
        b_str = info["bounds"]
        is_rotated = info.get("rotate", "false").lower() == "true" or info.get("rotate", "false") == "90"
        
        x, y, w, h = map(int, b_str.split(","))
        if is_rotated:
            crop = arr[y:y+w, x:x+h].copy()
            crop = np.rot90(crop, k=3)
            bw, bh = w, h
        else:
            crop = arr[y:y+h, x:x+w].copy()
            bw, bh = w, h

        skill_title = SKILL_TRANSLATIONS.get(i, f"Kỹ Năng {i}")

        text_region_mask = np.zeros((bh, bw), dtype=np.uint8)
        text_region_mask[6:bh-6, 85:325] = 255

        text_pixels = (crop[:, :, 3] > 100) & (crop[:, :, 0] > 150) & (crop[:, :, 1] > 150) & (crop[:, :, 2] > 150)
        inpaint_mask = text_pixels & (text_region_mask == 255)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        dilated_mask = cv2.dilate(inpaint_mask.astype(np.uint8), kernel, iterations=2)

        bgr = cv2.cvtColor(crop[:, :, :3], cv2.COLOR_RGB2BGR)
        inpainted_bgr = cv2.inpaint(bgr, dilated_mask, inpaintRadius=9, flags=cv2.INPAINT_TELEA)
        crop[:, :, :3] = cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)

        btn_pil = Image.fromarray(crop)
        btn_draw = ImageDraw.Draw(btn_pil)

        text_w = font_skill.getlength(skill_title)
        tx = int(85 + (240 - text_w) // 2)
        ty = int((bh - 25) // 2)

        btn_draw.text((tx + 1, ty + 1), skill_title, font=font_skill, fill=(5, 8, 15, 220)) # shadow
        btn_draw.text((tx, ty), skill_title, font=font_skill, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(15, 20, 32, 255))

        crop_edited = np.array(btn_pil)
        if is_rotated:
            crop_edited = np.rot90(crop_edited, k=1)
            arr[y:y+w, x:x+h] = crop_edited
        else:
            arr[y:y+h, x:x+w] = crop_edited

        print(f"  ✅ [Spine Skill {i}] {skill_title}")

    # 2. Special Buttons
    for name, (vn_txt, fill_c, stroke_c) in SPECIAL_BTNS.items():
        if name in regions:
            info = regions[name]
            b_str = info["bounds"]
            is_rotated = info.get("rotate", "false").lower() == "true" or info.get("rotate", "false") == "90"
            x, y, w, h = map(int, b_str.split(","))
            if is_rotated:
                crop = arr[y:y+w, x:x+h].copy()
                crop = np.rot90(crop, k=3)
                bw, bh = w, h
            else:
                crop = arr[y:y+h, x:x+w].copy()
                bw, bh = w, h
                
            text_pixels = (crop[:, :, 0] > 170) & (crop[:, :, 1] > 170) & (crop[:, :, 2] > 170) & (crop[:, :, 3] > 150)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            dilated_mask = cv2.dilate(text_pixels.astype(np.uint8), kernel, iterations=2)
            
            bgr = cv2.cvtColor(crop[:, :, :3], cv2.COLOR_RGB2BGR)
            inpainted_bgr = cv2.inpaint(bgr, dilated_mask, inpaintRadius=9, flags=cv2.INPAINT_TELEA)
            crop[:, :, :3] = cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)
            
            btn_pil = Image.fromarray(crop)
            btn_draw = ImageDraw.Draw(btn_pil)
            
            tx = int((bw - font_btn_lg.getlength(vn_txt)) // 2)
            ty = int((bh - 26) // 2)
            btn_draw.text((tx + 1, ty + 1), vn_txt, font=font_btn_lg, fill=(35, 8, 25, 200))
            btn_draw.text((tx, ty), vn_txt, font=font_btn_lg, fill=fill_c, stroke_width=2, stroke_fill=stroke_c)
            
            crop_edited = np.array(btn_pil)
            if is_rotated:
                crop_edited = np.rot90(crop_edited, k=1)
                arr[y:y+w, x:x+h] = crop_edited
            else:
                arr[y:y+h, x:x+w] = crop_edited

            print(f"  ✅ [Spine Special] {name} -> {vn_txt}")

    # 3. Turn Counter
    if "残りターン" in regions:
        b_str = regions["残りターン"]["bounds"]
        x, y, w, h = map(int, b_str.split(","))
        crop_turn = arr[y:y+h, x:x+w].copy()
        
        text_pixels = (crop_turn[:, :, 3] > 100) & (crop_turn[:, :, 0] > 150) & (crop_turn[:, :, 1] > 150) & (crop_turn[:, :, 2] > 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated_mask = cv2.dilate(text_pixels.astype(np.uint8), kernel, iterations=1)
        
        bgr = cv2.cvtColor(crop_turn[:, :, :3], cv2.COLOR_RGB2BGR)
        inpainted_bgr = cv2.inpaint(bgr, dilated_mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
        crop_turn[:, :, :3] = cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)
        
        img_turn = Image.fromarray(crop_turn)
        draw_t = ImageDraw.Draw(img_turn)
        draw_t.text((12, 14), "Còn", font=font_turn, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(10, 20, 40, 255))
        draw_t.text((116, 14), "Lượt", font=font_turn, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(10, 20, 40, 255))
        arr[y:y+h, x:x+w] = np.array(img_turn)
        print("  ✅ [Spine Turn Counter] Còn ... Lượt")

    final_img = Image.fromarray(arr)
    
    dest_game = SPINE_IMG
    dest_edited = ROOT_DIR / "translation" / "ui_images" / "edited" / "UI 戦闘.png"
    dest_vn_game = ROOT_DIR / "Tenshi_no_Hayarou_Clinic_VN" / "Game" / "img" / "spines" / "UI 戦闘.png"
    dest_patch = ROOT_DIR / "patch-release" / "patch" / "img" / "spines" / "UI 戦闘.png"

    dest_edited.parent.mkdir(parents=True, exist_ok=True)
    dest_vn_game.parent.mkdir(parents=True, exist_ok=True)
    dest_patch.parent.mkdir(parents=True, exist_ok=True)

    for dst in [dest_game, dest_edited, dest_vn_game, dest_patch]:
        final_img.save(dst)
        print(f"Saved: {dst}")

if __name__ == "__main__":
    main()
