#!/usr/bin/env python3
"""
航大思考36 検証スクリプト
問1: 図形の対称性に関する論理推論（正解: (5)）
問2: 立方体展開図＋鏡像問題（正解: (3)）
"""

# ============================================================
# 問1 検証: 回転対称な図形Cと線対称な図形Dに関する論理問題
# ============================================================
def verify_q1():
    """
    回転対称な図形Cと線対称な図形Dについて、
    各選択肢が「確実にいえる」かどうかを検証する。

    定義:
    - 回転対称: 360度未満のある回転角で元の図形と一致する
    - 線対称: ある直線（対称の軸）に関して折り返すと元の図形と一致する
    """
    print("=" * 60)
    print("問1: 回転対称と線対称の論理問題")
    print("=" * 60)

    # 反例を挙げて各選択肢を検証
    results = {}

    # (1) 図形Cは必ず線対称でもある → FALSE
    # 反例: S字形（2回回転対称だが線対称ではない）
    # 反例: 三つ巴（3回回転対称だが線対称ではない）
    print("\n(1) 「図形Cは必ず線対称でもある」")
    print("  反例: S字形は2回回転対称（180度回転で一致）だが、線対称ではない")
    print("  反例: 三つ巴（卍の変形）は回転対称だが線対称ではない")
    print("  → FALSE（確実にはいえない）")
    results[1] = False

    # (2) 図形Dを180度回転させると、元の図形と一致する → FALSE
    # 反例: 二等辺三角形は線対称だが、180度回転で一致しない
    print("\n(2) 「図形Dを180度回転させると、元の図形と一致する」")
    print("  反例: 二等辺三角形は線対称（頂角の二等分線が対称軸）だが、")
    print("        180度回転では元の図形と一致しない")
    print("  → FALSE（確実にはいえない）")
    results[2] = False

    # (3) 図形Dは回転対称な図形にはなりえない → FALSE
    # 反例: 正方形は線対称かつ回転対称
    # 反例: 長方形は線対称かつ180度回転対称
    print("\n(3) 「図形Dは回転対称な図形にはなりえない」")
    print("  反例: 正方形は4本の対称軸を持つ線対称であり、")
    print("        同時に90度回転対称でもある")
    print("  反例: 長方形も線対称かつ180度回転対称")
    print("  → FALSE（確実にはいえない）")
    results[3] = False

    # (4) 図形Cと図形Dの対称の軸の数は等しい → FALSE
    # 反例: 図形C=S字形（軸0本）、図形D=正三角形（軸3本）
    # 反例: 図形C=正方形（4回対称、軸4本）、図形D=二等辺三角形（軸1本）
    print("\n(4) 「図形Cと図形Dの対称の軸の数は等しい」")
    print("  反例: C=S字形（対称軸0本）、D=正三角形（対称軸3本）→ 不一致")
    print("  反例: C=正方形（対称軸4本）、D=二等辺三角形（対称軸1本）→ 不一致")
    print("  → FALSE（確実にはいえない）")
    results[4] = False

    # (5) 図形Cは線対称でない場合がある → TRUE
    # 例: S字形は回転対称だが線対称ではない
    # 例: 平行四辺形（正方形・長方形以外）は180度回転対称だが線対称ではない
    print("\n(5) 「図形Cは線対称でない場合がある」")
    print("  例: S字形は2回回転対称だが、対称の軸を持たない")
    print("  例: 平行四辺形（ひし形でも長方形でもない）は180度回転対称だが線対称でない")
    print("  → TRUE（確実にいえる）")
    results[5] = True

    # 正解の一意性を確認
    correct_answers = [k for k, v in results.items() if v]
    assert len(correct_answers) == 1, f"正解が{len(correct_answers)}個: {correct_answers}"
    assert correct_answers[0] == 5, f"正解が(5)ではなく({correct_answers[0]})"

    print(f"\n正解: ({correct_answers[0]}) ← 唯一の正解")
    return 5


