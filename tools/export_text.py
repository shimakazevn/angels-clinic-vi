#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
export_text.py -- Export toàn bộ text từ RPG Maker MZ JSON ra CSV để dịch tiếng Việt
Game: 天使の早漏治療クリニック (RJ01644040) — Bản tiếng Nhật

CSV output columns (9 cột):
  file          -- tên file JSON nguồn (CommonEvents, Map001, System...)
  entry_id      -- ID của event/entry
  event_name    -- tên CommonEvent hoặc tên Map Event
  map_name      -- tên map (tự động suy luận từ MapInfos.json cho CommonEvents)
  scene_type    -- phân loại cảnh: 18+_治療 / Story / UI / AfterCare / v.v.
  speaker_clean -- tên người nói đã làm sạch (không có mã màu \C[N])
  speaker_raw   -- tên người nói gốc (giữ nguyên mã màu)
  original_jp   -- văn bản tiếng Nhật gốc
  vietnamese    -- [ĐỂ TRỐNG] -- điền bản dịch vào đây

Cách dùng:
    python tools/export_text.py

Output: translation/text_export.csv
"""

import json
import csv
import re
from pathlib import Path
from collections import defaultdict

# ---- Cấu hình đường dẫn ----
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
GAME_DIR   = ROOT_DIR / "天使の早漏治療クリニック" / "Game"
DATA_DIR   = GAME_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "translation"
OUTPUT_CSV = OUTPUT_DIR / "text_export.csv"
OUTPUT_DIR.mkdir(exist_ok=True)

# ========== Helpers: Clean ==========

def clean_speaker(raw: str) -> str:
    """Làm sạch tên người nói: bỏ mã màu \\C[N], \\c[N], \\N[N]."""
    if not raw:
        return ""
    s = re.sub(r'\\[Cc]\[\d+\]', '', raw)   # màu: \C[4] \c[2]
    s = re.sub(r'\\[Nn]\[\d+\]', '', s)      # biến tên: \N[1]
    s = re.sub(r'\\[Vv]\[\d+\]', '', s)      # biến số: \v[84]
    return s.strip()

def is_empty(s):
    return not s or str(s).strip() == ""

def clean_text(s):
    if s is None: return ""
    return str(s).strip()

# ========== Phân loại scene ==========

MAP_SCENE_TYPE = {
    # 18+ scenes
    "治療":        "18+_治療",
    "アフターケア": "18+_AfterCare",
    "敗北":        "18+_Defeat",
    "回想":        "Flashback",
    # Story / UI
    "OP":          "Story_OP",
    "メインストーリー": "Story_Main",
    "ホーム画面":   "UI_Home",
    "買い物":      "UI_Shop",
    "編成":        "UI_Formation",
    "チュートリアル": "UI_Tutorial",
    "裏メニュー":   "UI_SecretMenu",
    "回想再生":     "UI_FlashbackPlayer",
    "治療導入":    "Story_TreatmentIntro",
}

def classify_scene(map_name: str, event_name: str = "") -> str:
    """Phân loại scene dựa trên tên map / tên event."""
    combined = (map_name or "") + " " + (event_name or "")
    for keyword, scene_type in MAP_SCENE_TYPE.items():
        if keyword in combined:
            return scene_type
    return "Other"

# ========== Load MapInfos ==========

def load_map_infos() -> dict:
    """Trả về {map_id: map_name}."""
    path = DATA_DIR / "MapInfos.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for entry in data:
        if entry:
            result[entry["id"]] = entry.get("name", "")
    return result

def infer_map_name(event_name: str, map_names: set) -> str:
    """Suy luận tên map cho CommonEvents dựa trên tên event và MapInfos."""
    if not event_name:
        return ""
    
    # 1. HシーンN -> 治療N
    m_h = re.search(r'Hシーン(\d+)', event_name)
    if m_h:
        target_map = f"治療{m_h.group(1)}"
        if target_map in map_names:
            return target_map

    # 2. Khớp trực tiếp hoặc chứa tên map
    for mname in sorted(map_names, key=len, reverse=True):
        if mname and (mname in event_name or event_name.startswith(mname)):
            return mname

    # 3. Nhận diện từ khóa
    if "メインストーリー" in event_name:
        return "メインストーリー"
    elif "治療" in event_name:
        m = re.search(r'治療\d+', event_name)
        if m and m.group(0) in map_names:
            return m.group(0)
        return "治療"
    elif "アフターケア" in event_name:
        m = re.search(r'アフターケア\d+', event_name)
        if m and m.group(0) in map_names:
            return m.group(0)
        return "アフターケア"
    elif "敗北" in event_name:
        return "敗北イベント"
    elif "ショップ" in event_name or "買い物" in event_name:
        return "買い物"

    return ""

# ========== Row builder ==========

rows = []  # danh sách các row sẽ ghi ra CSV

def add_row(
    file_key, entry_id, event_name, map_name, scene_type,
    speaker_raw, original_jp
):
    text = clean_text(original_jp)
    if is_empty(text):
        return
    rows.append({
        "file":          file_key,
        "entry_id":      entry_id,
        "event_name":    event_name or "",
        "map_name":      map_name or "",
        "scene_type":    scene_type or "",
        "speaker_clean": clean_speaker(speaker_raw),
        "speaker_raw":   speaker_raw or "",
        "original_jp":   text,
        "vietnamese":    "",
    })

# ========== Database files (System, Items, v.v.) ==========

def export_simple_db(filename, fields):
    path = DATA_DIR / filename
    if not path.exists(): return 0
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    file_key = filename.replace(".json", "")
    count = 0
    for entry in data:
        if entry is None: continue
        eid = entry.get("id", "?")
        for field in fields:
            val = entry.get(field)
            if val and not is_empty(val):
                add_row(file_key, eid, field, "", "UI_Database", "", val)
                count += 1
    print(f"  {filename}: {count} entries")
    return count

def export_system():
    path = DATA_DIR / "System.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    count = 0
    def sys_add(field, val):
        nonlocal count
        if val and not is_empty(str(val)):
            add_row("System", 0, field, "", "UI_System", "", str(val))
            count += 1

    sys_add("gameTitle", data.get("gameTitle"))

    for lst_field in ["armorTypes","weaponTypes","skillTypes","equipTypes","elements"]:
        for i, v in enumerate(data.get(lst_field, [])):
            sys_add(f"{lst_field}[{i}]", v)

    terms = data.get("terms", {})
    for i, v in enumerate(terms.get("basic", [])):    sys_add(f"terms.basic[{i}]", v)
    for i, v in enumerate(terms.get("commands", [])): sys_add(f"terms.commands[{i}]", v)
    for i, v in enumerate(terms.get("params", [])):   sys_add(f"terms.params[{i}]", v)
    for k, v in terms.get("messages", {}).items():    sys_add(f"terms.messages.{k}", v)

    print(f"  System.json: {count} entries")
    return count

def export_map_infos(map_infos: dict):
    count = 0
    for mid, mname in map_infos.items():
        if mname and not is_empty(mname):
            add_row("MapInfos", mid, "name", mname, "UI_MapName", "", mname)
            count += 1
    print(f"  MapInfos.json: {count} entries")
    return count

# ========== Event parser ==========

def get_speaker(cmd: dict) -> str:
    params = cmd.get("parameters", [])
    if len(params) > 4 and params[4]:
        return str(params[4])
    return ""

def extract_dialogue_blocks(cmd_list: list) -> list:
    blocks = []
    i = 0
    while i < len(cmd_list):
        cmd = cmd_list[i]
        code = cmd.get("code", 0)
        params = cmd.get("parameters", [])

        if code == 101:  # Show Text header
            speaker = get_speaker(cmd)
            lines = []
            j = i + 1
            while j < len(cmd_list) and cmd_list[j].get("code") == 401:
                p = cmd_list[j].get("parameters", [])
                if p: lines.append(str(p[0]))
                j += 1
            full_text = "\n".join(lines)
            if not is_empty(full_text):
                blocks.append({
                    "type": "dialogue",
                    "index": i,
                    "speaker_raw": speaker,
                    "text": full_text,
                })
            i = j
            continue

        elif code == 102:  # Show Choices
            choices = params[0] if params else []
            if isinstance(choices, list):
                for ci, choice in enumerate(choices):
                    if choice and not is_empty(str(choice)):
                        blocks.append({
                            "type": "choice",
                            "index": i,
                            "speaker_raw": "[Choice]",
                            "text": str(choice),
                            "choice_idx": ci,
                        })
        i += 1
    return blocks

def process_event_pages(
    file_key, entry_id, event_name, map_name, scene_type, pages
):
    count = 0
    for page_idx, page in enumerate(pages):
        if not page: continue
        cmd_list = page.get("list", [])
        if not cmd_list: continue

        blocks = extract_dialogue_blocks(cmd_list)

        for block in blocks:
            page_label = f"{event_name} [p{page_idx}]" if len(pages) > 1 else event_name
            speaker = block["speaker_raw"]
            text = block["text"]

            add_row(
                file_key, entry_id, page_label, map_name, scene_type,
                speaker, text
            )
            count += 1
    return count

# ========== CommonEvents ==========

def export_common_events(map_infos: dict):
    path = DATA_DIR / "CommonEvents.json"
    size_mb = path.stat().st_size / 1024 / 1024
    print(f"  CommonEvents.json: đang đọc ({size_mb:.0f} MB)...")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    map_names = set(mname for mname in map_infos.values() if mname)

    total = 0
    for entry in data:
        if entry is None: continue
        eid     = entry.get("id", "?")
        ename   = entry.get("name", f"CE_{eid}")
        cmd_list = entry.get("list", [])

        # Suy luận map_name cho CommonEvent
        inferred_map = infer_map_name(ename, map_names)

        scene = classify_scene(inferred_map, ename)

        fake_pages = [{"list": cmd_list}]
        total += process_event_pages(
            "CommonEvents", eid, ename, inferred_map, scene, fake_pages
        )

    print(f"  CommonEvents.json: {total} entries")
    return total

# ========== Map files ==========

def export_map(filename: str, map_infos: dict) -> int:
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    map_id_str = re.search(r'Map(\d+)', filename)
    map_id = int(map_id_str.group(1)) if map_id_str else 0
    map_name = map_infos.get(map_id, filename.replace(".json", ""))
    file_key = filename.replace(".json", "")
    scene_type = classify_scene(map_name)

    events = data.get("events", [])
    total = 0
    for event in events:
        if event is None: continue
        eid    = event.get("id", "?")
        ename  = event.get("name", f"Ev{eid}")
        pages  = event.get("pages", [])
        total += process_event_pages(
            file_key, eid, ename, map_name, scene_type, pages
        )
    return total

# ========== Battle Log (LogMessage plugin, code 357 + 657) ==========

def export_logtext():
    """Xuất các dòng battle log (plugin LogMessage, code 357) thành CSV riêng.

    Cột: original_jp, vietnamese. Mỗi text chỉ xuất 1 lần (duy nhất theo nội dung).
    Lệnh code 657 liền kề (`テキスト = ...`) sẽ được tự động patch cùng text.
    """
    from collections import Counter
    path_csv = OUTPUT_DIR / "logtext.csv"
    seen = Counter()

    def walk_cmd_list(cmd_list):
        for cmd in cmd_list:
            if cmd.get("code") != 357:
                continue
            p = cmd.get("parameters", [])
            if not p or p[0] != "LogMessage" or len(p) <= 3 or not isinstance(p[3], dict):
                continue
            t = str(p[3].get("text", "")).strip()
            if t:
                seen[t] += 1

    def scan_container(container):
        # CommonEvents: list of entries; Map: dict with events[]
        events = container.get("events") if isinstance(container, dict) else container
        if events is None:
            return
        for ev in events:
            if ev is None:
                continue
            pages = ev.get("pages", []) if isinstance(ev, dict) else [{"list": ev.get("list", [])}]
            for page in pages:
                if page:
                    walk_cmd_list(page.get("list", []))

    # CommonEvents
    ce_path = DATA_DIR / "CommonEvents.json"
    if ce_path.exists():
        with open(ce_path, encoding="utf-8") as f:
            ce_data = json.load(f)
        for entry in ce_data:
            if entry:
                walk_cmd_list(entry.get("list", []))

    # Maps
    for mf in sorted(DATA_DIR.glob("Map[0-9]*.json")):
        if mf.name == "MapInfos.json":
            continue
        with open(mf, encoding="utf-8") as f:
            mdata = json.load(f)
        scan_container(mdata)

    total_occ = sum(seen.values())
    print(f"  LogMessage: {len(seen)} unique texts / {total_occ} occurrences")

    with open(path_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["original_jp", "vietnamese"])
        for t, n in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0])):
            writer.writerow([t, ""])
    print(f"  -> {path_csv}")
    return len(seen)

def export_galge_choice():
    """Xuất prompt chọn lựa (plugin LL_GalgeChoiceWindow showChoice, code 357) thành CSV riêng.

    Cột: original_jp, vietnamese. Mỗi text (messageText + từng nhãn choice) xuất 1 lần
    duy nhất theo nội dung, để dịch theo bộ nhớ dùng chung giữa các prompt.
    """
    from collections import Counter
    path_csv = OUTPUT_DIR / "galge_choice.csv"
    seen = Counter()

    def walk_cmd_list(cmd_list):
        for cmd in cmd_list:
            if cmd.get("code") != 357:
                continue
            p = cmd.get("parameters", [])
            if not p or p[0] != "LL_GalgeChoiceWindow" or len(p) <= 3 or not isinstance(p[3], dict):
                continue
            mt = str(p[3].get("messageText", "")).strip()
            if mt:
                seen["MSG\t" + mt] += 1
            choices_raw = p[3].get("choices", "")
            try:
                choices = json.loads(choices_raw or "[]")
            except Exception:
                choices = []
            if isinstance(choices, list):
                for ci, elm in enumerate(choices):
                    try:
                        d = json.loads(elm)
                        label = str(d.get("label", "")).strip()
                    except Exception:
                        label = str(elm).strip()
                    if label:
                        seen["CH\t" + label] += 1

    def scan_container(container):
        events = container.get("events") if isinstance(container, dict) else container
        if events is None:
            return
        for ev in events:
            if ev is None:
                continue
            pages = ev.get("pages", []) if isinstance(ev, dict) else [{"list": ev.get("list", [])}]
            for page in pages:
                if page:
                    walk_cmd_list(page.get("list", []))

    ce_path = DATA_DIR / "CommonEvents.json"
    if ce_path.exists():
        with open(ce_path, encoding="utf-8") as f:
            ce_data = json.load(f)
        for entry in ce_data:
            if entry:
                walk_cmd_list(entry.get("list", []))

    for mf in sorted(DATA_DIR.glob("Map[0-9]*.json")):
        if mf.name == "MapInfos.json":
            continue
        with open(mf, encoding="utf-8") as f:
            mdata = json.load(f)
        scan_container(mdata)

    msgs = sum(n for k, n in seen.items() if k.startswith("MSG\t"))
    chs = sum(n for k, n in seen.items() if k.startswith("CH\t"))
    print(f"  GalgeChoice: {len(seen)} unique texts ({msgs} messageText, {chs} choice labels)")

    with open(path_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["original_jp", "vietnamese"])
        for k, n in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0])):
            writer.writerow([k.split("\t", 1)[1], ""])
    print(f"  -> {path_csv}")
    return len(seen)

# ========== Main ==========

def main():
    print("=" * 60)
    print("RPG Maker MZ -- Export Text to CSV (with Map Name Inference)")
    print(f"Game: {GAME_DIR}")
    print(f"Out:  {OUTPUT_CSV}")
    print("=" * 60)

    map_infos = load_map_infos()

    print("\n[1] Database files")
    export_simple_db("Actors.json",  ["name", "nickname", "profile"])
    export_simple_db("Items.json",   ["name", "description"])
    export_simple_db("Weapons.json", ["name", "description"])
    export_simple_db("Armors.json",  ["name", "description"])
    export_simple_db("Enemies.json", ["name"])
    export_simple_db("Classes.json", ["name"])
    export_simple_db("Skills.json",  ["name","description","message1","message2"])
    export_simple_db("States.json",  ["name","message1","message2","message3","message4"])
    export_system()
    export_map_infos(map_infos)

    print("\n[2] CommonEvents")
    export_common_events(map_infos)

    print("\n[3] Map files")
    map_files = sorted(DATA_DIR.glob("Map[0-9]*.json"))
    map_total = 0
    for mf in map_files:
        if mf.name == "MapInfos.json": continue
        n = export_map(mf.name, map_infos)
        if n > 0: print(f"  {mf.name}: {n} entries")
        map_total += n
    print(f"  Maps total: {map_total} entries")

    print(f"\n[3b] Battle log (LogMessage)")
    export_logtext()

    print(f"\n[3c] Choice prompts (LL_GalgeChoiceWindow)")
    export_galge_choice()

    print(f"\n[4] Ghi CSV ({len(rows)} rows)...")
    fieldnames = [
        "file", "entry_id", "event_name", "map_name", "scene_type",
        "speaker_clean", "speaker_raw",
        "original_jp", "vietnamese",
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nXong! {len(rows)} rows -> {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
