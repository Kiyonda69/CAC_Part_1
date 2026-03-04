#!/usr/bin/env python3
"""
セット23 検証スクリプト

問1: パスカルの三角形 mod 5 - 第12段の合計を求める
問2: サイコロ転がし - 10ステップ後の上面の数を求める
"""

def verify_problem1():
    """問1: パスカルの三角形 mod 5 の検証"""
    print("=" * 60)
    print("問1: パスカルの三角形 mod 5")
    print("=" * 60)

    # パスカルの三角形 mod 5 を生成
    rows = 15  # 余裕を持って15段まで計算
    triangle = []

    for n in range(rows):
        row = []
        for k in range(n + 1):
            if k == 0 or k == n:
                row.append(1)
            else:
                val = (triangle[n-1][k-1] + triangle[n-1][k]) % 5
                row.append(val)
        triangle.append(row)

    # 各段を表示
    for i, row in enumerate(triangle):
        row_str = " ".join(str(x) for x in row)
        row_sum = sum(row)
        print(f"第{i+1:2d}段: {row_str}  (合計: {row_sum})")

    # 第12段の合計
    target_row = 12
    answer = sum(triangle[target_row - 1])
    print(f"\n第{target_row}段の合計 = {answer}")

    # 二項係数 mod 5 でも検証
    from math import comb
    row_12_binomial = [comb(11, k) % 5 for k in range(12)]
    print(f"二項係数で検証: {row_12_binomial}")
    print(f"二項係数の合計: {sum(row_12_binomial)}")
    assert sum(row_12_binomial) == answer, "検証失敗！"

    # 各段の合計一覧
    print("\n--- 各段の合計一覧 ---")
    for i, row in enumerate(triangle):
        print(f"第{i+1:2d}段: 合計 = {sum(row)}")

    print(f"\n問1の正解: {answer}")
    return answer


def verify_problem2():
    """問2: サイコロ転がし問題の検証"""
    print("\n" + "=" * 60)
    print("問2: サイコロ転がし")
    print("=" * 60)

    # サイコロの状態: (top, front, right)
    # 対面: top+bottom=7, front+back=7, right+left=7

    def roll_right(top, front, right):
        """右方向に転がす"""
        return (7 - right, front, top)

    def roll_left(top, front, right):
        """左方向に転がす"""
        return (right, front, 7 - top)

    def roll_forward(top, front, right):
        """前方向（上方向）に転がす"""
        return (7 - front, top, right)

    def roll_backward(top, front, right):
        """後方向（下方向）に転がす"""
        return (front, 7 - top, right)

    # 初期状態: 上面=1, 正面=2, 右面=3
    top, front, right = 1, 2, 3

    # 経路: グリッド上の移動
    # 開始位置 (0, 0)
    # 経路: 右、右、上、上、右、上、左、上、左、左
    path = [
        ("right", roll_right),
        ("right", roll_right),
        ("up", roll_forward),
        ("up", roll_forward),
        ("right", roll_right),
        ("up", roll_forward),
        ("left", roll_left),
        ("up", roll_forward),
        ("left", roll_left),
        ("left", roll_left),
    ]

    # 位置追跡
    x, y = 0, 0
    dx_map = {"right": 1, "left": -1, "up": 0, "down": 0}
    dy_map = {"right": 0, "left": 0, "up": 1, "down": -1}

    print(f"開始: 位置({x},{y}), 上面={top}, 正面={front}, 右面={right}")
    print(f"      底面={7-top}, 背面={7-front}, 左面={7-right}")

    for i, (direction, roll_func) in enumerate(path):
        top, front, right = roll_func(top, front, right)
        x += dx_map[direction]
        y += dy_map[direction]
        print(f"Step {i+1:2d} ({direction:>5s}): 位置({x},{y}), 上面={top}, 正面={front}, 右面={right}")

    print(f"\n最終状態: 上面={top}")
    print(f"問2の正解: {top}")

    # 経路の座標を表示
    x, y = 0, 0
    coords = [(x, y)]
    directions_simple = ["right", "right", "up", "up", "right", "up", "left", "up", "left", "left"]
    for d in directions_simple:
        x += dx_map[d]
        y += dy_map[d]
        coords.append((x, y))
    print(f"\n経路座標: {coords}")

    return top


if __name__ == "__main__":
    ans1 = verify_problem1()
    ans2 = verify_problem2()

    print("\n" + "=" * 60)
    print("検証結果まとめ")
    print("=" * 60)
    print(f"問1の正解: {ans1}")
    print(f"問2の正解: {ans2}")

    assert ans1 == 8, f"問1: 期待値8, 実際{ans1}"
    assert ans2 == 3, f"問2: 期待値3, 実際{ans2}"
    print("\n全検証パス！")
