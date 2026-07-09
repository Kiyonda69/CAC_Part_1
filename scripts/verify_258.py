#!/usr/bin/env python3
"""航大思考258 検証: 編隊飛行の視点変換問題（解の一意性確認）

座標系: 平面位置 (x=東が正, y=北が正)。高度は数値(m)。
ビュー座標: (view_x, alt) — view_xは観測者から見て右が正。
"""


def view_from_south(plan, alt):
    """南側後方から北向きに編隊を見る: 東(+x)が観測者の右。"""
    return {k: (p[0], alt[k]) for k, p in plan.items()}


def view_from_east(plan, alt):
    """東側前方から西向きに編隊を見る: 北(+y)が観測者の右。"""
    return {k: (p[1], alt[k]) for k, p in plan.items()}


def rotate_cw90(plan):
    """編隊が右90°旋回（北→東）: 長機基準の相対位置ベクトルを時計回りに90°回転。
    (x, y) -> (y, -x)"""
    return {k: (p[1], -p[0]) for k, p in plan.items()}


def normalize(view):
    """左右位置の順位と高度の順位に正規化して比較する。"""
    xs = sorted(set(v[0] for v in view.values()))
    hs = sorted(set(v[1] for v in view.values()))
    return {k: (xs.index(v[0]), hs.index(v[1])) for k, v in view.items()}


def check(qname, correct_view, options, correct_no):
    target = normalize(correct_view)
    matches = [no for no, opt in options.items() if normalize(opt) == target]
    assert matches == [correct_no], f"{qname}: 一致した選択肢 {matches} (期待: [{correct_no}])"
    # 選択肢同士がすべて異なることも確認
    forms = [tuple(sorted(normalize(o).items())) for o in options.values()]
    assert len(set(forms)) == 5, f"{qname}: 選択肢に重複がある"
    print(f"{qname}: 正解 ({correct_no}) のみが導出結果と一致。選択肢5つはすべて相異なる。")


# ===== 問1 =====
# 編隊（真北へ飛行中）: L=長機, A=右後方, B=左後方, C=Aのさらに右後方
PLAN1 = {'L': (0, 0), 'A': (1, -1), 'B': (-1, -1), 'C': (2, -2)}
ALT1 = {'L': 1000, 'A': 1100, 'B': 900, 'C': 1000}

correct_q1 = view_from_south(PLAN1, ALT1)
# 期待: B(左,下) L(中央,中) A(右,上) C(右端,中)
assert correct_q1 == {'L': (0, 1000), 'A': (1, 1100), 'B': (-1, 900), 'C': (2, 1000)}

# 選択肢（正解は(5)）
OPT1 = {
    1: {'L': (0, 1000), 'A': (-1, 1100), 'B': (1, 900), 'C': (-2, 1000)},   # 左右反転
    2: {'L': (0, 1000), 'A': (1, 900), 'B': (-1, 1100), 'C': (2, 1000)},    # 高度反転
    3: {'L': (0, 1100), 'A': (1, 1000), 'B': (-1, 1000), 'C': (2, 900)},    # 平面図の前後を高さと混同
    4: {'L': (0, 1000), 'A': (-1, 900), 'B': (1, 1100), 'C': (-2, 1000)},   # 左右反転+高度反転
    5: correct_q1,                                                           # 正解
}
check('問1', correct_q1, OPT1, 5)

# ===== 問2 =====
# 右90°旋回（北→東）後、高度変更: L維持1000 / A→900 / B→1100 / C→1200
PLAN2 = rotate_cw90(PLAN1)
assert PLAN2 == {'L': (0, 0), 'A': (-1, -1), 'B': (-1, 1), 'C': (-2, -2)}
ALT2 = {'L': 1000, 'A': 900, 'B': 1100, 'C': 1200}

correct_q2 = view_from_east(PLAN2, ALT2)
# 期待: C(左端,最上) A(左,最下) L(中央,中) B(右,上から2番目)
assert correct_q2 == {'L': (0, 1000), 'A': (-1, 900), 'B': (1, 1100), 'C': (-2, 1200)}

# 選択肢（正解は(2)）
OPT2 = {
    1: {'L': (0, 1000), 'A': (1, 900), 'B': (-1, 1100), 'C': (2, 1200)},    # 左右反転（後方視と混同）
    2: correct_q2,                                                           # 正解
    3: {'L': (0, 1000), 'A': (-1, 1100), 'B': (1, 900), 'C': (-2, 1000)},   # 高度変更を忘れ旧高度のまま
    4: {'L': (0, 1000), 'A': (1, 1100), 'B': (-1, 900), 'C': (2, 1000)},    # 左右反転+旧高度
    5: {'L': (0, 1200), 'A': (-1, 1300), 'B': (1, 1100), 'C': (-2, 1000)},  # 高度の上下反転
}
check('問2', correct_q2, OPT2, 2)

print("検証OK: 問1・問2とも解は一意。")
