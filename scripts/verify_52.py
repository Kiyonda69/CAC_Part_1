"""
セット52 検証スクリプト
問1: 水道事業規模別データ - 職員1人あたりの年間総配水量が2番目に多い事業規模
問2: 地域別農業データ - 4つの記述ア～エの正誤判定
"""

def verify_q1():
    """問1: 水道事業規模別データの検証"""
    print("=" * 60)
    print("問1: 水道事業規模別データ")
    print("=" * 60)

    # データ: (事業規模, 事業体数, 給水人口(千人), 年間総配水量(千m³), 職員数(人))
    data = [
        ("大規模(給水人口50万人以上)", 12, 18456, 4128500, 28450),
        ("中規模(10万～50万人)", 78, 16234, 3245600, 18920),
        ("やや中規模(5万～10万人)", 115, 8124, 1586400, 9850),
        ("小規模(1万～5万人)", 482, 10856, 2124800, 12340),
        ("極小規模(1万人未満)", 685, 3248, 645200, 5680),
    ]

    print("\n職員1人あたりの年間総配水量:")
    ratios = []
    for name, n, pop, water, staff in data:
        ratio = water / staff
        ratios.append((name, ratio))
        print(f"  {name}: {water:,} / {staff:,} = {ratio:.1f} 千m³/人")

    # ソート
    ratios.sort(key=lambda x: x[1], reverse=True)
    print("\n順位:")
    for i, (name, ratio) in enumerate(ratios, 1):
        print(f"  {i}位: {name} ({ratio:.1f})")

    second = ratios[1][0]
    print(f"\n2番目: {second}")

    # 選択肢の順序と正解確認
    choices = [
        "(1) 大規模(給水人口50万人以上)",
        "(2) 中規模(10万～50万人)",
        "(3) やや中規模(5万～10万人)",
        "(4) 小規模(1万～5万人)",
        "(5) 極小規模(1万人未満)",
    ]
    print("\n選択肢:")
    for c in choices:
        print(f"  {c}")

    # 正解は中規模 → (2)
    assert "中規模" in second, f"Expected 中規模, got {second}"
    print("\n正解: (2) 中規模(10万～50万人)")

    # 合計行の検証
    total_n = sum(d[1] for d in data)
    total_pop = sum(d[2] for d in data)
    total_water = sum(d[3] for d in data)
    total_staff = sum(d[4] for d in data)
    print(f"\n合計: 事業体数={total_n}, 給水人口={total_pop:,}千人, "
          f"配水量={total_water:,}千m³, 職員数={total_staff:,}人")


def verify_q2():
    """問2: 地域別農業データの検証"""
    print("\n" + "=" * 60)
    print("問2: 地域別農業データ")
    print("=" * 60)

    # データ: (地域, 経営体数, 耕地面積(ha), 農業産出額(億円), 農業所得(億円), 農業就業人口(千人))
    data = [
        ("北海道", 36200, 1143000, 12667, 5024, 82),
        ("東北", 184500, 582400, 13840, 3912, 198),
        ("関東", 215300, 418600, 19280, 5865, 285),
        ("北陸", 52800, 168200, 3145, 780, 58),
        ("東海", 85600, 135800, 7524, 2148, 105),
        ("近畿", 78400, 103500, 5280, 1425, 89),
        ("中国四国", 105200, 178600, 7856, 2034, 124),
        ("九州", 132400, 348200, 17632, 5420, 196),
    ]

    # ア: 農業就業人口1千人あたりの農業産出額が最も高い地域は北海道である
    print("\nア: 農業就業人口1千人あたりの農業産出額")
    results_a = []
    for name, _, _, output, _, workers in data:
        ratio = output / workers
        results_a.append((name, ratio))
        print(f"  {name}: {output:,} / {workers} = {ratio:.1f}")
    results_a.sort(key=lambda x: x[1], reverse=True)
    a_correct = results_a[0][0] == "北海道"
    print(f"  最高: {results_a[0][0]} ({results_a[0][1]:.1f})")
    print(f"  ア: {'正しい' if a_correct else '誤り'}")

    # イ: 経営体1つあたりの耕地面積が2番目に広い地域は九州である
    print("\nイ: 経営体1つあたりの耕地面積")
    results_b = []
    for name, entities, area, _, _, _ in data:
        ratio = area / entities
        results_b.append((name, ratio))
        print(f"  {name}: {area:,} / {entities:,} = {ratio:.2f} ha")
    results_b.sort(key=lambda x: x[1], reverse=True)
    b_correct = results_b[1][0] == "九州"
    print(f"  1位: {results_b[0][0]} ({results_b[0][1]:.2f})")
    print(f"  2位: {results_b[1][0]} ({results_b[1][1]:.2f})")
    print(f"  イ: {'正しい' if b_correct else '誤り'}")

    # ウ: 農業産出額に占める農業所得の割合が最も低い地域は北陸である
    print("\nウ: 農業産出額に占める農業所得の割合")
    results_c = []
    for name, _, _, output, income, _ in data:
        ratio = income / output * 100
        results_c.append((name, ratio))
        print(f"  {name}: {income:,} / {output:,} = {ratio:.1f}%")
    results_c.sort(key=lambda x: x[1])
    c_correct = results_c[0][0] == "北陸"
    print(f"  最低: {results_c[0][0]} ({results_c[0][1]:.1f}%)")
    print(f"  ウ: {'正しい' if c_correct else '誤り'}")

    # エ: 耕地面積1haあたりの農業産出額が最も高い地域は関東である
    print("\nエ: 耕地面積1haあたりの農業産出額")
    results_d = []
    for name, _, area, output, _, _ in data:
        ratio = output / area * 10000  # 万円/haに変換（億円÷ha×10000）
        results_d.append((name, ratio))
        print(f"  {name}: {output:,}億円 / {area:,}ha = {ratio:.1f} 万円/ha")
    results_d.sort(key=lambda x: x[1], reverse=True)
    d_correct = results_d[0][0] == "関東"
    print(f"  最高: {results_d[0][0]} ({results_d[0][1]:.1f})")
    print(f"  エ: {'正しい' if d_correct else '誤り'}")

    # 結論
    print("\n" + "-" * 40)
    print(f"ア: {'正しい' if a_correct else '誤り'}")
    print(f"イ: {'正しい' if b_correct else '誤り'}")
    print(f"ウ: {'正しい' if c_correct else '誤り'}")
    print(f"エ: {'正しい' if d_correct else '誤り'}")

    correct_statements = []
    if a_correct: correct_statements.append("ア")
    if b_correct: correct_statements.append("イ")
    if c_correct: correct_statements.append("ウ")
    if d_correct: correct_statements.append("エ")
    print(f"\n正しい記述: {', '.join(correct_statements)}")

    # 選択肢:
    # (1) ア、イ  (2) ア、ウ  (3) イ、ウ  (4) ウ、エ  (5) ア、エ
    assert a_correct and not b_correct and c_correct and not d_correct, \
        f"Expected ア=True, イ=False, ウ=True, エ=False"
    print("正解: (2) ア、ウ")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 60)
    print("全検証完了: 問1正解=(2), 問2正解=(2)")
    print("=" * 60)
