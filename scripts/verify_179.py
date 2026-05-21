"""
航大思考179 検証スクリプト

問1: パターン認識
  列: 白円, 黒三角, 白四角, 黒円, 白三角, ?
  規則(形): 円, 三角, 四角 の3周期循環
  規則(色): 白, 黒 の2周期循環
  → ?=黒四角(■)

問2: フィボナッチ的な面積問題
  1辺1の正方形から、長辺を1辺とする正方形を加える操作を9回行う。
  → 面積 = F(10) × F(11) = 55 × 89 = 4895
"""


def verify_q1():
    """問1: パターン認識の一意性確認"""
    # 形 (0:円, 1:三角, 2:四角) 3周期
    # 色 (0:白, 1:黒) 2周期
    shapes = ["円", "三角", "四角"]
    colors = ["白", "黒"]

    sequence = []
    for i in range(6):
        sequence.append((colors[i % 2], shapes[i % 3]))

    print("問1: 列の構成")
    for i, (c, s) in enumerate(sequence, 1):
        marker = " ← ?" if i == 6 else ""
        print(f"  {i}: {c}{s}{marker}")

    expected_answer = ("黒", "四角")
    assert sequence[5] == expected_answer, f"答が一致しません: {sequence[5]} != {expected_answer}"
    print(f"問1 答: {sequence[5][0]}{sequence[5][1]}")

    # 選択肢で一致するのは■のみ
    options = [
        (1, "白", "円"),     # ○
        (2, "黒", "三角"),   # ▲
        (3, "黒", "四角"),   # ■ ← 正解
        (4, "白", "四角"),   # □
        (5, "黒", "円"),     # ●
    ]
    matches = [n for n, c, s in options if (c, s) == expected_answer]
    assert matches == [3], f"選択肢が一意でない: {matches}"
    print(f"問1 一意解: 選択肢({matches[0]})\n")


def verify_q2():
    """問2: 操作9回後の長方形面積"""
    # 初期: 1x1の正方形
    short, long_ = 1, 1
    print("問2: 操作ごとの長方形サイズ")
    print(f"  開始: {short}×{long_} (面積={short*long_})")

    for n in range(1, 10):
        # 長辺を1辺とする正方形を並べる
        # 短辺は元の長辺、長辺は (短辺+長辺) になる
        new_short = long_
        new_long = short + long_
        short, long_ = new_short, new_long
        print(f"  {n}回目: {short}×{long_} (面積={short*long_})")

    area = short * long_
    print(f"\n問2 答: {area}")
    assert area == 4895, f"想定と異なる: {area}"

    # フィボナッチで検証
    fib = [0, 1, 1]
    for _ in range(15):
        fib.append(fib[-1] + fib[-2])
    # 9回操作後は F(10) × F(11)
    expected = fib[10] * fib[11]
    print(f"  フィボナッチ検証: F(10)×F(11) = {fib[10]}×{fib[11]} = {expected}")
    assert area == expected

    # 選択肢と一意性
    options = {1: 4895, 2: 1870, 3: 2584, 4: 6765, 5: 3025}
    matches = [k for k, v in options.items() if v == area]
    assert matches == [1], f"選択肢が一意でない: {matches}"
    print(f"問2 一意解: 選択肢({matches[0]})\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("=== すべて検証完了 ===")
