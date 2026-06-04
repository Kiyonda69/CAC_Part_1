"""
航大思考198 検証スクリプト
資料解釈問題 - 読解力重視
"""


def verify_q1():
    """
    問1: スポーツクラブ年次報告書
    - 全会員1,800名（前年度1,500名から20%増）
    - 個人会員: 全会員の45% = 810名
    - 家族会員: 360名
    - シニア会員 = 学生会員 × 2
    - 残り = 1800 - 810 - 360 = 630
      → シニア + 学生 = 630, シニア = 2×学生
      → 学生 = 210, シニア = 420

    年会費:
    - 個人: 72,000円
    - 家族: 108,000円
    - シニア: 48,000円
    - 学生: 36,000円
    """
    total_members = 1800
    assert total_members == int(1500 * 1.2), "前年度比20%増の検証"

    individual = int(total_members * 0.45)
    family = 360
    remaining = total_members - individual - family

    # シニア = 学生 × 2
    student = remaining // 3
    senior = student * 2

    assert individual == 810
    assert family == 360
    assert student == 210
    assert senior == 420
    assert individual + family + senior + student == total_members

    revenue = (individual * 72000 + family * 108000
               + senior * 48000 + student * 36000)

    print(f"問1 計算:")
    print(f"  個人: {individual}名 × 72,000円 = {individual * 72000:,}円")
    print(f"  家族: {family}名 × 108,000円 = {family * 108000:,}円")
    print(f"  シニア: {senior}名 × 48,000円 = {senior * 48000:,}円")
    print(f"  学生: {student}名 × 36,000円 = {student * 36000:,}円")
    print(f"  合計: {revenue:,}円")

    assert revenue == 124_920_000, f"想定: 124,920,000円, 実際: {revenue:,}円"
    print(f"  → 1億{revenue // 10000 - 10000:,}万円")
    print(f"  正解: (1) 1億2,492万円")
    return revenue


def verify_q2():
    """
    問2: 4工場 品質管理レポート
    各工場の生産数・不良率・稼働率・従業員数

    α: 50,000個, 1.5%, 90%, 120名
    β: 65,000個 (前月50,000の30%増), 1.0%, 95%, 140名
    γ: β-5,000=60,000個, αと同じ1.5%, 85%, 130名
    δ: (α+β+γ)×0.4=70,000個, 1.2%, 80%, 90名
    """
    alpha = {"prod": 50000, "defect": 0.015, "rate": 0.90, "emp": 120}
    beta_prev = 50000
    beta = {"prod": int(beta_prev * 1.3), "defect": 0.010,
            "rate": 0.95, "emp": 140}
    assert beta["prod"] == 65000

    gamma = {"prod": beta["prod"] - 5000, "defect": alpha["defect"],
             "rate": 0.85, "emp": 130}
    assert gamma["prod"] == 60000

    delta_prod = int((alpha["prod"] + beta["prod"] + gamma["prod"]) * 0.4)
    delta = {"prod": delta_prod, "defect": 0.012, "rate": 0.80, "emp": 90}
    assert delta["prod"] == 70000

    factories = {"α": alpha, "β": beta, "γ": gamma, "δ": delta}

    print(f"\n問2 工場データ:")
    for name, f in factories.items():
        defect_count = int(f["prod"] * f["defect"])
        per_emp = f["prod"] / f["emp"]
        print(f"  {name}: 生産{f['prod']:,}個, 不良{defect_count}個, "
              f"1人あたり{per_emp:.1f}個, 稼働率{f['rate'] * 100:.0f}%")

    # 記述ア: 1人あたり生産数最大はβ
    per_emp = {k: v["prod"] / v["emp"] for k, v in factories.items()}
    max_per_emp = max(per_emp, key=per_emp.get)
    a_correct = (max_per_emp == "β")
    print(f"\n記述ア (1人あたり最大はβ): {a_correct} "
          f"(実際の最大は{max_per_emp})")
    assert a_correct == False

    # 記述イ: 不良品最大はδ（生産数最大も）
    defects = {k: v["prod"] * v["defect"] for k, v in factories.items()}
    max_defect = max(defects, key=defects.get)
    max_prod = max(factories, key=lambda k: factories[k]["prod"])
    b_correct = (max_defect == "δ" and max_prod == "δ")
    print(f"記述イ (不良最大δ＝生産最大δ): {b_correct} "
          f"(不良最大{max_defect}, 生産最大{max_prod})")
    assert b_correct == False  # 不良最大はγ、生産最大はδ

    # 記述ウ: α-γ差 = δ/7
    diff = abs(alpha["prod"] - gamma["prod"])
    seventh = delta["prod"] / 7
    c_correct = (diff == seventh)
    print(f"記述ウ (|α-γ| = δ/7): {c_correct} "
          f"({diff} vs {seventh})")
    assert c_correct == True

    # 記述エ: 稼働率90%以上の2工場、合計11万超
    high_rate = [k for k, v in factories.items() if v["rate"] >= 0.90]
    total_high = sum(factories[k]["prod"] for k in high_rate)
    d_correct = (len(high_rate) == 2 and total_high > 110000)
    print(f"記述エ (90%以上の2工場が11万超): {d_correct} "
          f"(該当{high_rate}, 合計{total_high:,})")
    assert d_correct == True

    correct_set = []
    if a_correct: correct_set.append("ア")
    if b_correct: correct_set.append("イ")
    if c_correct: correct_set.append("ウ")
    if d_correct: correct_set.append("エ")
    print(f"\n正しい記述: {correct_set}")
    print(f"正解: (5) ウ・エ")
    assert correct_set == ["ウ", "エ"]


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n=== 検証完了: 問1=(1), 問2=(5) ===")
