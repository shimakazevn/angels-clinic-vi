#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_and_apply_csv_translations.py

Logic:
  - Đọc text_export.csv: mỗi row CE có original_jp (gộp \n) và vietnamese (gộp \n)
  - Build dict: jp_merged -> list of vn_lines (split by \n)
  - Duyệt CommonEvents.json VN hiện tại:
    - Với mỗi block 101+401s: lấy toàn bộ jp text từng dòng, ghép \n
    - Nếu khớp với jp_merged trong dict → điền từng vn_line vào từng cmd 401
  - Ghi lại và sync
"""
import os, sys, csv, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")
CSV_FP     = os.path.join(ROOT, "translation", "text_export.csv")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

# ── 1. Build translation map: jp_merged -> [vn_line1, vn_line2, ...]
translation_map = {}  # jp_text -> list[str]

with open(CSV_FP, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') != 'CommonEvents':
            continue
        jp = row.get('original_jp', '').strip()
        vn = row.get('vietnamese', '').strip()
        if not jp or not vn:
            continue
        # Split by \n to get individual lines
        jp_lines = jp.split('\n')
        vn_lines = vn.split('\n')
        # Store: jp_merged -> vn_lines list
        translation_map[jp] = vn_lines
        # Also index individual lines for single-line blocks
        if len(jp_lines) == 1:
            translation_map[jp_lines[0]] = [vn_lines[0] if vn_lines else vn]

print(f"Loaded {len(translation_map)} translation entries from CSV")

# ── 2. Load VN CommonEvents.json
with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

# ── 3. Apply translations block by block
applied_blocks = 0
applied_lines  = 0
skipped_blocks = 0

for ev in ce:
    if not ev or 'list' not in ev:
        continue
    cmd_list = ev['list']
    i = 0
    while i < len(cmd_list):
        cmd = cmd_list[i]
        if cmd.get('code') == 101:
            # Collect all 401 lines in this block
            j = i + 1
            block_401_indices = []
            while j < len(cmd_list) and cmd_list[j].get('code') == 401:
                block_401_indices.append(j)
                j += 1

            if block_401_indices:
                # Get JP text for this block
                jp_parts = []
                for idx in block_401_indices:
                    p = cmd_list[idx].get('parameters', [])
                    jp_parts.append(p[0] if p else '')
                jp_merged = '\n'.join(jp_parts)

                # Check if any line is still Japanese
                has_jp = any(jp_regex.search(part) for part in jp_parts)

                if has_jp:
                    # Look up in translation map
                    vn_lines = None
                    if jp_merged in translation_map:
                        vn_lines = translation_map[jp_merged]
                    else:
                        # Try individual line lookup
                        vn_lines = []
                        all_found = True
                        for part in jp_parts:
                            if part in translation_map:
                                vn_lines.extend(translation_map[part])
                            else:
                                all_found = False
                                break
                        if not all_found:
                            vn_lines = None

                    if vn_lines is not None:
                        # Apply: each vn_line -> corresponding 401 cmd
                        for k, idx in enumerate(block_401_indices):
                            if k < len(vn_lines):
                                cmd_list[idx]['parameters'][0] = vn_lines[k]
                                applied_lines += 1
                        applied_blocks += 1
                    else:
                        skipped_blocks += 1

            i = j
        else:
            i += 1

print(f"Applied translations: {applied_blocks} blocks, {applied_lines} individual lines")
print(f"Skipped (no match in CSV): {skipped_blocks} blocks")

# ── 4. Check remaining JP
remaining = 0
for ev in ce:
    if ev and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if not txt.strip().startswith('.'):
                        remaining += 1

print(f"\nRemaining Japanese lines after split-apply: {remaining}")

# ── 5. Save and sync
with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(ce, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_DATA, "CommonEvents.json"))

print("Synced to patch-release and test game!")
