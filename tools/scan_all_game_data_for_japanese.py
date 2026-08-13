#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Tenshi_no_Hayarou_Clinic_VN", "Game", "data")
EN_DATA = os.path.join(ROOT, "The_Angelic_PE_Treatment_Clinic_v3_EN", "data")
ORIG_DATA = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

print("=== SCANNING ALL JSON DATA FILES IN TEST GAME FOR REMAINING JAPANESE ===")

jp_summary = {}

for fname in sorted(os.listdir(TEST_GAME_DATA)):
    if fname.endswith('.json'):
        fp = os.path.join(TEST_GAME_DATA, fname)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            continue

        file_jp_count = 0
        jp_samples = []

        if isinstance(data, list):
            for idx, item in enumerate(data):
                if not item: continue
                # Check events if Map or CommonEvents
                if isinstance(item, dict):
                    # Dialogue lines in list
                    if 'list' in item and isinstance(item['list'], list):
                        for cmd_idx, cmd in enumerate(item['list']):
                            if isinstance(cmd, dict):
                                code = cmd.get('code')
                                if code == 401 and cmd.get('parameters'):
                                    txt = cmd['parameters'][0]
                                    if isinstance(txt, str) and jp_regex.search(txt):
                                        file_jp_count += 1
                                        if len(jp_samples) < 5:
                                            ev_id = item.get('id', idx)
                                            jp_samples.append((ev_id, cmd_idx, txt))
                                elif code == 101 and cmd.get('parameters') and len(cmd['parameters']) >= 5:
                                    spk = cmd['parameters'][4]
                                    if isinstance(spk, str) and jp_regex.search(spk):
                                        file_jp_count += 1
                                        if len(jp_samples) < 5:
                                            ev_id = item.get('id', idx)
                                            jp_samples.append((ev_id, cmd_idx, f"Speaker: {spk}"))

        if file_jp_count > 0:
            jp_summary[fname] = {'count': file_jp_count, 'samples': jp_samples}

print(f"\nScan complete! Found Japanese text in {len(jp_summary)} files:")
for fname, info in jp_summary.items():
    print(f"\n--- FILE: {fname} ({info['count']} Japanese lines) ---")
    for sample in info['samples']:
        print(f"  [ID {sample[0]}, CMD {sample[1]}]: {sample[2]}")
