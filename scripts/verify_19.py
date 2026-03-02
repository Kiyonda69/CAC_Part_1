"""
verify_19.py - 航大思考19セット 解の一意性検証

問1: パスカルの三角形型数値表（隣接セル和の規則）
問2: タスク所要時間論理推論（5条件から所要時間を特定）
"""

from itertools import permutations
from math import factorial, comb


# ===== 問1: パスカルの三角形型数値表 =====
print("=" * 50)
print("問1: パスカルの三角形型数値表")
print("=" * 50)

# 規則: cell(r,c) = 左のセル + 上のセル（境界は1）
# 数学的に: cell(r,c) = C(r+c-2, c-1) (二項係数)
def cell(r, c):
    return comb(r + c - 2, c - 1)

print("\n【表の全値】")
print(f"{'':>5}", end="")
for c in range(1, 6):
    print(f"{'列'+str(c):>8}", end="")
print()

for r in range(1, 6):
    print(f"{'行'+str(r):>5}", end="")
    for c in range(1, 6):
        print(f"{cell(r,c):>8}", end="")
    print()

target = cell(4, 4)
print(f"\n【問の答え】cell(行4, 列4) = {target}")

# 規則の検証（隣接和）
print("\n【隣接和規則の確認】")
table = [[1] * 6 for _ in range(6)]  # 0-indexed, 1行目から使用
for r in range(1, 5):  # 行2〜5
    for c in range(1, 5):  # 列2〜5
        table[r][c] = table[r-1][c] + table[r][c-1]

print(f"再帰的計算でのcell(4,4) = {table[3][3]}")
assert table[3][3] == target, "矛盾"
print("検証完了: 隣接和規則は一致")

# 差分パターンの確認
print("\n【行4の差分パターン】")
row4 = [cell(4, c) for c in range(1, 6)]
print(f"行4: {row4}")
diffs1 = [row4[i+1] - row4[i] for i in range(len(row4)-1)]
print(f"1次差分: {diffs1}")
diffs2 = [diffs1[i+1] - diffs1[i] for i in range(len(diffs1)-1)]
print(f"2次差分: {diffs2}")
diffs3 = [diffs2[i+1] - diffs2[i] for i in range(len(diffs2)-1)]
print(f"3次差分: {diffs3} ← 定数(三角数の3次差分=1)")

print(f"\n正解: {target}")
print(f"選択肢: (1)15 (2)20 (3)18 (4)24 (5)28")
print(f"正解位置: 選択肢(2)")


# ===== 問2: タスク所要時間論理推論 =====
print("\n" + "=" * 50)
print("問2: タスク所要時間論理推論")
print("=" * 50)

print("\n【条件】")
print("[ア] A + B = C + D  (合計時間が等しい)")
print("[イ] B = C + 1      (BはCより1時間長い)")
print("[ウ] A < E          (AはEより短い)")
print("[エ] D > B          (DはBより長い)")
print("[オ] E = 1 or E = 5  (Eは1時間か5時間)")

valid = []
for perm in permutations(range(1, 6)):
    A, B, C, D, E = perm

    # [ア] A + B = C + D
    if A + B != C + D:
        continue
    # [イ] B = C + 1
    if B != C + 1:
        continue
    # [ウ] A < E
    if not (A < E):
        continue
    # [エ] D > B
    if not (D > B):
        continue
    # [オ] E = 1 or E = 5
    if E not in [1, 5]:
        continue

    valid.append({"A": A, "B": B, "C": C, "D": D, "E": E})

print(f"\n【有効解】")
for sol in valid:
    print(f"  A={sol['A']}時間, B={sol['B']}時間, C={sol['C']}時間, D={sol['D']}時間, E={sol['E']}時間")

assert len(valid) == 1, f"解が{len(valid)}個存在！一意性がない"
sol = valid[0]
print(f"\n解は唯一: D = {sol['D']}時間")
print(f"\n正解: {sol['D']}時間")
print(f"選択肢: (1)5時間 (2)2時間 (3)1時間 (4)4時間 (5)3時間")
print(f"正解位置: 選択肢(4)")

print("\n【推論手順の解説】")
print("[イ]より B = C + 1 → (B,C)の候補: (2,1),(3,2),(4,3),(5,4)")
print("[オ]より E ∈ {1,5}")
print()
for B, C in [(2,1),(3,2),(4,3),(5,4)]:
    remaining = [x for x in range(1,6) if x not in [B, C]]
    print(f"  B={B}, C={C}のとき: 残り{remaining}をA,D,Eに割り当て")
    for perm2 in permutations(remaining):
        A, D, E = perm2
        checks = [
            A + B == C + D,
            A < E,
            D > B,
            E in [1, 5]
        ]
        if all(checks):
            print(f"    → A={A}, D={D}, E={E} [全条件OK] ← 唯一解")
        elif B == 2 and C == 1:  # 詳細表示
            pass

print("\n=== 検証完了: 解の一意性確認 ===")
