"""
verify_174.py - セット174: 情報量の多い資料穴埋め問題 検証スクリプト
問1: 6空港 × 3ヶ月 × 2指標 = 36セル
問2: 5路線 × 4四半期 × 3指標 = 60セル

検証内容:
  - 表データの行・列合計の整合性
  - 各空欄の正解値
  - 選択肢が「正解1つ＋他は1箇所のみ誤り」になっているか
"""


def verify_q1():
    """問1: 6空港の月別貨物取扱量"""
    # [国内, 国際] のペア
    data = {
        "成田": {"7": [80, 320], "8": [95, 380], "9": [88, 340]},
        "羽田": {"7": [220, 180], "8": [250, 200], "9": [230, 190]},
        "関西": {"7": [90, 250], "8": [110, 290], "9": [100, 270]},
        "中部": {"7": [70, 100], "8": [85, 130], "9": [75, 115]},
        "福岡": {"7": [110, 60], "8": [130, 75], "9": [120, 65]},
        "那覇": {"7": [60, 40], "8": [75, 55], "9": [65, 45]},
    }

    # 行合計（空港別）
    airport_totals = {}
    for ap, months in data.items():
        kokunai = sum(months[m][0] for m in months)
        kokusai = sum(months[m][1] for m in months)
        airport_totals[ap] = {"国内": kokunai, "国際": kokusai, "合計": kokunai + kokusai}

    print("=== 問1: 空港別3ヶ月合計 ===")
    for ap, t in airport_totals.items():
        print(f"  {ap}: 国内={t['国内']} 国際={t['国際']} 合計={t['合計']}")

    # 列合計（月別）
    print("\n=== 問1: 月別6空港合計 ===")
    for m in ["7", "8", "9"]:
        kn = sum(data[ap][m][0] for ap in data)
        ks = sum(data[ap][m][1] for ap in data)
        print(f"  {m}月: 国内={kn} 国際={ks} 合計={kn+ks}")

    # 空欄値
    total_kokusai = sum(t["国際"] for t in airport_totals.values())
    total_kokunai = sum(t["国内"] for t in airport_totals.values())
    grand_total = total_kokusai + total_kokunai

    # (イ) 国際>国内の空港数
    kokusai_dominant = [ap for ap, t in airport_totals.items() if t["国際"] > t["国内"]]

    # (ウ) 3ヶ月合計（国内+国際）最大
    max_airport = max(airport_totals.items(), key=lambda x: x[1]["合計"])

    print(f"\n=== 問1: 空欄値 ===")
    print(f"  (ア) 国際便3ヶ月合計 = {total_kokusai}")  # 期待: 3105
    print(f"  (イ) 国際>国内の空港数 = {len(kokusai_dominant)} → {kokusai_dominant}")  # 期待: 3
    print(f"  (ウ) 3ヶ月合計最大 = {max_airport[0]}（{max_airport[1]['合計']}）")  # 期待: 成田 1303
    print(f"  (エ) 総合計 = {grand_total}")  # 期待: 5158

    assert total_kokusai == 3105, f"国際便合計が想定外: {total_kokusai}"
    assert total_kokunai == 2053, f"国内便合計が想定外: {total_kokunai}"
    assert len(kokusai_dominant) == 3, f"国際>国内の空港数が想定外: {len(kokusai_dominant)}"
    assert set(kokusai_dominant) == {"成田", "関西", "中部"}, f"空港集合不一致: {kokusai_dominant}"
    assert max_airport[0] == "成田", f"最大空港が想定外: {max_airport[0]}"
    assert max_airport[1]["合計"] == 1303
    assert grand_total == 5158, f"総合計が想定外: {grand_total}"
    print("  ✓ 問1: すべての空欄値が検証OK")

    # 選択肢検証: 正解(3) のみ全一致、他は1箇所のみ誤り
    correct = {"ア": 3105, "イ": 3, "ウ": "成田", "エ": 5158}
    options = {
        1: {"ア": 2053, "イ": 3, "ウ": "成田", "エ": 5158},   # アで誤り
        2: {"ア": 3105, "イ": 4, "ウ": "成田", "エ": 5158},   # イで誤り
        3: {"ア": 3105, "イ": 3, "ウ": "成田", "エ": 5158},   # 正解
        4: {"ア": 3105, "イ": 3, "ウ": "羽田", "エ": 5158},   # ウで誤り
        5: {"ア": 3105, "イ": 3, "ウ": "成田", "エ": 2053},   # エで誤り
    }
    print("\n=== 問1: 選択肢検証 ===")
    for n, opt in options.items():
        diffs = [k for k in correct if opt[k] != correct[k]]
        status = "正解" if not diffs else f"誤り箇所: {diffs}"
        print(f"  ({n}) {status}")
        if n == 3:
            assert not diffs, "正解(3)に差異あり"
        else:
            assert len(diffs) == 1, f"選択肢({n})は1箇所のみ誤りにすべき: {diffs}"
    print("  ✓ 問1: 選択肢構造OK（正解(3)が唯一）")


