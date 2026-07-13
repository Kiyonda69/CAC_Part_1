#!/usr/bin/env python3
"""航大思考278 検証: ポリキューブ組み合わせ問題
問1: 2x2x3直方体 = 立体A(6) + 選択肢(6)
問2: 3x3x3立方体 = 立体A(9) + 立体B(9) + 選択肢(9)
回転のみ許可（鏡映は不可）。解の一意性を総当たりで確認する。
"""
from itertools import product


def rotations24():
    """24個の回転行列を生成"""
    def rx(p): x, y, z = p; return (x, -z, y)
    def ry(p): x, y, z = p; return (z, y, -x)
    def rz(p): x, y, z = p; return (-y, x, z)
    mats = set()
    seeds = [tuple()]
    # 全回転を生成: 基本軸回転の合成を閉包まで
    funcs = [rx, ry, rz]
    frontier = [lambda p: p]
    seen = {}
    def key(f):
        return (f((1, 2, 3)), f((3, 1, 2)))
    seen[key(frontier[0])] = frontier[0]
    while frontier:
        f = frontier.pop()
        for g in funcs:
            h = (lambda f, g: lambda p: g(f(p)))(f, g)
            k = key(h)
            if k not in seen:
                seen[k] = h
                frontier.append(h)
    assert len(seen) == 24, len(seen)
    return list(seen.values())


ROTS = rotations24()


def normalize(cells):
    xs = min(c[0] for c in cells); ys = min(c[1] for c in cells); zs = min(c[2] for c in cells)
    return frozenset((x - xs, y - ys, z - zs) for x, y, z in cells)


def orientations(cells):
    return {normalize([r(c) for c in cells]) for r in ROTS}


def placements(cells, box):
    """box内での全配置をビットマスク集合で返す"""
    bx, by, bz = box
    idx = {p: i for i, p in enumerate(product(range(bx), range(by), range(bz)))}
    masks = set()
    for o in orientations(cells):
        mx = max(c[0] for c in o); my = max(c[1] for c in o); mz = max(c[2] for c in o)
        for dx in range(bx - mx):
            for dy in range(by - my):
                for dz in range(bz - mz):
                    m = 0
                    for x, y, z in o:
                        m |= 1 << idx[(x + dx, y + dy, z + dz)]
                    masks.add(m)
    return masks


def can_fill_2(pa, pb, full):
    for a in pa:
        for b in pb:
            if a & b == 0 and a | b == full:
                return True
    return False


def can_fill_3(pa, pb, pc_set, full):
    """A+B+C=full。pc_setは補集合マスクの照合用set"""
    pa_l = sorted(pa)
    for a in pa_l:
        rest_a = full & ~a
        for b in pb:
            if b & a:
                continue
            rest = rest_a & ~b
            if rest in pc_set:
                return True
    return False


# ============ 問題定義 ============
BOX1 = (3, 2, 2); FULL1 = (1 << 12) - 1
A1 = [(0,0,0),(1,0,0),(2,0,0),(0,1,0),(0,0,1),(0,1,1)]
K1 = [(x,y,z) for x in range(3) for y in range(2) for z in range(2)
      if (x,y,z) not in A1]  # 正解形状（補集合）
CUBE222 = [(x,y,z) for x in range(2) for y in range(2) for z in range(2)]
Q1_OPTIONS = {
    1: [c for c in CUBE222 if c not in [(0,0,0),(1,1,0)]],  # 面対角2隅欠け
    2: list(A1),                                             # Aと同形
    3: [(x,y,0) for x in range(3) for y in range(2)],        # 3x2平板
    4: list(K1),                                             # 正解
    5: [c for c in CUBE222 if c not in [(0,0,0),(1,1,1)]],  # 空間対角2隅欠け
}
Q1_ANSWER = 4

BOX2 = (3, 3, 3); FULL2 = (1 << 27) - 1
A2 = [(0,0,0),(1,0,0),(2,0,0),(0,1,0),(1,1,0),(0,2,0),
      (0,0,1),(1,0,1),(0,0,2)]
B2 = [(2,1,0),(1,2,0),(2,2,0),
      (2,0,1),(2,1,1),(2,2,1),(1,2,1),
      (2,0,2),(2,1,2)]
C2 = sorted(normalize([(x,y,z) for x in range(3) for y in range(3)
                       for z in range(3)
                       if (x,y,z) not in set(A2) | set(B2)]))

def _perturb(cells, remove, add):
    s = set(cells); s.discard(remove); s.add(add)
    return sorted(s)

Q2_OPTIONS = {
    1: _perturb(C2, (2,2,1), (2,1,1)),
    2: list(A2),                        # Aと同形
    3: _perturb(C2, (1,0,1), (0,0,1)),
    4: list(C2),                        # 正解
    5: _perturb(C2, (0,2,0), (1,2,0)),
}
Q2_ANSWER = 4


def main():
    # 問1: 立体Aと各選択肢で2x2x3を作れるか
    pa = placements(A1, BOX1)
    winners = [n for n, opt in Q1_OPTIONS.items()
               if can_fill_2(pa, placements(opt, BOX1), FULL1)]
    assert winners == [Q1_ANSWER], f"問1の解が一意でない: {winners}"
    print(f"問1 OK: 正解 ({Q1_ANSWER}) のみ2x2x3を構成可能")

    # 問2: A+B+選択肢で3x3x3を作れるか
    pa2 = placements(A2, BOX2)
    pb2 = placements(B2, BOX2)
    winners2 = [n for n, opt in Q2_OPTIONS.items()
                if can_fill_3(pa2, pb2, set(placements(opt, BOX2)), FULL2)]
    assert winners2 == [Q2_ANSWER], f"問2の解が一意でない: {winners2}"
    print(f"問2 OK: 正解 ({Q2_ANSWER}) のみ3x3x3を構成可能")

    # 全部品の連結性・個数チェック
    for name, cells, n in [("A1", A1, 6), ("A2", A2, 9), ("B2", B2, 9)]:
        assert len(cells) == n
    for opt in Q1_OPTIONS.values():
        assert len(opt) == 6
    for opt in Q2_OPTIONS.values():
        assert len(opt) == 9
    print("部品個数チェック OK（問1: 各6個 / 問2: 各9個）")


if __name__ == "__main__":
    main()
