"""
セット118 解の一意性検証
- 問1: N地方5県の観光統計（2024年度）
- 問2: Y社3部門×3年度の業績データ
"""


def verify_q1():
    """問1: 観光統計穴埋め"""
    # 表データ
    rows = {
        "A": {"visitors": 1200, "stay": 300, "spend": 2400, "emp": 50},
        "B": {"visitors": 800, "stay": 320, "spend": 1800, "emp": 30},
        "C": {"visitors": 1500, "stay": 300, "spend": 1800, "emp": 60},
        "D": {"visitors": 600, "stay": 210, "spend": 1200, "emp": 20},
        "E": {"visitors": 900, "stay": 180, "spend": 1800, "emp": 40},
    }
    total_visitors = sum(r["visitors"] for r in rows.values())
    total_stay = sum(r["stay"] for r in rows.values())
    total_spend = sum(r["spend"] for r in rows.values())
    total_emp = sum(r["emp"] for r in rows.values())

    print(f"[Q1] 観光入込客数合計: {total_visitors}万人")
    print(f"[Q1] 宿泊客数合計: {total_stay}万人")
    print(f"[Q1] 観光消費額合計: {total_spend}億円")
    print(f"[Q1] 雇用者数合計: {total_emp}千人")

    assert total_visitors == 5000
    assert total_stay == 1310
    assert total_spend == 9000
    assert total_emp == 200

    # (ア) 観光入込客数合計 = 5,000
    a = total_visitors
    # (イ) 観光消費額が最も多い県 = A
    b = max(rows, key=lambda k: rows[k]["spend"])
    # (ウ) 宿泊率(宿泊客数/観光入込客数)が最も高い県 = B
    rates = {k: rows[k]["stay"] / rows[k]["visitors"] for k in rows}
    c = max(rates, key=rates.get)
    # 一意性確認
    sorted_rates = sorted(rates.values(), reverse=True)
    assert sorted_rates[0] != sorted_rates[1], f"宿泊率が一意でない: {rates}"
    # (エ) 雇用者1人あたり観光消費額 ≒ 9000億÷200千人 = 450万円
    # 9000億円 = 9000 * 10^8円, 200千人 = 200 * 10^3 人
    yen_per_emp = (total_spend * 1e8) / (total_emp * 1e3)
    d = round(yen_per_emp / 1e4)  # 万円
    print(f"[Q1] 1人あたり消費額: {yen_per_emp:.0f}円 = {d}万円")
    assert d == 450

    correct_answer = (a, b, c, d)
    print(f"[Q1] 空欄正解: ア={a}, イ={b}, ウ={c}, エ={d}")

    options = [
        (5000, "A", "B", 450),     # (1) 正解
        (5000, "C", "B", 450),     # (2) イ誤り
        (5000, "A", "D", 450),     # (3) ウ誤り
        (1310, "A", "B", 450),     # (4) ア誤り
        (5000, "A", "B", 45),      # (5) エ誤り
    ]
    correct_count = sum(1 for o in options if o == correct_answer)
    print(f"[Q1] 正解と一致するoption数: {correct_count}")
    assert correct_count == 1, f"解が一意でない: {correct_count}個"
    correct_idx = options.index(correct_answer) + 1
    print(f"[Q1] 正解番号: ({correct_idx})")
    assert correct_idx == 1
    return True


