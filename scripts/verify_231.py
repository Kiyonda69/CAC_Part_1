# -*- coding: utf-8 -*-
"""航大思考231 検証スクリプト
問1: 売上集計表（販売数×単価＝売上, 構成比）の穴埋め → 商品Cの販売数ア
問2: 部門別損益表の穴埋め（連鎖推論）→ 全社営業利益率
"""


def verify_q1():
    """問1: 商品Cの販売数アの一意性を検証"""
    # 与えられた数値（空欄はNone）
    # 商品: 販売数, 単価, 売上高, 構成比(%)
    qty = {"A": 500, "B": 250, "C": None, "D": None, "E": 150}
    price = {"A": 800, "B": None, "C": 1400, "D": 1200, "E": 1600}
    sales = {"A": None, "B": 500000, "C": None, "D": 450000, "E": None}
    ratio = {"A": 16, "B": None, "C": None, "D": 18, "E": None}

    # 手順1: A売上 = 販売数 × 単価
    sales["A"] = qty["A"] * price["A"]            # 400,000
    # 手順2: A構成比16% → 総売上
    total = sales["A"] / (ratio["A"] / 100)        # 2,500,000
    # E売上 = 販売数 × 単価
    sales["E"] = qty["E"] * price["E"]             # 240,000
    # 手順3: C売上 = 総売上 − 他4商品の売上
    sales["C"] = total - sales["A"] - sales["B"] - sales["D"] - sales["E"]
    # 手順4: ア = C売上 ÷ C単価
    a = sales["C"] / price["C"]

    assert total == 2500000, total
    assert sales["C"] == 910000, sales["C"]
    assert a == int(a), a
    a = int(a)

    # 検算: 全構成比の合計が100%
    ratio["B"] = sales["B"] / total * 100
    ratio["C"] = sales["C"] / total * 100
    ratio["E"] = sales["E"] / total * 100
    s = ratio["A"] + ratio["B"] + ratio["C"] + ratio["D"] + ratio["E"]
    assert abs(s - 100) < 1e-9, s

    # 選択肢に正解が1つだけ含まれることを確認
    options = [600, 650, 627, 700, 580]
    assert options.count(a) == 1, options
    print("問1: ア =", a, "（販売数）")
    print("    総売上 =", int(total), " C売上 =", int(sales["C"]))
    print("    構成比 B/C/E =", round(ratio["B"], 1), round(ratio["C"], 1), round(ratio["E"], 1))
    print("    正解位置:", options.index(a) + 1)
    return a


def verify_q2():
    """問2: 全社営業利益率の一意性を検証
    関係式: 総利益=売上−原価, 営業利益=総利益−販管費, 利益率=営業利益/売上
    """
    # 部門: 売上, 原価, 総利益, 販管費, 営業利益（空欄None）
    rev = {"A": 5000, "B": 8000, "C": 6000, "D": None, "E": 4000}
    cost = {"A": 3000, "B": 5600, "C": None, "D": 4200, "E": 2800}
    gross = {"A": 2000, "B": 2400, "C": None, "D": None, "E": 1200}
    sga = {"A": 1200, "B": 1500, "C": 1400, "D": 1800, "E": None}
    op = {"A": 800, "B": 900, "C": 700, "D": 1000, "E": 500}

    # C: 総利益 = 営業利益 + 販管費 → 原価 = 売上 − 総利益
    gross["C"] = op["C"] + sga["C"]               # 2,100
    cost["C"] = rev["C"] - gross["C"]             # 3,900
    # D: 総利益 = 営業利益 + 販管費 → 売上 = 原価 + 総利益
    gross["D"] = op["D"] + sga["D"]               # 2,800
    rev["D"] = cost["D"] + gross["D"]             # 7,000
    # E: 販管費 = 総利益 − 営業利益
    sga["E"] = gross["E"] - op["E"]               # 700

    # 各部門の整合性チェック（総利益=売上−原価, 営業利益=総利益−販管費）
    for d in rev:
        assert gross[d] == rev[d] - cost[d], d
        assert op[d] == gross[d] - sga[d], d

    total_rev = sum(rev.values())                 # 30,000
    total_op = sum(op.values())                   # 3,900
    rate = total_op / total_rev * 100

    assert rev["D"] == 7000, rev["D"]
    assert total_rev == 30000, total_rev
    assert total_op == 3900, total_op
    assert abs(rate - 13) < 1e-9, rate

    # 参考: 各部門利益率の単純平均（重み付けと異なる概念）
    each = [op[d] / rev[d] * 100 for d in rev]
    naive = sum(each) / len(each)

    options = [11, 12, 14, 13, 13.5]
    rate_i = int(rate)
    assert options.count(rate_i) == 1, options
    print("問2: 全社営業利益率 =", rate_i, "%")
    print("    全社売上 =", total_rev, " 全社営業利益 =", total_op)
    print("    D売上 =", rev["D"], " C原価 =", cost["C"], " E販管費 =", sga["E"])
    print("    各部門率の単純平均 =", round(naive, 2), "%（トラップ）")
    print("    正解位置:", options.index(rate_i) + 1)
    return rate_i


if __name__ == "__main__":
    print("=== 航大思考231 検証 ===")
    verify_q1()
    print("-" * 30)
    verify_q2()
    print("=== 検証完了: 解は一意 ===")
