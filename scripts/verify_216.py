#!/usr/bin/env python3
"""航大思考216 検証コード: 立体ピースの嵌め合わせ（計算を使わない空間認識）

問1: 3×3×3立方体から5マス欠けた立体Aに、ぴったり嵌めて立方体を完成させる
     ピースを5つの候補から選ぶ。回転は自由、裏返し（鏡映）は不可。
問2: 2×2×3の直方体を3つのピース（各4マス）で組み立てる。ピースP・Qが
     与えられ、残り1つのピースを5つの候補から選ぶ。回転は自由。
"""
import itertools


def rotations24():
    """3次元の回転24種（軸の置換と符号で行列式+1のもの）"""
    mats = []
    for p in itertools.permutations(range(3)):
        for signs in itertools.product([1, -1], repeat=3):
            inv = sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])
            det = (-1) ** inv * signs[0] * signs[1] * signs[2]
            if det == 1:
                mats.append((p, signs))
    return mats


ROTS = rotations24()


def rotate(cells, rot):
    p, s = rot
    return frozenset(tuple(s[i] * c[p[i]] for i in range(3)) for c in cells)


def normalize(cells):
    mn = [min(c[i] for c in cells) for i in range(3)]
    return frozenset(tuple(c[i] - mn[i] for i in range(3)) for c in cells)


def all_orientations(cells):
    """回転24種の正規化形（鏡映は含まない）"""
    return {normalize(rotate(frozenset(cells), r)) for r in ROTS}


def fits_exactly(piece, cavity):
    """pieceを回転・平行移動して空洞cavityと完全一致できるか"""
    return normalize(frozenset(cavity)) in all_orientations(piece)


def mirror(cells):
    return frozenset((-x, y, z) for (x, y, z) in cells)


# ========== 問1 ==========
# 座標系: x=右(1..3), y=奥(1..3), z=上(1..3)
# 欠け: 上面手前の1列3マス ＋ 左端の1段下 ＋ 右端の1マス奥
CAVITY = frozenset({(3, 1, 3), (2, 1, 3), (1, 1, 3), (1, 1, 2), (3, 2, 3)})

Q1_OPTIONS = {
    1: ("U字型（バー3の両端に下向き1）",
        frozenset({(1, 1, 2), (2, 1, 2), (3, 1, 2), (1, 1, 1), (3, 1, 1)})),
    2: ("鏡像（正解を裏返した形）", mirror(CAVITY)),
    3: ("平面P型ペントミノ",
        frozenset({(1, 1, 1), (2, 1, 1), (3, 1, 1), (1, 2, 1), (2, 2, 1)})),
    4: ("正解（バー3・一端に下1・他端に奥1）", CAVITY),
    5: ("同端型（バー3・同じ端に下1と奥1）",
        frozenset({(1, 1, 3), (2, 1, 3), (3, 1, 3), (3, 1, 2), (3, 2, 3)})),
}


def verify_q1():
    # 正解ピースがキラル＝鏡像ピースは回転だけでは一致しないことを確認
    assert normalize(mirror(CAVITY)) not in all_orientations(CAVITY), \
        "欠け形状がアキラルのため鏡像の罠が成立しない"

    fitting = [n for n, (_, piece) in Q1_OPTIONS.items()
               if fits_exactly(piece, CAVITY)]
    assert fitting == [4], f"嵌まるピースが一意でない: {fitting}"
    print("問1: 嵌まるピースは選択肢(4)の形状のみ（鏡像・U字・同端型・平面P型は不一致）")
    for n, (name, piece) in Q1_OPTIONS.items():
        print(f"  形状{n} {name}: 嵌まる={fits_exactly(piece, CAVITY)}")


# ========== 問2 ==========
BOX = frozenset((x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1, 2))

P_TRIPOD = frozenset({(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)})   # 三脚型
Q_SKEW_L = frozenset({(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)})   # ねじれ型(左)

Q2_OPTIONS = {
    1: ("S字型（平面）", frozenset({(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)})),
    2: ("田型（2×2平面）", frozenset({(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)})),
    3: ("T字型（平面）", frozenset({(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0)})),
    4: ("ねじれ型(右)＝Qの鏡像", mirror(Q_SKEW_L)),
    5: ("L字型（平面）", frozenset({(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)})),
}


def placements(piece, region):
    """region内に収まるpieceの全配置（回転24種×平行移動）"""
    out = set()
    lo = [min(c[i] for c in region) for i in range(3)]
    hi = [max(c[i] for c in region) for i in range(3)]
    for ori in all_orientations(piece):
        for dx in range(lo[0], hi[0] + 1):
            for dy in range(lo[1], hi[1] + 1):
                for dz in range(lo[2], hi[2] + 1):
                    t = frozenset((c[0] + dx, c[1] + dy, c[2] + dz) for c in ori)
                    if t <= region:
                        out.add(t)
    return out


def can_complete(third):
    """P・Q・thirdの3ピースでBOXを過不足なく組めるか（総当たり）"""
    for a in placements(P_TRIPOD, BOX):
        for b in placements(Q_SKEW_L, BOX - a):
            rest = BOX - a - b
            if normalize(rest) in all_orientations(third):
                return True
    return False


def verify_q2():
    # Qがキラル＝鏡像（選択肢のねじれ型(右)）はQと回転で一致しないことを確認
    assert normalize(mirror(Q_SKEW_L)) not in all_orientations(Q_SKEW_L), \
        "Qがアキラルのため鏡像の罠が成立しない"

    completing = [n for n, (_, piece) in Q2_OPTIONS.items() if can_complete(piece)]
    assert completing == [3], f"完成できるピースが一意でない: {completing}"
    print("問2: 直方体を完成できる第3ピースは選択肢(3)のT字型のみ")
    for n, (name, piece) in Q2_OPTIONS.items():
        print(f"  形状{n} {name}: 完成可能={can_complete(piece)}")


if __name__ == "__main__":
    verify_q1()
    print()
    verify_q2()
    print("\n検証完了: 両問とも全候補の総当たり（回転24種×全配置）で唯一解を確認")
