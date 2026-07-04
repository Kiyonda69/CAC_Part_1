#!/usr/bin/env python3
"""航大思考243: 航法灯による機体方位の特定 - 解の一意性検証

灯火の可視規則（相対方位 = 機首を0°として時計回り）:
  0   真正面     : 赤・緑
  45  右斜め前   : 緑
  90  右真横     : 緑
  135 右斜め後ろ : 緑・白
  180 真後ろ     : 白
  225 左斜め後ろ : 赤・白
  270 左真横     : 赤
  315 左斜め前   : 赤
"""

DIRS = ["北", "北東", "東", "南東", "南", "南西", "西", "北西"]  # 0,45,...,315

VISIBLE = {
    0: {"赤", "緑"},
    45: {"緑"},
    90: {"緑"},
    135: {"緑", "白"},
    180: {"白"},
    225: {"赤", "白"},
    270: {"赤"},
    315: {"赤"},
}


def lights_seen(heading_deg, observer_dir_deg):
    """機首方位 heading の機体を、機体から見て observer_dir 方向にいる
    観測者が見たときの灯火の集合"""
    rel = (observer_dir_deg - heading_deg) % 360
    return VISIBLE[rel]


def q1():
    """問1: 観測者は機体の真南（機体から見て180°方向）。緑と白が見えた。
    機首方位は?"""
    sols = [h for h in range(0, 360, 45)
            if lights_seen(h, 180) == {"緑", "白"}]
    assert len(sols) == 1, f"問1: 解が{len(sols)}個 {sols}"
    print(f"問1 唯一解: 機首方位 {DIRS[sols[0] // 45]} ({sols[0]}°)")
    return sols[0]


def q2():
    """問2: 観測者Aは機体の真西(270°方向)から赤のみ、
    観測者Bは機体の真北(0°方向)から緑のみを同時に観測。
    (a) 機首方位は? (b) 機体の真南(180°方向)の観測者Cに見える灯火は?"""
    set_a = {h for h in range(0, 360, 45) if lights_seen(h, 270) == {"赤"}}
    set_b = {h for h in range(0, 360, 45) if lights_seen(h, 0) == {"緑"}}
    # 各観測は単独では絞り切れない（高難度の核心）
    assert len(set_a) >= 2, f"Aの観測が単独で一意: {set_a}"
    assert len(set_b) >= 2, f"Bの観測が単独で一意: {set_b}"
    both = set_a & set_b
    assert len(both) == 1, f"問2: 解が{len(both)}個 {both}"
    h = both.pop()
    c_lights = lights_seen(h, 180)
    print(f"問2 A単独候補: {sorted(DIRS[x // 45] for x in set_a)}")
    print(f"問2 B単独候補: {sorted(DIRS[x // 45] for x in set_b)}")
    print(f"問2 唯一解: 機首方位 {DIRS[h // 45]} ({h}°), "
          f"Cに見える灯火: {sorted(c_lights)}")
    return h, c_lights


if __name__ == "__main__":
    q1()
    q2()
    print("検証OK: 問1・問2とも唯一解")
