#!/usr/bin/env python3
"""航大思考280 検証スクリプト: 積み木立体・くり抜き立体の表面積

問1: 3x3の真上図（各マスの積み上げ個数）で表される積み木立体の表面積
問2: 3x3x3立方体から小立方体3個（頂点ア・辺の中央イ〔アと隣接〕・
     面の中央ウ〔他と非隣接〕）を取り除いた立体の表面積
"""


def surface_area(voxels):
    """単位立方体の集合の表面積（露出面の数）を数える"""
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    area = 0
    for (x, y, z) in voxels:
        for dx, dy, dz in dirs:
            if (x + dx, y + dy, z + dz) not in voxels:
                area += 1
    return area


def q1():
    # 真上から見た図（北=奥）: 奥の行から [3,1,2] / [2,2,1] / [1,1,1]
    heights = [[3, 1, 2],
               [2, 2, 1],
               [1, 1, 1]]
    voxels = set()
    for y, row in enumerate(heights):
        for x, h in enumerate(row):
            for z in range(h):
                voxels.add((x, y, z))
    n = len(voxels)
    area = surface_area(voxels)

    # 罠の検算: 6方向のシルエット合計（凹み部分の隠れ面を見落とした値）
    top = sum(1 for row in heights for h in row if h > 0)
    front = sum(max(heights[y][x] for y in range(3)) for x in range(3))
    side = sum(max(heights[y][x] for x in range(3)) for y in range(3))
    naive = top * 2 + front * 2 + side * 2

    print(f"[問1] 立方体の個数: {n}")
    print(f"[問1] 表面積: {area} cm^2")
    print(f"[問1] シルエット合計（罠）: {naive} cm^2")
    assert n == 14
    assert area == 46
    assert naive == 44
    options = [42, 44, 46, 48, 50]
    matches = [v for v in options if v == area]
    assert len(matches) == 1, "正解が選択肢中に一意でない"
    return area


def q2():
    # 3x3x3 のフル立方体
    full = {(x, y, z) for x in range(3) for y in range(3) for z in range(3)}
    assert surface_area(full) == 54

    # ア: 頂点 (2,0,2)（上・手前・右の3面露出）
    # イ: 上段手前の辺の中央 (1,0,2)（アと隣接、2面露出）
    # ウ: 左の面の中央 (0,1,1)（1面露出、ア・イと非隣接）
    removed = {(2, 0, 2), (1, 0, 2), (0, 1, 1)}
    for c in removed:
        assert c in full

    # 隣接関係の確認: ア-イ のみ隣接
    def adjacent(a, b):
        return sum(abs(p - q) for p, q in zip(a, b)) == 1
    assert adjacent((2, 0, 2), (1, 0, 2))
    assert not adjacent((2, 0, 2), (0, 1, 1))
    assert not adjacent((1, 0, 2), (0, 1, 1))

    solid = full - removed
    area = surface_area(solid)

    # 罠: 隣接を無視した「タイプ別増減の単純合計」 54+0+2+4=60
    naive = 54 + 0 + 2 + 4
    print(f"[問2] 残る小立方体: {len(solid)} 個")
    print(f"[問2] 表面積: {area} cm^2")
    print(f"[問2] 隣接無視の単純合計（罠）: {naive} cm^2")
    assert len(solid) == 24
    assert area == 58
    assert naive == 60
    options = [54, 56, 58, 60, 62]
    matches = [v for v in options if v == area]
    assert len(matches) == 1, "正解が選択肢中に一意でない"
    return area


if __name__ == "__main__":
    a1 = q1()
    a2 = q2()
    print(f"\n検証OK: 問1 = {a1} cm^2, 問2 = {a2} cm^2（いずれも唯一解）")
