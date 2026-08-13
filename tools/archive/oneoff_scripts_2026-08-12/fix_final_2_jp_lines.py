#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

ev502 = next((e for e in ce if e and e.get('id') == 502), None)

# CMD 382: mixed VN+JP → fix the kanji in the VN sentence
ev502['list'][382]['parameters'][0] = 'Nói cụ thể ra thì, khuôn mặt anh lúc cố nhẫn nại chịu đựng nhịn bắn tinh, và cả lúc không chịu nổi mà lên đỉnh, tất cả đều đáng yêu cực kỳ.'

# CMD 383: still full JP → clear to empty (already covered by the line above)
ev502['list'][383]['parameters'][0] = ''

print("Fixed CE 502 lines 382 and 383!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(ce, f, ensure_ascii=False, indent=4)
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_DATA, "CommonEvents.json"))
print("Synced!")
