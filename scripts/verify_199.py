"""
航大思考199 検証スクリプト
- 問1: 図書館年次報告書から4区分の登録者数を逆算し、年間総貸出冊数を計算
- 問2: 4工場の業績レポートを読み、4記述ア〜エの正誤判定で正しい組合せを選ぶ
"""


def verify_q1():
    """問1: 年間総貸出冊数の計算と選択肢検証"""
    total = 5000
    children = int(total * 0.20)
    students = int(children * 1.5)
    remaining = total - children - students
    # 高齢者 = 成人 × 1/4, 成人 + 高齢者 = remaining
    # 成人 × 5/4 = remaining → 成人 = remaining × 4/5
    adults = remaining * 4 // 5
    seniors = remaining - adults

    assert children == 1000, f"children={children}"
    assert students == 1500, f"students={students}"
    assert adults == 2000, f"adults={adults}"
    assert seniors == 500, f"seniors={seniors}"
    assert adults + seniors == remaining
    assert seniors * 4 == adults

    loans = children * 24 + students * 18 + adults * 36 + seniors * 48
    assert loans == 147000, f"loans={loans}"
    print(f"問1 正解: {loans:,}冊")

    # 罠の検証
    # (1) 児童を25%と誤読
    c1 = int(total * 0.25)
    s1 = int(c1 * 1.5)
    rem1 = total - c1 - s1
    a1 = rem1 * 4 // 5
    sen1 = rem1 - a1
    t1 = c1 * 24 + s1 * 18 + a1 * 36 + sen1 * 48
    print(f"  (1) 児童25%誤読: {t1:,}冊")

    # (2) 児童1人24冊を20冊と誤読
    t2 = children * 20 + students * 18 + adults * 36 + seniors * 48
    print(f"  (2) 児童20冊誤読: {t2:,}冊")

    # (3) 正解
    print(f"  (3) 正解: {loans:,}冊")

    # (4) 高齢者を成人の1/3と誤読
    # 成人 + 成人/3 = 2500 → 成人 × 4/3 = 2500 → 成人 = 1875、高齢者 = 625
    a4 = remaining * 3 // 4
    sen4 = remaining - a4
    t4 = children * 24 + students * 18 + a4 * 36 + sen4 * 48
    print(f"  (4) 高齢者1/3誤読: 成人{a4}人 高齢者{sen4}人 → {t4:,}冊")

    # (5) 学生を児童と同人数と誤読
    s5 = children
    rem5 = total - children - s5
    a5 = rem5 * 4 // 5
    sen5 = rem5 - a5
    t5 = children * 24 + s5 * 18 + a5 * 36 + sen5 * 48
    print(f"  (5) 学生=児童誤読: 学生{s5}人 成人{a5}人 高齢者{sen5}人 → {t5:,}冊")

    # 選択肢が一意であることを確認
    options = [t1, t2, loans, t4, t5]
    assert len(set(options)) == 5, f"選択肢に重複あり: {options}"
    print(f"  選択肢5つ: {options}")
    return loans


def verify_q2():
    """問2: 4工場の業績レポートから4記述の正誤判定"""
    A = {"production": 8000, "defect": 120, "operation_rate": 92, "employees": 80}
    B = {"production": int(A["production"] * 1.25), "defect": 200, "operation_rate": 88, "employees": 100}
    C = {"production": 12000, "defect": int(12000 * 0.015), "operation_rate": 78, "employees": 150}
    D = {"production": 12000 - 3000, "defect": 135, "operation_rate": A["operation_rate"], "employees": B["employees"]}

    assert B["production"] == 10000
    assert C["defect"] == 180
    assert D["production"] == 9000
    assert D["operation_rate"] == 92
    assert D["employees"] == 100
    print(f"A: {A}")
    print(f"B: {B}")
    print(f"C: {C}")
    print(f"D: {D}")

    # ア. 従業員1人あたりの月間生産数が最も多いのはA工場である
    per_employee = {k: v["production"] / v["employees"] for k, v in [("A", A), ("B", B), ("C", C), ("D", D)]}
    print(f"  1人あたり生産: {per_employee}")
    # Aは100、Bも100 → 「Aである（のみ）」は誤
    a_unique_max = per_employee["A"] > max(per_employee[k] for k in ["B", "C", "D"])
    assert not a_unique_max
    statement_a = False  # 誤

    # イ. 不良品が最も多い工場はB工場である
    defects = {"A": A["defect"], "B": B["defect"], "C": C["defect"], "D": D["defect"]}
    print(f"  不良品数: {defects}")
    statement_b = max(defects, key=defects.get) == "B" and list(defects.values()).count(max(defects.values())) == 1
    assert statement_b

    # ウ. 4工場の総生産数は40,000個を超える
    total_prod = A["production"] + B["production"] + C["production"] + D["production"]
    print(f"  総生産: {total_prod}")
    statement_c = total_prod > 40000  # 39000 → 誤
    assert not statement_c

    # エ. 稼働率の平均は87%以上である
    avg_op = (A["operation_rate"] + B["operation_rate"] + C["operation_rate"] + D["operation_rate"]) / 4
    print(f"  稼働率平均: {avg_op}")
    statement_d = avg_op >= 87  # 87.5 → 正
    assert statement_d

    results = {"ア": statement_a, "イ": statement_b, "ウ": statement_c, "エ": statement_d}
    print(f"  記述正誤: {results}")

    correct_set = set(k for k, v in results.items() if v)
    print(f"  正しい記述: {correct_set}")

    # 選択肢
    # (1) イとエ ← 正解
    # (2) アとイ
    # (3) ウとエ
    # (4) アとエ
    # (5) アとウ
    options = {
        1: {"イ", "エ"},
        2: {"ア", "イ"},
        3: {"ウ", "エ"},
        4: {"ア", "エ"},
        5: {"ア", "ウ"},
    }
    matched = [k for k, v in options.items() if v == correct_set]
    assert len(matched) == 1
    print(f"  正解: ({matched[0]})")
    return matched[0]


if __name__ == "__main__":
    print("=== 問1検証 ===")
    verify_q1()
    print()
    print("=== 問2検証 ===")
    verify_q2()
    print()
    print("両問とも一意解を確認")
