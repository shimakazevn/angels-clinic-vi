#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
TEST_DATA = os.path.join(ROOT, "Tenshi_no_Hayarou_Clinic_VN", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

total_401 = 0
translated_401 = 0
empty_401 = 0
jp_401 = 0

# Check CommonEvents.json
ce_fp = os.path.join(TEST_DATA, "CommonEvents.json")
with open(ce_fp, 'r', encoding='utf-8') as f:
    ce = json.load(f)

for ev in ce:
    if ev and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str):
                    total_401 += 1
                    if jp_regex.search(txt):
                        jp_401 += 1
                    elif not txt.strip():
                        empty_401 += 1
                    else:
                        translated_401 += 1

print("=== CommonEvents.json ===")
print(f"  Total code 401 lines: {total_401}")
print(f"  Translated (VN text): {translated_401} ({100*translated_401//total_401}%)")
print(f"  Empty (blank lines):  {empty_401} ({100*empty_401//total_401}%)")
print(f"  Still Japanese:       {jp_401}")
print()

# Check Map files
map_total_401 = 0
map_translated = 0
map_empty = 0
map_jp = 0
map_files_with_jp = []

for fname in sorted(os.listdir(TEST_DATA)):
    if not fname.startswith('Map') or fname == 'MapInfos.json':
        continue
    fp = os.path.join(TEST_DATA, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    events = data.get('events', [])
    file_jp = 0
    for ev in events:
        if not ev: continue
        for page in ev.get('pages', []):
            for cmd in page.get('list', []):
                if cmd.get('code') == 401 and cmd.get('parameters'):
                    txt = cmd['parameters'][0]
                    if isinstance(txt, str):
                        map_total_401 += 1
                        if jp_regex.search(txt):
                            map_jp += 1
                            file_jp += 1
                        elif not txt.strip():
                            map_empty += 1
                        else:
                            map_translated += 1
    if file_jp > 0:
        map_files_with_jp.append((fname, file_jp))

print("=== Map files ===")
print(f"  Total code 401 lines: {map_total_401}")
if map_total_401 > 0:
    print(f"  Translated (VN text): {map_translated} ({100*map_translated//map_total_401}%)")
    print(f"  Empty (blank lines):  {map_empty} ({100*map_empty//map_total_401}%)")
    print(f"  Still Japanese:       {map_jp}")
if map_files_with_jp:
    print(f"  Files with JP text:   {len(map_files_with_jp)}")
    for fname, cnt in map_files_with_jp[:10]:
        print(f"    {fname}: {cnt} JP lines")

# Grand total
g_total = total_401 + map_total_401
g_trans = translated_401 + map_translated
g_empty = empty_401 + map_empty
g_jp = jp_401 + map_jp

print()
print("=== GRAND TOTAL ===")
print(f"  Total dialogue lines:  {g_total}")
print(f"  Translated:            {g_trans} ({100*g_trans//g_total if g_total else 0}%)")
print(f"  Empty (no translation):{g_empty} ({100*g_empty//g_total if g_total else 0}%)")
print(f"  Still Japanese:        {g_jp}")
