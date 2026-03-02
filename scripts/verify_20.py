#!/usr/bin/env python3
"""
verify_20.py - 航大思考20 解の一意性検証スクリプト

問1: スケジューリング論理推論
  5人の候補生A〜Eが月曜日から金曜日に1日1人ずつ体力測定を受ける。
  条件を満たす配置が唯一であることを確認する。

問2: ヒット&ブロー（暗証番号推定）
  4つのヒントから3桁の暗証番号を特定する。
  コードが唯一であることを確認する。
"""

from itertools import permutations


def verify_q1():
    """
    問1: スケジューリング論理推論の検証

    5人（A,B,C,D,E）が月〜金（1〜5）に1日1人ずつ体力測定を受ける。
    条件:
      ① B < A  （BはAより早い曜日）
      ② A < C  （AはCより早い曜日）
      ③ E < C  （EはCより早い曜日）
      ④ |B - E| != 1  （BとEは連続した曜日でない）
      ⑤ C < D  （DはCより遅い曜日）
    """
    days = [1, 2, 3, 4, 5]  # 月=1, 火=2, 水=3, 木=4, 金=5
    day_names = {1: '月', 2: '火', 3: '水', 4: '木', 5: '金'}
    valid = []

    for A, B, C, D, E in permutations(days):
        if (B < A and            # 条件①
                A < C and        # 条件②
                E < C and        # 条件③
                abs(B - E) != 1 and  # 条件④
                C < D):          # 条件⑤
            sol = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E}
            valid.append(sol)

    print("=== 問1 スケジューリング論理推論 ===")
    print(f"有効な解の数: {len(valid)}")
    for sol in valid:
        named = {k: day_names[v] for k, v in sol.items()}
        print(f"  {named}")

    if len(valid) == 1:
        sol = valid[0]
        print("\n[検証成功] 唯一解が確認されました:")
        for person, day in sorted(sol.items()):
            print(f"  {person}: {day_names[day]}曜日（{day}日目）")
    else:
        print(f"\n[検証失敗] 解が{len(valid)}個存在します。条件を見直してください。")

    return valid


def verify_q2():
    """
    問2: ヒット&ブロー（暗証番号推定）の検証

    3桁の暗証番号（各桁1〜9の異なる数字）を4つのヒントから特定する。
    - ヒット（H）: 数字・位置ともに一致
    - ブロー（B）: 数字は合っているが位置が違う

    ヒント:
      試行1: 1 2 3 → 1H 0B
      試行2: 4 5 6 → 1H 0B
      試行3: 7 8 9 → 0H 1B
      試行4: 3 2 7 → 2H 0B
    """
    def check_guess(code, guess):
        """コードと試行を比較してヒット・ブロー数を返す"""
        hits = sum(c == g for c, g in zip(code, guess))
        blows = sum(g in code for g in guess) - hits
        return hits, blows

    # ヒント一覧
    hints = [
        ((1, 2, 3), (1, 0)),   # 試行1: 1H 0B
        ((4, 5, 6), (1, 0)),   # 試行2: 1H 0B
        ((7, 8, 9), (0, 1)),   # 試行3: 0H 1B
        ((3, 2, 7), (2, 0)),   # 試行4: 2H 0B
    ]

    # 1〜9の数字から3桁の異なる数字の組み合わせを全探索
    valid = []
    for code in permutations(range(1, 10), 3):
        if all(check_guess(code, guess) == result for guess, result in hints):
            valid.append(code)

    print("\n=== 問2 ヒット&ブロー（暗証番号推定） ===")
    print(f"有効な解の数: {len(valid)}")
    for sol in valid:
        print(f"  コード: {sol[0]} {sol[1]} {sol[2]}")

    # 正解の検証
    target = (4, 2, 7)
    for guess, expected in hints:
        actual = check_guess(target, guess)
        status = "✓" if actual == expected else "✗"
        print(f"  {status} 試行{guess}: 期待={expected}, 実際={actual}")

    if len(valid) == 1:
        sol = valid[0]
        print(f"\n[検証成功] 唯一解が確認されました: {sol[0]}{sol[1]}{sol[2]}")
    else:
        print(f"\n[検証失敗] 解が{len(valid)}個存在します。ヒントを見直してください。")

    return valid


if __name__ == '__main__':
    q1_solutions = verify_q1()
    q2_solutions = verify_q2()

    print("\n" + "=" * 50)
    if len(q1_solutions) == 1 and len(q2_solutions) == 1:
        print("両問題とも唯一解が確認されました。問題セット20は検証OKです。")
    else:
        print("検証失敗。問題の設計を見直してください。")
