#!/usr/bin/env python3
"""
航大思考71 - 解の一意性検証スクリプト
問1: 地形の断面図から等高線図を選ぶ（空間視覚化）
問2: 穴のある円柱の切断面を選ぶ（空間視覚化）
"""

import math


def verify_q1():
    """問1: 地形の等高線図の検証

    地形モデル: 2つのガウスピークの和
    - 主峰: 中心(2.5, 3.0), 高さ4.0, σx=1.2, σy=1.5
    - 副峰: 中心(5.5, 3.0), 高さ2.5, σx=0.5, σy=1.0
    """
    print("=" * 60)
    print("問1: 地形の断面図から等高線図を選ぶ")
    print("=" * 60)

    def terrain(x, y):
        z1 = 4.0 * math.exp(-((x - 2.5) ** 2 / (2 * 1.2 ** 2) + (y - 3.0) ** 2 / (2 * 1.5 ** 2)))
        z2 = 2.5 * math.exp(-((x - 5.5) ** 2 / (2 * 0.5 ** 2) + (y - 3.0) ** 2 / (2 * 1.0 ** 2)))
        return z1 + z2

    # XZ断面 (y=3.0) の検証
    print("\n【XZ断面 (y=3.0)の検証】")
    peaks = []
    prev_z, prev_slope = 0, 0
    for i in range(1, 701):
        x = i * 0.01
        z = terrain(x, 3.0)
        slope = z - prev_z
        if prev_slope > 0 and slope <= 0:
            peaks.append((x, z))
        prev_z, prev_slope = z, slope

    print(f"  ピーク数: {len(peaks)}")
    for j, (px, pz) in enumerate(peaks):
        print(f"  ピーク{j + 1}: x={px:.2f}, z={pz:.2f}")

    assert len(peaks) == 2, f"XZ断面のピーク数が{len(peaks)}（2であるべき）"
    assert peaks[0][1] > peaks[1][1], "主峰は副峰より高くなければならない"
    assert peaks[0][0] < peaks[1][0], "主峰は副峰より左になければならない"

    # YZ断面 (x=2.5) の検証
    print("\n【YZ断面 (x=2.5)の検証】")
    peaks_yz = []
    prev_z, prev_slope = 0, 0
    for i in range(1, 601):
        y = i * 0.01
        z = terrain(2.5, y)
        slope = z - prev_z
        if prev_slope > 0 and slope <= 0:
            peaks_yz.append((y, z))
        prev_z, prev_slope = z, slope

    print(f"  ピーク数: {len(peaks_yz)}")
    for j, (py, pz) in enumerate(peaks_yz):
        print(f"  ピーク{j + 1}: y={py:.2f}, z={pz:.2f}")

    assert len(peaks_yz) == 1, f"YZ断面のピーク数が{len(peaks_yz)}（1であるべき）"

    # 等高線の特性検証（各高さでの領域）
    print("\n【等高線の特性】")
    for level in [0.5, 1.0, 2.0, 3.0]:
        main_above = False
        sub_above = False
        for ix in range(701):
            x = ix * 0.01
            for iy in range(601):
                y = iy * 0.01
                if terrain(x, y) > level:
                    if x < 4.0:
                        main_above = True
                    if x > 4.0:
                        sub_above = True
        print(f"  z={level}: 主峰域={'あり' if main_above else 'なし'}, "
              f"副峰域={'あり' if sub_above else 'なし'}")

    # 各選択肢の評価
    print("\n【選択肢の評価】")
    # 正しい等高線の条件:
    # C1: 2つの独立した等高線群が存在する
    # C2: 左側（主峰）の等高線が大きい
    # C3: 右側（副峰）の等高線が小さい
    # C4: 等高線は東西方向に並ぶ（南北ではない）

    options = {
        1: {"peaks": 1, "main_size": "large", "sub_size": None,
            "alignment": "centered", "desc": "単一の大きな円形等高線"},
        2: {"peaks": 2, "main_size": "medium", "sub_size": "medium",
            "alignment": "east-west", "desc": "2つの等しい大きさの等高線"},
        3: {"peaks": 1, "main_size": "large", "sub_size": None,
            "alignment": "north-south", "desc": "南北方向に細長い等高線"},
        4: {"peaks": 2, "main_size": "large", "sub_size": "small",
            "alignment": "east-west", "desc": "大きな主峰等高線＋小さな副峰等高線"},
        5: {"peaks": 3, "main_size": "small", "sub_size": "small",
            "alignment": "triangle", "desc": "3つの小さな等高線"},
    }

    correct_count = 0
    for opt, info in options.items():
        c1 = info["peaks"] == 2
        c2 = info["main_size"] == "large"
        c3 = info["sub_size"] == "small"
        c4 = info["alignment"] == "east-west"
        is_correct = c1 and c2 and c3 and c4
        if is_correct:
            correct_count += 1
        mark = "★正解" if is_correct else "×不正解"
        print(f"  ({opt}) {info['desc']}")
        print(f"      C1(2峰)={c1}, C2(主峰大)={c2}, C3(副峰小)={c3}, C4(東西配列)={c4} → {mark}")

    assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
    print(f"\n正解: (4)")
    return True


