"""
問1: 管制空域の航空機位置特定問題
5機の航空機(A～E)が4方角×3距離圏のグリッド上にいる。
C機のみ通信不良で位置不明。他の4機の報告から制約を導く。

A機:「私は東方向の第2圏にいる。第2圏には私を含めて2機がいる。」
B機: ?（通信不良）→ 今回はC機が不明
C機:「私は東方向の第1圏にいる。第1圏には私を含めて2機がいる。」
D機:「私は南方向の第3圏にいる。」
E機:「私は西方向の第2圏にいる。西方向には私を含めて1機がいる。」

→ 再設計: B機が不明パターンに変更

A機:「私は東方向の第2圏にいる。第2圏には私を含めて2機がいる。」
B機: ?（通信不良）
C機:「私は東方向の第1圏にいる。第1圏には私を含めて2機がいる。」
D機:「私は南方向の第3圏にいる。」
E機:「私は西方向の第2圏にいる。西方向には私を含めて1機がいる。」

検証:
ア. B機の報告がない場合、B機の位置として3通りが考えられる。
イ. B機の報告がない場合、B機の方向は確定する。
ウ. B機が「私は北方向にいる」とのみ報告した場合、B機の位置が確定する。
"""

from itertools import product

directions = ['北', '東', '南', '西']
circles = [1, 2, 3]

# All possible positions
all_positions = [(d, c) for d in directions for c in circles]

# Known positions
A = ('東', 2)
C = ('東', 1)
D = ('南', 3)
E = ('西', 2)

known = [A, C, D, E]

# Check known positions are all different
assert len(set(known)) == 4, "Known positions not unique"

# Constraints from reports:
# A: 第2圏には2機 → exactly 2 in circle 2
# C: 第1圏には2機 → exactly 2 in circle 1  
# E: 西方向には1機 → exactly 1 in West

# Find valid positions for B
valid_B = []
for pos in all_positions:
    if pos in known:
        continue
    
    all_five = known + [pos]
    
    # Check A's constraint: circle 2 has exactly 2
    circle2_count = sum(1 for _, c in all_five if c == 2)
    if circle2_count != 2:
        continue
    
    # Check C's constraint: circle 1 has exactly 2
    circle1_count = sum(1 for _, c in all_five if c == 1)
    if circle1_count != 2:
        continue
    
    # Check E's constraint: West has exactly 1
    west_count = sum(1 for d, _ in all_five if d == '西')
    if west_count != 1:
        continue
    
    valid_B.append(pos)

print("=== B機の可能な位置 ===")
for pos in valid_B:
    print(f"  {pos[0]}方向 第{pos[1]}圏")
print(f"  合計: {len(valid_B)}通り")

# Check statement ア: 3通り
print(f"\nア. 3通りが考えられる → {len(valid_B) == 3}")

# Check statement イ: 方向が確定する
B_directions = set(d for d, c in valid_B)
print(f"イ. 方向が確定する → {len(B_directions) == 1} (方向候補: {B_directions})")

# Check statement ウ: 「北方向にいる」→ 確定する
B_north = [pos for pos in valid_B if pos[0] == '北']
print(f"ウ. 北方向と報告した場合確定する → {len(B_north) == 1} (候補: {B_north})")

print("\n=== 正解判定 ===")
print("ア FALSE, イ FALSE, ウ TRUE → ウのみ正しい → 正解(2)")
