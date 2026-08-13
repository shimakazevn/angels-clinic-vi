#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
ORIG_DATA = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data")
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Tenshi_no_Hayarou_Clinic_VN", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

with open(os.path.join(ORIG_DATA, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    orig_ce = json.load(f)

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    vn_ce = json.load(f)

# Master is Japanese Master
master = json.loads(json.dumps(orig_ce))

translated_count = 0

for i in range(min(len(orig_ce), len(vn_ce))):
    ev_o = orig_ce[i]
    ev_m = master[i]
    ev_v = vn_ce[i]

    if not (ev_o and ev_m and ev_v and 'list' in ev_o and 'list' in ev_m and 'list' in ev_v):
        continue

    list_o = ev_o['list']
    list_m = ev_m['list']
    list_v = ev_v['list']

    for j in range(min(len(list_o), len(list_v))):
        cmd_o = list_o[j]
        cmd_m = list_m[j]
        cmd_v = list_v[j]

        code = cmd_o.get('code')
        if code == 401:
            p_o = cmd_o.get('parameters', [])
            p_v = cmd_v.get('parameters', [])
            if p_o and p_v and len(p_o) > 0 and len(p_v) > 0:
                txt_o = p_o[0]
                txt_v = p_v[0]
                if isinstance(txt_o, str) and isinstance(txt_v, str):
                    if jp_regex.search(txt_o) and txt_v and not jp_regex.search(txt_v):
                        cmd_m['parameters'][0] = txt_v
                        translated_count += 1

print(f"Mapped {translated_count} Vietnamese dialogue commands from original VN file!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced master CommonEvents.json to patch-release and test game!")
