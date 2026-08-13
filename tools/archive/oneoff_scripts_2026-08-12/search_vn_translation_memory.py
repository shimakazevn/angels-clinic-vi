#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, glob

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
APP_DATA = r"C:\Users\Shimakaze\.gemini\antigravity-ide"

print("=== SEARCHING FOR COMMON EVENTS AND TRANSLATION MEMORY FILES ===")

for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f == 'CommonEvents.json' or 'vn' in f.lower() or 'tran' in f.lower():
            fp = os.path.join(root, f)
            print(f"Found file: {fp} ({os.path.getsize(fp)} bytes)")

for root, dirs, files in os.walk(os.path.join(APP_DATA, "brain")):
    for f in files:
        if f.endswith('.json') or f.endswith('.jsonl') or f.endswith('.py'):
            if 'CommonEvents' in f or 'translation' in f.lower():
                fp = os.path.join(root, f)
                print(f"Found brain file: {fp} ({os.path.getsize(fp)} bytes)")
