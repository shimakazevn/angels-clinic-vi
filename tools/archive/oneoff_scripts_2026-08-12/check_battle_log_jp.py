#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
VN   = os.path.join(ROOT, "translation", "data_vn")
jp_re = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')

# System.json - terms.messages (battle log messages)
with open(os.path.join(VN, "System.json"), 'r', encoding='utf-8') as f:
    sys_data = json.load(f)
msgs = sys_data.get('terms', {}).get('messages', {})
print("=== System.json terms.messages (JP remaining) ===")
jp_msgs = {k: v for k, v in msgs.items() if jp_re.search(str(v))}
if jp_msgs:
    for k, v in jp_msgs.items():
        print(f"  {k}: {repr(v)}")
else:
    print("  All clean!")

# Skills.json - message1/message2
with open(os.path.join(VN, "Skills.json"), 'r', encoding='utf-8') as f:
    skills = json.load(f)
print("\n=== Skills.json message1/message2 (JP remaining) ===")
found = 0
for s in skills:
    if not s: continue
    sid = s.get('id', '?')
    sname = s.get('name', '')
    for field in ['message1', 'message2']:
        v = s.get(field, '')
        if v and jp_re.search(v):
            print(f"  Skill {sid} ({sname}): {field}={repr(v)}")
            found += 1
if found == 0:
    print("  All clean!")

# States.json - messages
with open(os.path.join(VN, "States.json"), 'r', encoding='utf-8') as f:
    states = json.load(f)
print("\n=== States.json messages (JP remaining) ===")
found = 0
for s in states:
    if not s: continue
    sid = s.get('id', '?')
    sname = s.get('name', '')
    for field in ['message1', 'message2', 'message3', 'message4']:
        v = s.get(field, '')
        if v and jp_re.search(v):
            print(f"  State {sid} ({sname}): {field}={repr(v)}")
            found += 1
if found == 0:
    print("  All clean!")
