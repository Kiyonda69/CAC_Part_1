# -*- coding: utf-8 -*-
"""
航大思考232 検証スクリプト
テーマ: 直角に合わせた2枚の鏡（合わせ鏡）に映る立体の像

物理: 直角に合わせた2枚の垂直な鏡の角に向かって見ると、像は
左右反転ではなく「鉛直軸まわりの180度回転」になる（非反転鏡）。
真上から見た段数グリッドでは、合わせ鏡像 = グリッドの180度回転。

各変換（真上図グリッド）:
- そのまま      : identity
- 右の鏡(1枚)  : 各行を左右逆 = fliplr
- 奥の鏡(1枚)  : 行の並びを逆 = flipud
- 転置          : 行と列の入替 = transpose
- 合わせ鏡      : 180度回転 = rot180  ← 正解
"""

def fliplr(g):
    return [row[::-1] for row in g]

def flipud(g):
    return g[::-1]

def rot180(g):
    return [row[::-1] for row in g[::-1]]

def transpose(g):
    return [list(col) for col in zip(*g)]

def show(g):
    return " / ".join(" ".join(str(x) for x in row) for row in g)

# ===== 問1: 3x3 =====
print("===== 問1 =====")
G1 = [
    [3, 1, 2],
    [1, 0, 3],
    [2, 2, 1],
]
ans1 = {
    "そのまま(原図)":        G1,
    "右の鏡=左右反転(fliplr)": fliplr(G1),
    "奥の鏡=前後反転(flipud)": flipud(G1),
    "転置(transpose)":        transpose(G1),
    "合わせ鏡=180度回転":      rot180(G1),  # 正解
}
correct1 = rot180(G1)
for k, v in ans1.items():
    print(f"  {k:24s}: {show(v)}")
# 一意性: 5つの候補が全て相異なること
serial = [tuple(map(tuple, v)) for v in ans1.values()]
assert len(set(serial)) == 5, "問1: 選択肢に重複あり"
# 正解が180度回転と一致し、他のどの単独変換とも異なること
others = [fliplr(G1), flipud(G1), transpose(G1), G1]
for o in others:
    assert o != correct1, "問1: 正解が他変換と一致"
print("  -> 5択すべて相異なり、正解=180度回転で一意。OK")

# ===== 問2: 4x4 + 目印 =====
print("===== 問2 =====")
G2 = [
    [2, 0, 3, 1],
    [1, 3, 0, 2],
    [3, 1, 2, 0],
    [0, 2, 1, 3],
]
# 目印（黒マス）の位置: (row, col) 0-indexed
mark2 = (0, 3)  # 上から1行目・右端

def mark_transform(pos, n, kind):
    r, c = pos
    if kind == "id":      return (r, c)
    if kind == "fliplr":  return (r, n - 1 - c)
    if kind == "flipud":  return (n - 1 - r, c)
    if kind == "rot180":  return (n - 1 - r, n - 1 - c)
    if kind == "transpose": return (c, r)

n = 4
variants2 = {
    "そのまま(原図)":        ("id",        G2),
    "右の鏡=左右反転":        ("fliplr",    fliplr(G2)),
    "奥の鏡=前後反転":        ("flipud",    flipud(G2)),
    "合わせ鏡=180度回転":     ("rot180",    rot180(G2)),  # 正解
    "転置(transpose)":        ("transpose", transpose(G2)),
}
correct2 = rot180(G2)
correct2_mark = mark_transform(mark2, n, "rot180")
print(f"  原図目印: {mark2}")
for k, (kind, v) in variants2.items():
    m = mark_transform(mark2, n, kind)
    print(f"  {k:20s} 目印{m}: {show(v)}")

# 一意性: 数字配置とマークの組が全て相異なること
combo = []
for kind, v in variants2.values():
    m = mark_transform(mark2, n, kind)
    combo.append((tuple(map(tuple, v)), m))
assert len(set(combo)) == 5, "問2: (配置,目印)に重複あり"
# 正解(配置+目印)が他のどの単独変換とも一致しないこと
print(f"  正解配置: {show(correct2)} / 目印{correct2_mark}")
print("  -> (数字配置, 目印位置) の組が5択すべて相異なる。正解=180度回転で一意。OK")

print("\nすべての検証に合格しました。")
