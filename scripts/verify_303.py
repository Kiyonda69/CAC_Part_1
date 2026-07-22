#!/usr/bin/env python3
"""航大思考303 検証スクリプト
段々ピラミッド（第n番目: 1×1, 2×2, ..., n×n の層を積んだ立体）の
表面積と立方体個数をボクセル総当たりで検証する。
"""


def build_voxels(n):
    """第n番目の立体のボクセル集合を返す。
    層k (k=1..n) はサイズk×k、高さ z=n-k（下から数えて層nが z=0）。
    各層は角(0,0)をそろえて積む（表面積は中央そろえでも同じ）。
    """
    voxels = set()
    for k in range(1, n + 1):
        z = n - k
        for x in range(k):
            for y in range(k):
                voxels.add((x, y, z))
    return voxels


def surface_area(voxels):
    """露出面の総数（1面=1cm²）を数える。"""
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    area = 0
    for (x, y, z) in voxels:
        for dx, dy, dz in dirs:
            if (x + dx, y + dy, z + dz) not in voxels:
                area += 1
    return area


def verify_q1():
    """問1: 第6番目の表面積が156cm²で唯一であることを確認。"""
    # 公式 S(n) = 4n^2 + 2n をボクセル計算と照合
    for n in range(1, 13):
        v = build_voxels(n)
        s = surface_area(v)
        formula = 4 * n * n + 2 * n
        assert s == formula, f"n={n}: voxel={s}, formula={formula}"
    seq = [surface_area(build_voxels(n)) for n in range(1, 7)]
    print(f"問1 表面積の列(1〜6番目): {seq}")
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    print(f"    階差: {diffs}（公差8の等差数列）")
    answer = seq[5]
    assert answer == 156, f"第6番目の表面積が{answer}"
    options = [110, 148, 156, 164, 210]
    matches = [o for o in options if o == answer]
    assert len(matches) == 1, f"選択肢中の一致が{len(matches)}個"
    print(f"問1 正解値: {answer} cm²（選択肢中の一致は唯一）")


def verify_q2():
    """問2: 個数が表面積を初めて上回るのが第12番目で唯一であることを確認。"""
    first = None
    for n in range(1, 21):
        v = build_voxels(n)
        cubes = len(v)
        s = surface_area(v)
        total = n * (n + 1) * (2 * n + 1) // 6
        assert cubes == total, f"n={n}: 個数式が不一致"
        if n <= 13:
            rel = ">" if cubes > s else ("=" if cubes == s else "<")
            print(f"  n={n:2d}: 個数={cubes:4d} {rel} 表面積={s:4d}")
        if first is None and cubes > s:
            first = n
    assert first == 12, f"初めて上回るのは第{first}番目"
    # 第11番目はちょうど等しい（506=506）ことも確認
    v11 = build_voxels(11)
    assert len(v11) == surface_area(v11) == 506
    options = [10, 11, 12, 13, 14]
    matches = [o for o in options if o == first]
    assert len(matches) == 1
    print(f"問2 正解値: 第{first}番目（第11番目は506で等値・選択肢中の一致は唯一）")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証OK: 問1・問2とも解は唯一")