def verify_q2():
    """問2: 穴のある円柱の切断面の検証

    円柱: 半径3, 高さ10（鉛直軸）
    - 上部: 円柱型盲穴（半径1.5, 深さ3）
    - 底部: 円錐型穴（底面半径2, 頂点高さ3）
    - 側面: 水平貫通穴（半径0.7, 高さz=6）
    切断面: 中心軸を含む鉛直面（貫通穴に垂直）
    """
    print("\n" + "=" * 60)
    print("問2: 穴のある円柱の切断面")
    print("=" * 60)

    R = 3.0       # 円柱半径
    H = 10.0      # 円柱高さ
    r_blind = 1.5  # 上部盲穴の半径
    d_blind = 3.0  # 上部盲穴の深さ
    r_cone = 2.0   # 底部円錐の底面半径
    h_cone = 3.0   # 底部円錐の頂点高さ
    r_hole = 0.7   # 横穴の半径
    z_hole = 6.0   # 横穴の高さ

    print(f"\n【立体仕様】")
    print(f"  円柱: 半径{R}, 高さ{H}")
    print(f"  上部穴: 円柱型, 半径{r_blind}, 深さ{d_blind}")
    print(f"  底部穴: 円錐型, 底面半径{r_cone}, 頂点高さ{h_cone}")
    print(f"  横穴: 半径{r_hole}, 高さz={z_hole}")

    # 切断面の形状解析
    print(f"\n【切断面の形状（中心軸を含む鉛直面、横穴に垂直）】")

    print(f"  外形: {2 * R}×{H} の長方形")
    print(f"  上部: {2 * r_blind}×{d_blind} の長方形切り欠き（円柱穴の軸断面）")
    print(f"  底部: 底辺{2 * r_cone}×高さ{h_cone} の二等辺三角形切り欠き（円錐穴の軸断面）")
    print(f"  中央: 半径{r_hole}の円（横穴の垂直断面、z={z_hole}の位置）")

    # 幾何学的整合性の検証
    print(f"\n【整合性検証】")
    assert r_blind <= R, "上部穴が円柱をはみ出している"
    print(f"  上部穴: 半径{r_blind} <= 円柱半径{R} → OK")
    assert r_cone <= R, "底部円錐が円柱をはみ出している"
    print(f"  底部円錐: 半径{r_cone} <= 円柱半径{R} → OK")
    assert r_hole <= R, "横穴が円柱をはみ出している"
    print(f"  横穴: 半径{r_hole} <= 円柱半径{R} → OK")

    # 各特徴が重ならないか
    top_range = (H - d_blind, H)                     # z=7 to z=10
    bot_range = (0, h_cone)                           # z=0 to z=3
    hole_range = (z_hole - r_hole, z_hole + r_hole)   # z=5.3 to z=6.7

    assert top_range[0] > hole_range[1], "上部穴と横穴が重複"
    assert hole_range[0] > bot_range[1], "横穴と底部円錐が重複"
    print(f"  上部穴: z={top_range[0]:.1f}〜{top_range[1]:.1f}")
    print(f"  横穴:   z={hole_range[0]:.1f}〜{hole_range[1]:.1f}")
    print(f"  底部穴: z={bot_range[0]:.1f}〜{bot_range[1]:.1f}")
    print(f"  → 重複なし → OK")

    # 選択肢の検証
    print(f"\n【選択肢の検証】")
    options = {
        1: {"top": "rectangle", "bottom": "rectangle", "hole": True,
            "desc": "上=長方形, 下=長方形, 穴=あり"},
        2: {"top": "rectangle", "bottom": "triangle", "hole": True,
            "desc": "上=長方形, 下=三角形, 穴=あり ★正解"},
        3: {"top": "rectangle", "bottom": "triangle", "hole": False,
            "desc": "上=長方形, 下=三角形, 穴=なし"},
        4: {"top": "triangle", "bottom": "rectangle", "hole": True,
            "desc": "上=三角形, 下=長方形, 穴=あり（上下逆）"},
        5: {"top": "rectangle", "bottom": "semicircle", "hole": True,
            "desc": "上=長方形, 下=半円, 穴=あり"},
    }

    correct_count = 0
    for opt, info in options.items():
        is_correct = (info["top"] == "rectangle" and
                      info["bottom"] == "triangle" and
                      info["hole"] is True)
        if is_correct:
            correct_count += 1
        mark = "★正解" if is_correct else "×不正解"
        print(f"  ({opt}) {info['desc']} → {mark}")

        if not is_correct:
            reasons = []
            if info["top"] != "rectangle":
                reasons.append(f"上部が{info['top']}（正解: rectangle）")
            if info["bottom"] != "triangle":
                reasons.append(f"底部が{info['bottom']}（正解: triangle）")
            if not info["hole"]:
                reasons.append("横穴の断面が欠落")
            print(f"       理由: {', '.join(reasons)}")

    assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
    print(f"\n正解: (2)")
    return True


if __name__ == "__main__":
    print("航大思考71 - 解の一意性検証\n")

    q1_ok = verify_q1()
    q2_ok = verify_q2()

    print("\n" + "=" * 60)
    if q1_ok and q2_ok:
        print("全ての検証に成功しました。")
        print("問1 正解: (4) - 大きな主峰等高線＋小さな副峰等高線")
        print("問2 正解: (2) - 長方形外形＋長方形切り欠き（上）＋三角形切り欠き（下）＋円（横穴）")
    else:
        print("検証に失敗しました。")
    print("=" * 60)
