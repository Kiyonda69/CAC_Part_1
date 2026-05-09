"""航大思考168 解の一意性検証

問1: 野菜の出荷量推移（5品目×5年）
問2: ドラッグストアの販売実績（5年×5指標）

各5択のうち、確実にいえる/正しくいえるのが唯一であることを検証。
"""


def verify_q1():
    """問1：野菜の出荷量推移"""
    # 単位: t
    data = {
        "トマト":   {26: 720000, 27: 638000, 28: 670000, 29: 685000, 30: 700000},
        "きゅうり": {26: 540000, 27: 480000, 28: 510000, 29: 555000, 30: 525000},
        "なす":     {26: 285000, 27: 240000, 28: 270000, 29: 250000, 30: 245000},
        "ピーマン": {26: 200000, 27: 158000, 28: 172000, 29: 175000, 30: 180000},
        "レタス":   {26: 600000, 27: 568000, 28: 545000, 29: 528000, 30: 558000},
    }

    results = []

    # 選択肢1: H27→H29 増加量最大はトマト
    diffs = {k: v[29] - v[27] for k, v in data.items()}
    max_item = max(diffs, key=diffs.get)
    s1 = (max_item == "トマト")
    results.append(("1", s1, f"H27→H29 増加量: {diffs} 最大={max_item}"))

    # 選択肢2: 各年とも、トマト < 4×ピーマン
    s2 = all(data["トマト"][y] < 4 * data["ピーマン"][y] for y in range(26, 31))
    ratio = {y: data["トマト"][y] / data["ピーマン"][y] for y in range(26, 31)}
    results.append(("2", s2, f"トマト/ピーマン: {ratio}"))

    # 選択肢3: H27にトマトの対前年減少率 < なすの対前年減少率
    tomato_dec = (data["トマト"][26] - data["トマト"][27]) / data["トマト"][26]
    nasu_dec = (data["なす"][26] - data["なす"][27]) / data["なす"][26]
    s3 = tomato_dec < nasu_dec
    results.append(("3", s3, f"トマト減少率={tomato_dec:.4f}, なす={nasu_dec:.4f}"))

    # 選択肢4: ピーマンのH26に対するH28の減少率は15%より大きい
    piman_dec = (data["ピーマン"][26] - data["ピーマン"][28]) / data["ピーマン"][26]
    s4 = piman_dec > 0.15
    results.append(("4", s4, f"ピーマンH26→H28減少率={piman_dec:.4f}"))

    # 選択肢5: H26のレタスを100としたときのH29の指数は90を上回る
    lettuce_idx = data["レタス"][29] / data["レタス"][26] * 100
    s5 = lettuce_idx > 90
    results.append(("5", s5, f"レタス指数(H29)={lettuce_idx:.2f}"))

    print("=" * 60)
    print("問1 検証結果")
    print("=" * 60)
    trues = []
    for n, ok, info in results:
        mark = "○" if ok else "×"
        print(f"  選択肢{n}: {mark}  {info}")
        if ok:
            trues.append(n)
    assert len(trues) == 1, f"唯一でない: 真={trues}"
    print(f"  → 正解: ({trues[0]})")
    return trues[0]


def verify_q2():
    """問2：ドラッグストアの販売実績"""
    # 販売額総額(万円), 従業員数(人), 売場面積(㎡), 1人当(万円/人), 1㎡当(千円/㎡)
    data = {
        18: {"sales": 5200000, "emp": 22500, "area": 1250000, "perEmp": 231.1, "perArea": 41.6},
        19: {"sales": 5580000, "emp": 23400, "area": 1310000, "perEmp": 238.5, "perArea": 42.6},
        20: {"sales": 6030000, "emp": 24800, "area": 1360000, "perEmp": 243.1, "perArea": 44.3},
        21: {"sales": 6150000, "emp": 26100, "area": 1420000, "perEmp": 235.6, "perArea": 43.3},
        22: {"sales": 6275000, "emp": 27400, "area": 1460000, "perEmp": 229.0, "perArea": 43.0},
    }

    # 表示値の整合確認
    for y, d in data.items():
        c1 = d["sales"] / d["emp"]
        c2 = d["sales"] * 10 / d["area"]
        assert abs(c1 - d["perEmp"]) < 0.5, f"H{y} 1人当 不一致 計算={c1:.2f} 表示={d['perEmp']}"
        assert abs(c2 - d["perArea"]) < 0.5, f"H{y} 1㎡当 不一致 計算={c2:.2f} 表示={d['perArea']}"

    results = []

    # 選択肢1: H19-H22で1㎡当の対前年増加率最高はH19
    rates = {y: (data[y]["perArea"] - data[y - 1]["perArea"]) / data[y - 1]["perArea"] for y in range(19, 23)}
    max_y = max(rates, key=rates.get)
    s1 = (max_y == 19)
    results.append(("1", s1, f"対前年増加率: {rates}, 最高=H{max_y}"))

    # 選択肢2: H18の1人当を100としたH22の指数は約95
    idx = data[22]["perEmp"] / data[18]["perEmp"] * 100
    s2 = abs(idx - 95) < 1.5
    results.append(("2", s2, f"H22 指数={idx:.2f}, 約95か?"))

    # 選択肢3: 従業員1人当たりの平均売場面積は、H18よりH22が1割ほど多い
    h18_per = data[18]["area"] / data[18]["emp"]
    h22_per = data[22]["area"] / data[22]["emp"]
    rel = (h22_per - h18_per) / h18_per
    s3 = abs(rel - 0.1) < 0.02
    results.append(("3", s3, f"H18={h18_per:.2f}, H22={h22_per:.2f}, 増加率={rel:.4f}"))

    # 選択肢4: 販売額総額は年々増加し、1人当販売額も年々減少
    sales_inc = all(data[y]["sales"] > data[y - 1]["sales"] for y in range(19, 23))
    perEmp_dec = all(data[y]["perEmp"] < data[y - 1]["perEmp"] for y in range(19, 23))
    s4 = sales_inc and perEmp_dec
    results.append(("4", s4, f"販売額年々増加={sales_inc}, 1人当年々減少={perEmp_dec}"))

    # 選択肢5: H22の販売額総額対前年増加率 < 同年の従業員数のそれ
    sales_rate = (data[22]["sales"] - data[21]["sales"]) / data[21]["sales"]
    emp_rate = (data[22]["emp"] - data[21]["emp"]) / data[21]["emp"]
    s5 = sales_rate < emp_rate
    results.append(("5", s5, f"販売額={sales_rate:.4f}, 従業員={emp_rate:.4f}"))

    print("=" * 60)
    print("問2 検証結果")
    print("=" * 60)
    trues = []
    for n, ok, info in results:
        mark = "○" if ok else "×"
        print(f"  選択肢{n}: {mark}  {info}")
        if ok:
            trues.append(n)
    assert len(trues) == 1, f"唯一でない: 真={trues}"
    print(f"  → 正解: ({trues[0]})")
    return trues[0]


if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print()
    print(f"【最終】問1: ({a1})  問2: ({a2})")
