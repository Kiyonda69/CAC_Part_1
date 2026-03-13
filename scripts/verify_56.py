"""
セット56 解の一意性検証スクリプト
テーマ: 合板用素材の入荷量・消費量・在庫量データ（資料読み取り）
"""

def verify_q1():
    """問1: 前月在庫量の逆算と差の計算"""
    # 4月のデータ
    # 在庫量 = 前月の在庫量 + 今月の入荷量 - 今月の消費量
    # → 前月の在庫量 = 今月の在庫量 - 今月の入荷量 + 今月の消費量

    data = {
        "全国":   {"入荷": 987, "消費": 915, "在庫": 1847},
        "北海道": {"入荷": 15,  "消費": 68,  "在庫": 425},
        "岩手":   {"入荷": 26,  "消費": 22,  "在庫": 78},
        "埼玉":   {"入荷": 48,  "消費": 43,  "在庫": 115},
        "奈良":   {"入荷": 12,  "消費": 14,  "在庫": 18},
        "岡山":   {"入荷": 134, "消費": 118, "在庫": 28},
        "熊本":   {"入荷": 21,  "消費": 19,  "在庫": 52},
    }

    prev_stocks = {}
    for pref, d in data.items():
        prev_stocks[pref] = d["在庫"] - d["入荷"] + d["消費"]

    answer = prev_stocks["埼玉"] - prev_stocks["奈良"]
    assert answer == 90, f"問1の答えが90ではない: {answer}"
    print(f"問1: 埼玉3月在庫={prev_stocks['埼玉']}, 奈良3月在庫={prev_stocks['奈良']}, 差={answer}")
    print("問1: 正解 (4) 90千m³ ... OK")


def verify_q2():
    """問2: 4つの記述の正誤判定"""
    data = {
        "全国":   {"入荷": 987, "入荷差": 64,   "消費": 915, "消費差": -32,  "在庫": 1847},
        "北海道": {"入荷": 15,  "入荷差": -2,   "消費": 68,  "消費差": -3,   "在庫": 425},
        "岩手":   {"入荷": 26,  "入荷差": 5,    "消費": 22,  "消費差": 1,    "在庫": 78},
        "埼玉":   {"入荷": 48,  "入荷差": -7,   "消費": 43,  "消費差": 2,    "在庫": 115},
        "奈良":   {"入荷": 12,  "入荷差": 3,    "消費": 14,  "消費差": -1,   "在庫": 18},
        "岡山":   {"入荷": 134, "入荷差": 45,   "消費": 118, "消費差": -6,   "在庫": 28},
        "熊本":   {"入荷": 21,  "入荷差": -5,   "消費": 19,  "消費差": -2,   "在庫": 52},
    }

    # ア: 3月の全国消費量は950千m³を超える
    prev_cons_all = data["全国"]["消費"] - data["全国"]["消費差"]
    assert prev_cons_all == 947
    a_correct = prev_cons_all > 950
    assert a_correct == False, "アは誤りのはず"

    # イ: 3月→4月で在庫量が減少した道県は2つ
    decrease_count = 0
    for pref in ["北海道", "岩手", "埼玉", "奈良", "岡山", "熊本"]:
        if data[pref]["入荷"] < data[pref]["消費"]:
            decrease_count += 1
    assert decrease_count == 2
    b_correct = (decrease_count == 2)
    assert b_correct == True, "イは正しいはず"

    # ウ: 3月の岡山県の入荷量は90千m³未満
    prev_arrival_okayama = data["岡山"]["入荷"] - data["岡山"]["入荷差"]
    assert prev_arrival_okayama == 89
    c_correct = prev_arrival_okayama < 90
    assert c_correct == True, "ウは正しいはず"

    # エ: 3月の埼玉在庫は3月の奈良在庫の6倍超
    prev_stock_saitama = data["埼玉"]["在庫"] - data["埼玉"]["入荷"] + data["埼玉"]["消費"]
    prev_stock_nara = data["奈良"]["在庫"] - data["奈良"]["入荷"] + data["奈良"]["消費"]
    assert prev_stock_saitama == 110
    assert prev_stock_nara == 20
    d_correct = (prev_stock_saitama / prev_stock_nara) > 6
    assert d_correct == False, "エは誤りのはず"

    print(f"問2: ア={a_correct}, イ={b_correct}, ウ={c_correct}, エ={d_correct}")
    print("問2: 正解 (3) イ、ウ ... OK")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n全検証パス!")
