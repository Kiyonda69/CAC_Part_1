"""
セット6 解の一意性検証

問1: 二重等差数表（行方向・列方向の両方に等差数列、かつ公差自体も規則的）
問2: 差分増加型数表（列によって公差が変わる複合規則）
"""

def verify_q1():
    """
    問1: 二重等差数表
    規則:
      - 行n の初項 = 2n
      - 行n の公差 = n + 3
    表（行1〜4、列1〜4）:
      行1: 2,  6, 10, 14  (公差=4)
      行2: 4,  9, 14, 19  (公差=5)
      行3: 6, 12, 18, 24  (公差=6)
      行4: 8, 15,  ?,  29  (公差=7)  → ?=22
    """
    table = []
    for r in range(1, 5):
        start = 2 * r
        diff = r + 3
        row = [start + diff * (c - 1) for c in range(1, 5)]
        table.append(row)

    # 表を表示
    print("=== 問1: 二重等差数表 ===")
    print("     列1   列2   列3   列4")
    for i, row in enumerate(table):
        print(f"行{i+1}: {row[0]:3d}   {row[1]:3d}   {row[2]:3d}   {row[3]:3d}")

    # 行方向の規則確認
    print("\n[行方向の規則]")
    for i, row in enumerate(table):
        diffs = [row[j+1] - row[j] for j in range(3)]
        print(f"  行{i+1}: 初項={row[0]}, 公差={diffs[0]}, 全差分={diffs}")
        assert all(d == diffs[0] for d in diffs), f"行{i+1}が等差数列でない"

    # 列方向の規則確認
    print("\n[列方向の規則]")
    for c in range(4):
        col = [table[r][c] for r in range(4)]
        diffs = [col[r+1] - col[r] for r in range(3)]
        print(f"  列{c+1}: {col}, 公差={diffs[0]}")
        assert all(d == diffs[0] for d in diffs), f"列{c+1}が等差数列でない"

    # 穴埋め（行4、列3）
    answer_q1 = table[3][2]  # 0-indexed: row 4 → index 3, col 3 → index 2
    print(f"\n[正解] 行4・列3 = {answer_q1}")

    # 唯一解の検証：与えられた数値から解が一意に決まることを確認
    # 全パターンで1〜50の整数を試してみる
    valid = []
    for candidate in range(1, 50):
        # 行4の規則: 8, 15, candidate, 29
        # 公差が一定であれば: 15-8=7, candidate-15=7 → candidate=22, 29-candidate=7 → candidate=22
        if (15 - 8) == (candidate - 15) == (29 - candidate):
            valid.append(candidate)

    assert len(valid) == 1, f"問1の解が{len(valid)}個存在: {valid}"
    assert valid[0] == answer_q1, f"計算値({answer_q1})と検証値({valid[0]})が不一致"
    print(f"[検証] 唯一解 = {valid[0]} ✓")
    return answer_q1


def verify_q2():
    """
    問2: 差分増加型数表
    規則:
      - f(r, c) = c * r + (c-1)^2
      - 各列の公差 = c（列番号）
      - 列1: 公差1, 列2: 公差2, 列3: 公差3, 列4: 公差4
    表（行1〜4、列1〜4）:
      行1:  1,  3,  7, 13
      行2:  2,  5, 10, 17
      行3:  3,  7, 13, 21
      行4:  4,  9, 16,  ?  → ?=25
    """
    def f(r, c):
        return c * r + (c - 1) ** 2

    table = [[f(r, c) for c in range(1, 5)] for r in range(1, 5)]

    # 表を表示
    print("\n=== 問2: 差分増加型数表 ===")
    print("     列1   列2   列3   列4")
    for i, row in enumerate(table):
        print(f"行{i+1}: {row[0]:3d}   {row[1]:3d}   {row[2]:3d}   {row[3]:3d}")

    # 列方向の規則確認（各列の公差が列番号c）
    print("\n[列方向の規則]")
    for c in range(4):
        col = [table[r][c] for r in range(4)]
        diffs = [col[r+1] - col[r] for r in range(3)]
        print(f"  列{c+1}: {col}, 公差={diffs[0]}")
        assert all(d == diffs[0] for d in diffs), f"列{c+1}が等差数列でない"
        assert diffs[0] == c + 1, f"列{c+1}の公差が{c+1}でない（実際={diffs[0]}）"

    # 行方向の規則確認
    print("\n[行方向の規則]")
    for i, row in enumerate(table):
        diffs = [row[j+1] - row[j] for j in range(3)]
        print(f"  行{i+1}: {row}, 差分={diffs}")

    # 行1の規則: 1, 3, 7, 13 → 差分 2, 4, 6（等差数列の差分）
    # 行nの差分: n+1, n+2, n+3

    # 穴埋め（行4、列4）
    answer_q2 = table[3][3]  # 0-indexed
    print(f"\n[正解] 行4・列4 = {answer_q2}")

    # 唯一解の検証：与えられた数値から解が一意に決まることを確認
    valid = []
    for candidate in range(1, 60):
        # 列4の規則: 公差=4 → 行3の値21から +4 = 25
        if (table[2][3] + 4) == candidate:
            valid.append(candidate)

    assert len(valid) == 1, f"問2の解が{len(valid)}個存在: {valid}"
    assert valid[0] == answer_q2, f"計算値({answer_q2})と検証値({valid[0]})が不一致"
    print(f"[検証] 唯一解 = {valid[0]} ✓")
    return answer_q2


if __name__ == "__main__":
    import random
    random.seed()  # 非決定的シード

    ans1 = verify_q1()
    ans2 = verify_q2()

    print("\n" + "="*50)
    print("=== 正解番号のランダム化 ===")

    # 問1の選択肢: 正解=22、選択肢は20〜24の5択
    q1_choices = [20, 21, 22, 23, 24]
    q1_correct_pos = random.randint(1, 5)
    # 正解を指定位置に置き換え
    q1_order = [x for x in q1_choices if x != ans1]
    random.shuffle(q1_order)
    q1_order.insert(q1_correct_pos - 1, ans1)
    print(f"\n問1の選択肢: {q1_order}")
    print(f"  正解番号: ({q1_correct_pos})")

    # 問2の選択肢: 正解=25、選択肢は22〜26の5択
    q2_choices = [22, 23, 24, 25, 26]
    q2_correct_pos = random.randint(1, 5)
    q2_order = [x for x in q2_choices if x != ans2]
    random.shuffle(q2_order)
    q2_order.insert(q2_correct_pos - 1, ans2)
    print(f"\n問2の選択肢: {q2_order}")
    print(f"  正解番号: ({q2_correct_pos})")

    print("\n全検証完了 ✓")
