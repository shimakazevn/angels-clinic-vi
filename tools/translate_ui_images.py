#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate_ui_images.py — Pipeline v2: Dịch và dựng lại 55 ảnh UI đồ họa chuẩn phong cách gốc
Game: 天使の早漏治療クリニック (RJ01644040)
"""

import os
import sys
import shutil
import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ---- Cấu hình đường dẫn ----
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
TRANS_DIR = ROOT_DIR / "translation"
ORIGINAL_DIR = TRANS_DIR / "ui_images" / "original"
EDITED_DIR = TRANS_DIR / "ui_images" / "edited"
LIST_CSV = TRANS_DIR / "ui_images" / "image_list.csv"

EDITED_DIR.mkdir(parents=True, exist_ok=True)

font_bold = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 14)
font_regular = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 13)

TUTORIAL_TRANSLATIONS = {
    "チュートリアル1.png": (
        "MỤC TIÊU TRỊ LIỆU",
        ["Chịu đựng các đòn tấn công dâm mát", "của Y tá Sera và kiên nhẫn nhịn xuất tinh."]
    ),
    "チュートリアル2.png": (
        "THANH GAUGE XUẤT TINH",
        ["Nằm ở phía dưới màn hình", "là thanh Gauge Xuất Tinh của bạn."]
    ),
    "チュートリアル3.png": (
        "CẢNH BÁO THẤT BẠI",
        ["Nếu thanh Gauge Xuất Tinh đạt mức MAX,", "bạn sẽ xuất tinh và thất bại ngay lập tức."]
    ),
    "チュートリアル4.png": (
        "ĐIỀU KIỆN CHIẾN THẮNG",
        ["Nếu số lượt còn lại giảm về 0", "trước khi xuất tinh, bạn sẽ chiến thắng!"]
    ),
    "チュートリアル5.png": (
        "DỰ BÁO HÀNH ĐỘNG",
        ["Vùng này hiển thị loại hành động", "mà Sera sẽ thực hiện trong lượt hiện tại."]
    ),
    "チュートリアル6.png": (
        "TẤN CÔNG BẰNG TAY",
        ["Có vẻ như trong lượt này, Sera chuẩn bị", "tung ra đòn tấn công bằng tay (quay tay)."]
    ),
    "チュートリアル7.png": (
        "KỸ NĂNG PHÒNG THỦ",
        ["Hãy dùng kỹ năng phòng thủ (biểu tượng khiên)", "để giảm sát thương nhận phải trong lượt."]
    ),
    "チュートリアル8.png": (
        "KẾT QUẢ PHÒNG THỦ",
        ["Bị Sera tấn công làm tăng thanh Xuất Tinh,", "nhưng nhờ phòng thủ nên sát thương đã giảm!"]
    ),
    "チュートリアル9.png": (
        "THỜI GIAN HỒI KỸ NĂNG",
        ["Đổi lại, kỹ năng vừa sử dụng", "đã bước vào thời gian hồi (Cool Down)."]
    ),
    "チュートリアル10.png": (
        "QUẢN LÝ KỸ NĂNG",
        ["Lưu ý: Sau khi kích hoạt, kỹ năng sẽ bị khóa", "không thể dùng trong một số lượt nhất định."]
    ),
    "チュートリアル11.png": (
        "PHẢN CÔNG CHỦ ĐỘNG",
        ["Trong lúc kỹ năng phòng thủ đang hồi,", "lần này hãy thử chủ động phản công Sera!"]
    ),
    "チュートリアル12.png": (
        "THANH GAUGE XẤU HỔ",
        ["Phía trên màn hình là thanh Gauge Xấu Hổ.", "Làm đầy thanh này kích hoạt nhiều lợi ích!"]
    ),
    "チュートリアル13.png": (
        "DÙNG LỜI KHEN NGỢI",
        ["Để tích lũy thanh Gauge Xấu Hổ, hãy dùng", "kỹ năng Khen Ngợi (biểu tượng khung thoại)."]
    ),
    "チュートリアル14.png": (
        "TÍCH LŨY THÀNH CÔNG",
        ["Tuyệt vời! Bạn đã sử dụng lời khen ngợi", "để tăng thanh Gauge Xấu Hổ thành công!"]
    ),
    "チュートリアル15.png": (
        "TRẠNG THÁI TRÓI BUỘC",
        ["Tuy nhiên, ngay sau đó bạn đã bị Sera", "tung đòn khống chế Trói Buộc!"]
    ),
    "チュートリアル16.png": (
        "SỨC MẠNH TRÓI BUỘC",
        ["Khi ở trạng thái Trói Buộc, Sera sẽ tung ra", "những đòn tấn công mạnh bạo hơn bình thường."]
    ),
    "チュートリアル17.png": (
        "CÁCH GIẢI TRÓI BUỘC",
        ["Để giải trừ trạng thái Trói Buộc, bạn bắt buộc", "phải đẩy thanh Gauge Xấu Hổ lên mức MAX."]
    ),
    "チュートリアル18.png": (
        "ĐẨY LÊN MAX",
        ["Đã tích sẵn Gauge Xấu Hổ gần mức MAX,", "hãy dùng Lời Khen để đẩy lên MAX ngay!"]
    ),
    "チュートリアル19.png": (
        "GIẢI THOÁT THÀNH CÔNG",
        ["Bạn đã làm đầy thanh Xấu Hổ khiến Sera", "ngượng ngùng và giải trừ Trói Buộc thành công!"]
    ),
    "チュートリアル20.png": (
        "HIỆU ỨNG KHI SERA XẤU HỔ",
        ["Khi Sera ngượng ngùng (MAX Gauge Xấu Hổ):", "• Giải trừ lập tức trạng thái Trói Buộc", "• Hủy bỏ hành động lượt đó của Sera", "• Giảm 1 lượt trong tổng số lượt chịu đựng"]
    ),
    "チュートリアル21.png": (
        "CHIẾN THUẬT PHÒNG THỦ",
        ["Hãy phối hợp linh hoạt các loại kỹ năng", "để chinh phục các buổi trị liệu!"]
    ),
    "チュートリアル22.png": (
        "KIÊN TRÌ THỬ LẠI",
        ["Ban đầu bạn sẽ bị áp đảo bởi chiêu trò của Sera,", "nhưng dù thua vẫn có EXP và Tiền. Hãy thử lại!"]
    ),
    "チュートリアル23.png": (
        "CHỊU ĐỰNG CÀNG LÂU CÀNG TỐT",
        ["Thời gian chịu đựng càng dài thì tiền thưởng", "càng lớn. Hãy cố gắng trụ vững lâu nhất!"]
    ),
    "チュートリアル24.png": (
        "TĂNG GIỚI HẠN XUẤT TINH",
        ["Vất vả cho buổi trị liệu! Trải qua trị liệu đã", "giúp giới hạn Gauge Xuất Tinh của bạn tăng lên."]
    ),
    "チュートリアル25.png": (
        "MÀN HÌNH BIÊN CHẾ",
        ["Bây giờ hãy chuyển sang màn hình Biên Chế", "để chuẩn bị cho liệu trình tiếp theo."]
    ),
    "チュートリアル26.png": (
        "TRANG BỊ & KỸ NĂNG",
        ["Tại màn hình Biên Chế, bạn có thể tự do", "thay đổi kỹ năng và đeo trang bị hỗ trợ."]
    ),
    "チュートリアル27.png": (
        "VẬT PHẨM HỖ TRỢ",
        ["Trang bị khi đeo sẽ phát huy tác dụng liên tục.", "Hãy nhấp vào ô trống đầu tiên nhé."]
    ),
    "チュートリアル28.png": (
        "TIẾN HÀNH TRANG BỊ",
        ["Hãy nhấp chọn để trang bị vật phẩm", "vào ô trống!"]
    ),
    "チュートリアル29.png": (
        "SẴN SÀNG TRỊ LIỆU",
        ["Vật phẩm đã phát huy tác dụng! Hãy sẵn sàng", "bước vào buổi trị liệu tiếp theo!"]
    ),
    "チュートリアル30.png": (
        "CỬA HÀNG MỞ CỬA",
        ["Có vẻ như gần đây cửa hàng đã mở cửa.", "Hãy đến sắm kỹ năng hỗ trợ trị liệu nhé!"]
    ),
    "チュートリアル31.png": (
        "TÙY CHỌN CHEAT HỆ THỐNG",
        ["Nếu muốn trải nghiệm game nhanh gọn hơn,", "hãy bật 'Cài Đặt Cheat' trong menu Options!"]
    ),
    "チュートリアル23_2.png": (
        "KỸ NĂNG ĐẶC BIỆT",
        ["Ngoài ra còn có các kỹ năng đặc biệt khá nhạy cảm...", "Quyết định sử dụng hay không nằm ở bạn."]
    ),
    "チュートリアル24_2.png": (
        "TÙY CHỈNH GIỚI HẠN",
        ["Nhấn nút hình cây bút để tự do điều chỉnh", "giới hạn thanh gauge trong mức cho phép."]
    )
}

def process_tutorial(orig_path, dest_path, filename):
    img_pil = Image.open(orig_path).convert("RGBA")
    arr = np.array(img_pil)
    
    alpha = arr[:, :, 3]
    nonzero = np.argwhere(alpha > 10)
    if len(nonzero) == 0:
        img_pil.save(dest_path)
        return
        
    min_y, min_x = nonzero.min(axis=0)
    max_y, max_x = nonzero.max(axis=0)
    
    white_mask = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220) & (arr[:, :, 3] > 200)
    
    inner_mask = np.zeros_like(white_mask)
    inner_mask[min_y + 30 : max_y - 10, min_x + 10 : max_x - 10] = True
    
    dark_pixels = (arr[:, :, 0] < 160) & (arr[:, :, 1] < 160) & (arr[:, :, 2] < 160) & inner_mask
    
    kernel = np.ones((3, 3), np.uint8)
    dilated_mask = cv2.dilate(dark_pixels.astype(np.uint8), kernel, iterations=1)
    
    cleaned_arr = arr.copy()
    cleaned_arr[dilated_mask > 0] = [255, 255, 255, 255]
    
    cleaned_img = Image.fromarray(cleaned_arr)
    draw = ImageDraw.Draw(cleaned_img)
    
    title_text, body_lines = TUTORIAL_TRANSLATIONS.get(filename, ("HƯỚNG DẪN", ["Nội dung hướng dẫn"]))
    
    x_start = min_x + 18
    y_start = min_y + 36
    
    draw.text((x_start, y_start), title_text, font=font_bold, fill=(180, 30, 30, 255))
    y_start += 22
    
    for line in body_lines:
        draw.text((x_start, y_start), line, font=font_regular, fill=(26, 33, 48, 255))
        y_start += 19
        
    cleaned_img.save(dest_path)

def process_hud(orig_path, dest_path, filename):
    img = Image.open(orig_path).convert("RGBA")
    
    if filename in ["射精ゲージ1.png", "射精ゲージ2.png", "射精ゲージ_スリップダメージ.png"]:
        img = Image.new("RGBA", (171, 9), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 170, 8], fill=(40, 10, 20, 220), outline=(200, 50, 80, 255))
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 8)
        draw.text((3, 0), "XUẤT TINH", font=font, fill=(255, 100, 120, 255))
    elif filename in ["照れゲージ1.png", "照れゲージ2.png"]:
        img = Image.new("RGBA", (171, 9), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 170, 8], fill=(10, 30, 50, 220), outline=(80, 160, 240, 255))
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 8)
        draw.text((3, 0), "XẤU HỔ", font=font, fill=(140, 210, 255, 255))
    elif filename == "スリップダメージ表記.png":
        img = Image.new("RGBA", (33, 22), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(r"C:\Windows\Fonts\ariblk.ttf", 14)
        draw.text((2, 2), "+1", font=font, fill=(255, 60, 80, 255))
    elif filename in ["ホイール操作可.png", "ホイール操作可_上のみ.png"]:
        draw = ImageDraw.Draw(img)
        draw.rectangle([1200, 390, 1270, 480], fill=(0, 0, 0, 0))
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 12)
        txt = "Cuộn\nchuột" if filename == "ホイール操作可.png" else "Cuộn\nlên"
        draw.text((1210, 410), txt, font=font, fill=(255, 255, 255, 230))
        
    img.save(dest_path)

def process_title(orig_path, dest_path):
    orig_img = Image.open(orig_path).convert("RGBA")
    w, h = orig_img.size
    arr = np.array(orig_img)

    region_mask = np.zeros((h, w), dtype=np.uint8)
    region_mask[30:470, 50:730] = 255

    hand_mask = np.zeros((h, w), dtype=np.uint8)
    hand_mask[320:470, 560:730] = 255

    text_pixels = (arr[:, :, 0] > 190) & (arr[:, :, 1] > 190) & (arr[:, :, 2] > 190)
    glow_pixels = ((arr[:, :, 0] > 200) & (arr[:, :, 2] > 220)) | ((arr[:, :, 2] > 220) & (arr[:, :, 1] < 180))

    combined_mask = (text_pixels | glow_pixels) & (region_mask == 255) & (hand_mask == 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    dilated_mask = cv2.dilate(combined_mask.astype(np.uint8), kernel, iterations=2)

    bgr = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2BGR)
    inpainted_bgr = cv2.inpaint(bgr, dilated_mask, inpaintRadius=9, flags=cv2.INPAINT_TELEA)
    inpainted_rgb = cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)

    clean_arr = arr.copy()
    clean_arr[:, :, :3] = inpainted_rgb
    clean_img = Image.fromarray(clean_arr)

    logo_w, logo_h = 750, 480
    font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
    font_main_1 = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
    font_main_2 = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 44)

    def create_neon_text_layer(size, pos, text, font, fill_color, stroke_color, glow_color, stroke_w=6, glow_r=16):
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        
        glow_pass1 = Image.new("RGBA", size, (0, 0, 0, 0))
        d1 = ImageDraw.Draw(glow_pass1)
        d1.text(pos, text, font=font, fill=glow_color, stroke_width=stroke_w + 14, stroke_fill=glow_color)
        glow_blur1 = glow_pass1.filter(ImageFilter.GaussianBlur(glow_r))
        
        glow_pass2 = Image.new("RGBA", size, (0, 0, 0, 0))
        d2 = ImageDraw.Draw(glow_pass2)
        d2.text(pos, text, font=font, fill=glow_color, stroke_width=stroke_w + 6, stroke_fill=glow_color)
        glow_blur2 = glow_pass2.filter(ImageFilter.GaussianBlur(glow_r // 2))
        
        shadow = Image.new("RGBA", size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(shadow)
        sx, sy = pos[0] + 5, pos[1] + 5
        ds.text((sx, sy), text, font=font, fill=(10, 15, 30, 220), stroke_width=stroke_w, stroke_fill=(10, 15, 30, 220))
        
        stroke = Image.new("RGBA", size, (0, 0, 0, 0))
        dst = ImageDraw.Draw(stroke)
        dst.text(pos, text, font=font, fill=fill_color, stroke_width=stroke_w, stroke_fill=stroke_color)
        
        out = Image.alpha_composite(canvas, glow_blur1)
        out = Image.alpha_composite(out, glow_blur2)
        out = Image.alpha_composite(out, shadow)
        out = Image.alpha_composite(out, stroke)
        return out

    badge_canvas = Image.new("RGBA", (logo_w, logo_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge_canvas)
    bx, by, bw, bh = 220, 20, 310, 40
    bd.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=(255, 255, 255, 245), outline=(0, 180, 240, 255), width=3)
    bd.text((bx + 18, by + 7), "PHÒNG KHÁM THIÊN SỨ", font=font_badge, fill=(0, 110, 200, 255))

    line1_layer = create_neon_text_layer(
        size=(logo_w, logo_h),
        pos=(110, 75),
        text="TRỊ LIỆU",
        font=font_main_1,
        fill_color=(255, 255, 255, 255),
        stroke_color=(210, 0, 130, 255),
        glow_color=(255, 0, 170, 255),
        stroke_w=7,
        glow_r=16
    )

    line2_layer = create_neon_text_layer(
        size=(logo_w, logo_h),
        pos=(40, 160),
        text="XUẤT TINH SỚM",
        font=font_main_2,
        fill_color=(255, 255, 255, 255),
        stroke_color=(0, 120, 220, 255),
        glow_color=(0, 210, 255, 255),
        stroke_w=7,
        glow_r=16
    )

    sparkle_layer = Image.new("RGBA", (logo_w, logo_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sparkle_layer)
    import math
    def draw_starburst(d, cx, cy, r_outer, r_inner, color):
        pts = []
        for i in range(8):
            angle = i * (math.pi / 4)
            r = r_outer if i % 2 == 0 else r_inner
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        d.polygon(pts, fill=color)

    draw_starburst(sd, 115, 85, 18, 5, (255, 255, 255, 255))
    draw_starburst(sd, 115, 85, 24, 2, (255, 0, 170, 200))

    logo_composite = Image.alpha_composite(badge_canvas, line1_layer)
    logo_composite = Image.alpha_composite(logo_composite, line2_layer)
    logo_composite = Image.alpha_composite(logo_composite, sparkle_layer)

    rotated_logo = logo_composite.rotate(14.5, resample=Image.BICUBIC, expand=True)

    final_title = clean_img.copy()
    final_title.paste(rotated_logo, (35, 45), rotated_logo)
    final_title.save(dest_path)


def process_command_buttons(orig_path, dest_path, filename):
    img = Image.open(orig_path).convert("RGBA")
    arr = np.array(img)
    h, w, _ = arr.shape
    
    TEXT_DATA = {
        "Command_0.png": ("KHÁM LẦN ĐẦU", "Tạo mới hồ sơ bệnh án"),
        "Command_1.png": ("TÁI KHÁM", "Tiếp tục từ phần lưu trước"),
        "Command_2.png": ("TÙY CHỌN", "Thay đổi các cài đặt hệ thống")
    }
    
    if filename not in TEXT_DATA:
        img.save(dest_path)
        return

    main_txt, sub_txt = TEXT_DATA[filename]
    font_btn_main = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
    font_btn_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 11)

    # Clean Top Half Pink Badge Area
    top_region = arr[10:105, 15:295]
    top_alpha = top_region[:, :, 3]
    pink_clean = np.zeros_like(top_region)
    pink_clean[:, :] = [255, 63, 158, 255]
    pink_clean[:, :, 3] = top_alpha
    arr[10:105, 15:295] = pink_clean

    # Clean Bottom Half White Paper Area
    bot_region = arr[125:220, 15:295]
    bot_alpha = bot_region[:, :, 3]
    paper_clean = np.zeros_like(bot_region)
    paper_clean[:, :] = [248, 244, 235, 255]
    paper_clean[:, :, 3] = bot_alpha
    arr[125:220, 15:295] = paper_clean

    edited_img = Image.fromarray(arr)
    draw = ImageDraw.Draw(edited_img)

    # Render Top Half (White text on Pink Badge)
    t_m_x = int((w - font_btn_main.getlength(main_txt)) // 2)
    t_s_x = int((w - font_btn_sub.getlength(sub_txt)) // 2)
    draw.text((t_m_x, 28), main_txt, font=font_btn_main, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(180, 20, 100, 255))
    draw.text((t_s_x, 65), sub_txt, font=font_btn_sub, fill=(255, 230, 242, 255))

    # Render Bottom Half (Dark charcoal text on White Paper Tag)
    b_m_x = int((w - font_btn_main.getlength(main_txt)) // 2)
    b_s_x = int((w - font_btn_sub.getlength(sub_txt)) // 2)
    draw.text((b_m_x, 142), main_txt, font=font_btn_main, fill=(20, 25, 35, 255), stroke_width=1, stroke_fill=(200, 200, 200, 120))
    draw.text((b_s_x, 178), sub_txt, font=font_btn_sub, fill=(70, 75, 85, 255))

    edited_img.save(dest_path)



def main():
    print("=" * 60)
    print("UI Image Translation Pipeline (v2 Clean Inpaint Edition)")
    print(f"Original dir: {ORIGINAL_DIR}")
    print(f"Edited dir:   {EDITED_DIR}")
    print("=" * 60)

    # Clean EDITED_DIR of any stale files before processing
    for item in os.listdir(EDITED_DIR):
        item_p = EDITED_DIR / item
        if item_p.is_file():
            item_p.unlink()

    for f in os.listdir(ORIGINAL_DIR):
        orig_path = ORIGINAL_DIR / f
        dest_path = EDITED_DIR / f
        
        if f in TUTORIAL_TRANSLATIONS:
            process_tutorial(orig_path, dest_path, f)
            print(f"  ✅ [Tutorial Clean] {f}")
        elif f == "タイトル画面.png":
            process_title(orig_path, dest_path)
            print(f"  ✅ [Title Logo] {f}")
        elif f in ["Command_0.png", "Command_1.png", "Command_2.png"]:
            process_command_buttons(orig_path, dest_path, f)
            print(f"  ✅ [Title Command Clipboard Dual-State] {f}")
        elif f in ["射精ゲージ1.png", "射精ゲージ2.png", "射精ゲージ_スリップダメージ.png", "照れゲージ1.png", "照れゲージ2.png", "スリップダメージ表記.png", "ホイール操作可.png", "ホイール操作可_上のみ.png"]:
            process_hud(orig_path, dest_path, f)
            print(f"  ✅ [HUD] {f}")
        else:
            shutil.copy2(orig_path, dest_path)
            print(f"  ✅ [PC Frame Original Preserved] {f}")

    print(f"\n🎉 Pipeline v2 complete! All images saved to: {EDITED_DIR}")



if __name__ == "__main__":
    main()
