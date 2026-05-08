"""
航大思考154 解の一意性検証スクリプト

問1: 四半期売上表からの計算（複数選択肢から1つだけ正しい）
問2: 路線別運航データの複合グラフからの計算
"""


def verify_q1():
    """問1: 半導体メーカー4部門の四半期売上表"""
    sales = {
        "半導体":   [480, 540, 612, 720],
        "センサー": [320, 360, 396, 440],
        "モーター": [280, 290, 305, 312],
        "基板":     [220, 250, 285, 312],
    }
    totals = {k: sum(v) for k, v in sales.items()}
    grand_total = sum(totals.values())

    print("=== 問1 検証 ===")
    print(f"部門別合計: {totals}")
    print(f"全体合計: {grand_total}")

    # (1) Q4半導体 / Q1半導体 が 1.5倍を超えているか
    r1 = sales["半導体"][3] / sales["半導体"][0]
    c1 = r1 > 1.5
    print(f"(1) 720/480 = {r1:.4f} → 1.5倍超え? {c1}")

    # (2) センサー年間に占めるQ3比率は約27%か
    r2 = sales["センサー"][2] / totals["センサー"]
    c2 = abs(r2 - 0.27) < 0.005  # 27% ± 0.5%
    print(f"(2) 396/1516 = {r2*100:.2f}% → 約27%? {c2}")

    # (3) Q1→Q4の伸び率(Q4/Q1)が最大なのはモーター部門か
    growth = {k: v[3] / v[0] for k, v in sales.items()}
    max_dept = max(growth, key=growth.get)
    c3 = (max_dept == "モーター")
    print(f"(3) 伸び率: {growth} → 最大は{max_dept}, モーター? {c3}")

    # (4) 全体合計に占める半導体構成比は約38%か
    r4 = totals["半導体"] / grand_total
    c4 = abs(r4 - 0.38) < 0.01  # 約38%（37.5%〜38.5%程度の許容）
    print(f"(4) 2352/6122 = {r4*100:.2f}% → 約38%? {c4}")

    # (5) Q3基板 / Q3モーター が 95%以上か
    r5 = sales["基板"][2] / sales["モーター"][2]
    c5 = r5 >= 0.95
    print(f"(5) 285/305 = {r5*100:.2f}% → 95%以上? {c5}")

    correct = [c1, c2, c3, c4, c5]
    correct_indices = [i + 1 for i, v in enumerate(correct) if v]
    print(f"\n正しい選択肢: {correct_indices}")
    assert correct_indices == [4], f"解が一意でない: {correct_indices}"
    print("→ 問1の正解は (4) で一意\n")


def verify_q2():
    """問2: 路線別月間データ"""
    routes = {
        "A": {"flights": 180, "seats": 150, "rate": 0.80},
        "B": {"flights": 240, "seats": 200, "rate": 0.75},
        "C": {"flights": 120, "seats": 180, "rate": 0.70},
        "D": {"flights": 150, "seats": 160, "rate": 0.85},
        "E": {"flights": 200, "seats": 120, "rate": 0.90},
    }
    # 月間搭乗者数 = 便数 × 定員 × 搭乗率
    pax = {k: int(v["flights"] * v["seats"] * v["rate"]) for k, v in routes.items()}
    total_pax = sum(pax.values())
    total_seats = sum(v["flights"] * v["seats"] for v in routes.values())

    print("=== 問2 検証 ===")
    print(f"月間搭乗者数: {pax}")
    print(f"合計搭乗者数: {total_pax}")
    print(f"合計座席数: {total_seats}")

    # (1) B路線の搭乗者数は全体の1/3を超えるか
    r1 = pax["B"] / total_pax
    c1 = r1 > 1 / 3
    print(f"(1) B/合計 = {r1*100:.2f}% → 1/3(約33.3%)超? {c1}")

    # (2) A路線とE路線の搭乗者数は等しいか
    c2 = (pax["A"] == pax["E"])
    print(f"(2) A={pax['A']}, E={pax['E']} → 等しい? {c2}")

    # (3) C路線の搭乗者数はD路線の80%を超えるか
    r3 = pax["C"] / pax["D"]
    c3 = r3 > 0.80
    print(f"(3) C/D = {r3*100:.2f}% → 80%超? {c3}")

    # (4) 全路線の搭乗率（単純平均）は80%を超えるか
    avg_rate = sum(v["rate"] for v in routes.values()) / len(routes)
    weighted_rate = total_pax / total_seats
    c4 = avg_rate > 0.80  # 単純平均で判断
    print(f"(4) 単純平均搭乗率 = {avg_rate*100:.2f}%, 加重平均 = {weighted_rate*100:.2f}% → 単純平均が80%超? {c4}")

    # (5) E路線はC路線の1.5倍を超えるか
    r5 = pax["E"] / pax["C"]
    c5 = r5 > 1.5
    print(f"(5) E/C = {r5*100:.2f}% → 1.5倍超? {c5}")

    correct = [c1, c2, c3, c4, c5]
    correct_indices = [i + 1 for i, v in enumerate(correct) if v]
    print(f"\n正しい選択肢: {correct_indices}")
    assert correct_indices == [2], f"解が一意でない: {correct_indices}"
    print("→ 問2の正解は (2) で一意\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("✅ 両問とも解は一意")
