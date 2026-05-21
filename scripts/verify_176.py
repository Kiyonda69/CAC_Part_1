"""
航大思考176 検証スクリプト

問1: 平面図から正面シルエットを求める（標準難度）
問2: 正面シルエットと側面シルエットから整合する平面図を選ぶ（高難度）

テーマ: 空港貨物ULDコンテナの3D空間把握
"""


def front_silhouette(grid):
    """正面（南）から見たシルエット = 各列の最大値"""
    cols = len(grid[0])
    rows = len(grid)
    return [max(grid[r][c] for r in range(rows)) for c in range(cols)]


def side_silhouette(grid):
    """右側面（東）から見たシルエット = 各行の最大値"""
    return [max(row) for row in grid]


# ============================================================
# 問1: 平面図 → 正面シルエットを問う
# ============================================================
print("=" * 60)
print("問1 検証")
print("=" * 60)

q1_grid = [
    [2, 1, 3],
    [1, 2, 1],
    [2, 3, 2],
]

q1_front = front_silhouette(q1_grid)
print(f"上面図:")
for row in q1_grid:
    print(f"  {row}")
print(f"正面シルエット: {q1_front}")

q1_options = {
    1: [2, 3, 2],
    2: [3, 3, 3],
    3: [2, 3, 3],
    4: [1, 2, 3],
    5: [3, 2, 3],
}

correct_q1 = [k for k, v in q1_options.items() if v == q1_front]
print(f"\n選択肢ごとの正誤:")
for k, v in q1_options.items():
    mark = "○" if v == q1_front else "×"
    print(f"  ({k}) {v} {mark}")

assert len(correct_q1) == 1, f"問1: 解が{len(correct_q1)}個存在"
print(f"\n問1 正解: ({correct_q1[0]})")

# ============================================================
# 問2: 正面・側面シルエット → 整合する平面図を問う
# ============================================================
print()
print("=" * 60)
print("問2 検証")
print("=" * 60)

# 要求されるシルエット
required_front = [3, 3, 2]
required_side = [2, 3, 3]

print(f"要求 正面シルエット: {required_front}")
print(f"要求 側面シルエット: {required_side}")

q2_options = {
    1: [
        [2, 1, 3],
        [1, 3, 2],
        [3, 2, 1],
    ],
    2: [
        [2, 1, 2],
        [3, 3, 1],
        [1, 2, 1],
    ],
    3: [
        [3, 2, 3],
        [1, 2, 1],
        [2, 1, 2],
    ],
    4: [
        [1, 2, 1],
        [3, 1, 2],
        [2, 3, 1],
    ],
    5: [
        [1, 3, 1],
        [1, 2, 1],
        [3, 1, 2],
    ],
}

print(f"\n選択肢ごとの正誤:")
correct_q2 = []
for k, grid in q2_options.items():
    f = front_silhouette(grid)
    s = side_silhouette(grid)
    ok_front = f == required_front
    ok_side = s == required_side
    both_ok = ok_front and ok_side
    mark = "○" if both_ok else "×"
    print(f"  ({k}) 正面={f} {'✓' if ok_front else '✗'} / 側面={s} {'✓' if ok_side else '✗'} → {mark}")
    if both_ok:
        correct_q2.append(k)

assert len(correct_q2) == 1, f"問2: 整合する選択肢が{len(correct_q2)}個存在"
print(f"\n問2 正解: ({correct_q2[0]})")

# ============================================================
print()
print("=" * 60)
print(f"検証完了: 問1=({correct_q1[0]}), 問2=({correct_q2[0]})")
print("=" * 60)
