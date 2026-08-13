#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

with open(os.path.join(DATA_VN, "Map008.json"), 'r', encoding='utf-8') as f:
    map8 = json.load(f)

ev1 = next(e for e in map8['events'] if e and e.get('id') == 1)
cmds = ev1['pages'][0]['list']

# Rút gọn các dòng dài — giữ đúng 1 dòng 401 per slot
fixes = {
    41: 'Nhân vật chính trăn trở vì chứng xuất tinh sớm,',
    42: 'dễ dàng đầu hàng trước sự quyến rũ của Monster Girl.',
    51: 'Tình cờ bước vào phòng khám chuyên trị xuất tinh sớm,',
    52: 'anh gặp Sera — y tá Thiên Sứ với khuôn mặt lạnh lùng.',
    63: 'Để chữa trị, Sera đề xuất một liệu pháp:',
    64: 'tự thân mật với nhân vật chính',
    65: 'để anh quen dần và khắc phục bệnh.',
}

for idx, vn_text in fixes.items():
    if idx < len(cmds) and cmds[idx].get('code') == 401:
        old = cmds[idx]['parameters'][0]
        cmds[idx]['parameters'][0] = vn_text
        print(f"[{idx}] {repr(old)} → {repr(vn_text)}")

with open(os.path.join(DATA_VN, "Map008.json"), 'w', encoding='utf-8') as f:
    json.dump(map8, f, ensure_ascii=False, indent=4)
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(PATCH_DATA, "Map008.json"))
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(TEST_DATA, "Map008.json"))
print("Fixed line lengths and synced!")
