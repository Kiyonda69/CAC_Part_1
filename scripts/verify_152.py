#!/usr/bin/env python3
"""
航大思考152の検証スクリプト

問1: 3x3x3の立方体に穴を開けたとき、穴が開いていない小立方体の数を求める
問2: 正三角形上の6つの石の配置で、必ず正しいといえないものを選ぶ
"""

from itertools import permutations
from math import sqrt


def verify_problem1():
    """問1: 27個の小立方体のうち穴が開いていないものを数える

    座標系: (x, y, z) で 1 <= x,y,z <= 3
    - x: 左→右
    - y: 手前→奥
    - z: 下→上

    穴の構成:
    - 上面から垂直下方向: (x,y) = (1,1), (1,3), (3,1), (3,3) 4つ（四隅）
    - 手前面から後方向: (x,z) = (2,1), (2,3) 2つ（中央列の上下）
    """
    drilled = set()

    # 上面（z=3面）から垂直に穴を開ける
    top_holes = [(1, 1), (1, 3), (3, 1), (3, 3)]
    for x, y in top_holes:
        for z in range(1, 4):
            drilled.add((x, y, z))

    # 手前面（y=1面）から奥方向に穴を開ける
    front_holes = [(2, 1), (2, 3)]
    for x, z in front_holes:
        for y in range(1, 4):
            drilled.add((x, y, z))

    total_cubes = 27
    drilled_count = len(drilled)
    not_drilled_count = total_cubes - drilled_count

    print(f"問1: ドリル穴が通った小立方体: {drilled_count}個")
    print(f"問1: 穴が開いていない小立方体: {not_drilled_count}個")

    # 各層を確認
    for z in [1, 2, 3]:
        not_drilled_in_layer = [
            (x, y, z) for x in range(1, 4) for y in range(1, 4)
            if (x, y, z) not in drilled
        ]
        print(f"  z={z}層 穴なし: {len(not_drilled_in_layer)}個 {not_drilled_in_layer}")

    assert not_drilled_count == 9, f"想定9個だが実際{not_drilled_count}個"
    return not_drilled_count


def verify_problem2():
    """問2: 6つの石P,Q,R,S,T,Uを6つの点ア,イ,ウ,エ,オ,カに配置

    点座標（辺の長さ2）:
    ア(1, √3) - 頂点(上)
    イ(0.5, √3/2) - 左側中点
    ウ(1.5, √3/2) - 右側中点
    エ(0, 0) - 左下頂点
    オ(1, 0) - 底辺中点
    カ(2, 0) - 右下頂点

    条件:
    i)   PはQ以外の石とは等距離の場所にいる
    ii)  Q, T, Uは一直線上に並んでいる
    iii) SはRの真右にいる（同じy座標、xが大きい）
    """
    points = {
        'ア': (1, sqrt(3)),
        'イ': (0.5, sqrt(3) / 2),
        'ウ': (1.5, sqrt(3) / 2),
        'エ': (0, 0),
        'オ': (1, 0),
        'カ': (2, 0),
    }

    point_names = ['ア', 'イ', 'ウ', 'エ', 'オ', 'カ']

    # 一直線上にあるかどうか
    def collinear(p1, p2, p3):
        x1, y1 = points[p1]
        x2, y2 = points[p2]
        x3, y3 = points[p3]
        # 外積が0なら一直線
        return abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) < 1e-9

    # 距離
    def dist(p1, p2):
        x1, y1 = points[p1]
        x2, y2 = points[p2]
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # 「真右」: 同じy、xが大きい
    def directly_right(target, base):
        """targetがbaseの真右にあるか"""
        x1, y1 = points[base]
        x2, y2 = points[target]
        return abs(y1 - y2) < 1e-9 and x2 > x1

    valid_assignments = []

    # P,Q,R,S,T,U の順序で6つの点に配置（順列）
    stones = ['P', 'Q', 'R', 'S', 'T', 'U']
    for perm in permutations(point_names):
        assignment = dict(zip(stones, perm))
        P, Q, R, S, T, U = (assignment[s] for s in stones)

        # 条件i: PはQ以外の4つの石(R,S,T,U)から等距離
        d_R = dist(P, R)
        d_S = dist(P, S)
        d_T = dist(P, T)
        d_U = dist(P, U)
        if not (abs(d_R - d_S) < 1e-9
                and abs(d_R - d_T) < 1e-9
                and abs(d_R - d_U) < 1e-9):
            continue

        # 条件ii: Q,T,Uは一直線上
        if not collinear(Q, T, U):
            continue

        # 条件iii: SはRの真右
        if not directly_right(S, R):
            continue

        valid_assignments.append(assignment)

    print(f"\n問2: 有効な配置数 {len(valid_assignments)}")
    for i, a in enumerate(valid_assignments):
        print(f"  配置{i + 1}: " + ", ".join(f"{k}={v}" for k, v in a.items()))

    # 各選択肢の検証
    # 各小三角形の3頂点
    small_triangles = [
        {'ア', 'イ', 'ウ'},   # 上
        {'イ', 'エ', 'オ'},   # 左下
        {'ウ', 'オ', 'カ'},   # 右下
        {'イ', 'ウ', 'オ'},   # 中央(逆三角形)
    ]
    bottom_edge = {'エ', 'オ', 'カ'}

    print("\n各選択肢の検証:")

    # (1) Pは三角形の頂点(ア,エ,カ)にはいない
    vertices = {'ア', 'エ', 'カ'}
    opt1 = all(a['P'] not in vertices for a in valid_assignments)
    print(f"  (1) Pは三角形の頂点にいない: {'常に正しい' if opt1 else '誤りの場合あり'}")

    # (2) Q,R,Sは底辺上にいる
    opt2 = all({a['Q'], a['R'], a['S']} <= bottom_edge for a in valid_assignments)
    print(f"  (2) Q,R,Sは底辺上にいる: {'常に正しい' if opt2 else '誤りの場合あり'}")

    # (3) PとSは1つの小さな正三角形上にいる
    opt3 = all(
        any({a['P'], a['S']} <= tri for tri in small_triangles)
        for a in valid_assignments
    )
    print(f"  (3) PとSは1つの小さな正三角形上にいる: {'常に正しい' if opt3 else '誤りの場合あり'}")

    # (4) Tはアにいる
    opt4 = all(a['T'] == 'ア' for a in valid_assignments)
    opt4_some = any(a['T'] == 'ア' for a in valid_assignments)
    print(f"  (4) Tはアにいる: {'常に正しい' if opt4 else '誤りの場合あり'} "
          f"(成立するケースあり: {opt4_some})")

    # (5) TとUは1つの小さな正三角形上にいる
    opt5 = all(
        any({a['T'], a['U']} <= tri for tri in small_triangles)
        for a in valid_assignments
    )
    print(f"  (5) TとUは1つの小さな正三角形上にいる: {'常に正しい' if opt5 else '誤りの場合あり'}")

    # 「必ず正しいといえないもの」を見つける
    not_always = []
    if not opt1:
        not_always.append(1)
    if not opt2:
        not_always.append(2)
    if not opt3:
        not_always.append(3)
    if not opt4:
        not_always.append(4)
    if not opt5:
        not_always.append(5)

    print(f"\n必ず正しいといえない選択肢: {not_always}")
    assert not_always == [4], f"選択肢(4)のみが必ず正しいとは言えないはずだが、{not_always}"

    return valid_assignments


if __name__ == "__main__":
    print("=" * 60)
    print("航大思考152 検証")
    print("=" * 60)
    verify_problem1()
    verify_problem2()
    print("\n=== すべての検証が成功 ===")