def verify_q2():
    """問2: 食品メーカー3部門×3年度"""
    data = {
        ("製造", 2023): {"sales": 1200, "cost": 900, "profit": 200, "emp": 600},
        ("製造", 2024): {"sales": 1300, "cost": 970, "profit": 220, "emp": 620},
        ("製造", 2025): {"sales": 1400, "cost": 1050, "profit": 230, "emp": 640},
        ("販売", 2023): {"sales": 800, "cost": 600, "profit": 100, "emp": 300},
        ("販売", 2024): {"sales": 850, "cost": 640, "profit": 110, "emp": 320},
        ("販売", 2025): {"sales": 900, "cost": 670, "profit": 130, "emp": 330},
        ("物流", 2023): {"sales": 500, "cost": 380, "profit": 60, "emp": 200},
        ("物流", 2024): {"sales": 540, "cost": 410, "profit": 65, "emp": 210},
        ("物流", 2025): {"sales": 600, "cost": 450, "profit": 75, "emp": 220},
    }

    # 全社売上(2023, 2025)
    total_sales_2023 = sum(data[(d, 2023)]["sales"] for d in ["製造", "販売", "物流"])
    total_sales_2025 = sum(data[(d, 2025)]["sales"] for d in ["製造", "販売", "物流"])
    total_emp_2023 = sum(data[(d, 2023)]["emp"] for d in ["製造", "販売", "物流"])
    total_emp_2025 = sum(data[(d, 2025)]["emp"] for d in ["製造", "販売", "物流"])
    print(f"[Q2] 2023年度全社売上: {total_sales_2023}億円")
    print(f"[Q2] 2025年度全社売上: {total_sales_2025}億円")
    print(f"[Q2] 2023年度全社従業員: {total_emp_2023}人")
    print(f"[Q2] 2025年度全社従業員: {total_emp_2025}人")

    assert total_sales_2023 == 2500
    assert total_sales_2025 == 2900
    assert total_emp_2023 == 1100
    assert total_emp_2025 == 1190

    # (ア) 2025年度全社売上高 = 2,900
    a = total_sales_2025
    # (イ) 2023→2025成長率(分母:2023): 16.0
    growth = (total_sales_2025 - total_sales_2023) / total_sales_2023 * 100
    b = round(growth, 1)
    print(f"[Q2] 成長率: {growth}% → {b}%")
    assert b == 16.0
    # (ウ) 2025年度の営業利益率(profit/sales)が最も高い部門
    profit_rate_2025 = {
        d: data[(d, 2025)]["profit"] / data[(d, 2025)]["sales"] * 100
        for d in ["製造", "販売", "物流"]
    }
    print(f"[Q2] 営業利益率2025: {profit_rate_2025}")
    c = max(profit_rate_2025, key=profit_rate_2025.get)
    rates_sorted = sorted(profit_rate_2025.values(), reverse=True)
    assert rates_sorted[0] != rates_sorted[1], "営業利益率が一意でない"
    # (エ) 2025年度に従業員1人あたり営業利益が最も高い部門
    profit_per_emp_2025 = {
        d: data[(d, 2025)]["profit"] / data[(d, 2025)]["emp"]
        for d in ["製造", "販売", "物流"]
    }
    # 億/人 → 万円/人 = 億/人 * 10000
    profit_per_emp_man = {d: v * 10000 for d, v in profit_per_emp_2025.items()}
    print(f"[Q2] 1人あたり営業利益(万円): {profit_per_emp_man}")
    d_dept = max(profit_per_emp_2025, key=profit_per_emp_2025.get)
    sorted_pe = sorted(profit_per_emp_2025.values(), reverse=True)
    assert sorted_pe[0] != sorted_pe[1], "1人あたり営業利益が一意でない"
    # 確認: 販売は130/330=0.3939億/人 = 約3,939万円
    expected_e = round(profit_per_emp_man[d_dept])
    print(f"[Q2] 最高1人あたり営業利益: {d_dept}部門 約{expected_e}万円")
    # (オ) 2025年度全社従業員数 = 1,190
    e = total_emp_2025

    correct_answer = (a, b, c, d_dept, e)
    print(f"[Q2] 空欄正解: ア={a}, イ={b}, ウ={c}, エ={d_dept}, オ={e}")
    assert correct_answer == (2900, 16.0, "製造", "販売", 1190)

    options = [
        (2500, 16.0, "製造", "販売", 1190),  # (1) ア誤り
        (2900, 13.8, "製造", "販売", 1190),  # (2) イ誤り
        (2900, 16.0, "販売", "販売", 1190),  # (3) ウ誤り
        (2900, 16.0, "製造", "販売", 90),    # (4) オ誤り
        (2900, 16.0, "製造", "販売", 1190),  # (5) 正解
    ]
    # トラップ値の妥当性検証
    # (2) イ=13.8: 130/2900*100 ≒ 13.8 (分母を2025にした誤り)
    trap_b = (total_sales_2025 - total_sales_2023) / total_sales_2025 * 100
    print(f"[Q2] イ誤りトラップ値(分母を2025年度): {round(trap_b, 1)}%")
    assert round(trap_b, 1) == 13.8

    # (4) オ=90: 増加数 = 1190-1100 = 90
    trap_e = total_emp_2025 - total_emp_2023
    print(f"[Q2] オ誤りトラップ値(従業員増加数): {trap_e}")
    assert trap_e == 90

    correct_count = sum(1 for o in options if o == correct_answer)
    print(f"[Q2] 正解と一致するoption数: {correct_count}")
    assert correct_count == 1, f"解が一意でない: {correct_count}個"
    correct_idx = options.index(correct_answer) + 1
    print(f"[Q2] 正解番号: ({correct_idx})")
    assert correct_idx == 5
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("セット118 検証開始")
    print("=" * 60)
    verify_q1()
    print()
    verify_q2()
    print()
    print("=" * 60)
    print("検証成功: 両問とも解が一意に確定")
    print("=" * 60)
