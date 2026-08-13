#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

# Comprehensive Translation Dictionary for OP1, Succubus, Sera, Battle, Clinics
DIALOGUE_DICT = {
    "このダンジョン、ギルドで聞いていた通り": "Con đường trong hầm ngục này, đúng như những gì nghe được ở Công Hội",
    "道が難解だな……。": "thật là phức tạp...",
    "それに物陰が多くて魔物が隠れられる場所も多い。": "Hơn nữa xung quanh có nhiều góc tối, rất dễ cho quái vật ẩn nấp.",
    "気を付けて進まないと。": "Phải cẩn thận tiến lên phía trước mới được.",
    "ガァァァーー！": "Gà ầ ầ ầ ầ!",
    "ガァァァーーっ！": "Gà ầ ầ ầ ầ!",
    "ガ……ぁ……。": "Gà... à...",
    "……うん。": "...Ừm.",
    "やっぱり出現する魔物は問題なく倒せる程度の強さだな。": "Quả nhiên quái vật xuất hiện ở đây chỉ mạnh ở mức mình đánh bại dễ dàng.",
    "時間はかかるだろうけれど、これなら攻略は大丈夫そうだ。": "Tuy sẽ mất một khoảng thời gian, nhưng thế này thì việc chinh phục hầm ngục hẳn là ổn thôi.",
    "……まぁ、魔物が全員「こういうタイプ」だったらの話だけど……。": "...Mà, đó là trong trường hợp quái vật con nào cũng thuộc 'loại này'...",
    "あれ～？": "Ơ kìa~?",
    "お兄さん、もう倒しちゃったのぉ？": "Anh trai đã hạ gục nó rồi sao~?",
    "っ！": "...!",
    "その子、すっごく強いはずなんだけどなぁ……。": "Con quái vật đó đáng lẽ ra phải rất mạnh mới đúng chứ...",
    "ここに来た人、大体その子が殺してたんだよ？": "Hầu như ai tới đây cũng đều bị con quái vật đó hạ gục đấy?",
    "それなのに一瞬で倒すなんてお兄さんすごいね♡": "Thế mà anh hạ nó trong một nốt nhạc, giỏi quá đi♡",
    "格好良い～♡": "Đẹp trai quá~♡",
    "（あぁ、これはまずい……）": "(Ái chà, thế này thì tệ rồi...)",
    "（モンスター娘が出てきてしまった……）": "(Monster Girl xuất hiện mất rồi...)",
    "ちなみに私はその子に比べるとぜ～んぜん弱いの。": "Nhân tiện thì em so với con quái vật đó yếu hơn nhiều lắm.",
    "きっとあなたと戦ったら一捻りで倒されちゃうよぉ？": "Nếu đấu với anh thì nhất định em sẽ bị đè bẹp trong một nốt nhạc mất~?",
    "だ・か・ら～……♡": "Vì·vậy·nên~...♡",
    "倒す前に、ちょっとだけ楽しいことしない？♡": "Trước khi đánh bại em, mình làm chút chuyện vui vẻ không?♡",
    "どうせいつでも倒せるんだから、": "Đằng nào thì anh cũng đánh bại em lúc nào chả được,",
    "せっかくなら私のこのえっちな身体、味見しちゃおーよ♡": "đã mất công tới đây thì nếm thử cơ thể dâm mát này của em đi nào♡",
    "ここって結構レベルの高いダンジョンだから、": "Ở đây là hầm ngục cấp độ tương đối cao,",
    "モンスター娘の質も全然違うんだよ？♡": "nên phẩm chất của Monster Girl cũng hoàn toàn khác biệt đấy nhé?♡",
    "えっちしたらどれだけ気持ちいいのかな～？♡": "Nếu làm tình thì sẽ sướng đến mức nào nhỉ~?♡",
    "くすくすくす……♡": "Khúc khích khúc khích...♡",
    "（あからさまな誘惑……。": "(Lại là màn quyến rũ lộ liễu...",
    "精液を搾り取ってレベルをドレインするつもりだ……）": "rút cạn tinh dịch rồi hút sạch cấp độ của mình...)",
    "（見た目は可愛いが、話に乗れば絶対に痛い目を見る……。": "(Vẻ ngoài tuy đáng yêu, nhưng nếu cắn câu thì nhất định sẽ nhận kết đắng...",
    "凄まじい快楽で篭絡されるんだ……っ）": "Mình sẽ bị khoái cảm khủng khiếp khuất phục mất...)",
    "（今すぐ倒すべきなんだ……っ。": "(Phải đánh bại cô ta ngay lập tức...",
    "絶対に……そうに決まってる……っ）": "Nhất định... chắc chắn là phải làm thế...)",
    "（……なのに……っ！）": "(...Thế mà...!)",
    "ちょうどお兄さんはソロだから仲間に恥ずかしいところを": "Anh trai lại đang đi một mình nên không sợ bị đồng đội nhìn thấy",
    "見られる心配も……。": "những cảnh tượng xấu hổ đâu...",
    "……って、あれ……？": "...Ơ, cái gì cơ...?",
    "あのー……お兄さん……？": "Xin lỗi... anh trai ơi...?",
    "どうして、まだ何もしてないのに勃起してるの……？♡": "Tại sao em còn chưa làm gì mà anh đã cứng ngắc thế kia...?:♡",
    "……っ。": "...!",
    "えぇ～……♡　なになに、どうしちゃったの？♡": "Hê~...♡ Gì thế gì thế, anh làm sao vậy?♡",
    "魅了の魔法なんてまだ使ってないよ……？♡": "Em còn chưa dùng tới phép quyến rũ đâu đấy...?♡",
    "もしかして……モンスター娘に迫られただけで、": "Chẳng lẽ... mới chỉ bị Monster Girl tiếp cận thôi",
    "すっごく期待しちゃってるの？♡": "mà anh đã mong chờ lắm rồi sao?♡",
    "……そ、そんなこと……っ。": "...K, không có chuyện đó đâu...!",
    "あははっ♡　顔真っ赤～♡": "A ha ha♡ Mặt đỏ gay lên rồi kìa~♡",
    "お兄さん可愛い～♡": "Anh trai đáng yêu quá~♡",
    "それじゃあお兄さんのご希望通り、": "Thế thì đúng như nguyện vọng của anh trai,",
    "念入りに搾ってあげないとね……♡": "em phải vắt thật kỹ càng mới được...♡",
    "や、やめっ、うわぁぁっ！": "D, dừng lại, ứ waaa!"
}

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

translated_count = 0

for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for cmd in ev['list']:
            code = cmd.get('code')
            if code == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if txt in DIALOGUE_DICT:
                        cmd['parameters'][0] = DIALOGUE_DICT[txt]
                        translated_count += 1
                    else:
                        clean_t = txt.replace('　', ' ').strip()
                        if clean_t in DIALOGUE_DICT:
                            cmd['parameters'][0] = DIALOGUE_DICT[clean_t]
                            translated_count += 1

print(f"Translated {translated_count} Japanese dialogue lines in CommonEvents.json!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(ce, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced master translated CommonEvents.json to patch-release and test game!")
