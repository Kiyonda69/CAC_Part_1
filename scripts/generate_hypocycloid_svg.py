#!/usr/bin/env python3
"""
ハイポサイクロイド軌跡をSVGパスとして生成
"""

import math

def hypocycloid(R, r, d, t):
    """ハイポサイクロイドの座標を計算"""
    x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
    y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
    return x, y

def generate_svg_path(R, r, d, num_points=500, scale=1.0, offset_x=0, offset_y=0):
    """
    ハイポサイクロイドのSVGパスを生成

    Args:
        R: 大円の半径
        r: 小円の半径
        d: 接点までの距離
        num_points: サンプル点数
        scale: スケーリング係数
        offset_x, offset_y: オフセット

    Returns:
        SVGパスの文字列
    """
    path_data = []
    period = 2 * math.pi * R / r

    for i in range(num_points + 1):
        t = (i / num_points) * period
        x, y = hypocycloid(R, r, d, t)

        # スケーリングとオフセットを適用
        x = x * scale + offset_x
        y = y * scale + offset_y

        if i == 0:
            path_data.append(f"M {x:.1f} {y:.1f}")
        else:
            path_data.append(f"L {x:.1f} {y:.1f}")

    # パスを閉じる
    path_data.append("Z")

    return " ".join(path_data)

def main():
    # 問1: R=3, r=1, d=1 (デルトイド)
    print("<!-- 問1の軌跡: デルトイド（R=3, r=1） -->")
    print("<!-- 大円: 半径3, 小円: 半径1 -->")
    path1 = generate_svg_path(R=3, r=1, d=1, scale=50, offset_x=250, offset_y=150)
    print(f"Path for 問1: {path1}\n")

    # 問2: R=4, r=1, d=1 (アストロイド)
    print("<!-- 問2の軌跡: アストロイド（R=4, r=1） -->")
    print("<!-- 大円: 半径4, 小円: 半径1 -->")
    path2 = generate_svg_path(R=4, r=1, d=1, scale=40, offset_x=250, offset_y=150)
    print(f"Path for 問2: {path2}\n")

if __name__ == "__main__":
    main()
