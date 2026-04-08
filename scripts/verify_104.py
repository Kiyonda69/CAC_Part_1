"""
航大思考104 検証スクリプト
箱ひげ図の読解問題（2問とも内容は無関連）

問1: 4つの市立図書館の貸出冊数 - 単一正解
問2: マラソン大会の年代別完走タイム - 記述組み合わせ
"""


def verify_q1():
    """問1: 図書館貸出冊数（標準難度）"""
    libraries = {
        "A": {"min": 20, "Q1": 35, "Med": 50, "Q3": 65, "Max": 90},
        "B": {"min": 15, "Q1": 30, "Med": 55, "Q3": 80, "Max": 110},
        "C": {"min": 25, "Q1": 45, "Med": 60, "Q3": 75, "Max": 100},
        "D": {"min": 10, "Q1": 25, "Med": 40, "Q3": 60, "Max": 85},
    }

    # 統計量を表示
    print("=== 問1: 図書館貸出冊数 ===")
    for name, d in libraries.items():
        rng = d["Max"] - d["min"]
        iqr = d["Q3"] - d["Q1"]
        print(
            f"{name}館: Min={d['min']}, Q1={d['Q1']}, Med={d['Med']}, "
            f"Q3={d['Q3']}, Max={d['Max']}, Range={rng}, IQR={iqr}"
        )

    # 各選択肢の真偽判定
    statements = {}

    # (1) 4つの図書館の中で、貸出冊数の四分位範囲が最も大きいのはC館である
    iqr_max = max(libraries.items(), key=lambda x: x[1]["Q3"] - x[1]["Q1"])
    statements[1] = (iqr_max[0] == "C", f"IQR最大={iqr_max[0]}")

    # (2) D館の貸出冊数は、調査期間中すべての日において60冊以下であった
    statements[2] = (
        libraries["D"]["Max"] <= 60,
        f"D館Max={libraries['D']['Max']}",
    )

    # (3) B館の貸出冊数の範囲は、A館の貸出冊数の範囲よりちょうど25冊大きい (★正解)
    range_B = libraries["B"]["Max"] - libraries["B"]["min"]
    range_A = libraries["A"]["Max"] - libraries["A"]["min"]
    statements[3] = (range_B - range_A == 25, f"B範囲={range_B}, A範囲={range_A}, 差={range_B - range_A}")

    # (4) A館の第3四分位数とC館の第1四分位数は等しい
    statements[4] = (
        libraries["A"]["Q3"] == libraries["C"]["Q1"],
        f"A_Q3={libraries['A']['Q3']}, C_Q1={libraries['C']['Q1']}",
    )

    # (5) 4つの図書館の中で、中央値が最も大きいのはB館である
    med_max = max(libraries.items(), key=lambda x: x[1]["Med"])
    statements[5] = (med_max[0] == "B", f"中央値最大={med_max[0]}")

    print("\n選択肢の真偽:")
    for k, (truth, detail) in statements.items():
        mark = "○正解" if truth else "×誤り"
        print(f"  ({k}) {mark}: {detail}")

    correct = [k for k, (t, _) in statements.items() if t]
    assert len(correct) == 1, f"正解が{len(correct)}個あります: {correct}"
    assert correct[0] == 3, f"正解は(3)であるべき: 実際={correct[0]}"
    print(f"\n問1 正解: ({correct[0]}) ← OK")
    return correct[0]


def verify_q2():
    """問2: マラソン年代別完走タイム（高難度）"""
    groups = {
        "20代": {"min": 180, "Q1": 210, "Med": 240, "Q3": 275, "Max": 320},
        "30代": {"min": 190, "Q1": 220, "Med": 255, "Q3": 290, "Max": 340},
        "40代": {"min": 200, "Q1": 235, "Med": 270, "Q3": 310, "Max": 360},
        "50代": {"min": 215, "Q1": 250, "Med": 290, "Q3": 330, "Max": 380},
        "60代": {"min": 240, "Q1": 275, "Med": 320, "Q3": 360, "Max": 420},
    }

    print("\n=== 問2: マラソン完走タイム ===")
    for name, d in groups.items():
        rng = d["Max"] - d["min"]
        iqr = d["Q3"] - d["Q1"]
        print(
            f"{name}: Min={d['min']}, Q1={d['Q1']}, Med={d['Med']}, "
            f"Q3={d['Q3']}, Max={d['Max']}, Range={rng}, IQR={iqr}"
        )

    # 4つの記述ア〜エの真偽
    descriptions = {}

    # ア: 中央値は年代が上がるにつれて単調に増加している
    medians = [groups[g]["Med"] for g in ["20代", "30代", "40代", "50代", "60代"]]
    descriptions["ア"] = (
        all(medians[i] < medians[i + 1] for i in range(4)),
        f"中央値: {medians}",
    )

    # イ: 60代の第1四分位数は20代の最大値より小さい
    descriptions["イ"] = (
        groups["60代"]["Q1"] < groups["20代"]["Max"],
        f"60代Q1={groups['60代']['Q1']}, 20代Max={groups['20代']['Max']}",
    )

    # ウ: 50代の四分位範囲は、20代の四分位範囲の1.5倍以上である
    iqr_50 = groups["50代"]["Q3"] - groups["50代"]["Q1"]
    iqr_20 = groups["20代"]["Q3"] - groups["20代"]["Q1"]
    descriptions["ウ"] = (
        iqr_50 >= 1.5 * iqr_20,
        f"50代IQR={iqr_50}, 20代IQR={iqr_20}, 比={iqr_50/iqr_20:.3f}",
    )

    # エ: 30代の中央値と40代の中央値の差は、40代の中央値と50代の中央値の差より大きい
    diff_30_40 = abs(groups["30代"]["Med"] - groups["40代"]["Med"])
    diff_40_50 = abs(groups["40代"]["Med"] - groups["50代"]["Med"])
    descriptions["エ"] = (
        diff_30_40 > diff_40_50,
        f"30-40差={diff_30_40}, 40-50差={diff_40_50}",
    )

    print("\n記述の真偽:")
    for k, (truth, detail) in descriptions.items():
        mark = "○正" if truth else "×誤"
        print(f"  {k}: {mark}: {detail}")

    correct_set = {k for k, (t, _) in descriptions.items() if t}
    print(f"\n正しい記述: {sorted(correct_set)}")

    # 選択肢
    options = {
        1: {"ア", "イ"},  # ★正解
        2: {"ア", "ウ"},
        3: {"イ", "エ"},
        4: {"ウ", "エ"},
        5: {"ア", "エ"},
    }

    print("\n選択肢の検討:")
    for k, opt in options.items():
        match = opt == correct_set
        mark = "○正解" if match else "×"
        print(f"  ({k}) {{{','.join(sorted(opt))}}}: {mark}")

    valid = [k for k, opt in options.items() if opt == correct_set]
    assert len(valid) == 1, f"正解が{len(valid)}個: {valid}"
    assert valid[0] == 1, f"正解は(1)であるべき: 実際={valid[0]}"
    print(f"\n問2 正解: ({valid[0]}) ← OK")
    return valid[0]


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    print("\n" + "=" * 40)
    print(f"航大思考104 検証完了: 問1=({q1}), 問2=({q2})")
