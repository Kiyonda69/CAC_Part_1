"""
航大思考205 検証スクリプト
問1: 11人のテスト得点から5数要約と四分位範囲を求める
問2: 一部欠損の9人データを箱ひげ図情報と平均から復元する
"""

# ===== 問1の検証 =====
def verify_q1():
    data = [64, 36, 78, 50, 92, 70, 42, 75, 60, 55, 84]
    sorted_data = sorted(data)
    print("問1 整列データ:", sorted_data)

    n = len(sorted_data)
    assert n == 11

    min_v = sorted_data[0]
    max_v = sorted_data[-1]
    median = sorted_data[5]  # 6番目（インデックス5）

    # 下半分: インデックス 0-4 の中央値（3番目=インデックス2）
    lower = sorted_data[:5]
    q1 = lower[2]
    # 上半分: インデックス 6-10 の中央値（9番目=インデックス8）
    upper = sorted_data[6:]
    q3 = upper[2]

    iqr = q3 - q1
    rng = max_v - min_v

    print(f"  最小値={min_v}, Q1={q1}, 中央値={median}, Q3={q3}, 最大値={max_v}")
    print(f"  範囲={rng}, IQR={iqr}")

    assert (min_v, q1, median, q3, max_v, iqr) == (36, 50, 64, 78, 92, 28), \
        "問1の値が想定と異なる"
    print("  ✓ 問1検証OK 正解=(2): 最小36/Q1=50/中央64/Q3=78/最大92/IQR=28")


# ===== 問2の検証 =====
def verify_q2():
    """
    9人のデータ（昇順）: a, 38, 45, b, 58, c, 70, 75, d
    箱ひげ図情報:
      最小値=28, 第1四分位数=41.5, 中央値=58,
      第3四分位数=72.5, 最大値=88
    追加情報: 平均値=58, cはbより20点高い
    """
    solutions = []

    for a in range(0, 39):  # a ≤ 38（最小値）
        for d in range(75, 121):  # d ≥ 75（最大値）
            for b in range(45, 59):  # 45 ≤ b ≤ 58
                for c in range(58, 71):  # 58 ≤ c ≤ 70
                    seq = [a, 38, 45, b, 58, c, 70, 75, d]
                    # 昇順性チェック
                    if seq != sorted(seq):
                        continue
                    # 最小値・最大値
                    if min(seq) != 28 or max(seq) != 88:
                        continue
                    # 中央値（5番目=インデックス4）
                    if seq[4] != 58:
                        continue
                    # 第1四分位数: 下半分4個 → (2番目+3番目)/2 = インデックス1,2
                    q1 = (seq[1] + seq[2]) / 2
                    if q1 != 41.5:
                        continue
                    # 第3四分位数: 上半分4個 → (7番目+8番目)/2 = インデックス6,7
                    q3 = (seq[6] + seq[7]) / 2
                    if q3 != 72.5:
                        continue
                    # 平均値
                    if sum(seq) != 58 * 9:
                        continue
                    # 追加条件: c = b + 20
                    if c - b != 20:
                        continue
                    solutions.append((a, b, c, d))

    print(f"問2 解の個数: {len(solutions)}")
    for s in solutions:
        print(f"  (a,b,c,d) = {s}, 和 = {sum(s)}")

    assert len(solutions) == 1, f"解が一意でない: {len(solutions)}個"
    a, b, c, d = solutions[0]
    assert (a, b, c, d) == (28, 50, 70, 88), "問2の値が想定と異なる"
    assert sum(solutions[0]) == 236, "和が想定と異なる"
    print("  ✓ 問2検証OK 正解=(4): a+b+c+d=236")


if __name__ == "__main__":
    verify_q1()
    print()
    verify_q2()
    print("\nすべての検証が完了しました。")
