# -*- coding: utf-8 -*-
"""航大思考264 検証: 立方体の展開図（空間認識・公務員試験典型）

サイコロを展開図のマス上で転がすシミュレーションにより、
各マスが立方体のどの面になるかを求め、向かい合う面を確定する。
面は1..6で表し、向かい合う面の和は7となる。
"""


def fold(cells):
    """cells: [(x,y), ...] 展開図のマス座標（yは下向き）
    戻り値: {cell: face} 各マスが立方体のどの面(1..6)になるか。
    立方体にならない場合は None"""
    cellset = set(cells)
    start = cells[0]
    # 状態: (top, north, east)  北=y-1方向, 東=x+1方向
    state = {start: (1, 2, 3)}
    stack = [start]
    while stack:
        (x, y) = stack.pop()
        t, n, e = state[(x, y)]
        moves = {
            (x + 1, y): (7 - e, n, t),  # 東へ転がす
            (x - 1, y): (e, n, 7 - t),  # 西へ転がす
            (x, y - 1): (7 - n, t, e),  # 北へ転がす
            (x, y + 1): (n, 7 - t, e),  # 南へ転がす
        }
        for nc, ns in moves.items():
            if nc in cellset and nc not in state:
                state[nc] = ns
                stack.append(nc)
    if len(state) != 6:
        return None  # 非連結
    bottoms = {c: 7 - s[0] for c, s in state.items()}
    if len(set(bottoms.values())) != 6:
        return None  # 面が重なる → 立方体にならない
    return bottoms


def opposite_pairs(cells, labels):
    """向かい合う面のラベルの組を frozenset の集合で返す"""
    bottoms = fold(cells)
    assert bottoms is not None, "立方体にならない展開図"
    inv = {f: labels[c] for c, f in bottoms.items()}
    return {frozenset((inv[f], inv[7 - f])) for f in (1, 2, 3)}


def verify_q1():
    """問1: 2-3-1型展開図。面Bと向かい合う面を求める。
    [A][B]
       [C][D][E]
             [F]
    """
    cells = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2)]
    labels = {(0, 0): 'A', (1, 0): 'B', (1, 1): 'C',
              (2, 1): 'D', (3, 1): 'E', (3, 2): 'F'}
    pairs = opposite_pairs(cells, labels)
    assert pairs == {frozenset('AD'), frozenset('BF'), frozenset('CE')}, pairs

    # 面Bの対面
    ans = next(iter(p - {'B'}))[0] if False else None
    for p in pairs:
        if 'B' in p:
            ans = list(p - {'B'})[0]
    assert ans == 'F', ans

    # 解答は唯一（選択肢 A, C, D, E, F のうち F のみが対面）
    valid = [x for x in 'ACDEF' if frozenset(('B', x)) in pairs]
    assert valid == ['F'], valid

    # 解説で用いる変形後の展開図（面Aを回転移動した1-4-1型）でも同一結果
    cells2 = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]
    labels2 = {(1, 0): 'B', (0, 1): 'A', (1, 1): 'C',
               (2, 1): 'D', (3, 1): 'E', (3, 2): 'F'}
    assert opposite_pairs(cells2, labels2) == pairs
    print("問1 OK: 向かい合う面 =", sorted(''.join(sorted(p)) for p in pairs),
          "/ 面Bの対面 =", ans, "→ 選択肢(5) 面F")


def verify_q2():
    """問2: 階段型（2-2-2）展開図。向かい合う面3組の組合せを求める。
    [ア][イ]
        [ウ][エ]
            [オ][カ]
    """
    cells = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)]
    labels = {(0, 0): 'ア', (1, 0): 'イ', (1, 1): 'ウ',
              (2, 1): 'エ', (2, 2): 'オ', (3, 2): 'カ'}
    pairs = opposite_pairs(cells, labels)
    truth = {frozenset('アエ'), frozenset('イオ'), frozenset('ウカ')}
    assert pairs == truth, pairs

    # 選択肢（5つの組合せ）のうち正解が唯一であること
    options = {
        1: {frozenset('アエ'), frozenset('イオ'), frozenset('ウカ')},  # 正解
        2: {frozenset('アウ'), frozenset('イエ'), frozenset('オカ')},
        3: {frozenset('アエ'), frozenset('イカ'), frozenset('ウオ')},
        4: {frozenset('アオ'), frozenset('イエ'), frozenset('ウカ')},
        5: {frozenset('アカ'), frozenset('イウ'), frozenset('エオ')},
    }
    matches = [k for k, v in options.items() if v == pairs]
    assert matches == [1], matches
    # 各選択肢が6面の完全な分割になっていること（形式的妥当性）
    for k, v in options.items():
        faces = set().union(*v)
        assert faces == set('アイウエオカ'), (k, faces)

    # 解説で用いる変形後の展開図（ア・カを回転移動した1-4-1型）でも同一結果
    cells2 = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (2, 2)]
    labels2 = {(1, 0): 'イ', (0, 1): 'ア', (1, 1): 'ウ',
               (2, 1): 'エ', (3, 1): 'カ', (2, 2): 'オ'}
    assert opposite_pairs(cells2, labels2) == pairs
    print("問2 OK: 向かい合う面 =", sorted(''.join(sorted(p)) for p in pairs),
          "→ 選択肢(1)")


if __name__ == '__main__':
    # アルゴリズム自体の検証（十字型: 縦一直線の両端・横一直線の両端が対面）
    cross = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (1, 3)]
    lab = {(1, 0): 'U', (0, 1): 'W', (1, 1): 'C', (2, 1): 'E',
           (1, 2): 'D', (1, 3): 'B'}
    assert opposite_pairs(cross, lab) == {
        frozenset('UD'), frozenset('WE'), frozenset('CB')}
    verify_q1()
    verify_q2()
    print("全検証 OK")
