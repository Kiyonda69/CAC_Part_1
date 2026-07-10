#!/usr/bin/env python3
"""航大思考269: 平面図形の敷き詰め（ペントミノ）の解の一意性検証

問1: 5つのピースから4つを選んで4x5長方形を敷き詰める。
     使わないピースが一意に定まることを確認する。
問2: 5つのピースすべてで5x5(25マス)の図形を敷き詰めたとき、
     指定マスを覆うピースが全ての敷き詰め方で同一であることを確認する。
ピースは回転可・裏返し不可。
"""

# ペントミノ定義（(row, col) の集合、裏返しなしの基本形）
PENTOMINOES = {
    'L': [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    'P': [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    'T': [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    'U': [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
    'S': [(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)],  # N形
    'Y': [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)],
    'V': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    'W': [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    'Z': [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    'F': [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
    'I': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    'X': [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
}


def normalize(cells):
    r0 = min(r for r, c in cells)
    c0 = min(c for r, c in cells)
    return tuple(sorted((r - r0, c - c0) for r, c in cells))


def rotations(cells, allow_flip=False):
    """回転（90度刻み）で得られる向きの集合。裏返しは不可。"""
    shapes = set()
    cur = cells
    for _ in range(4):
        shapes.add(normalize(cur))
        cur = [(c, -r) for r, c in cur]  # 90度回転
    if allow_flip:
        cur = [(r, -c) for r, c in cells]
        for _ in range(4):
            shapes.add(normalize(cur))
            cur = [(c, -r) for r, c in cur]
    return shapes


def placements(shape_cells, region, allow_flip=False):
    """領域region(集合)内への全配置を列挙"""
    result = []
    region = set(region)
    rows = [r for r, c in region]
    cols = [c for r, c in region]
    for orient in rotations(shape_cells, allow_flip):
        for dr in range(min(rows), max(rows) + 1):
            for dc in range(min(cols), max(cols) + 1):
                place = frozenset((r + dr, c + dc) for r, c in orient)
                if place <= region:
                    result.append(place)
    return result


def tilings(region, piece_names, allow_flip=False):
    """piece_names のピースで region を敷き詰める全解を列挙"""
    region = frozenset(region)
    all_places = {name: placements(PENTOMINOES[name], region, allow_flip)
                  for name in piece_names}
    solutions = []

    def solve(remaining, unused, assignment):
        if not remaining:
            if not unused:
                solutions.append(dict(assignment))
            return
        # 最も左上のマスを必ず覆う
        target = min(remaining)
        for name in list(unused):
            for place in all_places[name]:
                if target in place and place <= remaining:
                    unused.remove(name)
                    assignment[name] = place
                    solve(remaining - place, unused, assignment)
                    del assignment[name]
                    unused.add(name)

    solve(region, set(piece_names), {})
    return solutions

# ===== 問題設定 =====
# ピース割当: ア=U, イ=T, ウ=P, エ=W, オ=V
LABELS = {'ア': 'U', 'イ': 'T', 'ウ': 'P', 'エ': 'W', 'オ': 'V'}
PIECES = ['U', 'T', 'P', 'W', 'V']

Q1_REGION = [(r, c) for r in range(4) for c in range(5)]

# 問2の領域: 5行6列から (0,0),(0,1),(0,4),(0,5),(1,0) を除いた25マス
Q2_REMOVED = {(0, 0), (0, 1), (0, 4), (0, 5), (1, 0)}
Q2_REGION = [(r, c) for r in range(5) for c in range(6)
             if (r, c) not in Q2_REMOVED]
Q2_STAR = (2, 3)  # ★印のマス


def verify_q1():
    """問1: 使わないピースが一意にUであることを検証"""
    import itertools
    results = []
    for unused in PIECES:
        four = [p for p in PIECES if p != unused]
        sols = tilings(Q1_REGION, four, allow_flip=False)
        if sols:
            results.append((unused, len(sols)))
    assert len(results) == 1, f"敷き詰め可能な組が{len(results)}個: {results}"
    assert results[0][0] == 'U', f"余りピースが想定と異なる: {results[0][0]}"
    print(f"問1 OK: 余りピース=U(ア)のみ敷き詰め可能 "
          f"(P,T,V,Wによる4x5の敷き詰め方 {results[0][1]}通り)")
    example = tilings(Q1_REGION, ['P', 'T', 'V', 'W'], allow_flip=False)[0]
    grid = {cell: name for name, place in example.items() for cell in place}
    for r in range(4):
        print('  ' + ' '.join(grid[(r, c)] for c in range(5)))


def verify_q2():
    """問2: 敷き詰め方が唯一で、★を覆うピースがTであることを検証"""
    sols = tilings(Q2_REGION, PIECES, allow_flip=False)
    assert len(sols) == 1, f"解が{len(sols)}個存在"
    sol = sols[0]
    star_piece = next(name for name, place in sol.items() if Q2_STAR in place)
    assert star_piece == 'T', f"★を覆うピースが想定と異なる: {star_piece}"
    print(f"問2 OK: 敷き詰め方は唯一、★{Q2_STAR}を覆うピース=T(イ)")
    grid = {cell: name for name, place in sol.items() for cell in place}
    for r in range(5):
        print('  ' + ' '.join(grid.get((r, c), '.') for c in range(6)))


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("検証完了: 問1正解=(1)ア, 問2正解=(2)イ")
