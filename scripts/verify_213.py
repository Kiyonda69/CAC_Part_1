#!/usr/bin/env python3
"""航大思考213 検証スクリプト

問1: 真上から見た図（各マスの積み上げ個数つき）から正面図を選ぶ問題
問2: 正面図と右側面図から立方体の個数の最大値・最小値の差を求める問題
"""
from itertools import product

# ============================================================
# 問1: 4x4 の高さグリッド（d=0が手前、x=0が左）
# ============================================================
GRID = [
    [1, 2, 0, 1],  # d=0 手前（正面側）
    [2, 0, 3, 1],  # d=1
    [0, 3, 1, 4],  # d=2
    [2, 1, 2, 0],  # d=3 奥
]


def front_view(grid):
    """正面（手前）から見たシルエット: 各列 x の奥行き方向最大値"""
    return [max(row[x] for row in grid) for x in range(4)]


def right_view(grid):
    """右側面から見たシルエット: 左→右が奥→手前"""
    return [max(grid[d]) for d in range(3, -1, -1)]


def verify_q1():
    fv = front_view(GRID)
    rv = right_view(GRID)
    total = sum(sum(row) for row in GRID)
    print(f"問1 正面図(左→右): {fv}")
    print(f"問1 右側面図(左→右=奥→手前): {rv}")
    print(f"問1 立方体総数: {total}")

    options = {
        1: [4, 3, 3, 2],  # 正面図の鏡像（背面から見た図）
        2: [2, 4, 3, 2],  # 右側面図
        3: [1, 2, 0, 1],  # 手前の1列のみの高さ
        4: [2, 3, 4, 4],  # 列3を1段高く誤読
        5: [2, 3, 3, 4],  # 正解
    }
    assert options[5] == fv, "正解選択肢が正面図と一致しない"
    matches = [k for k, v in options.items() if v == fv]
    assert matches == [5], f"正面図に一致する選択肢が複数/不在: {matches}"
    vals = [tuple(v) for v in options.values()]
    assert len(set(vals)) == 5, "選択肢に重複がある"
    print("問1 検証OK: 正解は(5)、選択肢はすべて異なる\n")


# ============================================================
# 問2: 正面図 f（列ごとの最大高さ）と右側面図から
#      個数の最大値・最小値を求める
# ============================================================
F = [3, 1, 4, 2]            # 正面図: x=0..3（左→右）の高さ
R_DISPLAY = [1, 3, 4, 2]    # 右側面図の表示: 左→右 = 奥→手前
R = list(reversed(R_DISPLAY))  # 奥行き d=0(手前)..3(奥) の高さ


def solve_min_max(f, r):
    """各列xの高さ割り当てをDPで全探索し、両投影と一致する
    配置の総数の最小値・最大値を厳密に求める"""
    n, m = len(f), len(r)
    # 状態: 行(奥行き)の最大値が達成済みかのビットマスク -> (最小和, 最大和)
    init_mask = 0
    for d in range(m):
        if r[d] == 0:
            init_mask |= 1 << d
    states = {init_mask: (0, 0)}
    for x in range(n):
        new_states = {}
        ranges = [range(0, min(f[x], r[d]) + 1) for d in range(m)]
        for col in product(*ranges):
            if f[x] > 0 and max(col) != f[x]:
                continue  # 列xの最大値がf[x]に一致しない
            s = sum(col)
            add = 0
            for d in range(m):
                if r[d] > 0 and col[d] == r[d]:
                    add |= 1 << d
            for mask, (mn, mx) in states.items():
                nm = mask | add
                if nm in new_states:
                    cmn, cmx = new_states[nm]
                    new_states[nm] = (min(cmn, mn + s), max(cmx, mx + s))
                else:
                    new_states[nm] = (mn + s, mx + s)
        states = new_states
    full = (1 << m) - 1
    assert full in states, "両投影を満たす配置が存在しない"
    return states[full]


def verify_q2():
    mn, mx = solve_min_max(F, R)
    print(f"問2 正面図: {F} / 右側面図(奥→手前): {R}")
    print(f"問2 最小: {mn}個, 最大: {mx}個, 差: {mx - mn}")
    assert mx == sum(min(fx, rd) for fx in F for rd in R) == 30, "最大値の検算不一致"
    assert mn == sum(F) == 10, "最小値の検算不一致"
    answer = mx - mn
    options = {1: 16, 2: 18, 3: 22, 4: 20, 5: 24}
    assert options[4] == answer, "正解選択肢(4)が答えと一致しない"
    matches = [k for k, v in options.items() if v == answer]
    assert matches == [4], f"答えに一致する選択肢が複数/不在: {matches}"
    print("問2 検証OK: 正解は(4) 差=20、解は一意\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証OK")
