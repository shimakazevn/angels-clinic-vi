#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

# Comprehensive Dictionary mapping English / Japanese H-scene dialogue -> Clean Vietnamese
H_SCENE_DICT = {
    # English lines from EN CommonEvents.json
    "Is it because of your physical condition, or is it\nalso related to mental issues?": "Là do thể chất của anh, hay còn liên quan đến cả vấn đề tâm lý nữa?",
    "So first, while determining the cause...": "Nên trước tiên vừa chẩn đoán nguyên nhân, vừa...",
    "I'll have you get used to it with me.": "giúp anh quen dần nhờ em.",
    "With the nurse...?": "Nhờ cô y tá...?",
    "Meaning...?": "Nghĩa là sao...?",
    "I will perform sexual acts on you, just like the\nattacks from monster girls, so please endure ejacul": "Em sẽ thực hiện các hành vi dâm mát với anh giống như đòn tấn công của Monster Girl, nên anh hãy kiềm chế không được xuất tinh.",
    "If you can endure for the specified time, we will\nmove on to the next stage of treatment.": "Nếu anh chịu đựng được đủ thời gian quy định, liệu trình sẽ chuyển sang giai đoạn tiếp theo.",
    "That is how we will aim for a full recovery.": "Cứ như vậy chúng ta sẽ hướng tới việc chữa khỏi hoàn toàn.",
    "Do you have any questions?": "Anh có thắc mắc gì không ạ?",
    "N-No, sexual acts...": "Kh, không, làm chuyện dâm mát...",
    "That's...": "chuyện đó...",
    "Do you have a complaint?": "Anh có điều gì không hài lòng sao?",
    "Despite saying that...": "Nói thế chứ...",
    "It seems your penis is already erect though.": "con cu của anh đã cứng ngắc lên từ lúc nào rồi kìa.",
    "Ah...!": "Ah...!",
    "S-Sorry...": "X, xin lỗi em...",
    "I always lose to temptation like this...": "Vì lúc nào anh cũng dễ bị gục ngã trước sự quyến rũ như thế này...",
    "When told by a beautiful person like Sera-san...": "Được một người xinh đẹp như Sera nói thế...",
    "It just happens on its own...": "nó tự động cứng lên mất rồi...",
    "I see.": "Ra là thế.",
    "I understand how you usually lose now.": "Em đã nắm được cách anh thường bị đánh bại rồi.",
    "In other words... when something like this is done\nto you...": "Nghĩa là... khi được làm những trò thế này...",
    "You become even less able to endure it.": "thì anh lại càng không thể kiềm chế nổi.",
    "(Gah! S-Sera-san's cleavage...!)": "(K, khe ngực của Sera...!)",
    "(I-It's big...!)": "(T, to quá...!)",
    "Your gaze is nailed to it, isn't it?": "Ánh mắt của anh bị hút chặt vào đó luôn rồi kìa.",
    "Your breathing is getting rough too.": "Hơi thở cũng dồn dập lên rồi đấy.",
    "If necessary for treatment, I don't mind showing\nyou not just the cleavage but the tip as well...": "Nếu cần thiết cho trị liệu, không chỉ khe ngực mà em có thể cho anh xem cả đầu nhũ hoa...",
    "Or letting you knead them, but...": "hoặc để anh xoa bóp nắn bóp thỏa thích cũng không sao hết...",
    "Even so, do you dislike this kind of treatment?": "Dù vậy, anh vẫn không thích liệu trình trị liệu này sao?",
    "Ah...! Ah...!": "Ah...!, ah...!",
    "N-No, I don't dislike it...!": "Kh, không ghét đâu...!",
    "So, like this, your current symptoms...": "Đó, như thế này đây, tình trạng hiện tại của anh...",
    "Have exceeded the level where it can heal naturally": "đã vượt quá mức có thể tự khỏi tự nhiên rồi.",
    "Because with such an obvious seduction...": "Bởi vì chỉ với màn quyến rũ lộ liễu thế này...",
    "You are easily beguiled.": "mà anh đã dễ dàng bị dụ dỗ hoàn toàn rồi.",
    "Ugh...": "Ưu...",
    "You want to become able to not lose to monster\ngirls, right?": "Anh muốn trở nên mạnh mẽ để không bị đánh bại bởi các Monster Girl đúng không.",
    "Then, even if it's embarrassing, this is a\nnecessary treatment...": "Thế thì dù có xấu hổ đi nữa thì đây cũng là điều trị cần thiết...",
    "So please suppress your shame.": "xin anh hãy nén sự ngại ngùng lại.",
    "...Yes...": "...Vâng...",
    "Please rest assured.": "Anh cứ yên tâm.",
    "I won't perform high-difficulty treatment right\nfrom the start.": "Ban đầu em sẽ không thực hiện các đợt trị liệu độ khó cao đâu.",
    "Losing to temptation using breasts like just now...": "Vào lúc này, việc bị khuất phục bởi vòng một quyến rũ...",
    "I judge that it can't be helped in your current\nstate. Therefore...": "cũng là điều khó tránh khỏi. Vì vậy...",
    "During treatment, it's fine if you look at my\nbreasts...": "Trong lúc trị liệu, anh có lén nhìn ngực em cũng được...",
    "Sit on the bed, open your legs, and present the\naffected area here.": "Xin mời anh ngồi lên giường, mở rộng chân ra và đưa vùng bệnh về phía em.",
    "Then... let us begin the treatment.": "Vậy thì... chúng ta bắt đầu trị liệu thôi."
}

# Translate all dialogue lines
translated_count = 0

for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for cmd in ev['list']:
            code = cmd.get('code')
            if code == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str):
                    clean_t = txt.replace('\r\n', '\n').strip()
                    if txt in H_SCENE_DICT:
                        cmd['parameters'][0] = H_SCENE_DICT[txt]
                        translated_count += 1
                    elif clean_t in H_SCENE_DICT:
                        cmd['parameters'][0] = H_SCENE_DICT[clean_t]
                        translated_count += 1

print(f"Applied {translated_count} translations to CommonEvents.json!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(ce, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced master translated CommonEvents.json to patch-release and test game!")
