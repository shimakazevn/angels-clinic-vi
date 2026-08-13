import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

SKILL_NAME_MAP = {
    211: 'スキル1_"Đáng Yêu"',
    212: 'スキル2_"Anh Yêu Em"',
    213: 'スキル3_"Thích Chị"',
    214: 'スキル4_"Dịu Dàng"',
    215: 'スキル5_"Giỏi Quá"',
    216: 'スキル6_"Ngầu Quá"',
    217: 'スキル7_"Đáng Tin"',
    218: 'スキル8_"Giọng Ấm"',
    219: 'スキル9_"Dâm Táo"',
    220: 'スキル10_"Khiêu Gợi"',
    221: "スキル11_Chịu Đựng I",
    222: "スキル12_Chịu Đựng II",
    223: "スキル13_Chịu Đựng III",
    224: "スキル14_Điều Hòa Nhịp Thở",
    225: "スキル15_Hít Thở Sâu",
    226: "スキル16_Phản Công • Tay",
    227: "スキル17_Phản Công • Miệng",
    228: "スキル18_Phản Công • Ngực",
    229: "スキル19_Phản Công • Chân",
    230: "スキル20_Phản Công • Cọ Xát",
    231: "スキル21_Thế Cảnh Giác I",
    232: "スキル22_Thế Cảnh Giác II",
    233: "スキル23_Phân Tích I",
    234: "スキル24_Phân Tích II",
    235: "スキル25_Luyện Tưởng Tượng I",
    236: "スキル26_Luyện Tưởng Tượng II",
    237: "スキル27_Thế Thân I",
    238: "スキル28_Thế Thân II",
    239: "スキル29_Tạm Hưu Chiến",
    240: "スキル30_Không Phòng Thủ",
    241: "スキル31_Hạ Nhiệt I",
    242: "スキル32_Hạ Nhiệt II",
    243: "スキル33_Hạ Nhiệt III",
    244: "スキル34_Hất Ra",
    245: "スキル35_Trò Chuyện Hài Hước",
    246: "スキル36_Hư Cấu",
    247: "スキル37_Xúc Xắc Giả",
    248: "スキル38_Nhịp Độ Nhanh"
}

ce_path = r"e:\天使の早漏治療クリニック - RJ01644040\translation\data_vn\CommonEvents.json"

with open(ce_path, "r", encoding="utf-8") as f:
    events = json.load(f)

count = 0
for ev in events:
    if ev and ev.get("id") in SKILL_NAME_MAP:
        old_name = ev["name"]
        new_name = SKILL_NAME_MAP[ev["id"]]
        ev["name"] = new_name
        print(f"Updated Event ID {ev['id']}: '{old_name}' -> '{new_name}'")
        count += 1

with open(ce_path, "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=4)

print(f"\n✅ Updated {count} skill event names in CommonEvents.json!")
