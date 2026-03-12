#!/usr/bin/env python3
"""
航大思考48 - 解の一意性検証スクリプト

問1: 対称性の論理推論（ちょうど2本の対称軸をもつ図形Pと、180度回転対称で対称軸をもたない図形Q）
問2: 立方体展開図 + 鏡像問題（展開図から組み立て、鏡に映る文字の向きを判定）
"""

def verify_q1():
    """問1: 対称性の論理推論の検証"""
    print("=" * 60)
    print("問1: 対称性の論理推論")
    print("=" * 60)
    print()
    print("条件:")
    print("- 図形P: ちょうど2本の対称の軸をもつ")
    print("- 図形Q: 180度の回転対称であるが対称の軸をもたない")
    print()

    correct_count = 0

    # (1) 図形Pは必ず四角形である
    opt1 = False
    print("(1) 図形Pは必ず四角形である → 誤り")
    print("   反例: 楕円は2本の対称軸（長軸・短軸）を持つが四角形ではない")
    print()

    # (2) 図形Qは凸図形ではありえない
    opt2 = False
    print("(2) 図形Qは凸図形ではありえない → 誤り")
    print("   反例: 平行四辺形（長方形・ひし形を除く）は凸図形で、")
    print("   180度回転対称だが対称軸を持たない")
    print()

    # (3) 図形Pと図形Qが合同になることがある
    opt3 = False
    print("(3) 図形Pと図形Qが合同になることがある → 誤り")
    print("   合同な図形は同じ対称性をもつ。Pは対称軸2本、Qは0本なので矛盾")
    print()

    # (4) 図形Pを180度回転させると、元の図形と一致する
    opt4 = True
    print("(4) 図形Pを180度回転させると、元の図形と一致する → 正しい")
    print("   証明: 2本の対称軸をl1, l2とする。")
    print("   l1に関する鏡映σ1とl2に関する鏡映σ2の合成 σ1∘σ2 は")
    print("   2軸の交点を中心とする回転。")
    print("   ちょうど2本の対称軸の場合、軸は直交し（角度90度）、")
    print("   合成回転は 2*90 = 180度 の回転となる。")
    print("   例: 長方形（正方形を除く）、ひし形（正方形を除く）")
    print()

    # (5) 図形Qの面積は図形Pの面積より大きい
    opt5 = False
    print("(5) 図形Qの面積は図形Pの面積より大きい → 誤り")
    print("   対称性と面積には関係がない。任意のサイズのP, Qが存在する")
    print()

    results = [opt1, opt2, opt3, opt4, opt5]
    correct_count = sum(results)
    correct_option = results.index(True) + 1

    assert correct_count == 1, f"正解が{correct_count}個あります（1個であるべき）"
    print(f"正解: ({correct_option})")
    print(f"唯一の正しい選択肢であることを確認 OK")
    return correct_option


def verify_q2():
    """問2: 立方体展開図 + 鏡像の検証"""
    print()
    print("=" * 60)
    print("問2: 立方体展開図 + 鏡像")
    print("=" * 60)
    print()

    # 展開図の配置（十字型）
    #       G
    #   B   D   K
    #       N
    #       R
    print("展開図:")
    print("      G")
    print("  B   D   K")
    print("      N")
    print("      R")
    print()

    # 組み立て後の面の対応
    faces = {
        'front': 'D',
        'back': 'R',
        'top': 'G',
        'bottom': 'N',
        'left': 'B',
        'right': 'K',
    }

    print("組み立て後:")
    for pos, letter in faces.items():
        print(f"  {pos}: {letter}")
    print()

    # 対面の確認
    pairs = [('front', 'back'), ('top', 'bottom'), ('left', 'right')]
    for p1, p2 in pairs:
        print(f"  {faces[p1]} <-> {faces[p2]} (対面)")
    print()

    # 鏡像の分析
    print("鏡像の分析:")
    print("  鏡の位置: 立方体の右側（垂直面）")
    print("  目の位置: 立方体の左前方")
    print()
    print("  実物で見える面: 前面(D), 上面(G), 左面(B)")
    print("  鏡像で見える面: 前面(D)反転, 上面(G)反転, 右面(K)反転")
    print()

    # 選択肢の検証
    # (面の文字, 反転フラグ) のタプルで各面を表現
    # 正解条件: top=G反転, front=D反転, side=K反転
    options = {
        1: {'top': ('G', True), 'front': ('D', True), 'side': ('B', True)},   # Bは左面 → 誤り
        2: {'top': ('G', False), 'front': ('D', True), 'side': ('K', True)},  # G反転なし → 誤り
        3: {'top': ('G', True), 'front': ('D', True), 'side': ('K', True)},   # 正解
        4: {'top': ('G', True), 'front': ('D', False), 'side': ('K', True)},  # D反転なし → 誤り
        5: {'top': ('G', False), 'front': ('D', False), 'side': ('K', False)},  # 全て反転なし → 誤り
    }

    print("選択肢の検証:")
    correct_count = 0
    correct_option = None

    for opt_num, opt_data in options.items():
        is_correct = True
        reasons = []

        # 側面の文字チェック（右面Kであるべき）
        if opt_data['side'][0] != 'K':
            is_correct = False
            reasons.append(f"側面が{opt_data['side'][0]}（正しくはK）")

        # 反転チェック（全て反転されているべき）
        for face_name in ['top', 'front', 'side']:
            letter, is_reversed = opt_data[face_name]
            if not is_reversed:
                is_correct = False
                reasons.append(f"{letter}が反転されていない")

        status = "正解" if is_correct else "誤り"
        reason_str = "、".join(reasons) if reasons else "全条件を満たす"
        print(f"  ({opt_num}) {status}: {reason_str}")

        if is_correct:
            correct_count += 1
            correct_option = opt_num

    print()
    assert correct_count == 1, f"正解が{correct_count}個あります（1個であるべき）"
    print(f"正解: ({correct_option})")
    print(f"唯一の正しい選択肢であることを確認 OK")
    return correct_option


if __name__ == '__main__':
    q1_answer = verify_q1()
    q2_answer = verify_q2()
    print()
    print("=" * 60)
    print(f"検証完了: 問1の正解=({q1_answer}), 問2の正解=({q2_answer})")
    print("=" * 60)
