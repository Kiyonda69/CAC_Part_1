#!/usr/bin/env python3
"""航大思考215 検証スクリプト
空間認識: 方位と旋回の追跡（デッドレコニング型）
問1: 90°旋回のみの5区間飛行 → 出発点からの直線距離と最終機首方位
問2: 45°/135°旋回を含む6区間飛行 → 出発点へ戻る旋回と距離
"""
import math

# 方位を北=0°、時計回りの度数で表す
DIRS = {0: "北", 45: "北東", 90: "東", 135: "南東",
        180: "南", 225: "南西", 270: "西", 315: "北西"}


def fly(start_heading, legs):
    """legs: (旋回角度[右=正/左=負, Noneは旋回なし], 距離) のリスト"""
    x, y = 0.0, 0.0
    h = start_heading
    for turn, dist in legs:
        if turn is not None:
            h = (h + turn) % 360
        rad = math.radians(h)
        # 北=+y, 東=+x
        x += dist * math.sin(rad)
        y += dist * math.cos(rad)
    return x, y, h


def verify_q1():
    legs = [
        (None, 4),    # 北へ4km
        (+90, 6),     # 右90° → 東へ6km
        (-90, 3),     # 左90° → 北へ3km
        (-90, 3),     # 左90° → 西へ3km
        (-90, 3),     # 左90° → 南へ3km
    ]
    x, y, h = fly(0, legs)
    dist = math.hypot(x, y)
    assert abs(x - 3) < 1e-9 and abs(y - 4) < 1e-9, f"位置誤り: ({x},{y})"
    assert abs(dist - 5) < 1e-9, f"距離誤り: {dist}"
    assert DIRS[h] == "南", f"方位誤り: {DIRS[h]}"
    # 選択肢（距離km, 方位）。正解は (5, 南) のみ一致することを確認
    options = [(4, "南"), (5, "南"), (5, "北"), (7, "南"), (5, "西")]
    matches = [o for o in options if abs(o[0] - dist) < 1e-9 and o[1] == DIRS[h]]
    assert len(matches) == 1 and matches[0] == (5, "南"), f"一意でない: {matches}"
    print(f"問1 OK: 最終位置({x:.0f},{y:.0f}) 距離{dist:.0f}km 機首{DIRS[h]} → 唯一解 (5km, 南)")


def verify_q2():
    s2 = math.sqrt(2)
    legs = [
        (None, 4),        # 東へ4km
        (-45, 2 * s2),    # 左45° → 北東へ2√2km
        (-45, 3),         # 左45° → 北へ3km
        (-90, 8),         # 左90° → 西へ8km
        (-45, 4 * s2),    # 左45° → 南西へ4√2km
        (+135, 5),        # 右135° → 北へ5km
    ]
    x, y, h = fly(90, legs)
    assert abs(x + 6) < 1e-9 and abs(y - 6) < 1e-9, f"位置誤り: ({x},{y})"
    assert DIRS[h] == "北", f"最終機首誤り: {DIRS[h]}"
    # 出発点Oへ戻る: P(-6,6) → O(0,0) は南東方向(135°)、距離6√2km
    back_bearing = math.degrees(math.atan2(0 - x, 0 - y)) % 360
    back_dist = math.hypot(x, y)
    assert abs(back_bearing - 135) < 1e-9, f"帰投方位誤り: {back_bearing}"
    assert abs(back_dist - 6 * s2) < 1e-9, f"帰投距離誤り: {back_dist}"
    # 必要旋回: 機首0°→135° = 右135°（左なら225°で、より小さい方を採用）
    turn = (back_bearing - h) % 360
    turn_dir, turn_deg = ("右", turn) if turn <= 180 else ("左", 360 - turn)
    assert (turn_dir, turn_deg) == ("右", 135), f"旋回誤り: {turn_dir}{turn_deg}"
    # 選択肢（旋回方向, 角度, 距離km）
    options = [
        ("右", 135, 6 * s2),
        ("左", 135, 6 * s2),
        ("右", 45, 6 * s2),
        ("右", 135, 12),
        ("右", 90, 6),
    ]
    matches = [o for o in options
               if o[0] == turn_dir and o[1] == turn_deg and abs(o[2] - back_dist) < 1e-9]
    assert len(matches) == 1 and matches[0] == ("右", 135, 6 * s2), f"一意でない: {matches}"
    print(f"問2 OK: 最終位置({x:.0f},{y:.0f}) 機首{DIRS[h]} → 唯一解 (右135°, 6√2km≈{back_dist:.2f}km)")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証パス: 両問とも唯一解")
