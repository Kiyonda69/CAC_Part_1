#!/usr/bin/env python3
"""航大思考265 検証スクリプト
問1: 一辺2の正方形が直線上を滑らずに転がるときの頂点Pの軌跡（形状）
問2: 縦1・横2の長方形が転がるときの頂点Pの軌跡の長さ
"""
import math


def roll_polygon(vertices, p_index, n_rolls):
    """直線(x軸)上を右へ滑らずに転がる凸多角形の追跡点Pの弧を返す。

    vertices: 反時計回りの頂点リスト（最初は底辺がx軸上にある配置）
    p_index: 追跡する頂点の番号
    n_rolls: 90度回転（多角形なら外角回転）の回数
    返り値: [(半径, 回転角ラジアン, 中心座標), ...]
    """
    pts = [complex(x, y) for x, y in vertices]
    p = pts[p_index]
    arcs = []
    for _ in range(n_rolls):
        # 回転軸 = 現在最も右下にある接地頂点（x最大かつy=0）
        ground = [z for z in pts if abs(z.imag) < 1e-9]
        pivot = max(ground, key=lambda z: z.real)
        # 回転角 = 外角。次にx軸に接する辺が決まるまで時計回りに回す
        # pivotを始点とする辺のうち、回転後に接地する辺を探す
        # 凸多角形: pivotから反時計回り側の隣接頂点が次に接地する
        # 単純に「pivot以外の頂点で、pivotから見た偏角が最小の点」が次接地点
        others = [z for z in pts if abs(z - pivot) > 1e-9]
        next_touch = min(others, key=lambda z: math.atan2((z - pivot).imag,
                                                          (z - pivot).real))
        ang = math.atan2((next_touch - pivot).imag, (next_touch - pivot).real)
        theta = ang  # 時計回りにangだけ回すと next_touch が x軸上に来る
        radius = abs(p - pivot)
        arcs.append((radius, theta, (pivot.real, pivot.imag)))
        rot = complex(math.cos(-theta), math.sin(-theta))
        pts = [pivot + (z - pivot) * rot for z in pts]
        # 数値誤差の除去
        pts = [complex(round(z.real, 9), round(z.imag, 9)) for z in pts]
        p = pivot + (p - pivot) * rot
        p = complex(round(p.real, 9), round(p.imag, 9))
    return arcs


def verify_q1():
    """問1: 一辺2の正方形、頂点P=左下(接地)、元の向きに戻るまで4回転"""
    s = 2.0
    square = [(0, 0), (s, 0), (s, s), (0, s)]  # P = index 0（左下）
    arcs = roll_polygon(square, 0, 4)
    radii = [round(r, 6) for r, t, c in arcs]
    angles = [round(math.degrees(t), 6) for r, t, c in arcs]
    # 期待値: 半径2, 2√2, 2, 0（4回目はP自身が軸なので弧なし）
    expected = [s, round(s * math.sqrt(2), 6), s, 0.0]
    assert radii == expected, f"半径列が想定外: {radii}"
    assert angles == [90.0] * 4, f"回転角が想定外: {angles}"
    # 実際に描かれる弧は3つ（半径0を除く）、いずれも四分円
    drawn = [r for r in radii if r > 0]
    assert drawn == [2.0, round(2 * math.sqrt(2), 6), 2.0]
    length = sum(r * math.pi / 2 for r, t, c in arcs)
    assert abs(length - (2 + math.sqrt(2)) * math.pi) < 1e-6
    print("問1 OK: 弧は3つ（四分円）、半径 = 2, 2√2, 2")
    print(f"  中央の弧だけ半径が大きい（2√2 ≈ {2*math.sqrt(2):.3f}）")
    print(f"  軌跡の長さ = (2+√2)π ≈ {length:.4f}")
    return radii


def verify_q2():
    """問2: 横2・縦1の長方形、頂点P=左下、元の向きに戻るまで4回転"""
    w, h = 2.0, 1.0
    rect = [(0, 0), (w, 0), (w, h), (0, h)]  # P = index 0（左下）
    arcs = roll_polygon(rect, 0, 4)
    radii = [round(r, 6) for r, t, c in arcs]
    angles = [round(math.degrees(t), 6) for r, t, c in arcs]
    d = math.sqrt(w * w + h * h)
    expected = [w, round(d, 6), h, 0.0]
    assert radii == expected, f"半径列が想定外: {radii}"
    assert angles == [90.0] * 4, f"回転角が想定外: {angles}"
    length = sum(r * math.pi / 2 for r, t, c in arcs)
    exact = (w + h + d) * math.pi / 2  # = (3+√5)π/2
    assert abs(length - exact) < 1e-6
    print(f"問2 OK: 弧は3つ（四分円）、半径 = 2, √5, 1")
    print(f"  軌跡の長さ = (3+√5)π/2 ≈ {length:.4f}")
    # 誤答選択肢との重複がないことを確認
    candidates = {
        "(3+√5)π/2": (3 + math.sqrt(5)) * math.pi / 2,   # 正解
        "(2+√5)π/2": (2 + math.sqrt(5)) * math.pi / 2,   # 最後の弧を見落とし
        "(4+√5)π/2": (4 + math.sqrt(5)) * math.pi / 2,   # 4本目の弧を加算
        "(3+√5)π": (3 + math.sqrt(5)) * math.pi,          # 半円と誤解
        "3π": 3 * math.pi,                                 # 対角線√5を2と誤り(2+2+1)... = 5π/2? -> 使わず単純誤答
    }
    vals = sorted(candidates.values())
    assert all(abs(a - b) > 1e-6 for a, b in zip(vals, vals[1:])), "選択肢が重複"
    print("  選択肢5値はすべて相異なる")
    return length


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n全検証OK: 解は一意に定まる")
