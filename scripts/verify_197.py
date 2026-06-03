"""航大思考197 検証スクリプト
問1: 航空機性能表からの条件絞り込み
問2: 複数路線運航における最適機種選択
"""

# ===========================
# 問1: 単一表での条件絞り込み
# ===========================

# 航空機5機種の性能表
aircraft_q1 = {
    "A": {"speed": 820, "range": 5500, "seats": 200, "fuel_rate": 2800},
    "B": {"speed": 870, "range": 4800, "seats": 220, "fuel_rate": 2900},
    "C": {"speed": 880, "range": 6200, "seats": 190, "fuel_rate": 2950},
    "D": {"speed": 860, "range": 5300, "seats": 160, "fuel_rate": 2700},
    "E": {"speed": 850, "range": 5800, "seats": 200, "fuel_rate": 3100},
}

# 条件
# - 巡航速度 ≥ 850 km/h
# - 航続距離 ≥ 5000 km
# - 座席数 ≥ 180席
# - 燃料消費率 ≤ 3000 kg/h


def verify_q1():
    valid = []
    for name, spec in aircraft_q1.items():
        if (
            spec["speed"] >= 850
            and spec["range"] >= 5000
            and spec["seats"] >= 180
            and spec["fuel_rate"] <= 3000
        ):
            valid.append(name)
    print(f"問1 条件を満たす機種: {valid}")
    assert len(valid) == 1, f"問1: 解が{len(valid)}個存在"
    assert valid[0] == "C", f"問1: 期待値Cではなく{valid[0]}"
    print("問1 OK: 機種C (選択肢3)")
    return valid[0]


# ===========================
# 問2: 複数表の組み合わせ問題
# ===========================

# 表1: 航空機5機種の仕様
aircraft_q2 = {
    "A": {"range": 5000, "seats": 180, "cost_per_h": 80, "speed": 800},
    "B": {"range": 6500, "seats": 220, "cost_per_h": 95, "speed": 850},
    "C": {"range": 7000, "seats": 200, "cost_per_h": 90, "speed": 870},
    "D": {"range": 8000, "seats": 200, "cost_per_h": 100, "speed": 900},
    "E": {"range": 9000, "seats": 250, "cost_per_h": 110, "speed": 880},
}

# 表2: 運航予定の路線
routes = {
    "α": {"distance": 4500, "passengers": 190},
    "β": {"distance": 6000, "passengers": 180},
    "γ": {"distance": 7500, "passengers": 200},
    "δ": {"distance": 7800, "passengers": 200},
}


def verify_q2():
    """全路線運航可能で、合計運航コストが最小の機種を選ぶ"""
    max_dist = max(r["distance"] for r in routes.values())
    max_pass = max(r["passengers"] for r in routes.values())
    total_dist = sum(r["distance"] for r in routes.values())

    print(f"問2 最長距離: {max_dist} km, 最大旅客数: {max_pass}人, 合計距離: {total_dist} km")

    candidates = []
    for name, spec in aircraft_q2.items():
        if spec["range"] >= max_dist and spec["seats"] >= max_pass:
            flight_h = total_dist / spec["speed"]
            total_cost = flight_h * spec["cost_per_h"]
            candidates.append((name, total_cost, flight_h))
            print(f"  {name}: 飛行時間 {flight_h:.2f}h, 合計コスト {total_cost:.1f}万円")
        else:
            reasons = []
            if spec["range"] < max_dist:
                reasons.append(f"航続距離不足({spec['range']}<{max_dist})")
            if spec["seats"] < max_pass:
                reasons.append(f"座席数不足({spec['seats']}<{max_pass})")
            print(f"  {name}: 不適合 - {', '.join(reasons)}")

    # 最小コストを探す
    candidates.sort(key=lambda x: x[1])
    best = candidates[0]
    # 2位との差をチェック（一意性）
    assert len(candidates) >= 2, "候補が少なすぎる"
    assert candidates[0][1] != candidates[1][1], "最小コストが一意でない"

    print(f"問2 最適機種: {best[0]} (合計コスト {best[1]:.1f}万円)")
    assert best[0] == "D", f"問2: 期待値Dではなく{best[0]}"
    print("問2 OK: 機種D (選択肢4)")
    return best[0]


if __name__ == "__main__":
    verify_q1()
    print()
    verify_q2()
