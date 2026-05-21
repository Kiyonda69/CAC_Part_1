"""
航大思考173 検証スクリプト
資料穴埋め問題（情報量多）の解の一意性を検証する。

問1: 製造業6工場 × 5製品ラインの月間生産台数（4箇所穴埋め）
問2: 8空港 × 4四半期 × 2指標（旅客数・貨物量）の年間統計（5箇所穴埋め）
"""

# ============================================================
# 問1: 6工場 × 5製品ライン の月間生産台数
# ============================================================
# 工場: A, B, C, D, E, F
# 製品: ①, ②, ③, ④, ⑤
factories_q1 = ['A', 'B', 'C', 'D', 'E', 'F']
products_q1 = ['①', '②', '③', '④', '⑤']

# 生産台数の表（行: 工場, 列: 製品）
q1_table = {
    'A': [120, 80, 150, 60, 100],
    'B': [80, 110, 90, 70, 130],
    'C': [200, 150, 180, 120, 250],
    'D': [100, 90, 110, 80, 140],
    'E': [60, 70, 80, 50, 90],
    'F': [140, 130, 160, 100, 170],
}


def verify_q1():
    # 工場別合計
    factory_totals = {f: sum(q1_table[f]) for f in factories_q1}
    print("問1 工場別合計:", factory_totals)

    # 製品別合計
    product_totals = [sum(q1_table[f][p] for f in factories_q1) for p in range(5)]
    print("問1 製品別合計:", dict(zip(products_q1, product_totals)))

    # 全体合計
    grand = sum(factory_totals.values())
    grand2 = sum(product_totals)
    assert grand == grand2, f"全体合計の不一致: {grand} vs {grand2}"

    # 空欄の値
    a = max(factory_totals, key=factory_totals.get)        # 最大工場
    # 同点チェック
    max_v = factory_totals[a]
    assert sum(1 for v in factory_totals.values() if v == max_v) == 1, "工場最大が一意でない"

    min_v = min(product_totals)
    assert product_totals.count(min_v) == 1, "製品最小が一意でない"
    b_idx = product_totals.index(min_v)
    b = products_q1[b_idx]

    c = product_totals[2]  # 製品③の合計
    d = grand

    print(f"問1 空欄: ア={a}, イ={b}, ウ={c}, エ={d}")
    assert a == 'C', f"期待値Cと不一致: {a}"
    assert b == '④', f"期待値④と不一致: {b}"
    assert c == 770, f"期待値770と不一致: {c}"
    assert d == 3460, f"期待値3460と不一致: {d}"
    return (a, b, c, d)


# ============================================================
# 問2: 8空港 × 4四半期 × 2指標
# ============================================================
# 旅客数 [Q1, Q2, Q3, Q4]（千人）と貨物量（トン）
airports_q2 = ['札幌', '仙台', '東京', '名古屋', '大阪', '福岡', '那覇', '広島']
q2_passenger = {
    '札幌':   [220, 280, 240, 200],
    '仙台':   [ 90, 110, 100,  80],
    '東京':   [800, 900, 850, 820],
    '名古屋': [220, 250, 240, 220],
    '大阪':   [450, 500, 470, 460],
    '福岡':   [280, 320, 300, 280],
    '那覇':   [180, 280, 220, 240],
    '広島':   [100, 120, 110,  90],
}
q2_cargo = {
    '札幌':   [ 80, 100,  90, 110],
    '仙台':   [ 30,  40,  35,  45],
    '東京':   [400, 450, 430, 460],
    '名古屋': [100, 110, 105, 115],
    '大阪':   [200, 220, 210, 230],
    '福岡':   [110, 130, 120, 140],
    '那覇':   [ 60,  80,  70,  90],
    '広島':   [ 40,  50,  45,  55],
}


def verify_q2():
    # 年間合計
    pax_year = {a: sum(q2_passenger[a]) for a in airports_q2}
    car_year = {a: sum(q2_cargo[a]) for a in airports_q2}
    print("問2 旅客年間:", pax_year)
    print("問2 貨物年間:", car_year)

    total_pax = sum(pax_year.values())
    total_car = sum(car_year.values())

    # 四半期合計でも検算
    for q in range(4):
        s_pax = sum(q2_passenger[a][q] for a in airports_q2)
        s_car = sum(q2_cargo[a][q] for a in airports_q2)
        print(f"  Q{q+1}: 旅客={s_pax}, 貨物={s_car}")

    # ア: 8空港の年間旅客数合計
    a_val = total_pax
    # イ: 1旅客あたり貨物量（トン/千人）最大の空港
    efficiency = {a: car_year[a] / pax_year[a] for a in airports_q2}
    print("問2 1人あたり貨物量:", {a: round(v, 4) for a, v in efficiency.items()})
    b_val = max(efficiency, key=efficiency.get)
    max_eff = efficiency[b_val]
    assert sum(1 for v in efficiency.values() if v == max_eff) == 1, "効率最大が一意でない"

    # ウ: Q4貨物がQ1の1.4倍以上の空港数
    c_val = 0
    qualifying = []
    for a in airports_q2:
        ratio = q2_cargo[a][3] / q2_cargo[a][0]
        if ratio >= 1.4:
            c_val += 1
            qualifying.append((a, round(ratio, 3)))
    print(f"問2 Q4/Q1≥1.4の空港: {qualifying}")

    # エ: 年間貨物量が最大の空港の値
    d_airport = max(car_year, key=car_year.get)
    max_car = car_year[d_airport]
    assert sum(1 for v in car_year.values() if v == max_car) == 1, "貨物最大が一意でない"
    d_val = max_car

    # オ: 8空港の年間貨物量合計
    e_val = total_car

    print(f"問2 空欄: ア={a_val}, イ={b_val}, ウ={c_val}, エ={d_val}, オ={e_val}")
    assert a_val == 10020, f"期待値10020と不一致: {a_val}"
    assert b_val == '東京', f"期待値東京と不一致: {b_val}"
    assert c_val == 2, f"期待値2と不一致: {c_val}"
    assert d_val == 1740, f"期待値1740と不一致: {d_val}"
    assert e_val == 4550, f"期待値4550と不一致: {e_val}"
    return (a_val, b_val, c_val, d_val, e_val)


if __name__ == '__main__':
    print("=" * 60)
    print("問1検証")
    print("=" * 60)
    q1 = verify_q1()
    print()
    print("=" * 60)
    print("問2検証")
    print("=" * 60)
    q2 = verify_q2()
    print()
    print("検証完了: 問1の正解=", q1, " 問2の正解=", q2)
