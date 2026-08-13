#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fill_overflow_401_with_empty.py

Với những block 401 mà VN đã được điền (dòng đầu) nhưng các dòng sau vẫn còn JP,
điền chuỗi rỗng "" vào để không hiển thị tiếng Nhật trong game.
"""
import os, sys, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
CE_JP_FP   = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json")
CE_VN_FP   = os.path.join(DATA_VN, "CommonEvents.json")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

with open(CE_JP_FP, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)
with open(CE_VN_FP, 'r', encoding='utf-8') as f:
    ce_vn = json.load(f)

vn_by_id = {ev.get('id'): ev for ev in ce_vn if ev}

cleared = 0
blocks_affected = 0

for ev_jp in ce_jp:
    if not ev_jp or 'list' not in ev_jp: continue
    ev_id = ev_jp.get('id')
    ev_vn = vn_by_id.get(ev_id)
    if not ev_vn or 'list' not in ev_vn: continue

    cmd_list_jp = ev_jp['list']
    cmd_list_vn = ev_vn['list']

    i = 0
    while i < len(cmd_list_jp):
        cmd = cmd_list_jp[i]
        if cmd.get('code') == 101:
            j = i + 1
            block_idxs = []
            while j < len(cmd_list_jp) and cmd_list_jp[j].get('code') == 401:
                block_idxs.append(j)
                j += 1

            if block_idxs:
                # Check if this block has mixed VN+JP lines
                has_vn = False
                has_jp = False
                for idx in block_idxs:
                    if idx >= len(cmd_list_vn): continue
                    txt = cmd_list_vn[idx].get('parameters', [''])[0]
                    if isinstance(txt, str):
                        if jp_regex.search(txt):
                            has_jp = True
                        elif txt.strip():
                            has_vn = True

                # If block has at least one VN line AND leftover JP lines → clear JP lines
                if has_vn and has_jp:
                    blocks_affected += 1
                    for idx in block_idxs:
                        if idx >= len(cmd_list_vn): continue
                        txt = cmd_list_vn[idx].get('parameters', [''])[0]
                        if isinstance(txt, str) and jp_regex.search(txt):
                            cmd_list_vn[idx]['parameters'][0] = ''
                            cleared += 1
            i = j
        else:
            i += 1

print(f"Cleared {cleared} overflow JP lines across {blocks_affected} blocks")

# Verify
remaining = 0
for ev in ce_vn:
    if ev and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if not txt.strip().startswith('.'):
                        remaining += 1

print(f"Remaining Japanese lines after clearing: {remaining}")

with open(CE_VN_FP, 'w', encoding='utf-8') as f:
    json.dump(ce_vn, f, ensure_ascii=False, indent=4)
shutil.copy2(CE_VN_FP, os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(CE_VN_FP, os.path.join(TEST_DATA, "CommonEvents.json"))
print("Synced!")
