#!/usr/bin/env python3
"""セット96 最終検証"""

def is_valid_cube_net(cells):
    cells = set(map(tuple, cells))
    if len(cells) != 6: return False
    start = min(cells)
    vis = set(); stk = [start]
    while stk:
        c = stk.pop()
        if c in vis: continue
        vis.add(c)
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = (c[0]+dr,c[1]+dc)
            if nb in cells: stk.append(nb)
    if len(vis) != 6: return False
    def mv(M, v):
        return tuple(sum(M[i][j]*v[j] for j in range(3)) for i in range(3))
    def mm(A, B):
        return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
    I = ((1,0,0),(0,1,0),(0,0,1))
    Ry_neg = ((0,0,-1),(0,1,0),(1,0,0))
    Ry_pos = ((0,0,1),(0,1,0),(-1,0,0))
    Rx_pos = ((1,0,0),(0,0,-1),(0,1,0))
    Rx_neg = ((1,0,0),(0,0,1),(0,-1,0))
    fold_info = {
        (0,1): (Ry_neg,(0.5,0,0.5)), (0,-1): (Ry_pos,(-0.5,0,0.5)),
        (-1,0): (Rx_pos,(0,0.5,0.5)), (1,0): (Rx_neg,(0,-0.5,0.5)),
    }
    face_data = {start: (I, (0.0,0.0,0.0))}
    queue = [start]; folded = {start}
    def r3(v): return tuple(round(x,4) for x in v)
    centers = {r3((0.0,0.0,0.0))}
    while queue:
        cur = queue.pop(0)
        M, C = face_data[cur]; r, c = cur
        for (dr,dc),(R_fold,off) in fold_info.items():
            nb = (r+dr,c+dc)
            if nb in cells and nb not in folded:
                folded.add(nb)
                M_new = mm(M, R_fold)
                off_w = mv(M, off)
                C_new = tuple(C[i]+off_w[i] for i in range(3))
                C_r = r3(C_new)
                if C_r in centers: return False
                centers.add(C_r)
                face_data[nb] = (M_new, C_new)
                queue.append(nb)
    return len(folded) == 6

# 最終問題: 8つのヘキソミノ (5有効 + 3無効)
final = {
    'ア': [(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)],       # 十字型 → 有効
    'イ': [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)],       # S階段型 → 有効
    'ウ': [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)],       # 2×3長方形 → 無効
    'エ': [(0,0),(1,0),(1,1),(1,2),(1,3),(2,3)],       # 1-4-1型A → 有効
    'オ': [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)],       # 2×3縦長方形 → 無効
    'カ': [(0,1),(1,0),(1,1),(1,2),(1,3),(2,2)],       # 1-4-1型B → 有効
    'キ': [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3)],       # コの字型 → 無効
    'ク': [(0,0),(0,1),(1,1),(2,1),(2,2),(3,2)],       # Z階段型 → 有効
}

print("=" * 50)
print("問1: 立方体の展開図の判別 (最終版)")
print("=" * 50)
vc=0; vn=[]; ivn=[]
for name in sorted(final.keys()):
    cells = final[name]
    result = is_valid_cube_net(cells)
    status = "有効" if result else "無効"
    rows = [r for r,c in cells]; cols = [c for r,c in cells]
    grid = [['.' for _ in range(max(cols)+1)] for _ in range(max(rows)+1)]
    for r,c in cells: grid[r][c] = '#'
    gs = ' / '.join([''.join(row) for row in grid])
    print(f"  {name}: {gs}  → {status}")
    if result: vc+=1; vn.append(name)
    else: ivn.append(name)

print(f"\n有効: {vc}個 ({', '.join(vn)})")
print(f"無効: {8-vc}個 ({', '.join(ivn)})")
print(f"\n正解: 成り立たないもの = {8-vc}個")
print(f"選択肢: (1)1個 (2)2個 (3)3個 (4)4個 (5)5個")
print(f"正解番号: ({8-vc})")

# 問2
print("\n" + "=" * 50)
print("問2: 嘘つき問題 (最終版)")
print("=" * 50)
print("A~Eの5人がいる。正直者は真実を、嘘つきは嘘を述べる。")
print("  A:「この中に嘘つきは2人以上いる」")
print("  B:「Dは正直者だ」")
print("  C:「Aは嘘つきだ」")
print("  D:「この中に嘘つきはちょうど3人いる」")
print("  E:「Cは正直者だ」")
print("嘘つきは何人か？")
sols = []
for s in range(32):
    h = [(s>>i)&1==1 for i in range(5)]; A,B,C,D,E=h
    liars = sum(1 for x in h if not x)
    if A!=(liars>=2) or B!=D or C!=(not A) or D!=(liars==3) or E!=C: continue
    sols.append({'A':A,'B':B,'C':C,'D':D,'E':E,'liars':liars})
print(f"\n解の数: {len(sols)} (唯一解であること)")
for sol in sols:
    st = {k:'正直' if v else '嘘つき' for k,v in sol.items() if k!='liars'}
    print(f"  {st}")
    print(f"  嘘つきの数: {sol['liars']}人")
print(f"\n正解: {sols[0]['liars']}人")
print(f"選択肢: (1)1人 (2)2人 (3)3人 (4)4人 (5)5人")
print(f"正解番号: ({sols[0]['liars']})")

# 全条件が解導出に必要か検証
print("\n--- 各条件の必要性チェック ---")
conditions = ['A', 'B', 'C', 'D', 'E']
for skip in conditions:
    sols2 = []
    for s in range(32):
        h = [(s>>i)&1==1 for i in range(5)]; A,B,C,D,E=h
        liars = sum(1 for x in h if not x)
        ok = True
        if skip != 'A' and A != (liars>=2): ok = False
        if skip != 'B' and B != D: ok = False
        if skip != 'C' and C != (not A): ok = False
        if skip != 'D' and D != (liars==3): ok = False
        if skip != 'E' and E != C: ok = False
        if ok: sols2.append(liars)
    unique = len(set(sols2))
    print(f"  {skip}の発言を除くと: {len(sols2)}個の解 (嘘つき数の種類: {unique})")