def verify_q2():
    """問2: 5路線の四半期別輸送統計"""
    # [乗客千人, 距離km, 運賃百万円]
    data = {
        "線A": {"Q1": [400, 120, 600], "Q2": [450, 120, 680], "Q3": [420, 120, 640], "Q4": [430, 120, 650]},
        "線B": {"Q1": [280, 100, 840], "Q2": [320, 100, 960], "Q3": [300, 100, 900], "Q4": [290, 100, 870]},
        "線C": {"Q1": [620, 60, 620], "Q2": [680, 60, 680], "Q3": [650, 60, 650], "Q4": [640, 60, 640]},
        "線D": {"Q1": [80, 80, 80], "Q2": [90, 80, 90], "Q3": [85, 80, 85], "Q4": [75, 80, 75]},
        "線E": {"Q1": [180, 40, 270], "Q2": [220, 40, 330], "Q3": [200, 40, 300], "Q4": [210, 40, 315]},
    }

    # 路線別年間合計
    line_totals = {}
    for line, qs in data.items():
        passengers = sum(qs[q][0] for q in qs)
        distance = sum(qs[q][1] for q in qs)
        fare = sum(qs[q][2] for q in qs)
        line_totals[line] = {"乗客": passengers, "距離": distance, "運賃": fare}

    print("\n=== 問2: 路線別年間合計 ===")
    for l, t in line_totals.items():
        per_p = t["運賃"] / t["乗客"]
        print(f"  {l}: 乗客={t['乗客']} 距離={t['距離']} 運賃={t['運賃']} 1人運賃={per_p:.3f}")

    # 四半期合計
    print("\n=== 問2: 四半期別5路線合計 ===")
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        p = sum(data[l][q][0] for l in data)
        d = sum(data[l][q][1] for l in data)
        f = sum(data[l][q][2] for l in data)
        print(f"  {q}: 乗客={p} 距離={d} 運賃={f}")

    # 空欄値
    # (ア) 年間乗客数合計
    total_pass = sum(t["乗客"] for t in line_totals.values())
    # (イ) 1人あたり運賃最大
    per_person = {l: t["運賃"] / t["乗客"] for l, t in line_totals.items()}
    max_per_person = max(per_person.items(), key=lambda x: x[1])
    # (ウ) 年間運賃最大
    max_fare = max(line_totals.items(), key=lambda x: x[1]["運賃"])
    # (エ) Q4運賃がQ1運賃の1.05倍以上の路線数
    threshold = 1.05
    q4_q1 = {l: data[l]["Q4"][2] / data[l]["Q1"][2] for l in data}
    qualifying = [l for l, r in q4_q1.items() if r >= threshold]
    # (オ) 年間運賃合計
    total_fare = sum(t["運賃"] for t in line_totals.values())

    print(f"\n=== 問2: 空欄値 ===")
    print(f"  (ア) 年間乗客数合計 = {total_pass}")  # 期待: 6620
    print(f"  (イ) 1人運賃最大 = {max_per_person[0]} ({max_per_person[1]:.3f})")  # 期待: 線B
    print(f"  (ウ) 年間運賃最大 = {max_fare[0]} ({max_fare[1]['運賃']})")  # 期待: 線B
    print(f"  (エ) Q4/Q1>=1.05 路線数 = {len(qualifying)} → {qualifying}")
    for l, r in q4_q1.items():
        print(f"        {l}: Q4/Q1 = {r:.4f}")
    print(f"  (オ) 年間運賃合計 = {total_fare}")  # 期待: 10275

    assert total_pass == 6620
    assert max_per_person[0] == "線B"
    assert max_fare[0] == "線B"
    assert max_fare[1]["運賃"] == 3570
    assert len(qualifying) == 2, f"想定外: {qualifying}"
    assert set(qualifying) == {"線A", "線E"}
    assert total_fare == 10275
    print("  ✓ 問2: すべての空欄値が検証OK")

    # 選択肢検証
    correct = {"ア": 6620, "イ": "線B", "ウ": "線B", "エ": 2, "オ": 10275}
    options = {
        1: {"ア": 1655, "イ": "線B", "ウ": "線B", "エ": 2, "オ": 10275},  # ア誤(Q3合計と混同)
        2: {"ア": 6620, "イ": "線A", "ウ": "線B", "エ": 2, "オ": 10275},  # イ誤(線A=1.512を最大と誤算)
        3: {"ア": 6620, "イ": "線B", "ウ": "線C", "エ": 2, "オ": 10275},  # ウ誤(乗客最大と混同)
        4: {"ア": 6620, "イ": "線B", "ウ": "線B", "エ": 3, "オ": 10275},  # エ誤(線Cを含めて誤算)
        5: {"ア": 6620, "イ": "線B", "ウ": "線B", "エ": 2, "オ": 10275},  # 正解
    }
    print("\n=== 問2: 選択肢検証 ===")
    for n, opt in options.items():
        diffs = [k for k in correct if opt[k] != correct[k]]
        status = "正解" if not diffs else f"誤り箇所: {diffs}"
        print(f"  ({n}) {status}")
        if n == 5:
            assert not diffs, "正解(5)に差異あり"
        else:
            assert len(diffs) == 1, f"選択肢({n})は1箇所のみ誤りにすべき: {diffs}"
    print("  ✓ 問2: 選択肢構造OK（正解(5)が唯一）")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n=== 全検証完了 ===")
