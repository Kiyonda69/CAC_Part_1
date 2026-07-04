#!/usr/bin/env python3
"""航大思考244: スモークトレイル（飛行軌跡）の3方向投影の検証

座標系: x=東, y=北, z=上
問1: 南北の鉛直面(x=0)内の円形ループ（宙返りのスモークの輪）
問2: 半径一定・一定上昇率の螺旋（真上から見て時計回りに2周）

各視点への投影:
- 真上から: (x, y) 平面（北が上）
- 真東から: (y, z) 平面（水平軸=南北, 縦軸=高度）
"""
import math

N = 3600  # サンプル点数


def classify(points):
    """2次元点列を形状分類する: circle / spiral / segment_h / segment_v / line_diag / wave"""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    rx = max(xs) - min(xs)
    ry = max(ys) - min(ys)
    eps = 1e-9

    # 線分（水平・垂直）
    if rx < eps and ry > eps:
        return "segment_v"
    if ry < eps and rx > eps:
        return "segment_h"

    # 中心からの距離
    dists = [math.hypot(x - cx, y - cy) for x, y in points]
    dmin, dmax = min(dists), max(dists)
    if dmax - dmin < 1e-6:
        return "circle"  # 半径一定の閉曲線 → 円（渦巻きではない）

    # 直線（対角）判定: 最小二乗直線からの残差
    n = len(points)
    mx, my = cx, cy
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx > eps:
        slope = sxy / sxx
        resid = max(abs((y - my) - slope * (x - mx)) for x, y in zip(xs, ys))
        if resid < 1e-6:
            return "line_diag"

    # 波形判定: 縦軸が単調増加かつ横軸が振動（符号変化が2回以上）
    if all(ys[i] < ys[i + 1] for i in range(n - 1)):
        crossings = sum(
            1 for i in range(n - 1) if xs[i] == 0 or xs[i] * xs[i + 1] < 0
        )
        if crossings >= 2:
            return "wave_up"

    # 半径が単調に変化する回転曲線 → 渦巻き
    return "spiral"


def q1_shapes():
    """問1: 南北鉛直面内のループ（中心高度h, 半径R）"""
    R, h = 1.0, 2.0
    pts3d = []
    for i in range(N):
        t = 2 * math.pi * i / N
        x = 0.0                      # 東西方向の広がりなし
        y = R * math.cos(t)          # 南北
        z = h + R * math.sin(t)      # 高度
        pts3d.append((x, y, z))
    top = classify([(x, y) for x, y, z in pts3d])    # 真上から
    east = classify([(y, z) for x, y, z in pts3d])   # 真東から
    # 真上からは南北の線分 → segment_v（北が上の地図で縦線）
    return top, east


def q2_shapes():
    """問2: 半径一定Rで時計回り2周・一定上昇率の螺旋"""
    R, climb = 1.0, 0.5
    pts3d = []
    for i in range(N * 2):
        t = 4 * math.pi * i / (N * 2)          # 2周
        x = R * math.sin(t)                    # 時計回り(真上から)
        y = R * math.cos(t)
        z = climb * t
        pts3d.append((x, y, z))
    top = classify([(x, y) for x, y, z in pts3d])
    east = classify([(y, z) for x, y, z in pts3d])
    return top, east


def verify():
    # ---------- 問1 ----------
    t1_top, t1_east = q1_shapes()
    # 選択肢: (東から, 真上から)
    q1_options = {
        1: ("circle", "circle"),        # 上からも円（投影の理解不足）
        2: ("segment_h", "circle"),     # 東からを線分・上からを円と逆転
        3: ("segment_v", "segment_v"),  # 東からを南からと混同（鉛直線分）
        4: ("circle", "segment_v"),     # 正: 東=円, 上=南北線分
        5: ("circle", "segment_h"),     # 上からの線分の向きを東西と誤る
    }
    actual1 = (t1_east, t1_top)
    match1 = [k for k, v in q1_options.items() if v == actual1]
    assert t1_east == "circle" and t1_top == "segment_v", (t1_east, t1_top)
    assert len(match1) == 1, f"問1の解が{len(match1)}個: {match1}"

    # ---------- 問2 ----------
    t2_top, t2_east = q2_shapes()
    # 選択肢: (真上から, 東から)
    q2_options = {
        1: ("spiral", "line_diag"),   # 両方誤り
        2: ("circle", "line_diag"),   # 上昇の振動を無視した斜め直線
        3: ("spiral", "wave_up"),     # 上からを渦巻きと誤解
        4: ("circle", "two_circles"), # 側面は円が2つ重なると誤解
        5: ("circle", "wave_up"),     # 正: 上=1つの円, 東=波打ちながら上昇
    }
    actual2 = (t2_top, t2_east)
    match2 = [k for k, v in q2_options.items() if v == actual2]
    assert t2_top == "circle" and t2_east == "wave_up", (t2_top, t2_east)
    assert len(match2) == 1, f"問2の解が{len(match2)}個: {match2}"

    print("問1: 真東から =", t1_east, "/ 真上から =", t1_top, "→ 唯一解 OK")
    print("問2: 真上から =", t2_top, "/ 真東から =", t2_east, "→ 唯一解 OK")
    print("検証完了: 両問とも解は一意")


if __name__ == "__main__":
    verify()
