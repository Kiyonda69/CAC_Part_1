#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考245 検証スクリプト
問1: 航空資料読取（風向と対地速度から最短所要時間の区間を特定）
問2: 航空資料読取（往復飛行の最小搭載燃料量の計算）

資料内で提示する航空知識:
- 風向は「風が吹いてくる方向」（090°=東からの風）
- 向かい風: GS = TAS - 風速 / 追い風: GS = TAS + 風速
- 予備燃料: 国内飛行は標準巡航30分相当
"""


def wind_component(course, wind_dir, wind_speed):
    """進行方位と風向から風成分を求める（正=追い風、負=向かい風）
    本問題では風向は進行方位と平行（同方位=向かい風、逆方位=追い風）のみ扱う
    """
    diff = (wind_dir - course) % 360
    if diff == 0:
        return -wind_speed  # 進行方向から吹いてくる → 向かい風
    elif diff == 180:
        return +wind_speed  # 背後から吹いてくる → 追い風
    else:
        raise ValueError(f"平行でない風: course={course}, wind={wind_dir}")


def verify_q1():
    """問1: 5区間の所要時間を計算し、最短区間が唯一であることを確認"""
    # (区間, 進行方位, 距離km, TAS km/h, 風向, 風速 km/h)
    legs = [
        (1, 90, 420, 250, 90, 40),
        (2, 180, 450, 220, 360, 50),
        (3, 270, 400, 220, 90, 30),
        (4, 360, 380, 210, 360, 20),
        (5, 90, 480, 250, 90, 10),
    ]
    times = {}
    for n, course, dist, tas, wd, ws in legs:
        gs = tas + wind_component(course, wd, ws)
        t = dist / gs * 60  # 分
        assert abs(t - round(t)) < 1e-9, f"区間{n}の時間が整数でない: {t}"
        times[n] = round(t)
    print("問1 各区間の所要時間(分):", times)
    expected = {1: 120, 2: 100, 3: 96, 4: 120, 5: 120}
    assert times == expected, f"期待値と不一致: {times}"
    min_t = min(times.values())
    winners = [n for n, t in times.items() if t == min_t]
    assert winners == [3], f"最短区間が唯一でない: {winners}"
    # 罠の検証: 風向を「吹いていく方向」と誤読すると区間1が最短に見える
    mis = {}
    for n, course, dist, tas, wd, ws in legs:
        gs = tas - wind_component(course, wd, ws)  # 符号反転
        mis[n] = dist / gs * 60
    mis_winner = min(mis, key=mis.get)
    assert mis_winner == 1, f"誤読時の最短が区間1でない: {mis_winner}"
    # 罠の検証: 風を無視(TASのみ)でも区間1が最短に見える
    ign = {n: d / tas * 60 for n, c, d, tas, wd, ws in legs}
    assert min(ign, key=ign.get) == 1
    # 距離最短(区間4)・TAS最大(区間1,5)も正解と一致しないこと
    assert min(legs, key=lambda x: x[2])[0] == 4
    print("問1 正解: 区間3（選択肢(3)）— 唯一解・罠3種確認済み")


def verify_q2():
    """問2: 往復飛行の最小搭載燃料量を計算"""
    dist = 600          # 片道距離 km
    tas = 250           # 標準巡航 TAS km/h
    burn = 120          # 標準巡航 燃料消費 L/h
    wind = 50           # 風向270°・50km/h（往路090°=追い風、復路270°=向かい風）
    extra_per_flight = 20   # 離陸〜着陸1回あたりの追加消費 L
    reserve_min = 30        # 国内飛行の予備燃料（標準巡航30分相当）

    t_out = dist / (tas + wind)   # 往路 追い風
    t_back = dist / (tas - wind)  # 復路 向かい風
    assert (t_out, t_back) == (2.0, 3.0)
    cruise_fuel = (t_out + t_back) * burn          # 600 L
    extra_fuel = 2 * extra_per_flight              # 40 L
    reserve_fuel = reserve_min / 60 * burn         # 60 L
    total = cruise_fuel + extra_fuel + reserve_fuel
    assert total == 700, f"最小搭載燃料が700Lでない: {total}"
    # 誤答選択肢の根拠を検証
    e2 = cruise_fuel + extra_fuel + 45 / 60 * burn        # 予備45分(国際)誤用
    e3 = cruise_fuel + 2 * 2 * extra_per_flight + reserve_fuel  # 離陸・着陸各20L誤読
    e4 = cruise_fuel + 2 * 2 * extra_per_flight + 45 / 60 * burn  # 両方複合
    e5 = 2 * (dist / (tas - wind)) * burn + extra_fuel + reserve_fuel  # 往復とも向かい風
    assert (e2, e3, e4, e5) == (730, 740, 770, 820), (e2, e3, e4, e5)
    opts = [700, 730, 740, 770, 820]
    assert len(set(opts)) == 5 and opts == sorted(opts)
    print("問2 正解: 700L（選択肢(1)）— 誤答根拠 730/740/770/820 確認済み")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 両問とも唯一解")
