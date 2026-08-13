#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_desync_403.py -- Fix desynced subtitle lines in text_export.csv for CommonEvents 403, 447, 508.
"""
import csv
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
CSV_PATH = ROOT_DIR / "translation" / "text_export.csv"

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    # 1. Fix CommonEvents 403 (53 rows)
    ce403_vn = [
        # 0 to 19 (Clinic after Treatment 1)
        "Trông anh ngơ ngác thế kia, anh có sao không?",
        "Tôi không sao... nhưng có nhiều chuyện quá nên hơi loạn...",
        "Ra là vậy. Lần đầu trị liệu nên cũng khó tránh khỏi.",
        "Lần tới anh đến lúc nào cũng được, nhưng xin hãy cố gắng đừng để khoảng cách quá xa nhé.",
        "Vì hiệu quả trị liệu sẽ bị giảm bớt đấy.",
        "Lần tới...",
        "(Lại còn có lần tới nữa sao... *nuốt nước bọt*...)",
        "...Ừm. Nếu anh không trả lời thì em không biết liệu anh có đến nữa hay không đâu.",
        "A, v-vâng. Tôi sẽ lại đến. Nhờ em giúp đỡ.",
        "Thế thì tốt rồi.",
        'Vì em là "y tá riêng của anh", nên nếu anh không đến thường xuyên thì em sẽ khó xử lắm.',
        "Y-Y tá riêng của tôi...?",
        "Ồ, bây giờ anh mới nhận ra sao? Trên bảng tên của em cũng có ghi mà.",
        "...A, phải rồi, em chưa cho anh xem. Tại mải mê với anh quá nên em quên mất.",
        "Một lần nữa xin tự giới thiệu, em là Sera, y tá riêng của anh. Từ nay về sau mong được anh giúp đỡ.",
        "(Tôi chẳng hiểu chuyện gì đang xảy ra nữa...)",
        "(Rốt cuộc đến đây thường xuyên thế này có ổn không nhỉ... Không chừng đây là bẫy mỹ nhân kế...?)",
        "Vậy anh hãy giữ gìn sức khỏe nhé.",
        "Lần tới anh lại đến nhé.",
        "……",
        # 20 to 30 (Succubus encounter in dungeon)
        "Hê~? Anh trai, anh lại đến nữa sao~?♡",
        "……！",
        "Không ngờ anh lại đến nữa! Em vui lắm đó~♡",
        "Có phải lần trước được em chơi cùng nên thành nghiện rồi đúng không?♡",
        "Hay là ở nhà cũng nhớ tới em rồi tự sướng?♡ Hì hì hì...♡",
        "Thế thì để em giúp anh trai lấp đầy hình bóng em trong đầu hơn nữa nhé♡",
        "... ah. Hà... phù...",
        "...Hà!",
        "...A..., s-sao lại... ah. Sao anh lại chịu đựng được chứ...?",
        "Rõ ràng con cu đang cứng ngắc mà... ah.",
        "Phù... Nguy hiểm thật..."
    ]

    ce403_indices = [i for i, r in enumerate(rows) if len(r) > 1 and r[0] == "CommonEvents" and r[1] == "403"]
    for k, vn_line in enumerate(ce403_vn):
        row_idx = ce403_indices[k]
        while len(rows[row_idx]) <= 8:
            rows[row_idx].append("")
        rows[row_idx][8] = vn_line

    # 2. Fix CommonEvents 447 (remove 6 bogus lines at rows 0-5)
    ce447_indices = [i for i, r in enumerate(rows) if len(r) > 1 and r[0] == "CommonEvents" and r[1] == "447"]
    ce447_vn_original = [rows[i][8] if len(rows[i]) > 8 else "" for i in ce447_indices]
    ce447_new_vn = ce447_vn_original[6:] + [
        "Tôi hiểu rồi...",
        "Quả nhiên là như vậy nhỉ.",
        "Cảm ơn cô nhiều.",
        "Hẹn gặp lại cô sau.",
        "……",
        "Chắc mình cũng phải cố gắng hơn thôi."
    ]
    for k, vn_line in enumerate(ce447_new_vn):
        row_idx = ce447_indices[k]
        while len(rows[row_idx]) <= 8:
            rows[row_idx].append("")
        rows[row_idx][8] = vn_line

    # 3. Fix CommonEvents 508 (remove 6 bogus lines at rows 0-5)
    ce508_indices = [i for i, r in enumerate(rows) if len(r) > 1 and r[0] == "CommonEvents" and r[1] == "508"]
    ce508_vn_original = [rows[i][8] if len(rows[i]) > 8 else "" for i in ce508_indices]
    ce508_new_vn = [
        'Con cu của anh đang bảo "Hàng rồi ạ~, xin hãy làm cho em sướng đi mà~♡" kìa.',
        "Vậy thì hãy để em tiếp tục bóc trần tiếng lòng bên trong anh hơn nữa nhé."
    ] + ce508_vn_original[6:]
    while len(ce508_new_vn) < len(ce508_indices):
        ce508_new_vn.append("……")

    for k, vn_line in enumerate(ce508_new_vn[:len(ce508_indices)]):
        row_idx = ce508_indices[k]
        while len(rows[row_idx]) <= 8:
            rows[row_idx].append("")
        rows[row_idx][8] = vn_line

    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ Successfully fixed text_export.csv for CommonEvents 403, 447, 508!")

if __name__ == "__main__":
    main()
