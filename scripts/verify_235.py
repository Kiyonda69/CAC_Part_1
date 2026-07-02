#!/usr/bin/env python3
"""航大思考235 検証スクリプト: 回転体の軸断面問題

問1: 軸ℓに接する階段状図形をℓの周りに1回転してできる立体を、
     ℓを含む平面で切断した断面の形を特定する。
問2: 軸ℓから1cm離れた穴あき正方形板をℓの周りに1回転してできる
     中空立体を、ℓを含む平面で切断した断面の形を特定する。

セルモデル: 1cm四方のマスを (x, y) で表す。マス(x, y)は
x〜x+1, y〜y+1 の領域を占める。軸ℓは x=0 の直線。
回転体をℓを含む平面で切った断面 = 図形F ∪ Fの鏡像(x→-x-1)。
"""


def mirror(cells):
    """軸 x=0 に関する鏡像。マス(x,y) → マス(-x-1,y)"""
    return {(-x - 1, y) for (x, y) in cells}


def cross_section(cells):
    """回転体をℓを含む平面で切断した断面（元の図形∪鏡像）"""
    return set(cells) | mirror(cells)


# ============ 問1 ============
# 図形F1: 軸に接する階段形（下段 幅3×高1、中段 幅2×高1、上段 幅1×高2）
F1 = {(0, 0), (1, 0), (2, 0),      # 下段 y=0
      (0, 1), (1, 1),              # 中段 y=1
      (0, 2), (0, 3)}              # 上の塔 y=2,3

Q1_CORRECT_SECTION = cross_section(F1)

# 選択肢（正解は(2)）
Q1_CHOICES = {
    # (1) 罠: 鏡像を忘れ元の図形のみ（非対称）
    1: set(F1),
    # (2) 正解: F1 ∪ 鏡像 → 幅6・4・2の左右対称な階段
    2: cross_section(F1),
    # (3) 罠: 対称だが上下逆（幅2,2,4,6が下から）
    3: {(x, 3 - y) for (x, y) in cross_section(F1)},
    # (4) 罠: 塔の高さを1と見誤る（最上段が欠落）
    4: {c for c in cross_section(F1) if c[1] <= 2},
    # (5) 罠: 鏡像でなく平行移動した複製を並べる
    5: set(F1) | {(x - 3, y) for (x, y) in F1},
}

# ============ 問2 ============
# 図形F2: 軸から1cm離れた1辺4cmの正方形板（マスx=1..4, y=0..3）
# 穴: 1辺1cm、内側の辺から1cm・上の辺から1cmの位置（マス(2,2)）
F2 = {(x, y) for x in range(1, 5) for y in range(0, 4)} - {(2, 2)}

Q2_CORRECT_SECTION = cross_section(F2)

# 選択肢（正解は(2)）
Q2_CHOICES = {
    # (1) 罠: 軸との隙間を忘れる（板が軸に接した位置）
    1: cross_section({(x - 1, y) for (x, y) in F2}),
    # (2) 正解: 隙間2cm・左右対称・穴も鏡像位置
    2: cross_section(F2),
    # (3) 罠: 鏡像でなく平行移動（左側の穴が外側の辺寄りになる）
    3: set(F2) | {(x - 6, y) for (x, y) in F2},
    # (4) 罠: 回転で穴が埋まると誤解（穴なしの2枚板）
    4: cross_section({(x, y) for x in range(1, 5) for y in range(0, 4)}),
    # (5) 罠: 点対称（180°回転）にする（左側の穴が上下逆の位置）
    5: set(F2) | {(-x - 1, 3 - y) for (x, y) in F2},
}


def verify(q_name, correct_section, choices, correct_no):
    """正解の断面と一致する選択肢が唯一であることを検証"""
    matches = [no for no, cells in sorted(choices.items())
               if cells == correct_section]
    assert matches == [correct_no], \
        f"{q_name}: 一致する選択肢が {matches}（期待: [{correct_no}]）"
    # 全選択肢が互いに異なることも確認
    sets = list(choices.values())
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            assert sets[i] != sets[j], f"{q_name}: 選択肢{i+1}と{j+1}が同一"
    print(f"{q_name}: 正解 ({correct_no}) のみが断面と一致 -- OK")


def describe(cells):
    """セル集合を行ごとの幅で要約表示"""
    ys = sorted({y for (_, y) in cells})
    for y in reversed(ys):
        xs = sorted(x for (x, yy) in cells if yy == y)
        print(f"  y={y}: x={xs}")


if __name__ == "__main__":
    print("=== 問1: 階段形の回転体の軸断面 ===")
    print("正しい断面（下から幅6・4・2・2の対称階段）:")
    describe(Q1_CORRECT_SECTION)
    verify("問1", Q1_CORRECT_SECTION, Q1_CHOICES, correct_no=2)

    print()
    print("=== 問2: 穴あき正方形板（軸から1cm）の回転体の軸断面 ===")
    print("正しい断面（軸の両側に隙間1cmずつ・穴は鏡像位置）:")
    describe(Q2_CORRECT_SECTION)
    verify("問2", Q2_CORRECT_SECTION, Q2_CHOICES, correct_no=2)

    print()
    print("全検証OK: 各問とも正解が唯一に定まる")
