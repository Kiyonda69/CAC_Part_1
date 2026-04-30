#!/usr/bin/env python3
"""
問題131: ハイポサイクロイド（内転円）の軌跡検証

問1: 半径3の円内で半径1の円を転がす場合
問2: 半径4の円内で半径1の円を転がす場合
（問2は半径を大きくして推論ステップを増やした高難度版）

ハイポサイクロイドの参数方程式：
x = (R - r) * cos(t) + d * cos((R - r) / r * t)
y = (R - r) * sin(t) - d * sin((R - r) / r * t)

R: 大円の半径
r: 小円の半径
d: 接点から測定する距離（通常 = r）
"""

import math
import json

def hypocycloid(R, r, d, t):
    """
    ハイポサイクロイドの点を計算

    Args:
        R: 大円の半径
        r: 小円の半径
        d: 接点から測定する距離
        t: パラメータ（0 から 2π まで）

    Returns:
        (x, y) 座標
    """
    x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
    y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
    return x, y

def analyze_hypocycloid(R, r, d, num_points=360):
    """
    ハイポサイクロイドの特性を分析

    Args:
        R: 大円の半径
        r: 小円の半径
        d: 接点から測定する距離
        num_points: 軌跡計算のサンプル点数

    Returns:
        dict: 軌跡の特性
    """
    points = []
    cusps = []  # 尖点

    # 一周分の軌跡を計算
    # 小円が大円を一周するには 2π * R/r のパラメータが必要
    period = 2 * math.pi * R / r

    for i in range(num_points + 1):
        t = (i / num_points) * period
        x, y = hypocycloid(R, r, d, t)
        points.append((x, y))

    # 軌跡の最大最小を計算
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    max_x = max(xs)
    min_x = min(xs)
    max_y = max(ys)
    min_y = min(ys)

    # 比率 R/r から尖点数を特定
    cusp_count = R // r if R % r == 0 else None

    return {
        "R": R,
        "r": r,
        "d": d,
        "ratio": R / r,
        "cusp_count": cusp_count,
        "x_range": (min_x, max_x),
        "y_range": (min_y, max_y),
        "is_line": abs(R - 2*r) < 1e-6,  # R = 2r の場合は直線
        "description": describe_hypocycloid(R, r)
    }

def describe_hypocycloid(R, r):
    """
    ハイポサイクロイドの軌跡を説明
    """
    ratio = R / r

    if ratio == 2:
        return "直線（R = 2r の場合、軌跡は大円の直径）"
    elif ratio == 3:
        return "デルトイド（3つの尖点を持つ曲線）"
    elif ratio == 4:
        return "アストロイド（4つの尖点を持つ星形）"
    elif ratio == 5:
        return "5尖点の星形曲線"
    else:
        return f"{int(ratio)}尖点の星形曲線（または分数倍数）"

def main():
    """問1と問2の軌跡を分析"""

    print("=" * 70)
    print("問題131: ハイポサイクロイド（内転円）の軌跡検証")
    print("=" * 70)

    # 問1: R=3, r=1, d=1
    print("\n【問1】半径3の円内で半径1の円を転がす場合")
    print("-" * 70)
    analysis1 = analyze_hypocycloid(R=3, r=1, d=1)
    print(f"大円の半径 R = {analysis1['R']}")
    print(f"小円の半径 r = {analysis1['r']}")
    print(f"接点までの距離 d = {analysis1['d']}")
    print(f"半径比 R/r = {analysis1['ratio']}")
    print(f"軌跡の特性: {analysis1['description']}")
    print(f"尖点の個数: {analysis1['cusp_count']}")
    print(f"X軸の範囲: [{analysis1['x_range'][0]:.2f}, {analysis1['x_range'][1]:.2f}]")
    print(f"Y軸の範囲: [{analysis1['y_range'][0]:.2f}, {analysis1['y_range'][1]:.2f}]")

    # 問2: R=4, r=1, d=1
    print("\n【問2】半径4の円内で半径1の円を転がす場合")
    print("-" * 70)
    analysis2 = analyze_hypocycloid(R=4, r=1, d=1)
    print(f"大円の半径 R = {analysis2['R']}")
    print(f"小円の半径 r = {analysis2['r']}")
    print(f"接点までの距離 d = {analysis2['d']}")
    print(f"半径比 R/r = {analysis2['ratio']}")
    print(f"軌跡の特性: {analysis2['description']}")
    print(f"尖点の個数: {analysis2['cusp_count']}")
    print(f"X軸の範囲: [{analysis2['x_range'][0]:.2f}, {analysis2['x_range'][1]:.2f}]")
    print(f"Y軸の範囲: [{analysis2['y_range'][0]:.2f}, {analysis2['y_range'][1]:.2f}]")

    # 参考: 問8との比較
    print("\n【参考】問8との比較")
    print("-" * 70)
    analysis_q8 = analyze_hypocycloid(R=2, r=1, d=1)
    print(f"問8: R=2, r=1, d=1")
    print(f"軌跡の特性: {analysis_q8['description']}")
    print(f"（問8の軌跡は直線で、これが最も識別しやすいパターン）")

    print("\n" + "=" * 70)
    print("結論:")
    print("=" * 70)
    print("問1の正解: デルトイド（3つの尖点）")
    print("問2の正解: アストロイド（4つの尖点を持つ星形）")
    print("=" * 70)

if __name__ == "__main__":
    main()
