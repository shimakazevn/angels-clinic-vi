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
cmd9 = ev1['pages'][0]['list'][9]
p = cmd9['parameters'][3]

# Fix the correct Japanese label
old = p['choices']
new = old.replace('スキップする', '2. Bỏ qua OP')
p['choices'] = new

print(f"Old: {repr(old)}")
print(f"New: {repr(new)}")

with open(os.path.join(DATA_VN, "Map008.json"), 'w', encoding='utf-8') as f:
    json.dump(map8, f, ensure_ascii=False, indent=4)
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(PATCH_DATA, "Map008.json"))
shutil.copy2(os.path.join(DATA_VN, "Map008.json"), os.path.join(TEST_DATA, "Map008.json"))
print("Fixed and synced!")
