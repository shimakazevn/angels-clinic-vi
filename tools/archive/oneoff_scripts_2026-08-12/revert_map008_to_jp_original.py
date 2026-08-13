#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revert Map008.json về bản JP gốc, sau đó chỉ dịch text
(giữ nguyên toàn bộ logic event, chỉ thay text tiếng Nhật bằng tiếng Việt).
"""
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_JP    = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data")
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

# Load JP original
with open(os.path.join(DATA_JP, "Map008.json"), 'r', encoding='utf-8') as f:
    map8 = json.load(f)

# Apply VN translations - chỉ dịch các chuỗi tiếng Nhật thành tiếng Việt
# Mapping thủ công các text cần dịch trong Map008
text_map = {
    # code 401 dialogue
    '主人公の名前を入力してください。': 'Vui lòng nhập tên cho nhân vật chính.',
    '～ 物語のあらすじ ～': '～ Tóm tắt cốt truyện ～',
    '主人公は早漏に悩んでおり、モンスターガールに': 'Nhân vật chính vô cùng trăn trở vì chứng xuất tinh sớm, khiến anh dễ dàng đầu hàng trước sự quyến rũ của các Monster Girl.',
    '誘惑されては敗北してしまっていた。': '',  # đã gộp vào dòng trên
    'ある日、早漏専門のクリニックに迷い込んだ主人公は、': 'Tình cờ bước vào một phòng khám chuyên trị xuất tinh sớm, anh đã gặp gỡ Sera — cô y tá Thiên Sứ với khuôn mặt lạnh lùng.',
    '無表情な天使の看護師・セラと出会う。': '',  # đã gộp
    '主人公の早漏を治療するため、セラは': 'Để chữa trị chứng xuất tinh sớm cho nhân vật chính, Sera đã đề xuất liệu pháp trị liệu "Tự mình làm chuyện dâm dục với anh để anh quen dần".',
    '「自分でいやらしいことをして慣れさせる」治療を提案する。': '',  # đã gộp

    # plugin choice window - messageText
    'OPをスキップしますか？\n\n※スキップした場合は最初のHシーン(=チュートリアル)からスタートします。': 'Bạn có muốn bỏ qua đoạn mở đầu (OP) không?\n\n※ Nếu bỏ qua, bạn sẽ bắt đầu từ cảnh H đầu tiên (= hướng dẫn chiến đấu).',
}

# Also handle the LL_GalgeChoiceWindow plugin command choices
choice_map = {
    'OPを見る（初回推奨）': '1. Xem OP (Khuyên dùng lần đầu)',
    'OPをスキップ': '2. Bỏ qua OP',
}

def translate_text(txt):
    if txt in text_map:
        return text_map[txt]
    return txt

def translate_choices_json(choices_json_str):
    """Translate label fields in choices JSON string"""
    try:
        import re
        for jp, vn in choice_map.items():
            choices_json_str = choices_json_str.replace(jp, vn)
        return choices_json_str
    except:
        return choices_json_str

# Apply to all events
translated = 0
for ev in map8.get('events', []):
    if not ev: continue
    for page in ev.get('pages', []):
        for cmd in page.get('list', []):
            code = cmd.get('code', 0)
            params = cmd.get('parameters', [])

            if code == 401 and params:
                txt = params[0]
                if isinstance(txt, str) and txt in text_map:
                    cmd['parameters'][0] = text_map[txt]
                    translated += 1

            elif code == 357 and len(params) >= 4:
                # Plugin command: LL_GalgeChoiceWindow
                plugin_params = params[3]
                if isinstance(plugin_params, dict):
                    if 'messageText' in plugin_params:
                        orig = plugin_params['messageText']
                        for jp, vn in text_map.items():
                            if jp in orig:
                                plugin_params['messageText'] = orig.replace(jp, vn)
                                translated += 1
                    if 'choices' in plugin_params:
                        orig = plugin_params['choices']
                        if isinstance(orig, str):
                            new = translate_choices_json(orig)
                            if new != orig:
                                plugin_params['choices'] = new
                                translated += 1
                        elif isinstance(orig, list):
                            for i, c in enumerate(orig):
                                new = translate_choices_json(c)
                                if new != c:
                                    orig[i] = new
                                    translated += 1

print(f"Translated {translated} items in Map008")

with open(os.path.join(DATA_VN, "Map008.json"), 'w', encoding='utf-8') as f:
    json.dump(map8, f, ensure_ascii=False, indent=4)
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(PATCH_DATA, "Map008.json"))
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(TEST_DATA, "Map008.json"))
print("Reverted to JP logic + VN text. Synced!")

# Verify the choice count
with open(os.path.join(DATA_VN, "Map008.json"), 'r', encoding='utf-8') as f:
    map8v = json.load(f)
for ev in map8v.get('events', []):
    if not ev: continue
    for page in ev.get('pages', []):
        for cmd in page.get('list', []):
            if cmd.get('code') == 357:
                p = cmd.get('parameters', [])
                if len(p) >= 4 and isinstance(p[3], dict) and 'choices' in p[3]:
                    import json as j2
                    choices = p[3]['choices']
                    print(f"\nChoices in game:")
                    if isinstance(choices, str):
                        import re
                        labels = re.findall(r'"label":\s*"([^"]+)"', choices)
                        for lbl in labels:
                            print(f"  - {lbl}")
                    elif isinstance(choices, list):
                        for c in choices:
                            import re
                            labels = re.findall(r'"label":\s*"([^"]+)"', c)
                            for lbl in labels:
                                print(f"  - {lbl}")
