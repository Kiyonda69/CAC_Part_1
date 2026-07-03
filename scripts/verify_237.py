"""航大思考237 検証コード
展開図の各面に描いた対角線が、組み立て後に閉じた図形になるかを
「転がりキューブ法」による折りたたみシミュレーションで検証する。

問1: 十字型展開図・3面の対角線 → 閉じた正三角形になる候補が唯一か
問2: 階段型展開図・6面の対角線 → 2つの閉じた正三角形になる候補が唯一か
"""
from collections import defaultdict


def roll(verts, direction, cell):
    """cell=(row,col) 上の立方体を direction へ90度転がす"""
    r, c = cell
    new = {}
    for k, (x, y, z) in verts.items():
        if direction == 'E':
            new[k] = (c + 1 + z, y, -(x - (c + 1)))
        elif direction == 'W':
            new[k] = (c - z, y, x - c)
        elif direction == 'S':
            new[k] = (x, r + 1 + z, -(y - (r + 1)))
        elif direction == 'N':
            new[k] = (x, r - z, y - r)
    return new


def fold_net(cells):
    """展開図を折りたたみ、各セルの角点(x,y)→立方体頂点ラベルの対応を返す"""
    start = min(cells)
    r0, c0 = start
    verts = {}
    i = 0
    for z in (0, 1):
        for y in (r0, r0 + 1):
            for x in (c0, c0 + 1):
                verts[i] = (float(x), float(y), float(z))
                i += 1

    def bottom_map(v, cell):
        r, c = cell
        m = {(round(x), round(y)): k for k, (x, y, z) in v.items() if abs(z) < 1e-9}
        assert set(m) == {(c, r), (c + 1, r), (c, r + 1), (c + 1, r + 1)}
        return m

    corner_map = {start: bottom_map(verts, start)}
    visited = {start}
    stack = [(start, verts)]
    dirs = {'E': (0, 1), 'W': (0, -1), 'S': (1, 0), 'N': (-1, 0)}
    while stack:
        cell, v = stack.pop()
        for d, (dr, dc) in dirs.items():
            nb = (cell[0] + dr, cell[1] + dc)
            if nb in cells and nb not in visited:
                nv = roll(v, d, cell)
                visited.add(nb)
                corner_map[nb] = bottom_map(nv, nb)
                stack.append((nb, nv))
    assert visited == set(cells), "展開図が連結でない"
    return corner_map


def segments(diag, corner_map):
    """diag: {(r,c): 'main'(＼) or 'anti'(／)} → 立方体頂点ペアのリスト"""
    segs = []
    for (r, c), typ in diag.items():
        m = corner_map[(r, c)]
        if typ == 'main':
            segs.append(frozenset((m[(c, r)], m[(c + 1, r + 1)])))
        else:
            segs.append(frozenset((m[(c + 1, r)], m[(c, r + 1)])))
    return segs


def classify(segs):
    """線分集合の位相を判定: cycle3 / cycle3+cycle3 / open など"""
    if len(set(segs)) != len(segs):
        return 'duplicate'
    deg, adj = defaultdict(int), defaultdict(list)
    for s in segs:
        a, b = tuple(s)
        deg[a] += 1; deg[b] += 1
        adj[a].append(b); adj[b].append(a)
    if any(d != 2 for d in deg.values()):
        return 'open'
    seen, comps = set(), []
    for n in deg:
        if n in seen:
            continue
        comp, q = {n}, [n]
        seen.add(n)
        while q:
            for w in adj[q.pop()]:
                if w not in seen:
                    seen.add(w); comp.add(w); q.append(w)
        comps.append(len(comp))
    return '+'.join(f'cycle{c}' for c in sorted(comps))


def verify():
    # ===== 問1: 十字型 A(0,1) B(1,0) C(1,1) D(1,2) E(1,3) F(2,1) =====
    cross = {(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1)}
    cm1 = fold_net(cross)
    # 対面ペアの検算（頂点を共有しない面同士が対面）
    faces = {cell: frozenset(m.values()) for cell, m in cm1.items()}
    opp = {tuple(sorted((a, b))) for a in faces for b in faces
           if a < b and not (faces[a] & faces[b])}
    assert opp == {((0, 1), (2, 1)), ((1, 1), (1, 3)), ((1, 0), (1, 2))}, opp

    tri_faces = [(0, 1), (1, 1), (1, 2)]  # A, C, D
    q1_cands = {1: 'mmm', 2: 'amm', 3: 'maa', 4: 'aaa', 5: 'ama'}
    q1_ok = []
    for no, pat in q1_cands.items():
        diag = {f: ('main' if ch == 'm' else 'anti') for f, ch in zip(tri_faces, pat)}
        res = classify(segments(diag, cm1))
        print(f"問1 候補({no}) {pat}: {res}")
        if res == 'cycle3':
            q1_ok.append(no)
    assert q1_ok == [5], f"問1 正解が一意でない: {q1_ok}"

    # ===== 問2: 階段型 G(0,0) H(0,1) I(1,1) J(1,2) K(2,2) L(2,3) =====
    stair = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
    cm2 = fold_net(set(stair))
    q2_cands = {1: 'mmaama', 2: 'ammama', 3: 'aaaaaa', 4: 'amaaam', 5: 'amaama'}
    q2_ok = []
    for no, pat in q2_cands.items():
        diag = {f: ('main' if ch == 'm' else 'anti') for f, ch in zip(stair, pat)}
        segs = segments(diag, cm2)
        res = classify(segs)
        print(f"問2 候補({no}) {pat}: {res}  線分={sorted(tuple(sorted(s)) for s in segs)}")
        if res == 'cycle3+cycle3':
            q2_ok.append(no)
    assert q2_ok == [5], f"問2 正解が一意でない: {q2_ok}"

    print("\n検証OK: 問1 正解(5) / 問2 正解(5) が唯一解")


if __name__ == '__main__':
    verify()
