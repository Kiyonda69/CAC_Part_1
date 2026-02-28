"""
セット14 規則性問題 - 解の検証スクリプト

問1: 数列シフト表（a(n+1) = 2a(n) - 1 の数列をシフトして構成した5×5表）
問2: 階乗×平方表（a(i,j) = i! × j²）
"""

import math


def verify_q1():
    """
    問1: 表中の「？」の値を検証する

    数列: a(1)=2, a(n+1) = 2*a(n) - 1
    表のセル: table[i][j] = seq[i+j]  (i,j は 0-indexed)
    求める値: table[4][4] = seq[8]
    """
    # 数列を生成
    seq = [2]
    for _ in range(8):
        seq.append(2 * seq[-1] - 1)
    # seq[0..8] = [2, 3, 5, 9, 17, 33, 65, 129, 257]

    print("=== 問1検証 ===")
    print(f"数列: {seq}")
    print()

    # 5×5表を構成
    table = [[seq[i + j] for j in range(5)] for i in range(5)]

    print("表の内容:")
    headers = ["", "A列", "B列", "C列", "D列", "E列"]
    row_labels = ["①行", "②行", "③行", "④行", "⑤行"]
    print("  " + "  ".join(f"{h:>5}" for h in headers))
    for i, row in enumerate(table):
        vals = [f"{v:>5}" for v in row]
        print(f"  {row_labels[i]:>4}  " + "  ".join(vals))

    missing = table[4][4]
    print(f"\n求める値 (⑤行, E列) = seq[8] = {missing}")

    # 規則の確認: 各行で a(n+1) = 2*a(n) - 1 が成立するか
    print("\n規則確認（各行で次の項 = 2×前の項 - 1）:")
    all_valid = True
    for i, row in enumerate(table[:-1]):  # 最後の行を除く
        for j in range(len(row) - 1):
            expected = 2 * row[j] - 1
            actual = row[j + 1]
            if expected != actual:
                print(f"  ⑤行{i+1}, {j+1}→{j+2}: {row[j]}×2-1={expected}, 実際={actual} NG")
                all_valid = False
    # 最終行も確認（最後のセルは「？」なので4要素）
    row5 = table[4][:4]
    for j in range(len(row5) - 1):
        expected = 2 * row5[j] - 1
        actual = row5[j + 1]
        if expected != actual:
            print(f"  ⑤行最終, {j+1}→{j+2}: NG")
            all_valid = False

    if all_valid:
        print("  すべての規則が一致 OK")

    # ？の検証
    answer = 2 * table[4][3] - 1  # ⑤行D列 × 2 - 1
    assert answer == missing, f"検証失敗: {answer} != {missing}"
    print(f"\n正解: {missing}")
    print(f"選択肢での正解番号: 2番（②）")
    return missing


def verify_q2():
    """
    問2: 表中の「？」の値を検証する

    規則: a(i,j) = i! × j²  (i,j は 1-indexed)
    求める値: a(5,5) = 5! × 5² = 120 × 25 = 3000
    """
    print("\n=== 問2検証 ===")

    # 5×5表を構成
    table = [[math.factorial(i) * (j ** 2) for j in range(1, 6)]
             for i in range(1, 6)]

    print("表の内容:")
    headers = ["", "1列", "2列", "3列", "4列", "5列"]
    row_labels = ["①行", "②行", "③行", "④行", "⑤行"]
    print("  " + "  ".join(f"{h:>6}" for h in headers))
    for i, row in enumerate(table):
        vals = [f"{v:>6}" for v in row]
        print(f"  {row_labels[i]:>4}  " + "  ".join(vals))

    missing = table[4][4]
    print(f"\n求める値 (⑤行, 5列) = 5! × 5² = {math.factorial(5)} × {5**2} = {missing}")

    # 規則の確認
    print("\n規則確認: a(i,j) = i! × j²")
    all_valid = True
    for i in range(1, 6):
        for j in range(1, 6):
            expected = math.factorial(i) * (j ** 2)
            actual = table[i - 1][j - 1]
            if expected != actual:
                print(f"  ({i},{j}): 期待={expected}, 実際={actual} NG")
                all_valid = False
    if all_valid:
        print("  すべてのセルで規則が一致 OK")

    # 1列目が階乗であることの確認
    col_a = [table[i][0] for i in range(5)]
    factorials = [math.factorial(i) for i in range(1, 6)]
    assert col_a == factorials, f"1列目が階乗でない: {col_a}"
    print(f"\n1列目（j=1, j²=1）: {col_a} = 1!, 2!, 3!, 4!, 5! の階乗")

    assert missing == 3000, f"検証失敗: {missing} != 3000"
    print(f"\n正解: {missing}")
    print(f"選択肢での正解番号: 2番（②）")
    return missing


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("\n=== 最終確認 ===")
    print(f"問1 正解: {q1_answer}（選択肢2番）")
    print(f"問2 正解: {q2_answer}（選択肢2番）")
    print("全検証完了")
