#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
seed_galge_choice.py -- Tạo translation/galge_choice.csv từ data_vn hiện tại.

Vì các prompt GalgeChoice (code 357) được dịch trực tiếp trong data_vn (không nằm
trong text_export.csv), script này ghép song song game gốc (JP) với data_vn (VN)
theo đúng thứ tự duyệt để xây LUT original_jp -> vietnamese.
"""
import json
import csv
import os
from pathlib import Path
from collections import OrderedDict

ROOT = Path(r"E:\天使の早漏治療クリニック - RJ01644040")
JP_DIR = ROOT / "天使の早漏治療クリニック" / "Game" / "data"
VN_DIR = ROOT / "translation" / "data_vn"
OUT_CSV = ROOT / "translation" / "galge_choice.csv"


def collect(data, tag):
    """Trả về list (tag, value) theo thứ tự duyệt: messageText trước, từng label sau,
    cộng với các command code-657 (bản mirror hiển thị trong editor của GalgeChoice)."""
    out = []

    def walk_cmd_list(cmd_list):
        for cmd in cmd_list:
            if not isinstance(cmd, dict):
                continue
            p = cmd.get("parameters", [])
            if not isinstance(p, list) or not p:
                continue
            if cmd.get("code") == 357:
                if p[0] != "LL_GalgeChoiceWindow" or len(p) <= 3 or not isinstance(p[3], dict):
                    continue
                mt = str(p[3].get("messageText", ""))
                if mt:
                    out.append(("MSG", mt))
                choices_raw = p[3].get("choices", "")
                try:
                    choices = json.loads(choices_raw or "[]")
                except Exception:
                    choices = []
                if isinstance(choices, list):
                    for elm in choices:
                        try:
                            d = json.loads(elm)
                            label = str(d.get("label", ""))
                        except Exception:
                            label = str(elm)
                        if label:
                            out.append(("CH", label))
            elif cmd.get("code") == 657 and isinstance(p[0], str):
                if p[0].startswith(("質問メッセージ = ", "選択肢リスト = ")):
                    out.append(("657", p[0]))

    containers = data.get("events") if isinstance(data, dict) else data
    if containers is None:
        return out
    for ev in containers:
        if ev is None:
            continue
        pages = ev.get("pages", []) if isinstance(ev, dict) else [{"list": ev.get("list", [])}]
        for page in pages:
            if page:
                walk_cmd_list(page.get("list", []))
    return out


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    lut = OrderedDict()
    files = sorted(f for f in JP_DIR.glob("*.json") if f.name.startswith("Map") and f.name != "MapInfos.json")
    files.append(JP_DIR / "CommonEvents.json")

    for jp_path in files:
        name = jp_path.name
        vn_path = VN_DIR / name
        if not vn_path.exists():
            continue
        jp_list = collect(load_json(jp_path), "jp")
        vn_list = collect(load_json(vn_path), "vn")
        if len(jp_list) != len(vn_list):
            print(f"  ⚠️  {name}: JP {len(jp_list)} != VN {len(vn_list)} (bỏ qua)")
            continue
        for (jt, jv), (vt, vv) in zip(jp_list, vn_list):
            if jt != vt:
                print(f"  ⚠️  {name}: loại lệch ({jt} vs {vt})")
                continue
            if jv != vv and vv:  # chỉ lưu khi khác nhau (đã dịch)
                lut[jv.strip()] = vv

    print(f"Seeded {len(lut)} entries -> {OUT_CSV}")
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["original_jp", "vietnamese"])
        for jp, vn in lut.items():
            writer.writerow([jp, vn])


if __name__ == "__main__":
    main()
