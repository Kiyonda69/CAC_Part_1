#!/usr/bin/env python3
"""航大思考212: 立方体ブロックの貫通穴くり抜き問題の検証

問1: 3x3x3の小立方体27個からなる大立方体に3本の貫通穴
問2: 4x4x4の小立方体64個からなる大立方体に6本の貫通穴
残った小立方体の個数を包除原理で確認する。
座標系: x=左→右, y=前→奥, z=下→上（いずれも1始まり）
"""


def solve_q1():
    n = 3
    cubes = {(x, y, z) for x in range(1, n + 1)
             for y in range(1, n + 1) for z in range(1, n + 1)}
    removed = set()
    # 穴A: 前面の (x=2, z=2) から奥へ貫通（y方向）
    removed |= {(2, y, 2) for y in range(1, n + 1)}
    # 穴B: 上面の (x=2, y=2) から下へ貫通（z方向）
    removed |= {(2, 2, z) for z in range(1, n + 1)}
    # 穴C: 右面の (y=1, z=2) から左へ貫通（x方向）
    removed |= {(x, 1, 2) for x in range(1, n + 1)}
    remaining = len(cubes) - len(removed)
    print(f"問1: 全体{len(cubes)} 除去{len(removed)} 残り{remaining}")
    # 交差の確認
    holes = [
        {(2, y, 2) for y in range(1, n + 1)},
        {(2, 2, z) for z in range(1, n + 1)},
        {(x, 1, 2) for x in range(1, n + 1)},
    ]
    for i in range(3):
        for j in range(i + 1, 3):
            inter = holes[i] & holes[j]
            if inter:
                print(f"  穴{i+1}∩穴{j+1} = {sorted(inter)}")
    assert remaining == 20, remaining
    # 罠: 交差無視 27-9=18
    print("  罠(交差無視): 27-9=18")
    return remaining


def solve_q2():
    n = 4
    cubes = {(x, y, z) for x in range(1, n + 1)
             for y in range(1, n + 1) for z in range(1, n + 1)}
    holes = [
        # 前面から（y方向貫通）
        {(2, y, 3) for y in range(1, n + 1)},  # P1: x=2, z=3
        {(4, y, 1) for y in range(1, n + 1)},  # P2: x=4, z=1
        # 右面から（x方向貫通）
        {(x, 2, 3) for x in range(1, n + 1)},  # Q1: y=2, z=3
        {(x, 3, 2) for x in range(1, n + 1)},  # Q2: y=3, z=2
        # 上面から（z方向貫通）
        {(2, 2, z) for z in range(1, n + 1)},  # R1: x=2, y=2
        {(3, 3, z) for z in range(1, n + 1)},  # R2: x=3, y=3
    ]
    removed = set()
    for h in holes:
        removed |= h
    remaining = len(cubes) - len(removed)
    print(f"問2: 全体{len(cubes)} 除去{len(removed)} 残り{remaining}")
    names = ["P1", "P2", "Q1", "Q2", "R1", "R2"]
    for i in range(6):
        for j in range(i + 1, 6):
            inter = holes[i] & holes[j]
            if inter:
                print(f"  {names[i]}∩{names[j]} = {sorted(inter)}")
    # 三重交差点の確認
    triple = holes[0] & holes[2] & holes[4]
    print(f"  三重交差 P1∩Q1∩R1 = {sorted(triple)}")
    assert remaining == 43, remaining
    # 罠: 交差無視 64-24=40 / 三重交差を二重と数える 64-22=42
    print("  罠(交差無視): 64-24=40, 罠(三重を二重扱い): 42")
    return remaining


if __name__ == "__main__":
    a1 = solve_q1()
    a2 = solve_q2()
    print(f"\n問1の答え: {a1}個 / 問2の答え: {a2}個")
    print("検証OK: いずれも唯一解")
