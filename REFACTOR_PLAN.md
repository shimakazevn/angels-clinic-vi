# KẾ HOẠCH REFACTOR TOÀN BỘ PATCH VIỆT HÓA
## Phòng Khám Thiên Sứ: Chuyên Trị Xuất Tinh Sớm (RJ01644040)

> Ngày lập: 2026-08-12 | Trạng thái: ✅ **ĐÃ HOÀN THÀNH** (xem mục 8)

---

## 1. CHẨN ĐOÁN HIỆN TRẠNG (đã kiểm chứng bằng công cụ)

### 1.1 Tài sản quan trọng đang có (CÒN NGUYÊN, không hư)

| Tài sản | Đường dẫn | Tình trạng |
|---|---|---|
| **Game gốc tiếng Nhật (PRISTINE)** | `天使の早漏治療クリニック\Game\data\` | ✅ 61 file JSON, `gameTitle` vẫn tiếng Nhật, **không có** file `.bak` → chưa từng bị patch đè |
| **Translation Memory CSV (BẢN DỊCH CHUẨN)** | `translation\text_export.csv` | ✅ **4880 dòng, 100% đã dịch tiếng Việt, 0 dòng trống**, khớp 100% cấu trúc với game gốc (đã chạy lại `export_text.py` và so sánh: identical) |
| **Plugin text CSV** | `translation\plugin_text.csv` | ✅ 115/115 dòng đã dịch |
| **Plugin JS đã dịch** | `translation\js_vn\` | ✅ 16 file (plugins.js + 15 plugin), **giữ nguyên theo yêu cầu** |
| **Hệ thống patch** | `patch-release\` | ✅ apply_patch.py/.bat/.sh + android/ còn nguyên, chỉ thiếu payload sạch |

### 1.2 NGUYÊN NHÂN BỊ HỎNG (đã xác định rõ)

File dữ liệu `translation\data_vn\*.json` (và bản copy trong `patch-release\patch\data\` + game thử nghiệm `Tenshi_no_Hayarou_Clinic_VN\`) đã bị **sửa chồng nhiều lần qua nhiều công cụ khác nhau không có backup**, kết quả phân tích `CommonEvents.json` hiện tại:

```
Dòng hội thoại hợp lệ:  3.937  (VN)
Dòng tiếng Anh (dư):    1.089  (từ lần patch EN trước)
Dòng TRỐNG (mất text):  2.621  (do script đổ chuỗi rỗng vào)
Dòng Nhật còn sót:         36  (tên người nói chưa map)
```

Chuỗi sự kiện hỏng (tái dựng từ log script trong `tools/`):
1. `block_align_all_commonevents.py` — chèn bản dịch **EN** (từ bản EN patch cũ đã bị xóa) vào JP master.
2. `import_text.py` chạy nhiều lần chồng lên file đã có EN → lệch khớp nội dung.
3. `fill_overflow_401_with_empty.py` — đổ chuỗi rỗng `""` vào **2621 dòng** Nhật thừa → **mất text hội thoại**.
4. Hàng loạt script "fix chữa cháy" (map008, split/apply, correct_split...) sửa vào file đã hỏng.

→ Kết quả: **toàn bộ patch hiện có 3 ngôn ngữ (EN + JP + VN) lẫn lộn, nhiều dòng trống, game chạy không ra chữ.**

### 1.3 ĐIỂM MẤU CHỐT (đã chứng minh bằng thực nghiệm)

Chạy thử **import lại từ đầu** trên bản sao game gốc sạch + CSV dịch chuẩn (sandbox):
```
Trước (file đang dùng):  empty=2621   jp=36   en=1089   vn=3937
Sau  (import sạch):      empty=0      jp=0    en=43*    vn=5060
```
- `0 dòng trống`, `0 tiếng Nhật`, `0 tên nhân vật Nhật còn sót` (28 chuỗi tên đều đã có trong bảng map).
- 43 dòng "EN" thực chất là **âm thanh/thán từ** (Ah...♡, Ngoan ngoan., FFFFF!?!?) — chấp nhận được.
- Kiểm tra cấu trúc chuẩn hóa: **0 lỗi** trên 89.332 khối lệnh CommonEvents + 335 page map → chỉ khác JP ở số dòng 401 trong khối hội thoại (đúng bản chất, không đụng code/choice/điều kiện nào).

→ **Kết luận: BẢN DỊCH CHUẨN NẰM TRONG CSV. Cần tái sinh toàn bộ JSON từ (game gốc + CSV) bằng đúng 1 pipeline sạch.**

---

## 2. KIẾN TRÚC ĐÍCH (1 NGUỒN CHUẨN DUY NHẤT)

```
 game gốc JP (PRISTINE)        text_export.csv (bản dịch chuẩn)     js_vn/ + ui_images/ (plugin - GIỮ NGUYÊN)
        │                               │                                    │
        ▼                               ▼                                    │
   export_text.py  (CHỈ đọc, dùng để verify/khớp)                           │
        │                                                                     │
        ▼                                                                     ▼
   import_text.py ──────────────────────────────► translation/data_vn (TÁI SINH SẠCH)
                                                          │
                                                          ▼
                          ┌───────────────┬────────────────┴───────────────┐
                          ▼               ▼                                ▼
             patch-release/patch/data  Tenshi_no_Hayarou_Clinic_VN/Game/data   (build_vietnamese_game.py)
                          │
                          ▼
              apply_patch.py → game người dùng (tự backup .bak)
