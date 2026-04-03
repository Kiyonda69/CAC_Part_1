#!/usr/bin/env python3
"""セット96検証: 立方体展開図判定(orientation matrix) + 嘘つき問題"""

def is_valid_cube_net(cells):
    cells = set(map(tuple, cells))
    if len(cells) != 6: return False
    start = min(cells)
    # Connectivity check
    vis = set(); stk = [start]
    while stk:
        c = stk.pop()
        if c in vis: continue
        vis.add(c)
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = (c[0]+dr,c[1]+dc)
            if nb in cells: stk.append(nb)
    if len(vis) != 6: return False
    
    # Matrix-vector multiply
    def mv(M, v):
        return tuple(sum(M[i][j]*v[j] for j in range(3)) for i in range(3))
    # Matrix-matrix multiply
    def mm(A, B):
        return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
    
    I = ((1,0,0),(0,1,0),(0,0,1))
    # Rotation matrices for 90° folds in LOCAL frame:
    Ry_neg = ((0,0,-1),(0,1,0),(1,0,0))   # RIGHT: +X → +Z
    Ry_pos = ((0,0,1),(0,1,0),(-1,0,0))   # LEFT: -X → +Z
    Rx_pos = ((1,0,0),(0,0,-1),(0,1,0))    # UP: +Y → +Z
    Rx_neg = ((1,0,0),(0,0,1),(0,-1,0))    # DOWN: -Y → +Z
    
    # Local center offset after fold for each direction
    # RIGHT: (0.5, 0, 0.5), LEFT: (-0.5, 0, 0.5)
    # UP: (0, 0.5, 0.5), DOWN: (0, -0.5, 0.5)
    
    fold_info = {
        (0, 1):  (Ry_neg, (0.5, 0, 0.5)),   # RIGHT (dc=+1)
        (0, -1): (Ry_pos, (-0.5, 0, 0.5)),  # LEFT (dc=-1)
        (-1, 0): (Rx_pos, (0, 0.5, 0.5)),   # UP (dr=-1)
        (1, 0):  (Rx_neg, (0, -0.5, 0.5)),  # DOWN (dr=+1)
    }
    
    # BFS
    face_data = {start: (I, (0.0, 0.0, 0.0))}
    queue = [start]
    folded = {start}
    
    # Track centers for overlap detection
    def r3(v): return tuple(round(x, 4) for x in v)
    centers = {r3((0.0, 0.0, 0.0))}
    
    while queue:
        cur = queue.pop(0)
        M, C = face_data[cur]
        r, c = cur
        
        for (dr, dc), (R_fold, offset_local) in fold_info.items():
            nb = (r+dr, c+dc)
            if nb in cells and nb not in folded:
                folded.add(nb)
                M_new = mm(M, R_fold)
                offset_world = mv(M, offset_local)
                C_new = tuple(C[i] + offset_world[i] for i in range(3))
                
                C_rounded = r3(C_new)
                if C_rounded in centers:
                    return False  # Overlap
                centers.add(C_rounded)
                
                face_data[nb] = (M_new, C_new)
                queue.append(nb)
    
    return len(folded) == 6

# Tests
print("=== 既知の展開図テスト ===")
tests = [
    ("十字型", [(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)], True),
    ("T型", [(0,0),(0,1),(0,2),(0,3),(1,2),(2,2)], True),
    ("L型", [(0,0),(1,0),(2,0),(3,0),(3,1),(3,2)], True),
    ("S階段型", [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)], True),
    ("1-4-1型", [(0,0),(1,0),(1,1),(1,2),(1,3),(2,3)], True),
    ("Z型", [(0,0),(0,1),(1,1),(2,1),(2,2),(2,3)], True),
    ("2x3長方形", [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)], False),
    ("直線6", [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0)], False),
    ("2x3縦", [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)], False),
    ("コの字", [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3)], False),
]
ok_all = True
for name, cells, expected in tests:
    result = is_valid_cube_net(cells)
    ok = "OK" if result == expected else "FAIL"
    if ok == "FAIL": ok_all = False
    print(f"  {name}: {result} (期待: {expected}) {ok}")

if ok_all:
    print("\n全テスト合格!")
else:
    print("\n!!! テスト失敗あり !!!")

# Count all valid hexominoes
print("\n=== 全35ヘキソミノ検証 ===")
def gen_all_hexominoes():
    found = set()
    def canonical(cells):
        cells = list(cells)
        mr, mc = min(r for r,c in cells), min(c for r,c in cells)
        return tuple(sorted((r-mr, c-mc) for r,c in cells))
    def all_orient(cells):
        orients = set()
        coords = list(cells)
        for _ in range(4):
            orients.add(canonical(coords))
            orients.add(canonical((-r,c) for r,c in coords))
            coords = [(-c,r) for r,c in coords]
        return orients
    def grow(cells):
        if len(cells) == 6:
            c = min(all_orient(cells))
            found.add(c)
            return
        for r,c in list(cells):
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nb = (r+dr, c+dc)
                if nb not in cells:
                    cells.add(nb)
                    grow(cells)
                    cells.remove(nb)
    grow({(0,0)})
    return found

all_hex = gen_all_hexominoes()
print(f"全ヘキソミノ数: {len(all_hex)} (期待: 35)")

valid_hexominoes = []
for h in sorted(all_hex):
    if is_valid_cube_net(h):
        valid_hexominoes.append(h)

print(f"有効な展開図: {len(valid_hexominoes)} (期待: 11)")
for i, h in enumerate(valid_hexominoes, 1):
    rows = [r for r,c in h]; cols = [c for r,c in h]
    grid = [['.' for _ in range(max(cols)+1)] for _ in range(max(rows)+1)]
    for r,c in h: grid[r][c] = '#'
    gs = ' '.join([''.join(row) for row in grid])
    print(f"  {i:2d}. {gs}")


# ===== 問題用の8つのヘキソミノ設計 =====
print("\n" + "=" * 50)
print("問題用ヘキソミノ候補")
print("=" * 50)

# 有効な展開図を5つ、無効を3つ選ぶ（答え: 3個が無効）
candidates = {
    'ア': [(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)],       # 十字型
    'イ': [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)],       # S階段型
    'ウ': [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)],       # 2×3長方形
    'エ': [(0,0),(1,0),(1,1),(1,2),(1,3),(2,3)],       # 1-4-1型A
    'オ': [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)],       # 2×3縦長方形
    'カ': [(0,1),(1,0),(1,1),(1,2),(1,3),(2,2)],       # 1-4-1型B
    'キ': [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3)],       # コの字型
    'ク': [(0,0),(0,1),(1,0),(1,1),(2,0),(3,0)],       # P字型
}

vc2 = 0; vn2 = []; ivn2 = []
for name in sorted(candidates.keys()):
    cells = candidates[name]
    result = is_valid_cube_net(cells)
    status = "有効" if result else "無効"
    rows = [r for r,c in cells]; cols = [c for r,c in cells]
    grid = [['.' for _ in range(max(cols)+1)] for _ in range(max(rows)+1)]
    for r,c in cells: grid[r][c] = '#'
    gs = ' / '.join([''.join(row) for row in grid])
    print(f"  {name}: {gs}  → {status}")
    if result: vc2+=1; vn2.append(name)
    else: ivn2.append(name)

print(f"\n有効: {vc2}個 ({', '.join(vn2)})")
print(f"無効: {8-vc2}個 ({', '.join(ivn2)})")
print(f"\n問題: 「成り立たないものはいくつあるか」")
print(f"正解: {8-vc2}個")

