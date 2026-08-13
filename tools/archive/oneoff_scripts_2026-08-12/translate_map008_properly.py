#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply proper VN translations to Map008.json (JP original structure).
"""
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_JP    = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data")
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

# Start fresh from JP master
with open(os.path.join(DATA_JP, "Map008.json"), 'r', encoding='utf-8') as f:
    map8 = json.load(f)

# Ev 1, page 0 — direct index mapping
ev1 = next(e for e in map8['events'] if e and e.get('id') == 1)
cmds = ev1['pages'][0]['list']

# code 401 text translations (by cmd index)
text_401 = {
    7:  'Vui lòng nhập tên cho nhân vật chính.',
    26: '～ Tóm tắt cốt truyện ～',
    41: 'Nhân vật chính vô cùng trăn trở vì chứng xuất tinh sớm,',
    42: 'khiến anh dễ dàng đầu hàng trước sự quyến rũ của các Monster Girl.',
    51: 'Tình cờ bước vào một phòng khám chuyên trị xuất tinh sớm,',
    52: 'anh đã gặp gỡ Sera — cô y tá Thiên Sứ với khuôn mặt lạnh lùng.',
    63: 'Để chữa trị chứng xuất tinh sớm cho nhân vật chính,',
    64: 'Sera đã đề xuất liệu pháp trị liệu',
    65: '"Tự mình làm chuyện dâm dục với anh để anh quen dần".',
}

for idx, vn_text in text_401.items():
    if idx < len(cmds) and cmds[idx].get('code') == 401:
        cmds[idx]['parameters'][0] = vn_text
        print(f"  [{idx}] ← {repr(vn_text)}")

# Plugin command at [9]: LL_GalgeChoiceWindow
cmd9 = cmds[9]
if cmd9.get('code') == 357:
    plugin_params = cmd9['parameters'][3]
    # Translate messageText
    plugin_params['messageText'] = (
        'Bạn có muốn bỏ qua đoạn mở đầu (OP) không?\n\n'
        '※ Nếu bỏ qua, bạn sẽ xem tóm tắt cốt truyện\n'
        '\u3000rồi bắt đầu từ hướng dẫn chiến đấu.'
    )
    # Translate choices
    import re
    choices_str = plugin_params.get('choices', '')
    choices_str = choices_str.replace('OPを見る（初回推奨）', '1. Xem OP (Khuyên dùng lần đầu)')
    choices_str = choices_str.replace('OPをスキップ', '2. Bỏ qua OP')
    plugin_params['choices'] = choices_str
    print(f"  [9] Plugin choices translated")

# Save
with open(os.path.join(DATA_VN, "Map008.json"), 'w', encoding='utf-8') as f:
    json.dump(map8, f, ensure_ascii=False, indent=4)
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(PATCH_DATA, "Map008.json"))
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(TEST_DATA, "Map008.json"))
print("\nDone! Map008 synced with correct 2-choice JP structure + VN text.")
