# Patch Việt Hóa — 天使の早漏治療クリニック (Angelic Clinic)

<div align="center">

![Version](https://img.shields.io/badge/version-v1.5.0-blue.svg?style=flat-square)
![Platform](https://img.shields.io/badge/platform-PC%20%7C%20Android%20%7C%20iOS-brightgreen.svg?style=flat-square)
![Engine](https://img.shields.io/badge/engine-RPG%20Maker%20MZ-orange.svg?style=flat-square)
![Status](https://img.shields.io/badge/status-Completed-success.svg?style=flat-square)

Bản patch Tiếng Việt hoàn chỉnh dành cho tựa game **天使の早漏治療クリニック (RJ01644040)**.

</div>

---

## 🚀 Nhật ký cập nhật v1.5.0 (Changelog)

### 🛠️ Sửa lỗi hệ thống & Tương thích đa nền tảng
- **Khắc phục triệt để lỗi treo/đơ game trên Android & iOS** tại **Main Story 17** (`CE 437`).
- **Khắc phục lỗi crash trong chiến đấu (`Animation not found: 能力変化_主人公3_残り6`)**: Nâng cấp plugin `PictureSpine.js` và thư viện `pixi-spine.js` tự động fallback số lượt hiệu ứng còn lại (`_残り5`) và chặn hoàn toàn các ngoại lệ thiếu animation Spine làm dừng game.
- **Sửa lỗi hiển thị thông báo hệ thống**: Điều chỉnh đúng thông báo điều khiển con lăn chuột (`\C[2]con lăn chuột\C[0]`) tại các H-scene 13, 14, 18 (`CE 514`, `CE 515`, `CE 519`).
- **Tối ưu hóa pipeline đóng gói**: Hỗ trợ xuất đồng thời bộ cài đặt PC (Full Game ZIP), Android (APK) và iOS (IPA).

### 📖 Sửa lỗi lệch kịch bản (Desync) & Trau chuốt dịch thuật
- **MEMO 5 & MEMO 6**:
  - Sửa lỗi chính tả `uốn tréo lưng` $\rightarrow$ `uốn éo thắt lưng`, `nhai nhồm nhàm` $\rightarrow$ `nhai nhồm nhoàm`.
  - Căn chỉnh và nạp lại toàn bộ **31 dòng** kịch bản màn thủ dâm bằng đồ lót của Sera (`CE 507`).
- **MEMO 9**:
  - Dịch lại nửa đầu Main Story 9-2 (`CE 421`): Đoạn mời rượu nho & đùa kiểu Thiên Sứ (*Angel joke*) không còn bị trùng lặp với đoạn say xỉn.
  - Căn chỉnh lại nửa sau H-scene 10 (`CE 511`): Nạp lại đầy đủ thoại Sera kích thích và nuốt trọn tinh dịch thay cho đoạn đếm ngược bị lệch.
- **MEMO 10**:
  - Căn chỉnh lại toàn bộ **19 câu đối thoại** giữa Sera, Succubus và Main tại tiệm sách 18+ (`CE 423`), sửa đúng vai nhân vật và nội dung.
- **MEMO 11**:
  - Sửa phân đoạn uống thuốc teo nhỏ cơ thể (Shota) trong Main Story 11-1 (`CE 424`).
  - Dịch và nạp lại toàn bộ **33 dòng** màn kẹp ngực Shota (`CE 513`) bám sát kịch bản gốc tiếng Nhật.
- **MEMO 12**:
  - Sửa dòng thông báo con lăn chuột bị chèn vào giữa H-scene 14 (`CE 515`).
  - Sửa toàn bộ lỗi chính tả `ăn ăn kiểm điểm` $\rightarrow$ `ăn năn kiểm điểm` trong các màn xuất tinh trừng phạt.
  - Trau chuốt lời thoại của Succubus ở Main Story 12-2 (`CE 427`).
- **EX 1 & EX 3**:
  - Căn chỉnh ngữ cảnh khổ dâm và sửa lỗi chính tả tại `CE 509`.
  - Dịch và nạp lại toàn bộ **39 dòng** màn trừng phạt sục cu từ phía sau tư thế bò 4 chân (`CE 509`).
  - Căn chỉnh 10 dòng đối thoại an ủi & vỗ về phục hồi tinh thần của Sera trong `CE 514`.

---

## 📥 Hướng dẫn cài đặt

### 💻 Dành cho Windows (PC)

#### Cách 1: Cài đặt tự động qua Script (Khuyến nghị)
1. Tải file `AUTO_UPDATE_PATCH_VIET_HOA.bat` từ phần Releases.
2. Đặt file `.bat` vào cùng thư mục chứa file `Game.exe`.
3. Nhấp đúp chuột chạy file `.bat` để script tự động tải và cập nhật bản patch mới nhất.

#### Cách 2: Cài đặt thủ công (Offline)
1. Tải gói ZIP `ThienSuClinic-PC-v1.5.0.zip` từ mục Releases và giải nén.
2. Chạy trực tiếp `Game.exe` để trải nghiệm game đã tích hợp sẵn tiếng Việt.

---

### 📱 Dành cho Android
1. Tải file `ThienSuClinic-Android-v1.5.0.apk` từ mục Releases.
2. Cài đặt trực tiếp file APK lên thiết bị Android của bạn (cho phép cài đặt từ nguồn không xác định nếu được yêu cầu).
3. Mở game và trải nghiệm (đã tích hợp đầy đủ tính năng cảm ứng và plugin tự động ngắt dòng).

---

### 🍏 Dành cho iOS / iPadOS
1. Tải file `ThienSuClinic-iOS-v1.5.0.ipa` từ mục Releases.
2. Sử dụng **TrollStore** (nếu thiết bị hỗ trợ), **Sideloadly** hoặc **AltStore** để cài đặt file `.ipa` vào máy.

---

## 📌 Tính năng bản Patch
- **Dịch thuật trọn vẹn 100%**: Bao gồm toàn bộ cốt truyện chính, các bài trị liệu, H-scene, danh mục vật phẩm, nhật ký chiến đấu (*Battle Log*) và các lựa chọn hội thoại.
- **Hệ thống tự động xuống dòng (AutoWordWrap)**: Căn chỉnh chữ mượt mà, không bị tràn màn hình trên mọi kích thước hiển thị.
- **Giao diện & Nút bấm tinh chỉnh**: Giữ nguyên tính thẩm mỹ của giao diện gốc và bổ sung các phím bấm hỗ trợ cảm ứng trên thiết bị di động.

---

## 📝 Lưu ý & Báo lỗi
- Nếu bạn gặp bất kỳ lỗi dịch thuật, lỗi hiển thị hoặc lỗi đơ game trong quá trình trải nghiệm, vui lòng tạo Issue trên GitHub hoặc liên hệ với nhóm dịch để được hỗ trợ khắc phục sớm nhất.
