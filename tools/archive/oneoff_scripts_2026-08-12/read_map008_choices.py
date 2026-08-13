#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
with open(os.path.join(ROOT, 'translation', 'data_vn', 'Map008.json'), 'r', encoding='utf-8') as f:
    map8 = json.load(f)

ev1 = next(e for e in map8['events'] if e and e.get('id') == 1)
cmd9 = ev1['pages'][0]['list'][9]
p = cmd9['parameters'][3]
print('messageText:', repr(p.get('messageText', '')))
print()
print('choices raw:', repr(p.get('choices', '')))
