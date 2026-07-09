#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考262: 高度計規正（QNH/標準気圧・遷移高度・巡航高度方式）の資料空欄穴埋め
解の一意性検証スクリプト

規則:
- 規則1: 規正値1hPaの変化 = 指示高度約30ft（規正値を上げると指示は上がる）。真高度は不変
- 規則2: QNH規正 → 海抜高度を指示。標準気圧1013hPa規正の指示をFLで表す（FL = 指示高度÷100）
- 規則3: 遷移高度14,000ft。以下はQNH、超はQNE(1013)
- 規則4: 半円周方式: 磁針路0°〜179° → 奇数FL、180°〜359° → 偶数FL
"""

FT_PER_HPA = 30
STD = 1013
TA = 14000  # 遷移高度


def indicated_on_ground(elev_ft, qnh, setting):
    """駐機中（真高度=標高）で規正値settingとしたときの指示高度"""
    return elev_ft + (setting - qnh) * FT_PER_HPA


def true_alt_of_fl(fl, qnh):
    """標準気圧規正でFLを維持したときの海抜高度（真高度）"""
    return fl * 100 - (STD - qnh) * FT_PER_HPA


def is_valid_fl_for_course(fl, course):
    """半円周方式: 千の位（FL/10）の偶奇で判定"""
    thousands = fl // 10
    if 0 <= course < 180:
        return thousands % 2 == 1
    return thousands % 2 == 0


# ========== 問1 ==========
def solve_q1():
    elev_a, qnh = 400, 998
    course = 255
    fl_range = range(150, 181, 10)  # FL150〜FL180
    obstacle = 12000

    a = indicated_on_ground(elev_a, qnh, STD)          # (ア)
    valid = [fl for fl in fl_range if is_valid_fl_for_course(fl, course)]
    b = min(valid)                                      # (イ) 最も低い適合FL
    c = true_alt_of_fl(b, qnh)                          # (ウ)
    d = c - obstacle                                    # (エ)
    return a, b, c, d


# ========== 問2 ==========
def solve_q2():
    qnh = 976
    course = 85
    obstacle = 13600
    buffer = 2000

    a = true_alt_of_fl(150, qnh)                        # (ア) FL150の海抜高度
    # (イ) 転移レベル: 海抜高度がTA以上となる最低のFL（1,000ft刻み）
    fl = 100
    while true_alt_of_fl(fl, qnh) < TA:
        fl += 10
    b = fl
    # (ウ) 最低使用可能FL: 海抜 >= 障害物+2,000ft かつ 方式適合 かつ 転移レベル以上
    need = obstacle + buffer
    fl = b
    while not (true_alt_of_fl(fl, qnh) >= need and is_valid_fl_for_course(fl, course)):
        fl += 10
    c = fl
    d = true_alt_of_fl(c, qnh)                          # (エ) (ウ)でQNH規正時の指示=海抜高度
    return a, b, c, d


def check_unique(name, options, correct_key):
    """選択肢中、計算結果と完全一致するものが唯一であることを確認"""
    matches = [k for k, v in options.items() if v == options[correct_key]]
    assert matches == [correct_key], f"{name}: 一致選択肢が{matches}"


if __name__ == "__main__":
    a1, b1, c1, d1 = solve_q1()
    print(f"問1: (ア)={a1}ft (イ)=FL{b1} (ウ)={c1}ft (エ)={d1}ft")
    assert (a1, b1, c1, d1) == (850, 160, 15550, 3550)

    # 問1 誤答選択肢（それぞれ特徴的な単一エラーに基づく内部整合な組）
    q1_opts = {
        "correct":  (850, 160, 15550, 3550),
        "reversed": (-50, 160, 16450, 4450),   # 補正方向の逆転
        "oddeven":  (850, 150, 14550, 2550),   # 奇数偶数の取り違え(FL150)
        "nocorr":   (400, 160, 16000, 4000),   # 気圧差補正なし
        "noelev":   (450, 160, 15550, 3550),   # (ア)で標高加算忘れ
    }
    check_unique("問1", q1_opts, "correct")
    # 誤答組の検算
    assert q1_opts["oddeven"][2] == true_alt_of_fl(150, 998) == 14550
    assert q1_opts["reversed"][0] == 400 - (STD - 998) * FT_PER_HPA

    a2, b2, c2, d2 = solve_q2()
    print(f"問2: (ア)={a2}ft (イ)=FL{b2} (ウ)=FL{c2} (エ)={d2}ft")
    assert (a2, b2, c2, d2) == (13890, 160, 170, 15890)
    # FL160が転移レベル: FL150は13,890 < 14,000、FL160は14,890 >= 14,000
    assert true_alt_of_fl(150, 976) == 13890 < TA <= true_alt_of_fl(160, 976) == 14890
    # FL170が最低使用可能: 奇数でFL150は13,890 < 15,600、FL170は15,890 >= 15,600
    assert true_alt_of_fl(170, 976) == 15890 >= 15600

    # 問2 誤答選択肢
    q2_opts = {
        "correct":  (13890, 160, 170, 15890),
        "reversed": (16110, 140, 150, 16110),  # 補正符号の逆転(+1,110ft)→FL140が転移レベル
        "nocorr":   (15000, 140, 170, 17000),  # 補正なし(FL=海抜と誤解)
        "nobuffer": (13890, 160, 150, 13890),  # 2,000ft加算と転移レベル制約の見落とし
        "oddeven":  (13890, 160, 180, 16890),  # 偶数FLを選ぶ誤り(FL160不足→FL180)
    }
    check_unique("問2", q2_opts, "correct")
    assert len(set(q2_opts.values())) == 5 and len(set(q1_opts.values())) == 5
    # 誤答組の検算
    assert 15000 + (STD - 976) * FT_PER_HPA == 16110
    assert true_alt_of_fl(180, 976) == 16890

    print("検証OK: 問1・問2とも唯一解を確認")
