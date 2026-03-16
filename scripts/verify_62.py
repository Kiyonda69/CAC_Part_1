#!/usr/bin/env python3
"""セット62 検証スクリプト - 展開図問題"""
from collections import deque

def is_valid_cube_net(positions):
    """折りたたみシミュレーションで有効な展開図か判定"""
    if len(positions) != 6:
        return False
    pos_set = set(positions)
    visited = {positions[0]}
    queue = deque([positions[0]])
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = (r+dr, c+dc)
            if nb in pos_set and nb not in visited:
                visited.add(nb)
                queue.append(nb)
    if len(visited) != 6:
        return False
    
    neg = lambda v: (-v[0], -v[1], -v[2])
    face_info = {positions[0]: ((0,0,1), (0,1,0), (-1,0,0))}
    queue = deque([positions[0]])
    visited2 = {positions[0]}
    while queue:
        curr = queue.popleft()
        n, rv, uv = face_info[curr]
        r, c = curr
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = (r+dr, c+dc)
            if nb in pos_set and nb not in visited2:
                visited2.add(nb)
                if (dr,dc)==(0,1):  nn,nr,nu = rv, neg(n), uv
                elif (dr,dc)==(0,-1): nn,nr,nu = neg(rv), n, uv
                elif (dr,dc)==(-1,0): nn,nr,nu = uv, rv, neg(n)
                else:                 nn,nr,nu = neg(uv), rv, n
                face_info[nb] = (nn, nr, nu)
                queue.append(nb)
    normals = [face_info[p][0] for p in positions]
    return len(set(normals)) == 6

def get_opposites(positions):
    """有効な展開図の対面関係を返す"""
    pos_set = set(positions)
    neg = lambda v: (-v[0], -v[1], -v[2])
    face_info = {positions[0]: ((0,0,1), (0,1,0), (-1,0,0))}
    queue = deque([positions[0]])
    visited = {positions[0]}
    while queue:
        curr = queue.popleft()
        n, rv, uv = face_info[curr]
        r, c = curr
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = (r+dr, c+dc)
            if nb in pos_set and nb not in visited:
                visited.add(nb)
                if (dr,dc)==(0,1):  nn,nr,nu = rv, neg(n), uv
                elif (dr,dc)==(0,-1): nn,nr,nu = neg(rv), n, uv
                elif (dr,dc)==(-1,0): nn,nr,nu = uv, rv, neg(n)
                else:                 nn,nr,nu = neg(uv), rv, n
                face_info[nb] = (nn, nr, nu)
                queue.append(nb)
    
    normals = {pos: face_info[pos][0] for pos in positions}
    opposites = {}
    for p1 in positions:
        for p2 in positions:
            if p1 != p2 and tuple(-x for x in normals[p1]) == normals[p2]:
                opposites[p1] = p2
    return opposites, normals

# ============================================================
# 問1: 十字型展開図の対面関係
# ============================================================
print("=" * 60)
print("問1: 立方体の展開図 - 対面関係（標準難度）")
print("=" * 60)

# 十字型展開図（各面にア〜カの記号）:
#       [ウ]
#    [エ][ア][イ]
#       [オ]
#       [カ]
#
# positions in grid:
cross_net = [(0,1), (1,0), (1,1), (1,2), (2,1), (3,1)]
cross_labels = {(0,1):'ウ', (1,0):'エ', (1,1):'ア', (1,2):'イ', (2,1):'オ', (3,1):'カ'}

assert is_valid_cube_net(cross_net), "十字型が無効"

opposites, normals = get_opposites(cross_net)
normal_to_dir = {
    (0,0,1):'上', (0,0,-1):'下', (0,1,0):'右', (0,-1,0):'左', (1,0,0):'奥', (-1,0,0):'手前'
}

print("\n各面の位置:")
for pos in cross_net:
    label = cross_labels[pos]
    direction = normal_to_dir.get(normals[pos], '?')
    print(f"  {label}: {direction}")

print("\n対面関係:")
shown = set()
for p1, p2 in opposites.items():
    pair = tuple(sorted([cross_labels[p1], cross_labels[p2]]))
    if pair not in shown:
        shown.add(pair)
        print(f"  {cross_labels[p1]} ↔ {cross_labels[p2]}")

