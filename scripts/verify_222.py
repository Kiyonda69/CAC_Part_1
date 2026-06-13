# -*- coding: utf-8 -*-
"""航大思考222 検証: 立方体ULDコンテナの展開図(net)折りたたみ。

立方体を盤面上で転がす(roll)シミュレーションにより、各展開図の升を
立方体の6面(固定ID)へ割り当て、対面関係を求める。
- 問1: 十字型展開図で面Cの対面を確認
- 問2: 5つの展開図候補のうち P面とU面が対面になるものが一意であることを確認
"""
from collections import deque

# world方向 -> faceID。対面ペア(固定): (U=0,D=1),(N=2,S=3),(E=4,W=5)
def roll(state, d):
    U, D, N, S, E, W = (state['U'], state['D'], state['N'],
                        state['S'], state['E'], state['W'])
    if d == 'E':  # 右(+col)へ転がす
        return {'U': W, 'E': U, 'D': E, 'W': D, 'N': N, 'S': S}
    if d == 'W':
        return {'U': E, 'W': U, 'D': W, 'E': D, 'N': N, 'S': S}
    if d == 'S':  # 下(+row)へ転がす
        return {'U': N, 'S': U, 'D': S, 'N': D, 'E': E, 'W': W}
    if d == 'N':
        return {'U': S, 'N': U, 'D': N, 'S': D, 'E': E, 'W': W}


def fold(net):
    """展開図(net: {(r,c): label})を折り、対面関係 {label: 対面label} を返す。
    無効な展開図(非連結・面重複)なら (None, 理由) を返す。"""
    cells = list(net.keys())
    start = cells[0]
    # 連結性チェック(4近傍)
    seen = {start}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nb = (r + dr, c + dc)
            if nb in net and nb not in seen:
                seen.add(nb)
                q.append(nb)
    if len(seen) != 6:
        return None, "非連結"
    init = {'U': 0, 'D': 1, 'N': 2, 'S': 3, 'E': 4, 'W': 5}
    paint = {}
    visited = {start}
    q = deque([(start, init)])
    while q:
        (r, c), st = q.popleft()
        fid = st['D']  # 接地面=その升のラベル
        if fid in paint and paint[fid] != net[(r, c)]:
            return None, "面重複(無効ネット)"
        paint[fid] = net[(r, c)]
        for dr, dc, d in [(-1, 0, 'N'), (1, 0, 'S'), (0, -1, 'W'), (0, 1, 'E')]:
            nb = (r + dr, c + dc)
            if nb in net and nb not in visited:
                visited.add(nb)
                q.append((nb, roll(st, d)))
    if len(set(paint.values())) != 6:
        return None, "6面そろわず"
    opp = {}
    for a, b in [(0, 1), (2, 3), (4, 5)]:
        opp[paint[a]] = paint[b]
        opp[paint[b]] = paint[a]
    return opp, "OK"


def main():
    # ===== 問1: 十字型(1-4-1)展開図 =====
    #        A
    #      B C D E
    #        F
    net1 = {(0, 1): 'A', (1, 0): 'B', (1, 1): 'C',
            (1, 2): 'D', (1, 3): 'E', (2, 1): 'F'}
    o1, msg = fold(net1)
    assert o1, f"問1ネット無効: {msg}"
    print("=== 問1: 対面の組 ===")
    for a in 'ACB':
        print(f"  {a} <-> {o1[a]}")
    assert o1['C'] == 'E', "問1: Cの対面はEのはず"
    print("問1 正解: 面Cの対面は E -> 選択肢pos3(=E) が正解\n")

    # ===== 問2: 5つの展開図候補。P-U対面が一意であることを確認 =====
    q2nets = {
        1: {(0, 1): 'S', (1, 0): 'R', (1, 1): 'P', (1, 2): 'U', (1, 3): 'T', (2, 2): 'Q'},
        2: {(0, 0): 'R', (0, 1): 'U', (1, 1): 'S', (1, 2): 'P', (2, 2): 'T', (2, 3): 'Q'},
        3: {(0, 1): 'P', (1, 0): 'U', (1, 1): 'R', (1, 2): 'S', (1, 3): 'Q', (2, 1): 'T'},
        4: {(0, 1): 'P', (1, 1): 'R', (1, 2): 'U', (1, 3): 'T', (1, 4): 'S', (2, 1): 'Q'},
        5: {(0, 1): 'Q', (1, 0): 'U', (1, 1): 'S', (1, 2): 'P', (1, 3): 'T', (2, 1): 'R'},
    }
    print("=== 問2: 各候補で P の対面 ===")
    hit = []
    for k, net in q2nets.items():
        o, msg = fold(net)
        assert o, f"({k})は無効な展開図: {msg}"
        print(f"  ({k}): P <-> {o['P']}   P-U対面={o['P'] == 'U'}")
        if o['P'] == 'U':
            hit.append(k)
    assert hit == [5], f"P-U対面が一意でない: {hit}"
    print("問2 正解: P と U が対面になるのは (5) のみ\n")
    print("検証OK: 問1=(3), 問2=(5)")


if __name__ == "__main__":
    main()
