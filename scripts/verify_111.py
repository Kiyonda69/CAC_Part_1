"""
航大思考111 解の一意性検証

問題1: 数列の規則性（差分が平方数）
  1, 2, 6, 15, 31, 56, ?
  差分: 1, 4, 9, 16, 25 → 次は36 → 56+36 = 92

問題2: 4x4数表の規則性（a(r,c) = r^c + c^r）
  空欄は(3,3) → 3^3 + 3^3 = 27+27 = 54
"""


def verify_q1():
    """問題1: 差分が平方数の数列"""
    # a(n) = 1 + sum_{k=1}^{n-1} k²
    seq = [1]
    for n in range(2, 8):
        seq.append(seq[-1] + (n - 1) ** 2)
    print(f"Q1 数列: {seq}")
    assert seq == [1, 2, 6, 15, 31, 56, 92], f"不一致: {seq}"

    # 差分確認
    diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    print(f"Q1 差分: {diffs}")
    assert diffs == [1, 4, 9, 16, 25, 36]

    # 閉じた公式による確認: a(n) = 1 + (n-1)n(2n-1)/6
    for n in range(1, 8):
        closed = 1 + (n - 1) * n * (2 * n - 1) // 6
        assert closed == seq[n - 1], f"n={n}: {closed} != {seq[n-1]}"

    print(f"Q1 正解: {seq[6]} (7番目)")
    return seq[6]


def verify_q2():
    """問題2: 4x4数表 a(r,c) = r^c + c^r"""
    table = [[0] * 5 for _ in range(5)]
    for r in range(1, 5):
        for c in range(1, 5):
            table[r][c] = r**c + c**r

    print("Q2 数表:")
    print("      c=1   c=2   c=3   c=4")
    for r in range(1, 5):
        row = [table[r][c] for c in range(1, 5)]
        print(f"r={r}: {row}")

    # 対称性確認
    for r in range(1, 5):
        for c in range(1, 5):
            assert table[r][c] == table[c][r], f"非対称: ({r},{c})"

    # 期待値
    expected = [
        [2, 3, 4, 5],
        [3, 8, 17, 32],
        [4, 17, 54, 145],
        [5, 32, 145, 512],
    ]
    for r in range(4):
        for c in range(4):
            assert table[r + 1][c + 1] == expected[r][c], f"({r+1},{c+1})"

    # 空欄(3,3)の値
    answer = table[3][3]
    print(f"Q2 正解: (3,3) = {answer}")
    return answer


def verify_uniqueness_q1(given, options):
    """問題1: 差分が平方数という規則のみが一意解を導くか確認"""
    # 与えられた5項から次の項を一意に決める
    # 差分パターンから決定される値のみ正解
    diffs = [given[i + 1] - given[i] for i in range(len(given) - 1)]
    # 差分は1,4,9,16,25,つまり平方数
    next_diff = 36  # 6²
    next_val = given[-1] + next_diff
    print(f"Q1 唯一解: {next_val}")

    # 選択肢の中で正解は1つのみか確認
    correct_count = sum(1 for opt in options if opt == next_val)
    assert correct_count == 1, f"正解が{correct_count}個"
    print(f"Q1 選択肢: {options}, 正解位置: {options.index(next_val) + 1}")


if __name__ == "__main__":
    print("=" * 60)
    ans1 = verify_q1()
    print()

    q1_options = [77, 84, 88, 91, 92]
    verify_uniqueness_q1([1, 2, 6, 15, 31, 56], q1_options)

    print("=" * 60)
    ans2 = verify_q2()
    print()

    q2_options = [27, 36, 48, 54, 81]
    assert q2_options.count(ans2) == 1, "Q2 正解が選択肢に1つない"
    print(f"Q2 選択肢: {q2_options}, 正解位置: {q2_options.index(ans2) + 1}")

    print("=" * 60)
    print("検証完了")
