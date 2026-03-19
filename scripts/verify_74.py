"""
航大思考74 検証スクリプト
問1: 数表パズル（加法的行列）
問2: 図形パターン認識（3進数エンコーディング）
"""


def verify_q1():
    """問1: 数表パズルの解の一意性を検証"""
    print("=== 問1: 数表パズル ===")

    # 既知のセル値
    table = [
        [48, 41, 46],
        [38, 31, 36],
        [30, 23, 28],
        [46, None, 44],  # ?は(3,1)
    ]

    # 全選択肢を検証
    choices = {1: 39, 2: 33, 3: 36, 4: 41, 5: 44}
    valid = []

    for choice_num, value in choices.items():
        table[3][1] = value
        # 全ての2x2部分行列で加法的性質を確認
        # a[i][j] - a[i][k] が行iに依存しない
        is_valid = True
        for j in range(3):
            for k in range(j + 1, 3):
                diffs = set()
                for i in range(4):
                    diffs.add(table[i][j] - table[i][k])
                if len(diffs) != 1:
                    is_valid = False
                    break
            if not is_valid:
                break
        if is_valid:
            valid.append((choice_num, value))
            print(f"  選択肢({choice_num}) {value}: 有効")
        else:
            print(f"  選択肢({choice_num}) {value}: 無効")

    assert len(valid) == 1, f"解が{len(valid)}個: {valid}"
    assert valid[0] == (1, 39), f"正解が(1) 39でない: {valid[0]}"
    print(f"  正解: ({valid[0][0]}) {valid[0][1]}")
    print("  解の一意性: OK\n")


def verify_q2():
    """問2: 3進数エンコーディングの検証"""
    print("=== 問2: 3進数図形パターン ===")

    def to_base3(n):
        """数値を4桁の3進数タプルに変換"""
        q1 = n // 27
        r = n % 27
        q2 = r // 9
        r = r % 9
        q3 = r // 3
        q4 = r % 3
        return (q1, q2, q3, q4)

    def from_base3(digits):
        """3進数タプルから数値を復元"""
        return digits[0] * 27 + digits[1] * 9 + digits[2] * 3 + digits[3]

    # 1-12の検証
    print("  例示パターン (1-12):")
    colors = {0: "白", 1: "灰", 2: "黒"}
    for n in range(1, 13):
        d = to_base3(n)
        assert from_base3(d) == n, f"{n}の変換が不正"
        c = ",".join(colors[x] for x in d)
        print(f"    {n:2d} = {d} ({c})")

    # 47の検証
    target = 47
    d47 = to_base3(target)
    assert from_base3(d47) == target
    print(f"\n  目標: {target} = {d47}")

    # 選択肢の検証
    choices = {
        1: (1, 1, 2, 2),  # 44
        2: (1, 2, 0, 1),  # 46
        3: (1, 2, 1, 0),  # 48
        4: (1, 2, 1, 2),  # 50
        5: (1, 2, 0, 2),  # 47 (正解)
    }

    print("\n  選択肢:")
    valid = []
    for num, digits in sorted(choices.items()):
        val = from_base3(digits)
        is_correct = val == target
        status = "正解" if is_correct else "不正解"
        c = ",".join(colors[x] for x in digits)
        print(f"    ({num}) {digits} ({c}) = {val} [{status}]")
        if is_correct:
            valid.append(num)

    assert len(valid) == 1, f"正解が{len(valid)}個"
    assert valid[0] == 5, f"正解が(5)でない: ({valid[0]})"
    print(f"\n  正解: ({valid[0]})")
    print("  解の一意性: OK\n")

    # エンコーディング全体の一意性確認
    seen = {}
    for n in range(0, 81):
        d = to_base3(n)
        assert d not in seen, f"重複: {n} と {seen[d]}"
        seen[d] = n
    print("  3進エンコーディングの一意性 (0-80): OK")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n全検証完了: 問1・問2ともに唯一解を確認")