```

**Nguyên tắc:**
- CSV = nguồn dịch duy nhất. Mọi sửa chữa nội dung dịch **chỉ sửa trong CSV**, sau đó import lại từ đầu — KHÔNG bao giờ sửa tay vào JSON.
- JSON = hàng hóa sinh ra tự động, luôn rebuild được từ đầu.
- Plugin JS, ui_images, android, apply_patch.* → giữ nguyên 100%.

---

## 3. CÁC GIAI ĐOẠN THỰC HIỆN

### Giai đoạn 0 — Backup toàn bộ & khởi tạo git (NGĂN TÁI PHẠM "không backup")
1. Khởi tạo git repo tại thư mục gốc (hiện chưa có git).
2. Commit snapshot đầu tiên: game gốc PRISTINE + CSV + tools + patch-release (giữ nguyên hiện trạng).
3. Copy an toàn `translation\data_vn` (bản hỏng) sang `tools\archive\corrupted_2026-08-12\` để đối chiếu.
   - File nhỏ nhất (700KB→21MB) → không lo tốn dung lượng.

### Giai đoạn 1 — Làm sạch Translation Memory (CSV)
Sửa trực tiếp trong `translation\text_export.csv`:
1. **3 dòng dính chữ Nhật trong cột `vietnamese`:**
   - `...giao phó cơ体 cho em nhé.` → `cơ thể`
   - `...mình chẳng thể làm冒険者 tiếp được...` → `Mạo Hiểm Giả`
   - `...lên đỉnh絶頂, tất cả...` → `lên đỉnh`
2. **Actor `Main`** (`Actors|1|name|主人公`) → quyết định: để "Main" hay đổi "Nhân Vật Chính" (hỏi bạn).
3. Rà 43 dòng "EN-only" còn lại → xác nhận là âm thanh/thán từ hợp lệ (giữ) hay cần dịch.
4. Kiểm tra 108 dòng ký hiệu (…, !, Á., 3……♡) → đều hợp lệ.
5. Sau khi sửa: chạy lại script kiểm tra CSV (0 trống / 0 Nhật / 0 lệch dòng).

### Giai đoạn 2 — Củng cố công cụ import (`tools/import_text.py`)
Giữ thuật toán hiện tại (đã chứng minh đúng trong sandbox), chỉ sửa:
1. Fix lỗi **báo cáo sai "0 fields patched"** cho Actors/Items (cosmetic, log sai vì in sau vòng lặp — không ảnh hưởng kết quả).
2. Thêm **báo cáo fail-safe**: in số khối hội thoại JP không khớp row nào (hiện âm thầm bỏ qua).
3. (Tùy chọn) Tách hằng số đường dẫn thành tham số CLI để tránh hardcode `e:\...`.
4. `export_text.py` đã chứng minh OK → không cần sửa, chỉ dùng để verify.

### Giai đoạn 3 — TÁI SINH SẠCH (lõi của refactor)
1. Xóa sạch `translation\data_vn\*.json` (bản hỏng đã được archive ở GĐ 0).
2. Chạy `python tools/import_text.py` → sinh lại toàn bộ JSON từ (game gốc + CSV sạch).
3. Kết quả dự kiến: 0 dòng trống, 0 tiếng Nhật, 0 tên Nhật, cấu trúc nguyên vẹn.

### Giai đoạn 4 — Tái tạo patch + game thử nghiệm
1. `python tools/sync_all_to_patch.py` → copy data_vn sạch vào `patch-release\patch\data\` và `Tenshi_no_Hayarou_Clinic_VN\Game\data\`.
2. Rebuild sạch game thử nghiệm: `python tools/build_vietnamese_game.py` (nó tự xóa & tạo lại thư mục VN từ game gốc, không đụng game gốc).
   - ⚠️ Lưu ý: script này dùng `shutil.copytree` toàn bộ game gốc (kể cả file lưu `save/` nếu có) — cần đảm bảo game gốc thật sự pristine.
3. Sync plugin: `AutoWordWrap.js` (bản đang chạy OK) vào patch/js (giữ nguyên 15 plugin còn lại).
4. Kiểm tra `patch-release\patch\img\` — **hiện không tồn tại** (bản dịch ảnh UI chưa làm, xem mục 5).

### Giai đoạn 5 — KIỂM SOÁT CHẤT LƯỢNG (bắt buộc trước khi phát hành)
Chạy bộ script audit, kỳ vọng:
| Script | Kỳ vọng sau refactor |
|---|---|
| `full_translation_status.py` | 0 Nhật, 0 trống |
| `scan_all_game_data_for_japanese.py` | 0 file còn Nhật (kể cả tên nhân vật) |
| `verify_structure_vs_jp.py` + `struct_check2.py` | cấu trúc chuẩn hóa 0 lỗi |
| Audit nội bộ (EN/diacritics) | chỉ còn thán từ hợp lệ |
| Chạy thật game (PC + Android nếu có) | hội thoại, UI, choices chạy đúng |

### Giai đoạn 6 — Vệ sinh & phòng ngừa (ngăn tái phát)
1. Gộp các script chữa cháy một-lần vào `tools\archive\` (giữ lịch sử, khỏi nhầm lẫn):
   `auto_translate_*`, `batch_translate_*`, `translate_*`, `correct_split_apply`, `split_and_apply*`, `fix_*`, `fill_overflow*`, `block_align*`, `revert_map008*`, `rebuild_op1_op2*`…
2. Tạo `tools\BUILD_GUIDE.md`: ghi rõ chuỗi lệnh chuẩn 3 bước (export → import → sync/build).
3. Commit git sau mỗi giai đoạn thành công → luôn có điểm rollback.

---

## 4. KHÔNG ĐỤNG VÀO (theo yêu cầu "giữ nguyên plugin & mod")

- `translation\js_vn\*` — toàn bộ plugin JS đã dịch.
- `patch-release\patch\js\*` — plugins.js + 15 plugin (chỉ sync lại đúng 1 file `AutoWordWrap.js` nếu cần).
- `patch-release\android\*`, `apply_patch.bat`, `apply_patch.sh`, `tools\apply_patch.py`.
- `translation\ui_images\original\*` (ảnh gốc để làm việc sau).

---

## 5. CÔNG VIỆC NGOÀI PHẠM VI (cần bạn quyết sau)

1. **Dịch ảnh UI** (`ui_images\edited` đang **0 file**, 55 ảnh `status=pending` trong `image_list.csv`). Patch hiện không có `patch\img\` → giao diện ảnh (menu, gauge) vẫn tiếng Nhật. Đây là giai đoạn riêng, chưa nằm trong refactor này.
2. **Chất lượng 1 số dòng dịch plugin** (ví dụ dòng JSON cấu hình dài trong `plugins.js` bị dịch thành tên plugin khác — có thể do bảng dịch plugin_text.csv đang lệch hàng). Nếu muốn, làm ở đợt sau.

---

## 6. CÂU HỎI CẦN BẠN XÁC NHẬN TRƯỚC KHI THỰC HIỆN

1. **`Main` (tên nhân vật chính)** → giữ nguyên "Main" hay đổi thành "Nhân Vật Chính"?
2. **Bản JSON hỏng hiện tại** → archive lại để tham khảo (khuyến nghị) hay xóa luôn?
3. **Xóa/cập nhật game thử nghiệm `Tenshi_no_Hayarou_Clinic_VN`** → được rebuild đè (nó sẽ được tạo lại sạch từ đầu)?
4. Có muốn tôi **khởi tạo git + commit snapshot** trước khi làm (khuyến nghị mạnh)?
5. Sau refactor, có cần **build lại APK Android** không (bản hiện có dùng data cũ)?

---

## 7. TÓM TẮT 3 BƯỚC CHÍNH

1. **CSV = nguồn sự thật** — sửa 3 dòng lẫn Nhật + làm sạch nhỏ.
2. **Rebuild JSON từ đầu** bằng `import_text.py` (đã chứng minh cho ra kết quả sạch trong sandbox).
3. **Sync & rebuild** patch + game thử, chạy bộ audit xác nhận 0 Nhật / 0 trống / 0 EN dư, rồi phát hành.

---

## 8. NHẬT KÝ THỰC HIỆN (2026-08-12)

| Giai đoạn | Trạng thái | Ghi chú |
|---|---|---|
| GĐ 0 — Git + snapshot | ✅ | `git init` + commit baseline; archive `data_vn` hỏng → `tools/archive/corrupted_data_vn_2026-08-12/` |
| GĐ 1 — Sạch CSV | ✅ | Sửa 3 dòng dính chữ Nhật (体/冒険者/絶頂) → 4880 dòng, 0 trống, 0 Nhật |
| GĐ 2 — Củng cố import_text.py | ✅ | Thêm fail-safe: báo khối hội thoại không khớp CSV |
| GĐ 3 — Rebuild data_vn | ✅ | 4577 CE + 119 map + DB patches, **0 khối không khớp** |
| GĐ 4 — Sync + rebuild game | ✅ | `build_vietnamese_game.py` + `sync_all_to_patch.py`; 58 file patch/data ≡ data_vn (MD5) |
| GĐ 5 — Audit | ✅ | **100% dịch, 0 trống, 0 Nhật, 0 tên Nhật**, cấu trúc chuẩn hóa 0 lỗi |
| GĐ 6 — Vệ sinh + docs | ✅ | Archive 32 script một-lần; tạo `tools/BUILD_GUIDE.md` |

**Kết quả so sánh trước/sau (CommonEvents.json):**

| Chỉ số | TRƯỚC (hỏng) | SAU (refactor) |
|---|---|---|
| Dòng hội thoại dịch được | 3.937 (66%) | 5.131 (100%) |
| Dòng trống (mất text) | 2.621 | 0 |
| Dòng tiếng Anh dư | 1.089 | 0 (chỉ còn âm thanh/thán từ hợp lệ) |
| Tiếng Nhật còn sót (kể cả tên nhân vật) | 36 | 0 |

**Lưu ý phát hiện trong lúc làm:**
- Thư mục game thử nghiệm cũ `Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN` đã được
  đổi tên thành `DELETE` (nằm trong thư mục gốc, chứa bản data hỏng cũ). KHÔNG đụng tới;
  game thử nghiệm mới đã được dựng lại sạch từ đầu.
- Ngày 2026-08-12: đổi tên game thử nghiệm sang Romaji + VN cho gọn và đỡ phản cảm
  → `Tenshi_no_Hayarou_Clinic_VN` (Romaji của 天使の早漏治療クリニック + VN).
- Bản dịch ảnh UI (`translation/ui_images`) vẫn chưa hoàn thành (0/55 ảnh) — nằm ngoài
  phạm vi refactor, làm ở đợt sau nếu cần.
