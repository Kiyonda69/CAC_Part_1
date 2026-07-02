#!/usr/bin/env python3
"""航大思考234 検証スクリプト（差し替え版）
問1: 同一立体の識別（5個の小立方体・回転一致は1つのみ、鏡像の罠）
問2: 仲間はずれ探し（5つの図のうち4つは同一立体の回転、1つだけ鏡像）
計算不要の純粋空間認識問題。回転24種の総当たりで一意性を検証する。
"""
from itertools import permutations, product


def rotations24():
    """3次元の回転行列24種（行列式+1のみ）を列挙"""
    mats = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3):
                m[i][perm[i]] = signs[i]
            det = (
                m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
            )
            if det == 1:
                mats.append(m)
    assert len(mats) == 24
    return mats


ROTS = rotations24()


def apply(m, c):
    return tuple(sum(m[i][j] * c[j] for j in range(3)) for i in range(3))


def normalize(cubes):
    """平行移動を除去して正規化"""
    mn = [min(c[i] for c in cubes) for i in range(3)]
    return frozenset(tuple(c[i] - mn[i] for i in range(3)) for c in cubes)


def all_orientations(cubes):
    """回転24種の正規化形の集合"""
    return {normalize([apply(m, c) for c in cubes]) for m in ROTS}


def mirror(cubes):
    return [(-x, y, z) for (x, y, z) in cubes]


def same_solid(a, b):
    """回転のみで一致するか（裏返し不可）"""
    return normalize(b) in all_orientations(a)


def is_chiral(cubes):
    return not same_solid(cubes, mirror(cubes))

# ============ 問1: 同一立体の識別 ============
# 立体A: 横3連の列＋右端の奥に1個＋左端の上に1個（キラルな5キューブ）
Q1_BASE = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (0, 0, 1)]

# 選択肢（描画する向きそのままの座標で定義）
Q1_OPTIONS = {
    "correct": [(0, 1, 0), (1, 1, 0), (2, 1, 0), (0, 0, 0), (2, 1, 1)],  # Aをz軸180°回転
    "mirror":  [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (2, 0, 1)],  # Aの鏡像（罠）
    "d1":      [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 0, 1)],  # 奥腕と上が同じ右端
    "d2":      [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (1, 0, 1)],  # 上が中央
    "d3":      [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (0, 0, 1)],  # 奥腕と上が同じ左端
}


def verify_q1():
    assert is_chiral(Q1_BASE), "問1: 立体Aがキラルでない（鏡像の罠が成立しない）"
    matches = [k for k, v in Q1_OPTIONS.items() if same_solid(Q1_BASE, v)]
    assert matches == ["correct"], f"問1: 一致する選択肢が {matches}"
    assert same_solid(mirror(Q1_BASE), Q1_OPTIONS["mirror"]), "問1: mirror選択肢が鏡像でない"
    for k in ("d1", "d2", "d3"):
        assert not same_solid(mirror(Q1_BASE), Q1_OPTIONS[k]), f"問1: {k}が鏡像と一致"
    print("問1 検証OK: 回転一致は correct のみ・mirrorは鏡像の罠として成立")


# ============ 問2: 仲間はずれ探し ============
# 共通立体Q: L字4キューブ（横3連＋右端の奥に1個）＋その奥の1個の上に1個
Q2_PIECE = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 1, 1)]

# 描画する5姿勢（R1/V/R3/R4はQの回転・Mだけが鏡像＝仲間はずれ）
Q2_VIEWS = {
    "R1": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 1, 1)],
    "V":  [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2)],
    "R3": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 0, 0), (1, 0, 1)],
    "R4": [(0, 2, 0), (0, 2, 1), (1, 0, 0), (1, 1, 0), (1, 2, 0)],
    "M":  [(0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 0), (2, 0, 0)],
}


def verify_q2():
    assert is_chiral(Q2_PIECE), "問2: 立体Qがキラルでない"
    odd = [k for k, v in Q2_VIEWS.items() if not same_solid(Q2_PIECE, v)]
    assert odd == ["M"], f"問2: 仲間はずれが {odd}"
    assert same_solid(mirror(Q2_PIECE), Q2_VIEWS["M"]), "問2: Mが鏡像でない"
    # R1〜R4が互いにすべて回転一致することも確認
    keys = ["R1", "V", "R3", "R4"]
    for i in range(4):
        for j in range(i + 1, 4):
            assert same_solid(Q2_VIEWS[keys[i]], Q2_VIEWS[keys[j]])
    print("問2 検証OK: 仲間はずれは M（鏡像）のみ・他4姿勢は相互に回転一致")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証OK")
