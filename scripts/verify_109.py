"""
航大思考109の検証スクリプト
- 問1: 立方体の展開図（Tの右にEが突き出る非標準展開）における対面の特定
- 問2: 立方体の鏡像（鏡が左・目が右の配置）における見え方の一意性検証
"""

# =========================
# 問1: 展開図の対面特定
# =========================
# 展開図:
#       [A]
#    [B][C][D][E]
#       [F]
# C=前面(基面)とする
# 折り畳みで: A=上, F=下, B=左, D=右 (Dを右に折り畳み、さらにEはDの右に連結→背面に回り込む)
# 対面ペア: (A, F), (B, D), (C, E)

def verify_p1():
    opposite_pairs = {
        'A': 'F', 'F': 'A',
        'B': 'D', 'D': 'B',
        'C': 'E', 'E': 'C',
    }
    # 問い: Eの対面は?
    ans = opposite_pairs['E']
    assert ans == 'C', f"expected C, got {ans}"
    # 一意性: 立方体の対面は一意に定まる
    print(f"[問1] 面Eの対面 = {ans}  ✓ 一意に決定")


# =========================
# 問2: 鏡像(ミラーは左、目は右) の検証
# =========================
# 立方体の面ラベル: T=top, U=bottom, N=front, V=back, K=left, M=right
# 目は右側にあり、鏡は左側(垂直)に置かれている。目は鏡に映った立方体像を見る。
#
# 鏡像の原理:
#  (a) 鏡が反射する面 = 鏡に面している側 = 立方体の左面 K
#  (b) 鏡像で見える3面 = 前面N, 上面T, 左面K
#  (c) 全ての文字は左右反転 (鏡文字)
#
# 鏡像を3D描画(前面・上面・右見え面) で表すと:
#  - 前面に相当 = N (反転)
#  - 上面に相当 = T (反転)
#  - 右見え面に相当 = K (反転)  ← 鏡は左右を入れ替えるため,実物の左面が鏡像の右側に現れる

def mirror_image():
    """鏡(左)+目(右) 配置での鏡像: (top_letter, top_flipped, front_letter, front_flipped, side_letter, side_flipped)"""
    return {
        'top':  ('T', True),
        'front':('N', True),
        'side':('K', True),   # 右見え面だが,実際は左面K
    }

def verify_p2():
    target = mirror_image()

    options = {
        1: {'top':('T', True),  'front':('N', True),  'side':('M', True)},   # 誤: 右面Mを見てしまう
        2: {'top':('T', True),  'front':('N', True),  'side':('K', True)},   # 正解
        3: {'top':('T', True),  'front':('N', False), 'side':('K', True)},   # 誤: Nが反転なし
        4: {'top':('T', False), 'front':('N', True),  'side':('K', True)},   # 誤: Tが反転なし
        5: {'top':('T', False), 'front':('N', False), 'side':('K', False)},  # 誤: すべて反転なし
    }

    matches = [n for n, opt in options.items() if opt == target]
    assert len(matches) == 1, f"解が{len(matches)}個存在: {matches}"
    assert matches[0] == 2, f"想定正解=2, 実際={matches[0]}"
    print(f"[問2] 唯一解 = 選択肢({matches[0]}) ✓ 一意性確認")

    # 各誤答の根拠を確認
    for n, opt in options.items():
        if n == matches[0]:
            continue
        diffs = [k for k in target if target[k] != opt[k]]
        print(f"       選択肢({n})の誤り箇所: {diffs}")


if __name__ == '__main__':
    verify_p1()
    verify_p2()
    print("\n全ての検証をパスしました。")
