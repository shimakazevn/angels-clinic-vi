#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync toàn bộ data_vn -> patch/data, patch-release/patch/data, test game/data, và android assets/data
"""
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT           = Path(r"e:\天使の早漏治療クリニック - RJ01644040")
DATA_VN        = ROOT / "translation" / "data_vn"
PATCH_DATA_ROOT = ROOT / "patch" / "data"
PATCH_DATA_REL  = ROOT / "patch-release" / "patch" / "data"
TEST_DATA_1    = ROOT / "Tenshi_no_Hayarou_Clinic_VN" / "Game" / "data"
TEST_DATA_2    = ROOT / "天使の早漏治療クリニック - TEST" / "Game" / "data"
ANDROID_DATA   = ROOT / "patch-release" / "android" / "template" / "app" / "src" / "main" / "assets" / "data"

target_dirs = [PATCH_DATA_ROOT, PATCH_DATA_REL]
if TEST_DATA_1.parent.exists(): target_dirs.append(TEST_DATA_1)
if TEST_DATA_2.parent.exists(): target_dirs.append(TEST_DATA_2)
if ANDROID_DATA.parent.exists(): target_dirs.append(ANDROID_DATA)

synced = 0
for src_file in sorted(DATA_VN.glob("*.json")):
    for dst_dir in target_dirs:
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_dir / src_file.name)
    synced += 1

print(f"Synced {synced} files from data_vn -> {[str(d) for d in target_dirs]}")

# Also sync AutoWordWrap.js & DarkPlasma_TextLog.js to patch dirs
for plugin_name in ["AutoWordWrap.js", "DarkPlasma_TextLog.js"]:
    game_js = ROOT / "天使の早漏治療クリニック - TEST" / "Game" / "js" / "plugins" / plugin_name
    for js_dst in [ROOT / "patch" / "js" / "plugins", ROOT / "patch-release" / "patch" / "js" / "plugins"]:
        js_dst.mkdir(parents=True, exist_ok=True)
        if game_js.exists():
            shutil.copy2(game_js, js_dst / plugin_name)
            print(f"Synced {plugin_name} to {js_dst}")
