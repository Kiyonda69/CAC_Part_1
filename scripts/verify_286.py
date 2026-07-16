#!/usr/bin/env python3
"""航大思考286: 立方体骨組み（棒と玉）の規則性の検証

問1: 横一列にn個連結した立方体骨組みの棒(単位辺)と玉(格子点)
問2: n×n×n 格子状骨組みの棒の本数
総当たりで格子の単位辺・格子点を列挙して公式と照合する。
"""


def count_lattice(nx, ny, nz):
    """nx×ny×nz 個の単位立方体からなる格子の単位辺(棒)と格子点(玉)を総当たりで数える"""
    points = [(x, y, z)
              for x in range(nx + 1)
              for y in range(ny + 1)
              for z in range(nz + 1)]
    balls = len(points)
    rods = 0
    pset = set(points)
    for (x, y, z) in points:
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            if (x + dx, y + dy, z + dz) in pset:
                rods += 1
    return rods, balls


def q1():
    """問1: 横一列 n個連結。棒=8n+4, 玉=4n+4。差が60になる n の一意性"""
    solutions = []
    for n in range(1, 101):
        rods, balls = count_lattice(n, 1, 1)
        assert rods == 8 * n + 4, f"n={n}: rods {rods} != {8*n+4}"
        assert balls == 4 * n + 4, f"n={n}: balls {balls} != {4*n+4}"
        if rods - balls == 60:
            solutions.append(n)
    assert len(solutions) == 1, f"解が{len(solutions)}個存在: {solutions}"
    print(f"問1: 第1〜3番目の棒 = {[count_lattice(k,1,1)[0] for k in (1,2,3)]}")
    print(f"問1: 第1〜3番目の玉 = {[count_lattice(k,1,1)[1] for k in (1,2,3)]}")
    print(f"問1: 棒-玉=60 となるのは第{solutions[0]}番目（唯一解）")
    return solutions[0]


def q2():
    """問2: n×n×n 格子。棒=3n(n+1)²。第6番目の本数"""
    seq = []
    for n in range(1, 8):
        rods, balls = count_lattice(n, n, n)
        assert rods == 3 * n * (n + 1) ** 2, f"n={n}: rods {rods}"
        assert balls == (n + 1) ** 3, f"n={n}: balls {balls}"
        seq.append(rods)
    print(f"問2: 棒の本数列(n=1..7) = {seq}")
    ans = seq[5]
    # 主要な誤答（罠）の値も確認
    n = 6
    traps = {
        "3n^3(方向ごとn^3と誤る)": 3 * n ** 3,
        "3n^2(n+1)(次元の取り違え)": 3 * n ** 2 * (n + 1),
        "第5番目で打ち切り": seq[4],
        "第7番目(off-by-one)": seq[6],
    }
    for k, v in traps.items():
        assert v != ans, f"罠と正解が一致: {k}"
        print(f"  罠 {k} = {v}")
    print(f"問2: 第6番目の棒 = {ans}本（唯一解・公式一致）")
    return ans


if __name__ == "__main__":
    a1 = q1()
    a2 = q2()
    assert a1 == 15 and a2 == 882
    print("検証OK: 問1=第15番目, 問2=882本")
