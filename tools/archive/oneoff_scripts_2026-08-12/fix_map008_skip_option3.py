#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Map008: conditional at [23] currently checks Var[12] == 2
Change to Var[12] >= 2 so option 3 doesn't accidentally trigger CE 402 (OP cutscene).

RPG Maker MZ conditional comparison types:
  0 = ==, 1 = >=, 2 = <=, 3 = >, 4 = <, 5 = !=
params format: [1, varId, comparisonType, value, 0]
"""
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

fp = os.path.join(DATA_VN, "Map008.json")
with open(fp, 'r', encoding='utf-8') as f:
    map8 = json.load(f)

fixed = False
for ev in map8.get('events', []):
    if not ev or ev.get('id') != 1: continue
    for page in ev.get('pages', []):
        for i, cmd in enumerate(page.get('list', [])):
            # Find: code=111, params=[1, 12, 0, 2, 0]  → Var[12] == 2
            if (cmd.get('code') == 111 and
                cmd.get('parameters') == [1, 12, 0, 2, 0]):
                print(f"Found conditional at [{i}]: {cmd['parameters']}")
                # Change comparison from == (0) to >= (1)
                cmd['parameters'] = [1, 12, 1, 2, 0]
                print(f"Fixed to: {cmd['parameters']}  (Var[12] >= 2)")
                fixed = True
                break

if fixed:
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(map8, f, ensure_ascii=False, indent=4)
    shutil.copy2(fp, os.path.join(PATCH_DATA, "Map008.json"))
    shutil.copy2(fp, os.path.join(TEST_DATA, "Map008.json"))
    print("Saved and synced!")
else:
    print("ERROR: Conditional not found - check map structure")