# 問題: 各面に模様を描いて、特定の面の向かい側を問う
# 面の模様（SVGで描画可能なシンプルなもの）:
# ア: 丸(○), イ: 三角(△), ウ: 四角(□), 
# エ: 星(☆), オ: 十字(+), カ: 菱形(◇)
#
# 問題: 「丸(○)が描かれた面の向かい側にある模様はどれか」
# ア(○)の対面 = カ(◇)
# 正解: ◇

print("\n--- 問1の設計 ---")
patterns = {'ア':'丸○', 'イ':'三角△', 'ウ':'四角□', 'エ':'星☆', 'オ':'十字+', 'カ':'菱形◇'}
target = 'ア'
answer_label = cross_labels[opposites[dict((v,k) for k,v in cross_labels.items())[target]]]
# Find position of ア
for pos, lbl in cross_labels.items():
    if lbl == target:
        target_pos = pos
        break
opposite_pos = opposites[target_pos]
answer_label = cross_labels[opposite_pos]
print(f"問題: {patterns[target]}の面の対面は？")
print(f"正解: {patterns[answer_label]}（{answer_label}面）")

# 選択肢（対面でない4面 + 正解）:
choices_q1 = ['三角△', '四角□', '星☆', '十字+', '菱形◇']
print(f"\n選択肢: {choices_q1}")
print(f"正解: 菱形◇")

# 各対面ペアの確認
print("\n全対面ペア（模様）:")
shown2 = set()
for p1, p2 in opposites.items():
    pair = tuple(sorted([cross_labels[p1], cross_labels[p2]]))
    if pair not in shown2:
        shown2.add(pair)
        l1, l2 = cross_labels[p1], cross_labels[p2]
        print(f"  {patterns[l1]} ↔ {patterns[l2]}")

# ============================================================
# 問2: 5つの展開図から立方体にならないものを選ぶ
# ============================================================
print("\n" + "=" * 60)
print("問2: 展開図の判別（高難度）")
print("=" * 60)

# 有効4つ + 無効1つ
net_choices = {
    1: {'pos': [(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)], 'name': '十字型'},
    2: {'pos': [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)], 'name': 'S字型'},
    3: {'pos': [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)], 'name': '2x3長方形'},  # 無効
    4: {'pos': [(0,0),(1,0),(1,1),(2,1),(2,2),(3,2)], 'name': '階段型'},
    5: {'pos': [(0,0),(0,1),(1,1),(1,2),(1,3),(2,3)], 'name': 'S字型2'},
}

print("\n各展開図の判定:")
for num in sorted(net_choices.keys()):
    info = net_choices[num]
    valid = is_valid_cube_net(info['pos'])
    status = "有効" if valid else "無効"
    print(f"  ({num}) {info['name']}: {status}")

def draw(positions, label):
    pos_set = set(positions)
    min_r = min(r for r,c in positions)
    max_r = max(r for r,c in positions)
    min_c = min(c for r,c in positions)
    max_c = max(c for r,c in positions)
    lines = []
    for r in range(min_r, max_r+1):
        row = ""
        for c in range(min_c, max_c+1):
            row += "[■]" if (r,c) in pos_set else "   "
        lines.append(row)
    print(f"\n  ({label}):")
    for line in lines:
        print(f"    {line}")

for num in sorted(net_choices.keys()):
    draw(net_choices[num]['pos'], num)

invalid = [n for n,i in net_choices.items() if not is_valid_cube_net(i['pos'])]
assert len(invalid) == 1, f"無効が{len(invalid)}個"
print(f"\n問2の正解: ({invalid[0]}) - {net_choices[invalid[0]]['name']}")

# ============================================================
# 検証結果サマリー
# ============================================================
print("\n" + "=" * 60)
print("検証結果サマリー")
print("=" * 60)
print(f"問1: 対面関係 → 正解は{patterns[answer_label]}")
print(f"問2: 無効な展開図 → 正解は({invalid[0]})")
print("両問題とも解は一意 ✓")
