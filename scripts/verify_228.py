# -*- coding: utf-8 -*-
"""
航大思考228 検証スクリプト
問1: 市立図書館 地区別・分野別 貸出冊数報告書（4地区×3分野＋合計）の穴埋め
問2: 製造会社 四半期別・製品別 売上高報告書（4四半期×3製品＋合計）の穴埋め
情報量の多い表（クロス集計表）から、文章中の条件で空欄を確定する。
"""


def verify_q1():
    """問1: 図書館 地区別・分野別 貸出冊数表の一意性検証"""
    # 確定値（表に提示される値）
    # 行: 東, 西, 南, 北   列: 文学, 実用, 児童, 合計
    higashi = {"文学": 320, "実用": 180, "児童": 150, "合計": 650}
    nishi   = {"文学": 280, "実用": 220, "児童": 200, "合計": 700}
    minami  = {"文学": 240, "実用": 160}            # 児童=ア, 合計=550(表)
    kita    = {"実用": 200, "児童": 180}            # 文学=イ, 合計=ウ

    minami_total = 550          # 表に提示
    bungaku_total = 1140        # 文学列の合計（文章/表で提示）
    grand_total = 2580          # 総合計（文章で提示）

    # ア: 南地区の児童 = 南合計 - 南文学 - 南実用
    a = minami_total - minami["文学"] - minami["実用"]
    # イ: 北地区の文学 = 文学列合計 - 東 - 西 - 南
    b = bungaku_total - higashi["文学"] - nishi["文学"] - minami["文学"]
    # ウ: 北地区の合計 = 北文学(イ) + 北実用 + 北児童
    c = b + kita["実用"] + kita["児童"]

    # 検算: 総合計 = 各地区合計の和
    assert higashi["合計"] + nishi["合計"] + minami_total + c == grand_total, "総合計が一致しない"
    # 検算: ウは総合計からも導ける
    assert grand_total - higashi["合計"] - nishi["合計"] - minami_total == c

    options = {
        1: (150, 280, 660),
        2: (160, 300, 680),
        3: (150, 320, 700),
        4: (150, 300, 680),   # 正解
        5: (130, 300, 660),
    }
    correct = (a, b, c)
    matches = [k for k, v in options.items() if v == correct]
    assert correct == (150, 300, 680), f"想定解と不一致: {correct}"
    assert matches == [4], f"一意でない/位置誤り: {matches}"
    print(f"問1: ア={a}, イ={b}, ウ={c} -> 正解(4)  一意性OK")


def verify_q2():
    """問2: 製造会社 四半期別・製品別 売上高表の一意性検証（連鎖推論）"""
    # 行: Q1,Q2,Q3,Q4   列: X,Y,Z,合計（単位: 万円）
    q1 = {"X": 1500, "Y": 1200, "Z": 900, "計": 3600}
    q2 = {"X": 1650, "Y": 1140, "Z": 900, "計": 3690}
    q3 = {"Y": 1260, "Z": 990, "計": 4050}   # X=ア
    q4 = {"X": 1980, "計": 4200}             # Y=イ, Z=ウ

    # ア: Q3のX = Q1のX の1.2倍
    a = int(q1["X"] * 1.2)
    assert a == q3["計"] - q3["Y"] - q3["Z"], "Q3の表計と不整合"
    # イ: Q4のY = Q4合計の30%
    b = int(q4["計"] * 0.30)
    # ウ: Q4のZ = Q4合計 - Q4のX - Q4のY
    c = q4["計"] - q4["X"] - b

    # 年間合計による交差検算
    x_year = q1["X"] + q2["X"] + a + q4["X"]
    y_year = q1["Y"] + q2["Y"] + q3["Y"] + b
    z_year = q1["Z"] + q2["Z"] + q3["Z"] + c
    grand = q1["計"] + q2["計"] + q3["計"] + q4["計"]
    assert x_year == 6930 and y_year == 4860 and z_year == 3750
    assert x_year + y_year + z_year == grand == 15540, "年間総計が不一致"

    options = {
        1: (1980, 1260, 960),
        2: (1800, 1290, 930),
        3: (1980, 1260, 990),
        4: (1800, 1260, 1140),
        5: (1800, 1260, 960),   # 正解
    }
    correct = (a, b, c)
    matches = [k for k, v in options.items() if v == correct]
    assert correct == (1800, 1260, 960), f"想定解と不一致: {correct}"
    assert matches == [5], f"一意でない/位置誤り: {matches}"
    print(f"問2: ア={a}, イ={b}, ウ={c} -> 正解(5)  一意性OK")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証パス")
