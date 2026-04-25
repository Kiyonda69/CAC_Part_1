"""
航大思考119: 箱ひげ図の資料読取問題（2問1セット）
- 問1: 4工場の製品重量の箱ひげ図から正しい記述を選ぶ
- 問2: 5科目のテスト得点の箱ひげ図から正しい記述の組合せを選ぶ
"""


def verify_q1():
    """問1: 4工場の製品重量データの箱ひげ図"""
    factories = {
        "A": {"min": 42, "q1": 46, "med": 50, "q3": 54, "max": 58},
        "B": {"min": 44, "q1": 49, "med": 53, "q3": 57, "max": 62},
        "C": {"min": 40, "q1": 45, "med": 52, "q3": 58, "max": 64},
        "D": {"min": 46, "q1": 50, "med": 54, "q3": 56, "max": 60},
    }

    iqr = {k: v["q3"] - v["q1"] for k, v in factories.items()}
    rng = {k: v["max"] - v["min"] for k, v in factories.items()}

    statements = []

    # (1) 四分位範囲が最も小さいのはD工場
    smallest_iqr = min(iqr, key=iqr.get)
    s1 = (smallest_iqr == "D")
    statements.append(("(1) IQR最小=D工場", s1))

    # (2) 最大値が最も大きいのはB工場
    largest_max = max(factories, key=lambda k: factories[k]["max"])
    s2 = (largest_max == "B")
    statements.append(("(2) 最大値最大=B工場", s2))

    # (3) A工場のすべての日において、重量は55g以下
    s3 = (factories["A"]["max"] <= 55)
    statements.append(("(3) A工場すべて55g以下", s3))

    # (4) D工場の中央値はC工場の中央値より3g大きい
    diff = factories["D"]["med"] - factories["C"]["med"]
    s4 = (diff == 3)
    statements.append(("(4) D中央値-C中央値=3", s4))

    # (5) B工場の範囲はC工場の範囲より大きい
    s5 = (rng["B"] > rng["C"])
    statements.append(("(5) B範囲>C範囲", s5))

    print("=== 問1: 各工場の統計量 ===")
    for k, v in factories.items():
        print(f"  {k}: Min={v['min']}, Q1={v['q1']}, Med={v['med']}, Q3={v['q3']}, Max={v['max']}, IQR={iqr[k]}, Range={rng[k]}")

    print("\n=== 問1: 各記述の真偽 ===")
    correct_count = 0
    correct_idx = None
    for i, (desc, val) in enumerate(statements, 1):
        mark = "○" if val else "×"
        print(f"  {desc}: {mark}")
        if val:
            correct_count += 1
            correct_idx = i

    assert correct_count == 1, f"問1: 正解が{correct_count}個 (想定: 1個)"
    assert correct_idx == 1, f"問1: 正解番号={correct_idx} (想定: 1)"
    print(f"\n問1 正解: ({correct_idx}) ✓")
    return correct_idx


def verify_q2():
    """問2: 5科目のテスト得点データの箱ひげ図"""
    subjects = {
        "国語": {"min": 30, "q1": 50, "med": 60, "q3": 72, "max": 90},
        "数学": {"min": 20, "q1": 42, "med": 58, "q3": 78, "max": 98},
        "英語": {"min": 35, "q1": 55, "med": 65, "q3": 75, "max": 92},
        "理科": {"min": 25, "q1": 48, "med": 63, "q3": 74, "max": 95},
        "社会": {"min": 40, "q1": 58, "med": 68, "q3": 80, "max": 95},
    }

    iqr = {k: v["q3"] - v["q1"] for k, v in subjects.items()}

    # ア．5科目の中で、中央値が最も高いのは数学である
    highest_med = max(subjects, key=lambda k: subjects[k]["med"])
    a = (highest_med == "数学")

    # イ．数学の四分位範囲は、英語の四分位範囲の2倍以上である
    b = (iqr["数学"] >= 2 * iqr["英語"])

    # ウ．5科目の中で、最大値が最も高いのは数学である
    highest_max = max(subjects, key=lambda k: subjects[k]["max"])
    c = (highest_max == "数学")

    # エ．国語の第3四分位数は、理科の第3四分位数より小さい
    d = (subjects["国語"]["q3"] < subjects["理科"]["q3"])

    print("\n=== 問2: 各科目の統計量 ===")
    for k, v in subjects.items():
        print(f"  {k}: Min={v['min']}, Q1={v['q1']}, Med={v['med']}, Q3={v['q3']}, Max={v['max']}, IQR={iqr[k]}")

    print(f"\n=== 問2: 各記述の真偽 ===")
    print(f"  ア．中央値が最も高いのは数学: {'○' if a else '×'} (中央値最大={highest_med})")
    print(f"  イ．数学IQR≧2×英語IQR: {'○' if b else '×'} (数学IQR={iqr['数学']}, 英語IQR={iqr['英語']}, 比={iqr['数学']/iqr['英語']:.2f})")
    print(f"  ウ．最大値が最も高いのは数学: {'○' if c else '×'} (最大値最大={highest_max})")
    print(f"  エ．国語Q3<理科Q3: {'○' if d else '×'} (国語Q3={subjects['国語']['q3']}, 理科Q3={subjects['理科']['q3']})")

    correct_set = set()
    if a: correct_set.add("ア")
    if b: correct_set.add("イ")
    if c: correct_set.add("ウ")
    if d: correct_set.add("エ")

    options = {
        1: {"ア", "ウ"},
        2: {"ア", "エ"},
        3: {"イ", "ウ"},
        4: {"イ", "エ"},
        5: {"ウ", "エ"},
    }

    print(f"\n  正しい記述の集合: {sorted(correct_set)}")

    matching = [n for n, s in options.items() if s == correct_set]
    assert len(matching) == 1, f"問2: マッチする選択肢が{len(matching)}個 (想定: 1個)"
    assert matching[0] == 5, f"問2: 正解番号={matching[0]} (想定: 5)"
    print(f"\n問2 正解: ({matching[0]}) ✓")
    return matching[0]


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    print(f"\n=== 検証完了: 問1={q1}, 問2={q2} ===")
