"""
航大思考181 解の一意性検証スクリプト

問1: 飛行機の三面図問題
  - 上面図と正面図から正しい側面図を選ぶ
  - 飛行機の特徴: 機首右向き、垂直尾翼が後部上方、エンジンが主翼下

問2: 立方体の展開図問題
  - T字型展開図の6面に航空シンボル
  - 組み立て後の特定視点からの面を問う
"""


def verify_q1():
    """問1: 三面図の論理整合性検証"""

    # 飛行機の特徴(機首が右を向く側面図の場合)
    # nose_dir: 機首方向 (right=右, left=左, flat=尖っていない)
    # vstab_pos: 垂直尾翼の位置 (rear_top=後部上, rear_bottom=後部下, front_top=前部上, none=なし)
    # hstab_pos: 水平尾翼の位置 (rear=後部, middle=中央, none=なし)
    # engine_visible: エンジンが見える (True/False)

    correct_side_view = {
        'nose_dir': 'right',
        'vstab_pos': 'rear_top',
        'hstab_pos': 'rear',
        'engine_visible': True,
    }

    options = [
        # (1) 機首が左向き(機尾と機首が逆)
        {'nose_dir': 'left', 'vstab_pos': 'rear_top', 'hstab_pos': 'rear', 'engine_visible': True},
        # (2) 垂直尾翼が機首側(前後逆)
        {'nose_dir': 'right', 'vstab_pos': 'front_top', 'hstab_pos': 'rear', 'engine_visible': True},
        # (3) 正解
        {'nose_dir': 'right', 'vstab_pos': 'rear_top', 'hstab_pos': 'rear', 'engine_visible': True},
        # (4) 垂直尾翼が下を向いている
        {'nose_dir': 'right', 'vstab_pos': 'rear_bottom', 'hstab_pos': 'rear', 'engine_visible': True},
        # (5) 機首が平らで尖っていない
        {'nose_dir': 'flat', 'vstab_pos': 'rear_top', 'hstab_pos': 'rear', 'engine_visible': True},
    ]

    matches = [i + 1 for i, opt in enumerate(options) if opt == correct_side_view]
    assert len(matches) == 1, f"解が一意でない: {matches}"
    print(f"問1 正解: ({matches[0]})")
    return matches[0]


def verify_q2():
    """問2: 立方体の展開図の組み立て検証

    T字型展開図:
            [B]
        [A][C][D][E]
            [F]

    展開図の初期配置(Cを正面とする標準向き):
        前: C, 上: B, 下: F, 左: A, 右: D, 後: E
    """

    # 立方体の各面のシンボル
    # 初期状態: Cを正面に置いた時の各位置
    cube = {
        'front': 'C',   # 滑走路(Runway)
        'top': 'B',     # 雲(Cloud)
        'bottom': 'F',  # レーダー(Radar)
        'left': 'A',    # 飛行機(Aircraft)
        'right': 'D',   # 管制塔(Tower)
        'back': 'E',    # ヘリポート(Helicopter)
    }

    # 操作: 「Bを正面、Cを下」にする
    # = 立方体を手前に90度倒す(X軸回りに前傾)
    # 元の上→前, 元の前→下, 元の下→後, 元の後→上
    # 左右は不変
    rotated = {
        'front': cube['top'],     # B
        'top': cube['back'],      # E
        'bottom': cube['front'],  # C
        'back': cube['bottom'],   # F
        'left': cube['left'],     # A
        'right': cube['right'],   # D
    }

    # 検証: 正面B, 下C の条件を満たすか
    assert rotated['front'] == 'B', f"正面はBでない: {rotated['front']}"
    assert rotated['bottom'] == 'C', f"下面はCでない: {rotated['bottom']}"

    # 質問: 右側面に見える文字
    right_face = rotated['right']

    # 選択肢
    options = ['F', 'D', 'A', 'E', 'C']  # (1)〜(5)

    matches = [i + 1 for i, opt in enumerate(options) if opt == right_face]
    assert len(matches) == 1, f"解が一意でない: {matches}"
    print(f"問2 正解: ({matches[0]}) = {right_face}")

    # 全選択肢の意味を確認
    print(f"  (1) F = 下面(矛盾)")
    print(f"  (2) D = 右側面 ← 正解")
    print(f"  (3) A = 左側面")
    print(f"  (4) E = 上面(矛盾)")
    print(f"  (5) C = 下面(矛盾)")

    return matches[0]


if __name__ == '__main__':
    a1 = verify_q1()
    a2 = verify_q2()
    assert a1 == 3, f"問1の正解が3でない: {a1}"
    assert a2 == 2, f"問2の正解が2でない: {a2}"
    print("\n検証完了: 問1=3, 問2=2")
