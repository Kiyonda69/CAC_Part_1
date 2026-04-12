"""
航大思考108 解の一意性検証

問1: 市営プール利用状況調査 - 3空欄穴埋め
問2: T運輸会社 路線別運行実績月報 - 3空欄穴埋め
"""


def verify_q1():
    """問1: 市営プール利用状況調査"""
    # 報告文の条件
    # 総利用者数: 6,000人
    # 一般: 40%
    # 学生: 1,500人
    # 高齢者: 1,200人
    # 幼児: 600人
    # 団体: 残り
    # 一般の1人あたり料金: 500円
    # 団体の1人あたり料金: 一般の70%

    total = 6000
    ippan_ratio = 0.40
    gakusei = 1500
    koureisha = 1200
    youji = 600
    ippan_fee = 500
    dantai_fee_ratio = 0.70

    # ア: 一般の利用者数
    a = int(total * ippan_ratio)
    # イ: 団体の利用者数（残り）
    b = total - a - gakusei - koureisha - youji
    # ウ: 団体の1人あたり料金
    c = int(ippan_fee * dantai_fee_ratio)

    assert a == 2400, f"ア={a}"
    assert b == 300, f"イ={b}"
    assert c == 350, f"ウ={c}"

    # 割合検算
    assert abs(a/total - 0.40) < 1e-9
    assert abs(gakusei/total - 0.25) < 1e-9
    assert abs(koureisha/total - 0.20) < 1e-9
    assert abs(youji/total - 0.10) < 1e-9
    assert abs(b/total - 0.05) < 1e-9

    print(f"問1 正解: ア={a}人, イ={b}人, ウ={c}円")
    return (a, b, c)


def verify_q2():
    """問2: T運輸会社 路線別運行実績月報"""
    # 報告文の条件
    # 総便数: 400便
    # 総走行距離: 83,000km
    # 全路線共通燃費: 4.0 km/L
    # 路線A-B: 120便, 1便あたり150km, 総走行距離18,000km
    # 路線A-C: 80便, 1便あたり200km, 総走行距離16,000km
    # 路線B-D: ア便, 1便あたり250km, 総走行距離25,000km
    # 路線C-E: 60便, 1便あたりイkm, 総走行距離12,000km
    # 路線D-E: 40便, 1便あたり300km, 総走行距離?, 燃料消費量ウL

    total_flights = 400
    total_distance = 83000
    fuel_efficiency = 4.0

    # 既知データ
    ab_flights, ab_per, ab_total = 120, 150, 18000
    ac_flights, ac_per, ac_total = 80, 200, 16000
    bd_per, bd_total = 250, 25000
    ce_flights, ce_total = 60, 12000
    de_flights, de_per = 40, 300

    # ア: 路線B-Dの便数
    a = bd_total // bd_per
    assert a == 100, f"ア={a}"

    # 検算: 総便数
    assert ab_flights + ac_flights + a + ce_flights + de_flights == total_flights

    # イ: 路線C-Eの1便あたり走行距離
    b = ce_total // ce_flights
    assert b == 200, f"イ={b}"

    # 路線D-Eの総走行距離
    de_total = de_flights * de_per
    assert de_total == 12000

    # 検算: 総走行距離
    assert ab_total + ac_total + bd_total + ce_total + de_total == total_distance

    # ウ: 路線D-Eの燃料消費量
    c = int(de_total / fuel_efficiency)
    assert c == 3000, f"ウ={c}"

    print(f"問2 正解: ア={a}便, イ={b}km, ウ={c}L")
    return (a, b, c)


def check_q1_options():
    """問1選択肢の検証"""
    options = {
        1: (2400, 300, 300),   # 誤: 団体料金を一般と混同(×1.0ではなく×0.6)
        2: (2400, 400, 350),   # 誤: 団体人数計算ミス
        3: (2400, 300, 350),   # 正解
        4: (2000, 300, 350),   # 誤: 33.3%で計算
        5: (2400, 300, 250),   # 誤: 50%で計算
    }
    correct = verify_q1()
    assert options[3] == correct, f"選択肢(3)が正解と一致しない: {options[3]} vs {correct}"
    # 他の選択肢が全て異なることを確認
    seen = set()
    for k, v in options.items():
        assert v not in seen, f"選択肢の重複: {k}"
        seen.add(v)
    print("問1選択肢OK（正解=(3)）")


def check_q2_options():
    """問2選択肢の検証"""
    options = {
        1: (125, 200, 3000),   # 誤: 総便数から差し引く誤算
        2: (100, 200, 2400),   # 誤: 燃費5.0で計算
        3: (100, 150, 3000),   # 誤: 他路線との混同
        4: (100, 200, 4000),   # 誤: 燃費3.0で計算
        5: (100, 200, 3000),   # 正解
    }
    correct = verify_q2()
    assert options[5] == correct, f"選択肢(5)が正解と一致しない: {options[5]} vs {correct}"
    seen = set()
    for k, v in options.items():
        assert v not in seen, f"選択肢の重複: {k}"
        seen.add(v)
    print("問2選択肢OK（正解=(5)）")


if __name__ == "__main__":
    check_q1_options()
    check_q2_options()
    print("\nすべての検証に合格しました。")
