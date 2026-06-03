"""
航大思考196 解の一意性検証

問1: 航空会社4社の運航データ表の空欄補充
- 各社: 運航便数 × 平均搭乗率 × 座席数/便 = 旅客数
- 4社の旅客数合計を求める

問2: 航空5路線の収支データ表
- 売上 = 旅客数 × 平均運賃
- 旅客数 = 運航便数 × 平均搭乗率 × 座席数/便
- 運航費合計 = 運航便数 × 1便あたり運航費
- 利益 = 売上 - 運航費合計
- 利益率 = 利益 / 売上
- 5記述ア〜オの正誤判定
"""


def verify_q1():
    """問1: 4社合計旅客数を計算"""
    # A航空: 平均搭乗率80%, 座席数200, 旅客数96,000人 → 運航便数を求める
    A_flights = 96000 / (0.80 * 200)
    assert A_flights == 600, f"A航空運航便数: {A_flights}"

    # B航空: 運航便数400, 座席数250, 旅客数75,000人 → 平均搭乗率を求める
    B_load = 75000 / (400 * 250)
    assert B_load == 0.75, f"B航空搭乗率: {B_load}"

    # C航空: 運航便数500, 平均搭乗率70%, 旅客数70,000人 → 座席数を求める
    C_seats = 70000 / (500 * 0.70)
    assert C_seats == 200, f"C航空座席数: {C_seats}"

    # D航空: 運航便数300, 平均搭乗率85%, 座席数220 → 旅客数を求める
    D_pax = 300 * 0.85 * 220
    assert D_pax == 56100, f"D航空旅客数: {D_pax}"

    total = 96000 + 75000 + 70000 + D_pax
    print(f"問1: 4社合計旅客数 = {total:,}人")

    # 選択肢候補: (1) 297,100人  (2) 281,100人  (3) 287,400人  (4) 307,100人  (5) 313,500人
    assert total == 297100, f"合計が異なる: {total}"
    return total


def verify_q2():
    """問2: 5路線の収支分析"""
    routes = [
        # 路線, 便数, 搭乗率, 座席/便, 平均運賃, 1便運航費
        ("A", 400, 0.80, 200, 25000, 3_000_000),
        ("B", 350, 0.75, 220, 30000, 4_000_000),
        ("C", 300, 0.85, 250, 35000, 5_000_000),
        ("D", 500, 0.70, 180, 15000, 2_000_000),
        ("E", 250, 0.65, 200, 20000, 2_500_000),
    ]

    results = {}
    for name, flights, load, seats, fare, cost_per in routes:
        pax = flights * load * seats
        revenue = pax * fare
        total_cost = flights * cost_per
        profit = revenue - total_cost
        margin = profit / revenue
        results[name] = {
            "pax": pax,
            "revenue": revenue,
            "profit": profit,
            "margin": margin,
        }
        print(
            f"  {name}: 旅客={pax:>8,.0f}人 売上={revenue/1e8:>6.3f}億円 "
            f"利益={profit/1e8:>+6.3f}億円 利益率={margin*100:>+6.2f}%"
        )

    # 各種ランキング
    max_pax = max(results, key=lambda k: results[k]["pax"])
    max_rev = max(results, key=lambda k: results[k]["revenue"])
    max_profit = max(results, key=lambda k: results[k]["profit"])
    max_margin = max(results, key=lambda k: results[k]["margin"])
    losers = [k for k, v in results.items() if v["profit"] < 0]
    winners = [k for k, v in results.items() if v["profit"] > 0]
    high_margin = [k for k, v in results.items() if v["margin"] >= 0.20]

    print(f"\n旅客数最多: {max_pax}")
    print(f"売上最多: {max_rev}")
    print(f"利益最多: {max_profit}")
    print(f"利益率最高: {max_margin}")
    print(f"赤字路線: {losers}")
    print(f"黒字路線: {winners}")
    print(f"利益率20%以上: {high_margin}")

    # 5記述
    sta_a = max_pax == "A"  # ア: 旅客数最多はA路線
    sta_b = max_rev == "C" and max_profit == "C" and max_margin == "C"  # イ: 売上・利益・利益率すべてC路線
    sta_c = len(high_margin) == 3  # ウ: 利益率20%以上が3路線
    sta_d = losers == ["D"]  # エ: 赤字はD路線のみ
    sta_e = len(winners) == 4  # オ: 黒字が4路線

    print(f"\nア: {sta_a} (A最多={max_pax == 'A'})")
    print(f"イ: {sta_b}")
    print(f"ウ: {sta_c} (利益率20%以上={len(high_margin)}路線)")
    print(f"エ: {sta_d}")
    print(f"オ: {sta_e}")

    correct = [name for name, val in [("ア", sta_a), ("イ", sta_b), ("ウ", sta_c), ("エ", sta_d), ("オ", sta_e)] if val]
    print(f"\n正しい記述: {correct}")

    # 選択肢:
    # (1) ア、イ
    # (2) イ、エ、オ
    # (3) ア、イ、ウ
    # (4) ア、イ、エ、オ
    # (5) ア、イ、ウ、エ、オ
    assert correct == ["ア", "イ", "エ", "オ"], f"正解集合が異なる: {correct}"
    return correct


if __name__ == "__main__":
    print("=== 問1検証 ===")
    verify_q1()
    print("\n=== 問2検証 ===")
    verify_q2()
    print("\n✓ 全検証パス")
