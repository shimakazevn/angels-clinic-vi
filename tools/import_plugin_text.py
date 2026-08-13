#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
import_plugin_text.py -- Đọc translation/plugin_text.csv (nếu đã điền 'vietnamese')
và patch ngược vào js/plugins.js cũng như các file js trong js/plugins/

Output: translation/js_vn/ (chứa plugins.js và thư mục plugins/ đã patch)
Cách dùng:
    python tools/import_plugin_text.py
"""

import os
import csv
import shutil
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
GAME_DIR   = ROOT_DIR / "天使の早漏治療クリニック" / "Game"
PLUGINS_DIR = GAME_DIR / "js" / "plugins"
PLUGINS_JS  = GAME_DIR / "js" / "plugins.js"
TRANS_DIR   = ROOT_DIR / "translation"
INPUT_CSV   = TRANS_DIR / "plugin_text.csv"
OUTPUT_JS_DIR = TRANS_DIR / "js_vn"

OUTPUT_JS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("Import Plugin JS Translations from CSV")
    print(f"Input CSV: {INPUT_CSV}")
    print(f"Output:    {OUTPUT_JS_DIR}")
    print("=" * 60)

    if not INPUT_CSV.exists():
        print(f"❌ Không tìm thấy: {INPUT_CSV}")
        return

    trans = defaultdict(list)  # {plugin_file: [(line_num, orig_jp, vietnamese)]}
    total = 0
    translated = 0

    with open(INPUT_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            vn = row.get("vietnamese", "").strip()
            if vn:
                translated += 1
                trans[row["plugin_file"]].append((int(row["line_num"]), row["original_jp"], vn))

    print(f"  CSV loaded: {total} rows, {translated} đã dịch")

    if translated == 0:
        print("⚠️ Không có bản dịch plugin nào trong CSV (cột 'vietnamese' trống).")
        return

    # Patch plugins.js nếu có dịch
    if "plugins.js" in trans and PLUGINS_JS.exists():
        content = PLUGINS_JS.read_text(encoding="utf-8", errors="ignore")
        count = 0
        for line_num, orig, vn in trans["plugins.js"]:
            if orig in content:
                content = content.replace(orig, vn)
                count += 1
        out_pjs = OUTPUT_JS_DIR / "plugins.js"
        out_pjs.write_text(content, encoding="utf-8")
        print(f"  plugins.js: {count} strings patched -> {out_pjs}")

    # Patch các file .js trong plugins/
    out_plugins_sub = OUTPUT_JS_DIR / "plugins"
    out_plugins_sub.mkdir(exist_ok=True)

    for pfile, items in trans.items():
        if pfile == "plugins.js":
            continue
        src_path = PLUGINS_DIR / pfile
        if not src_path.exists():
            continue

        content = src_path.read_text(encoding="utf-8", errors="ignore")
        count = 0
        for line_num, orig, vn in items:
            if orig in content:
                content = content.replace(orig, vn)
                count += 1

        out_file = out_plugins_sub / pfile
        out_file.write_text(content, encoding="utf-8")
        print(f"  plugins/{pfile}: {count} strings patched -> {out_file}")

    print(f"\n✅ Patch plugin hoàn tất! Kết quả tại: {OUTPUT_JS_DIR}")
    print("   Để apply: copy plugins.js và thư mục plugins/ vào game/js/")

if __name__ == "__main__":
    main()
