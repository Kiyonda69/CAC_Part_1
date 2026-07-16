#!/usr/bin/env python3
"""航大思考282 検証: 立方体の頂点切り落とし（切頂立体）の面・辺・頂点数

問1: 立方体の8頂点を「各辺の3等分点（頂点に近い側）」を通る平面で切り落とす
     → 切り口同士は交わらない → 切頂立方体型
問2: 同じ立方体を「各辺の中点」を通る平面で切り落とす
     → 隣り合う切り口が辺の中点で接し、元の辺は消滅 → 立方八面体

検証方法: 実座標で凸多面体を構成し、面（支持平面ごとの頂点集合）・
辺（面の境界の共有）・頂点を直接数え、オイラーの定理 V-E+F=2 も確認する。
"""
from fractions import Fraction
from itertools import product


def truncated_cube_points(t):
    """1辺6の立方体の各頂点を、各辺上で頂点から距離 6*t の点を通る平面で切る。
    切断後の立体の頂点候補 = 各辺上の切断点（t=1/2では両側が一致）"""
    L = 6
    pts = set()
    corners = [tuple(Fraction(c) for c in p) for p in product([0, L], repeat=3)]
    for cx, cy, cz in corners:
        for axis in range(3):
            p = [cx, cy, cz]
            # 頂点から辺方向に L*t 進んだ点
            direction = 1 if p[axis] == 0 else -1
            p[axis] = p[axis] + direction * Fraction(t) * L
            pts.add(tuple(p))
    return sorted(pts)


def count_faces_edges(pts):
    """凸包の面を支持平面ごとに集計し、(面数, 辺数, 頂点数, 面種別) を返す。
    面の平面族: 立方体の6面 (x=0, x=6, y=0, y=6, z=0, z=6) と
    8頂点の切断面 (±x±y±z = c 型)。全頂点が半空間内にあることも確認。"""
    L = 6
    planes = []
    for axis in range(3):
        for val, sign in [(0, 1), (L, -1)]:
            # sign*(coord - val) >= 0 が立体側
            planes.append(("cube", axis, val, sign))
    for corner in product([0, L], repeat=3):
        planes.append(("cut", corner, None, None))
    faces = []
    for pl in planes:
        on_plane = []
        if pl[0] == "cube":
            _, axis, val, sign = pl
            for p in pts:
                d = sign * (p[axis] - val)
                assert d >= 0, "頂点が立体の外側にある"
                if d == 0:
                    on_plane.append(p)
        else:
            corner = pl[1]
            # 切断面: 頂点からの L1 距離 = 一定
            dists = [sum(abs(p[i] - corner[i]) for i in range(3)) for p in pts]
            dmin = min(dists)
            for p, d in zip(pts, dists):
                if d == dmin:
                    on_plane.append(p)
        if len(on_plane) >= 3:
            faces.append((pl[0], sorted(on_plane)))
    # 辺 = 同一面上の頂点を凸多角形として並べた境界。凸包なので
    # 各面の頂点数 = 多角形の辺数。辺は2面で共有される。
    total_face_edges = sum(len(f[1]) for f in faces)
    assert total_face_edges % 2 == 0
    E = total_face_edges // 2
    V = len(pts)
    F = len(faces)
    kinds = {}
    for kind, vs in faces:
        key = (kind, len(vs))
        kinds[key] = kinds.get(key, 0) + 1
    return F, E, V, kinds


def main():
    # 問1: t = 1/3（切り口は交わらない）
    pts1 = truncated_cube_points(Fraction(1, 3))
    F1, E1, V1, kinds1 = count_faces_edges(pts1)
    print(f"問1（3等分点で切断）: 面={F1}, 辺={E1}, 頂点={V1}, 内訳={kinds1}")
    assert V1 == 24, V1
    assert (F1, E1, V1) == (14, 36, 24)
    assert F1 - E1 + V1 == 2, "オイラーの定理不成立"
    assert kinds1 == {("cube", 8): 6, ("cut", 3): 8}  # 八角形6面+三角形8面

    # 問2: t = 1/2（切り口が中点で接し、元の辺が消滅）
    pts2 = truncated_cube_points(Fraction(1, 2))
    F2, E2, V2, kinds2 = count_faces_edges(pts2)
    print(f"問2（中点で切断）    : 面={F2}, 辺={E2}, 頂点={V2}, 内訳={kinds2}")
    assert V2 == 12, V2  # 24候補が中点で一致し12個
    assert (F2, E2, V2) == (14, 24, 12)
    assert F2 - E2 + V2 == 2, "オイラーの定理不成立"
    assert kinds2 == {("cube", 4): 6, ("cut", 3): 8}  # 正方形6面+三角形8面

    # 一意性: 選択肢候補の中で条件を満たす組は1つだけであることを確認
    q1_options = [(14, 36, 24), (14, 36, 16), (14, 24, 12),
                  (12, 36, 24), (14, 30, 20)]
    ok1 = [o for o in q1_options if o == (F1, E1, V1)]
    assert len(ok1) == 1, f"問1の解が{len(ok1)}個"
    q2_options = [(14, 24, 12), (14, 36, 24), (14, 24, 24),
                  (12, 24, 12), (14, 36, 12)]
    ok2 = [o for o in q2_options if o == (F2, E2, V2)]
    assert len(ok2) == 1, f"問2の解が{len(ok2)}個"
    print("検証OK: 問1=(面14,辺36,頂点24) / 問2=(面14,辺24,頂点12) いずれも唯一解")


if __name__ == "__main__":
    main()
