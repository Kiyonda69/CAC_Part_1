"""
航大思考209 検証スクリプト
問1: 物流路線の3ヶ月総利益が最大の路線を特定
問2: 複合評価ルールに基づく最高評価点の営業職員を特定
"""


def verify_q1():
    """問1: 3ヶ月総利益 = 輸送量合計 × 単価 - 固定費 × 3"""
    routes = {
        "A": {"vol": [20, 24, 22], "unit": 8, "fix": 30},
        "B": {"vol": [15, 18, 20], "unit": 10, "fix": 40},
        "C": {"vol": [22, 25, 28], "unit": 7, "fix": 25},
        "D": {"vol": [18, 20, 24], "unit": 9, "fix": 35},
        "E": {"vol": [12, 14, 16], "unit": 12, "fix": 20},
    }
    profits = {}
    for name, d in routes.items():
        total_vol = sum(d["vol"])
        revenue = total_vol * d["unit"]
        fix_total = d["fix"] * 3
        profits[name] = revenue - fix_total
    print("問1 路線別3ヶ月総利益:")
    for n, p in profits.items():
        print(f"  路線{n}: {p}千円")
    max_name = max(profits, key=profits.get)
    max_value = profits[max_name]
    tied = [n for n, v in profits.items() if v == max_value]
    assert len(tied) == 1, f"最大値が複数: {tied}"
    label_map = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    print(f"  最大: 路線{max_name} ({max_value}千円) → 選択肢({label_map[max_name]})")
    return label_map[max_name]


def verify_q2():
    """問2: 評価点 = 新規×5 + 継続×2 + 解約×(-3) + 条件付ボーナス・ペナルティ"""
    staff = {
        "A": {"new": 8, "cont": 12, "cancel": 3},
        "B": {"new": 6, "cont": 15, "cancel": 1},
        "C": {"new": 9, "cont": 14, "cancel": 2},
        "D": {"new": 4, "cont": 18, "cancel": 2},
        "E": {"new": 10, "cont": 8, "cancel": 4},
    }
    scores = {}
    for name, d in staff.items():
        s = d["new"] * 5 + d["cont"] * 2 + d["cancel"] * (-3)
        if d["cancel"] <= 2:
            s += 10
        if d["new"] <= 3:
            s -= 5
        scores[name] = s
    print("問2 営業職員別評価点:")
    for n, s in scores.items():
        print(f"  {n}さん: {s}点")
    max_name = max(scores, key=scores.get)
    max_value = scores[max_name]
    tied = [n for n, v in scores.items() if v == max_value]
    assert len(tied) == 1, f"最大値が複数: {tied}"
    label_map = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    print(f"  最大: {max_name}さん ({max_value}点) → 選択肢({label_map[max_name]})")
    return label_map[max_name]


if __name__ == "__main__":
    ans1 = verify_q1()
    ans2 = verify_q2()
    print(f"\n=== 正解 ===\n問1: ({ans1})\n問2: ({ans2})")
    assert ans1 == 4, "問1の正解位置が4でない"
    assert ans2 == 3, "問2の正解位置が3でない"
    print("✓ 検証完了 - 解の一意性確認")
