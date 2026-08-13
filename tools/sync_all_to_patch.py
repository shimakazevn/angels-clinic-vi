#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync toàn bộ data_vn -> patch/data và test game/data
"""
import os, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA_1 = os.path.join(ROOT, "Tenshi_no_Hayarou_Clinic_VN", "Game", "data")
TEST_DATA_2 = os.path.join(ROOT, "天使の早漏治療クリニック - TEST", "Game", "data")
ANDROID_DATA = os.path.join(ROOT, "patch-release", "android", "template", "app", "src", "main", "assets", "data")

target_dirs = [PATCH_DATA]
if os.path.exists(TEST_DATA_1): target_dirs.append(TEST_DATA_1)
if os.path.exists(TEST_DATA_2): target_dirs.append(TEST_DATA_2)
if os.path.exists(ANDROID_DATA): target_dirs.append(ANDROID_DATA)

synced = 0
for fname in sorted(os.listdir(DATA_VN)):
    if not fname.endswith('.json'): continue
    src = os.path.join(DATA_VN, fname)
    for dst_dir in target_dirs:
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, fname)
        shutil.copy2(src, dst)
    synced += 1

print(f"Synced {synced} files from data_vn -> {target_dirs}")

# Also sync AutoWordWrap.js to patch
game_js_1 = os.path.join(ROOT, "Tenshi_no_Hayarou_Clinic_VN", "Game", "js", "plugins", "AutoWordWrap.js")
game_js_2 = os.path.join(ROOT, "天使の早漏治療クリニック - TEST", "Game", "js", "plugins", "AutoWordWrap.js")
game_js = game_js_1 if os.path.exists(game_js_1) else game_js_2

patch_js_dir = os.path.join(ROOT, "patch-release", "patch", "js", "plugins")
os.makedirs(patch_js_dir, exist_ok=True)
if os.path.exists(game_js):
    shutil.copy2(game_js, os.path.join(patch_js_dir, "AutoWordWrap.js"))
    print("Synced AutoWordWrap.js to patch")
