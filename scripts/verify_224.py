# -*- coding: utf-8 -*-
"""航大思考224 解の一意性検証: 紙折りと穴あけ問題

正方形の航空図(8x8座標, 左下原点, y上向き)を折りたたみ、
折りたたんだ状態で1点に穴をあけ、広げたときの穴の配置を求める。
折りは「重ねる側を折り線で鏡映する」ことで表現できる。
"""


def reflect_x(p, line):
    x, y = p
    return (2 * line - x, y)


def reflect_y(p, line):
    x, y = p
    return (x, 2 * line - y)


def reflect_diag(p):
    """y=x に関する鏡映"""
    x, y = p
    return (y, x)


def unfold(punch, folds):
    """折り操作の逆順に鏡映の像を加え、穴の全集合を返す。

    folds: 折り操作のリスト。各要素は ('x', line) / ('y', line) / ('diag',)。
    展開は最後に折った順の逆 = リストを逆順に鏡映を加える。
    """
    holes = {punch}
    for f in reversed(folds):
        new = set()
        for p in holes:
            if f[0] == 'x':
                new.add(reflect_x(p, f[1]))
            elif f[0] == 'y':
                new.add(reflect_y(p, f[1]))
            elif f[0] == 'diag':
                new.add(reflect_diag(p))
        holes |= new
    return frozenset(holes)


def S(pts):
    return frozenset(pts)


# ============================================================
# 問1: 2回の直交折り
#   折り1: 右半分を左へ (折り線 x=4)
#   折り2: 上半分を下へ (折り線 y=4)
#   穴: (3,1)
# ============================================================
P1_folds = [('x', 4), ('y', 4)]
P1_punch = (3, 1)
C1 = unfold(P1_punch, P1_folds)

P1_options = {
    1: S([(3, 2), (5, 2), (3, 6), (5, 6)]),   # 中心からの距離を誤認
    2: S([(1, 3), (7, 3), (1, 5), (7, 5)]),   # 折り方向を取り違え
    3: S([(3, 1), (5, 1), (3, 3), (5, 3)]),   # 折り2を忘れた
    4: S([(1, 1), (7, 1), (1, 7), (7, 7)]),   # 穴位置を隅と誤認
    5: S([(3, 1), (5, 1), (3, 7), (5, 7)]),   # 正解パターン
}

# ============================================================
# 問2: 2回の直交折り + 対角折り
#   折り1: 上半分を下へ (y=4)
#   折り2: 右半分を左へ (x=4)
#   折り3: 対角 y=x で折る (下側を上へ)
#   穴: (3,1)   ※最終の三角領域 y<=x, [0,4]^2 内
# ============================================================
P2_folds = [('y', 4), ('x', 4), ('diag',)]
P2_punch = (3, 1)
C2 = unfold(P2_punch, P2_folds)

P2_options = {
    1: S([(3, 1), (5, 1), (3, 7), (5, 7)]),    # 対角折りを無視
    2: S([(1, 3), (7, 3), (1, 5), (7, 5)]),    # 直交折りを無視
    3: S([(3, 1), (5, 1), (3, 7), (5, 7),
          (2, 3), (6, 3), (2, 5), (6, 5)]),    # 対角像の位置誤り
    4: S([(3, 1), (5, 1), (3, 7), (5, 7),
          (1, 3), (7, 3), (1, 5), (7, 5)]),    # 正解(8穴)
    5: S([(3, 1), (5, 1), (3, 7), (5, 7),
          (1, 2), (7, 2), (1, 6), (7, 6)]),    # 対角を別軸で誤反映
}


def check(name, correct_set, options):
    matches = [k for k, v in options.items() if v == correct_set]
    print(f"--- {name} ---")
    print("正解の穴集合:", sorted(correct_set))
    print("穴の数:", len(correct_set))
    print("一致する選択肢:", matches)
    assert len(matches) == 1, f"一致が{len(matches)}個 (一意でない)"
    # 全選択肢が相異なることも確認
    vals = list(options.values())
    assert len(set(vals)) == len(vals), "選択肢に重複あり"
    print("正解番号:", matches[0])
    print("=> 一意性OK\n")
    return matches[0]


if __name__ == '__main__':
    a1 = check("問1 (2回直交折り)", C1, P1_options)
    a2 = check("問2 (直交2回+対角折り)", C2, P2_options)
    print(f"問1正解=選択肢{a1} / 問2正解=選択肢{a2}")
