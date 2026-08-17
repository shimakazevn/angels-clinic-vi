# Patch Việt Hóa — 天使の早漏治療クリニック (Angelic Clinic)

<div align="center">

![Version](https://img.shields.io/badge/version-v2.0.0-gold.svg?style=flat-square)
![Platform](https://img.shields.io/badge/platform-PC%20%7C%20Android%20%7C%20iOS-brightgreen.svg?style=flat-square)
![Engine](https://img.shields.io/badge/engine-RPG%20Maker%20MZ-orange.svg?style=flat-square)
![Status](https://img.shields.io/badge/status-Completed-success.svg?style=flat-square)

Bản patch Tiếng Việt hoàn chỉnh dành cho tựa game **天使の早漏治療クリニック (RJ01644040)**.

</div>

---

## 🚀 Nhật ký cập nhật v2.0.0 (Changelog)

### 🌟 Đại tu dịch thuật & Khắc phục 100% lỗi lệch kịch bản (Full Project Audit)
- **Hoàn thiện 100% toàn bộ kịch bản cốt truyện & H-scene**:
  - **MEMO 18 & MEMO 22**: Sửa lỗi thoại dồn ép tâm lý (`CE 439`, `CE 446`).
  - **MEMO 23 (Cow Girl Sữa Mẹ)**: Căn chỉnh phân đoạn bú sữa và cưng nựng trong `CE 449`.
  - **MEMO 25 (Đại kết cục / Ending)**: Căn chỉnh toàn bộ **12 dòng đối thoại kết thúc game** (`CE 453`), lời bộc bạch xúc động của Sera về nơi chốn thuộc về cô và lời hứa mãi mãi bên cạnh Main.
  - **H-scene 3 (`CE 504`)**: Căn chỉnh 20 dòng màn kẹp ngực tra tấn quy đầu và phần thưởng bắn tinh vào khe ngực.
  - **H-scene 20 & 21 (`CE 521`, `CE 522`)**: Dịch và căn chỉnh toàn bộ màn làm tình cưỡi ngựa lọt khe ngoài trời tại hẻm nhỏ bãi biển, loại bỏ các chuỗi header bị chèn nhầm.
  - **H-scene 23 (`CE 524`)**: Dịch trọn vẹn màn làm tình kem tăng độ nhạy cảm x10.
  - **H-scene 28 (Climax Post-game `CE 529`)**: Dịch và khôi phục toàn bộ **64 dòng thoại cao trào** (màn cưỡng bức ân ái dồn dập, kích thích tam giác 3 điểm và xuất tinh nhiều lần liên tục), xóa sạch các chuỗi tag menu bị lỗi trước đó.
  - **Hệ thống Aftercare**: Căn chỉnh toàn bộ lời thoại mở khóa và hướng dẫn chăm sóc tinh thần sau trị liệu (`CE 364`).

### 🛠️ Sửa lỗi hệ thống & Tương thích đa nền tảng
- **Khắc phục triệt để lỗi treo/đơ game trên Android & iOS** tại **Main Story 17** (`CE 437`).
- **Khắc phục lỗi crash trong chiến đấu (`Animation not found: 能力変化_主人公3_残り6`)**: Nâng cấp plugin `PictureSpine.js` và thư viện `pixi-spine.js` tự động fallback số lượt hiệu ứng còn lại (`_残り5`) và chặn hoàn toàn các ngoại lệ thiếu animation Spine làm dừng game.
- **Sửa lỗi hiển thị thông báo hệ thống**: Điều chỉnh đúng thông báo điều khiển con lăn chuột (`\C[2]con lăn chuột\C[0]`) tại các H-scene 13, 14, 18 (`CE 514`, `CE 515`, `CE 519`).
- **Việt hóa 100% tất cả các Lựa chọn (Choices) trong Game**:
  - Dịch toàn bộ các nhánh lựa chọn trong chiến đấu, sự kiện, H-scene và Aftercare (`ま、ママ……っ`, `ま……ママ、しーしーさせて……っ`, `反応する/反応しない`, `楽しかったです/ソワソワしました`, `胸を揉む`, `こと細かく教える`...) sang tiếng Việt hoàn chỉnh.
- **Tối ưu hóa pipeline đóng gói**: Hỗ trợ xuất đồng thời bộ cài đặt PC (Full Game ZIP), Android (APK) và iOS (IPA).
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
1. Tải gói ZIP `ThienSuClinic-PC-v2.0.0.zip` từ mục Releases và giải nén.
2. Chạy trực tiếp `Game.exe` để trải nghiệm game đã tích hợp sẵn tiếng Việt.

---

### 📱 Dành cho Android
1. Tải file `ThienSuClinic-Android-v2.0.0.apk` từ mục Releases.
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