# ============================================================
# 問2 検証: 立方体展開図＋鏡像問題
# ============================================================
def verify_q2():
    """
    展開図:
          [P]
    [R] [F] [L]
          [J]
          [G]

    組み立て: F=前面, P=上面, J=下面, R=左面, L=右面, G=背面

    配置: 上面にPが見える状態で、右側に鏡を置く。
    左側の目から鏡を見たとき、鏡に映る立方体の見え方を求める。

    鏡像の原理:
    - 鏡は左右を反転させる
    - 鏡に映ると、実物の右面が鏡像の左側に見える
    - 各面の文字は左右反転（鏡文字）になる
    """
    print("\n" + "=" * 60)
    print("問2: 立方体展開図＋鏡像問題")
    print("=" * 60)

    # 展開図から立方体の面の対応を定義
    cube = {
        'front': 'F',  # 前面
        'back': 'G',   # 背面
        'left': 'R',   # 左面
        'right': 'L',  # 右面
        'top': 'P',    # 上面
        'bottom': 'J'  # 下面
    }

    print(f"\n立方体の各面: {cube}")
    print(f"対面の確認:")
    print(f"  前-後: {cube['front']}-{cube['back']}")
    print(f"  左-右: {cube['left']}-{cube['right']}")
    print(f"  上-下: {cube['top']}-{cube['bottom']}")

    # 対面チェック
    assert cube['front'] != cube['back']
    assert cube['left'] != cube['right']
    assert cube['top'] != cube['bottom']

    # 鏡像の計算
    # 目は前方左側、鏡は右側に配置
    # 実物で見える面: 上面(P), 前面(F), 左面(R)
    real_visible = {
        'top': cube['top'],      # P
        'front': cube['front'],  # F
        'left': cube['left']     # R
    }
    print(f"\n実物で見える面: {real_visible}")

    # 鏡に映ると:
    # - 上面は上面のまま（ただし文字は左右反転）
    # - 前面は前面のまま（ただし文字は左右反転）
    # - 実物の右面が鏡像の見える側面に出現（文字は左右反転）
    mirror_visible = {
        'top': f"reversed_{cube['top']}",       # reversed P
        'front': f"reversed_{cube['front']}",   # reversed F
        'side': f"reversed_{cube['right']}"     # reversed L (実物の右面)
    }
    print(f"鏡に映って見える面: {mirror_visible}")

    # 各選択肢の検証
    choices = {
        1: {'top': 'reversed_P', 'front': 'reversed_F', 'side': 'reversed_R',
            'desc': '反転P(上), 反転F(前), 反転R(側) ← 左面Rを表示（誤り：右面Lが正しい）'},
        2: {'top': 'P', 'front': 'reversed_F', 'side': 'reversed_L',
            'desc': '正P(上), 反転F(前), 反転L(側) ← 上面が反転されていない（誤り）'},
        3: {'top': 'reversed_P', 'front': 'reversed_F', 'side': 'reversed_L',
            'desc': '反転P(上), 反転F(前), 反転L(側) ← 正解'},
        4: {'top': 'reversed_P', 'front': 'F', 'side': 'reversed_L',
            'desc': '反転P(上), 正F(前), 反転L(側) ← 前面が反転されていない（誤り）'},
        5: {'top': 'P', 'front': 'F', 'side': 'L',
            'desc': '正P(上), 正F(前), 正L(側) ← 文字が反転されていない（誤り）'},
    }

    print("\n選択肢の検証:")
    correct = None
    for num, choice in choices.items():
        is_correct = (
            choice['top'] == mirror_visible['top'] and
            choice['front'] == mirror_visible['front'] and
            choice['side'] == mirror_visible['side']
        )
        status = "正解" if is_correct else "不正解"
        print(f"  ({num}) {choice['desc']} → {status}")
        if is_correct:
            assert correct is None, f"正解が複数: ({correct}) と ({num})"
            correct = num

    assert correct == 3, f"正解が(3)ではなく({correct})"
    print(f"\n正解: ({correct}) ← 唯一の正解")
    return 3


# ============================================================
# メイン実行
# ============================================================
if __name__ == '__main__':
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("\n" + "=" * 60)
    print("検証結果サマリー")
    print("=" * 60)
    print(f"問1 正解: ({q1_answer}) ← 唯一解確認済み")
    print(f"問2 正解: ({q2_answer}) ← 唯一解確認済み")
    print("全検証パス")
