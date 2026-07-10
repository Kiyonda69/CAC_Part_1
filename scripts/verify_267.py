#!/usr/bin/env python3
"""航大思考267 検証コード: 投影図（正面図・右側面図）からの積み木の個数

問1: 3×3の床面に立方体を積んだ立体。正面図の各列の高さ=(左3,中1,右2)、
     右側面図の各行の高さ=(奥2,中3,手前1)。マスに積まない（高さ0）ことも
     許されるとき、立方体の最少個数を求める。
問2: 3×3の床面全マスに1個以上積む（真上から見ると9マスすべて正方形）。
     正面図=(左2,中4,右3)、右側面図=(奥4,中2,手前3)。
     最多個数と最少個数の差を求める。
"""
from itertools import product


def solve(front, side, min_h, max_h):
    """front[j]=列jの最大高さ, side[i]=行iの最大高さ となる高さ配置を全探索"""
    counts = []
    n = len(front)
    for heights in product(range(min_h, max_h + 1), repeat=n * n):
        h = [heights[i * n:(i + 1) * n] for i in range(n)]
        if all(max(h[i][j] for i in range(n)) == front[j] for j in range(n)) \
           and all(max(h[i]) == side[i] for i in range(n)):
            counts.append(sum(heights))
    return counts


def q1():
    front = (3, 1, 2)   # 正面図: 左・中・右の列の高さ
    side = (2, 3, 1)    # 右側面図: 奥・中・手前の行の高さ
    counts = solve(front, side, min_h=0, max_h=3)
    lo, hi = min(counts), max(counts)
    print(f"問1: 有効配置 {len(counts)}通り / 最少 {lo}個 / 最多 {hi}個")
    assert lo == 6, f"最少個数が想定(6)と不一致: {lo}"
    assert hi == 14, f"最多個数が想定(14)と不一致: {hi}"
    # 最少を与える配置の例を表示
    for heights in product(range(0, 4), repeat=9):
        h = [heights[i * 3:(i + 1) * 3] for i in range(3)]
        if sum(heights) == lo \
           and all(max(h[i][j] for i in range(3)) == front[j] for j in range(3)) \
           and all(max(h[i]) == side[i] for i in range(3)):
            print(f"  最少配置例(奥→手前): {h}")
            break


def q2():
    front = (2, 4, 3)
    side = (4, 2, 3)
    counts = solve(front, side, min_h=1, max_h=4)  # 全マス1個以上
    lo, hi = min(counts), max(counts)
    print(f"問2: 有効配置 {len(counts)}通り / 最少 {lo}個 / 最多 {hi}個 / 差 {hi - lo}")
    assert lo == 15, f"最少個数が想定(15)と不一致: {lo}"
    assert hi == 23, f"最多個数が想定(23)と不一致: {hi}"
    assert hi - lo == 8, f"差が想定(8)と不一致: {hi - lo}"


if __name__ == "__main__":
    q1()
    q2()
    print("検証OK: 問1の最少個数=6、問2の差=23-15=8")
