#!/usr/bin/env python3
"""航大思考235 検証スクリプト: 軸をまたぐ図形の回転体の軸断面

問1: 直線ℓを「またぐ」図形（左右両側に部分を持つ）をℓの周りに
     1回転してできる立体を、ℓを含む平面で切断した断面を特定する。
     各高さで、左右のうち軸から遠い方までが断面の半径になる。
問2: ℓをまたぎ、右側に2つの穴を持つ図形の回転体の軸断面。
     穴の位置に反対側の材料がかぶると穴は埋まり、どちらの側にも
     材料がない半径の穴だけが断面に残る（穴の生存判定）。

セルモデル: 1cm四方のマスを (x, y) で表す。マス(x, y)は
x〜x+1, y〜y+1 の領域を占める。軸ℓは x=0 の直線。
点(x,y)が回転体に含まれる ⇔ 高さyで軸から距離|x|の位置に
図形の材料がある ⇔ (x,y)∈F または (-x,y)∈F。
よって軸断面 = F ∪ mirror(F)（マスでは (x,y) → (-x-1,y)）。
"""


def mirror(cells):
    """軸 x=0 に関する鏡像。マス(x,y) → マス(-x-1,y)"""
    return {(-x - 1, y) for (x, y) in cells}


def cross_section(cells):
    """回転体をℓを含む平面で切断した断面（図形∪鏡像）"""
    return set(cells) | mirror(cells)


def radius_cells(cells):
    """各高さの半径マス集合 {(r,y)}（r=軸からの距離のマス番号）"""
    return {(x if x >= 0 else -x - 1, y) for (x, y) in cells}


# ============ 問1 ============
# 軸をまたぐ図形F1（右側と左側で各高さの張り出しが異なる）
#   y=0: 右3マス・左1マス / y=1: 右1マス・左2マス
#   y=2: 右2マス・左1マス / y=3: 右1マスのみ
F1 = {(0, 0), (1, 0), (2, 0), (-1, 0),
      (0, 1), (-1, 1), (-2, 1),
      (0, 2), (1, 2), (-1, 2),
      (0, 3)}

Q1_CORRECT_SECTION = cross_section(F1)

# 期待形状の手計算検算: 各高さの半径 = max(右, 左)
_expected_q1 = set()
for y, r in [(0, 3), (1, 2), (2, 2), (3, 1)]:
    for k in range(r):
        _expected_q1 |= {(k, y), (-k - 1, y)}
assert Q1_CORRECT_SECTION == _expected_q1, "問1: 半径の手計算と不一致"

# 選択肢（正解は(5)）
Q1_CHOICES = {
    # (1) 罠: 元の図形のまま（回転しても軸断面は変わらないという誤解）
    1: set(F1),
    # (2) 罠: 右側だけを回転させた断面（左側の張り出しを無視）
    2: cross_section({(x, y) for (x, y) in F1 if x >= 0}),
    # (3) 罠: 元の図形の鏡像（左右を折り返しただけ）
    3: mirror(F1),
    # (4) 罠: 正解の上下逆（幅2・4・4・6が下から）
    4: {(x, 3 - y) for (x, y) in cross_section(F1)},
    # (5) 正解: 各高さで軸から遠い方が半径（幅6・4・4・2の左右対称形）
    5: cross_section(F1),
}

# ============ 問2 ============
# 右側: 横5cm×縦4cmの長方形の板（マスx=0..4, y=0..3）から
#        穴A=マス(1,1)（軸から1〜2cm・下から2段目）と
#        穴B=マス(3,2)（軸から3〜4cm・下から3段目）を除いたもの
# 左側: 下端の橋（マスx=-1..-4, y=0）と縦柱（マスx=-4, y=0..3）
#        （縦柱は軸から3〜4cmの位置で全高にわたる）
F2_RIGHT = {(x, y) for x in range(0, 5) for y in range(0, 4)} - {(1, 1), (3, 2)}
F2_LEFT = {(-1, 0), (-2, 0), (-3, 0), (-4, 0)} | {(-4, y) for y in range(0, 4)}
F2 = F2_RIGHT | F2_LEFT

Q2_CORRECT_SECTION = cross_section(F2)

# 穴の生存判定の検算:
#   穴B(3,2): 左の縦柱が同じ高さ・同じ半径(3)にある → 埋まる
#   穴A(1,1): 高さ1で半径1にはどちらの側にも材料がない → 残る
_rc = radius_cells(F2)
assert (3, 2) in _rc, "問2: 穴Bは縦柱で埋まるはず"
assert (1, 1) not in _rc, "問2: 穴Aは残るはず"
_full = {(x, y) for x in range(-5, 5) for y in range(0, 4)}
assert Q2_CORRECT_SECTION == _full - {(1, 1), (-2, 1)}, "問2: 断面の手計算と不一致"

# 選択肢（正解は(5)）
Q2_CHOICES = {
    # (1) 罠: 両方の穴が左右対称の位置に残る（穴は常に残るという誤解）
    1: _full - {(1, 1), (-2, 1), (3, 2), (-4, 2)},
    # (2) 罠: 穴が両方とも埋まる（埋まる理屈の過剰適用）
    2: set(_full),
    # (3) 罠: 穴Bだけが残る（生存判定が逆）
    3: _full - {(3, 2), (-4, 2)},
    # (4) 罠: 元の図形の輪郭のまま（非対称・穴も元の位置のまま）
    4: set(F2),
    # (5) 正解: 10×4の長方形に、穴Aだけが左右対称の位置に残る
    5: cross_section(F2),
}


def verify(q_name, correct_section, choices, correct_no):
    """正解の断面と一致する選択肢が唯一であることを検証"""
    matches = [no for no, cells in sorted(choices.items())
               if cells == correct_section]
    assert matches == [correct_no], \
        f"{q_name}: 一致する選択肢が {matches}（期待: [{correct_no}]）"
    sets = list(choices.values())
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            assert sets[i] != sets[j], f"{q_name}: 選択肢{i+1}と{j+1}が同一"
    print(f"{q_name}: 正解 ({correct_no}) のみが断面と一致 -- OK")


def describe(cells):
    """セル集合を行ごとに要約表示"""
    ys = sorted({y for (_, y) in cells})
    for y in reversed(ys):
        xs = sorted(x for (x, yy) in cells if yy == y)
        print(f"  y={y}: x={xs}")


if __name__ == "__main__":
    print("=== 問1: 軸をまたぐ図形の回転体の軸断面 ===")
    describe(Q1_CORRECT_SECTION)
    verify("問1", Q1_CORRECT_SECTION, Q1_CHOICES, correct_no=5)

    print()
    print("=== 問2: 穴の生存判定を要する回転体の軸断面 ===")
    describe(Q2_CORRECT_SECTION)
    verify("問2", Q2_CORRECT_SECTION, Q2_CHOICES, correct_no=5)

    print()
    print("全検証OK: 各問とも正解が唯一に定まる")
