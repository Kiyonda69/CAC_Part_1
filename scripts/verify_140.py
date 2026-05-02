#!/usr/bin/env python3
"""航大思考140 解の一意性検証"""

print("=== 問1 検証: 方眼紙の経路追跡 ===")

# 方向: 0=East, 1=North, 2=West, 3=South
DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def trace(start, facing, steps):
    x, y = start
    d = facing
    path = [(x, y)]
    for turn, n in steps:
        if turn == 'L':
            d = (d + 1) % 4
        elif turn == 'R':
            d = (d - 1) % 4
        x += DIR[d][0] * n
        y += DIR[d][1] * n
        path.append((x, y))
    return path


# 問1: スタート(0,0)、東向き
# (1) 2マス進む  (2) 左に曲がり3マス  (3) 右に曲がり2マス
# (4) 右に曲がり1マス  (5) 左に曲がり3マス
instructions_q1 = [
    ('S', 2),
    ('L', 3),
    ('R', 2),
    ('R', 1),
    ('L', 3),
]

path = trace((0, 0), 0, instructions_q1)
print(f"経路: {path}")
assert path == [(0, 0), (2, 0), (2, 3), (4, 3), (4, 2), (7, 2)], f"不一致: {path}"
print("正解経路 OK: (0,0)→(2,0)→(2,3)→(4,3)→(4,2)→(7,2)")

# 各方向を言語で確認
dirs_text = ['東', '北', '西', '南']
d = 0
for i, (turn, n) in enumerate(instructions_q1, 1):
    if turn == 'L':
        d = (d + 1) % 4
    elif turn == 'R':
        d = (d - 1) % 4
    print(f"  ({i}) {dirs_text[d]}へ{n}マス")

print()

print("=== 問2 検証: 五角形の座標変換 ===")

original = [(0, 2), (2, 4), (4, 3), (3, 0), (1, 0)]
labels = ['A', 'B', 'C', 'D', 'E']


def cw90(p):
    """時計回り90度回転: (x,y) → (y,-x)"""
    return (p[1], -p[0])


def xref(p):
    """x軸に関して対称移動: (x,y) → (x,-y)"""
    return (p[0], -p[1])


step1 = [cw90(p) for p in original]
step2 = [xref(p) for p in step1]

print("元の頂点:")
for label, p in zip(labels, original):
    print(f"  {label}{p}")

print("操作1後 (時計回り90°):")
for label, p in zip(labels, step1):
    print(f"  {label}'{p}")

print("操作2後 (x軸反射) = 最終結果:")
for label, p in zip(labels, step2):
    print(f"  {label}'{p}")

assert step2 == [(2, 0), (4, 2), (3, 4), (0, 3), (0, 1)], f"不一致: {step2}"
print("正解 OK: A'(2,0), B'(4,2), C'(3,4), D'(0,3), E'(0,1)")

# 補足: 2操作の組み合わせは y=x に関する反射と等価
print()
print("補足: CW90 + x軸反射 = (x,y)→(y,x) = 対角線 y=x に関する反射")
for label, p in zip(labels, original):
    p2 = (p[1], p[0])
    assert p2 == xref(cw90(p)), "等価性不一致!"
print("等価性確認 OK")

print()
print("全検証完了! Q1正解=4, Q2正解=1")
