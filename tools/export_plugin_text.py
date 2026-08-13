#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
export_plugin_text.py -- Quét các file JS plugin trong game/js/plugins/ và game/js/plugins.js
để tìm chuỗi tiếng Nhật có khả năng hiển thị trong UI và export ra CSV để dịch.

Output: translation/plugin_text.csv
"""

import os
import re
import csv
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
GAME_DIR   = ROOT_DIR / "天使の早漏治療クリニック" / "Game"
PLUGINS_DIR = GAME_DIR / "js" / "plugins"
PLUGINS_JS  = GAME_DIR / "js" / "plugins.js"
OUTPUT_CSV  = ROOT_DIR / "translation" / "plugin_text.csv"

# Pattern nhận biết ký tự tiếng Nhật
JP_RE = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')

IGNORE_PLUGINS = {
    "Text2Frame.js",
    "DevToolsManage.js",
    "PluginCommonBase.js",
}

STR_RE = re.compile(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`)')

def extract_strings_from_file(filepath: Path, file_label: str):
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    extracted = []
    in_multiline_comment = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if in_multiline_comment:
            if "*/" in line:
                in_multiline_comment = False
                line = line.split("*/", 1)[1]
            else:
                continue

        if "/*" in line and "*/" not in line:
            in_multiline_comment = True
            line = line.split("/*", 1)[0]

        if "//" in line:
            parts = line.split("//", 1)
            if not line.split("//")[0].strip():
                continue
            line = parts[0]

        if not JP_RE.search(line):
            continue

        matches = STR_RE.findall(line)
        for m in matches:
            raw_str = m[1:-1]
            # Unwrap escaped quotes in raw_str if needed
            raw_clean = raw_str.replace(r'\"', '"').replace(r"\'", "'")
            if JP_RE.search(raw_clean) and len(raw_clean.strip()) > 0:
                if raw_clean.startswith("@") or raw_clean.startswith("http"):
                    continue
                # Bỏ qua tên file ảnh (ví dụ "システム/照れゲージ1")
                if "/" in raw_clean and (raw_clean.endswith("1") or raw_clean.endswith("2") or raw_clean.startswith("スチル") or raw_clean.startswith("UI")):
                    continue
                extracted.append((file_label, idx, raw_clean))

    return extracted

def main():
    print("=" * 60)
    print("Export Plugin JS Strings to CSV")
    print(f"Plugins dir: {PLUGINS_DIR}")
    print(f"Output CSV:  {OUTPUT_CSV}")
    print("=" * 60)

    rows = []
    total_files = 0
    total_strings = 0

    # 1. Quét plugins.js (nơi chứa option names, cheat headers...)
    if PLUGINS_JS.exists():
        pjs_strings = extract_strings_from_file(PLUGINS_JS, "plugins.js")
        if pjs_strings:
            total_files += 1
            print(f"  plugins.js: {len(pjs_strings)} strings")
            for flabel, line_num, s in pjs_strings:
                rows.append({
                    "plugin_file": flabel,
                    "line_num": line_num,
                    "original_jp": s,
                    "vietnamese": ""
                })
                total_strings += 1

    # 2. Quét các plugin .js trong plugins/
    if PLUGINS_DIR.exists():
        for js_file in sorted(PLUGINS_DIR.glob("*.js")):
            if js_file.name in IGNORE_PLUGINS:
                continue

            strings = extract_strings_from_file(js_file, js_file.name)
            if strings:
                total_files += 1
                print(f"  {js_file.name}: {len(strings)} strings")
                for flabel, line_num, s in strings:
                    rows.append({
                        "plugin_file": flabel,
                        "line_num": line_num,
                        "original_jp": s,
                        "vietnamese": ""
                    })
                    total_strings += 1

    print(f"\n[+] Tổng cộng: {total_files} files, {total_strings} strings -> {OUTPUT_CSV}")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["plugin_file", "line_num", "original_jp", "vietnamese"])
        writer.writeheader()
        writer.writerows(rows)

    print("✅ Export plugin text hoàn tất!")

if __name__ == "__main__":
    main()
