#!/usr/bin/env python3
"""
解の一意性検証テンプレート

このファイルは問題作成時にコピーして使用します。
各問題タイプに応じたテンプレートを選択し、条件を記述してください。

使用方法:
    1. このファイルを scripts/verify_XX.py としてコピー
    2. 問題に応じたテンプレートを選択
    3. 条件を記述して実行
    4. 解が唯一であることを確認

例:
    cp scripts/verify_template.py scripts/verify_21.py
    python3 scripts/verify_21.py
"""

from itertools import permutations, product
from typing import List, Set, Tuple, Any


# ============================================================
# テンプレート1: 順序配置問題
# ============================================================
def verify_ordering_problem():
    """
    順序配置問題の検証テンプレート

    例: A, B, C, D, Eの5人を1〜5番目に配置する問題
    """
    items = ['A', 'B', 'C', 'D', 'E']
    valid_solutions = []

    for perm in permutations(items):
        # perm[0]が1番目、perm[1]が2番目、...
        pos = {item: i + 1 for i, item in enumerate(perm)}

        # ===== ここに制約条件を記述 =====
        # 例: AはBより前
        if not (pos['A'] < pos['B']):
            continue

        # 例: CはDの隣
        if not (abs(pos['C'] - pos['D']) == 1):
            continue

        # 例: Eは3番目ではない
        if pos['E'] == 3:
            continue

        # ===== 制約条件ここまで =====

        valid_solutions.append(perm)

    print(f"有効な解の数: {len(valid_solutions)}")
    for sol in valid_solutions:
        print(f"  {sol}")

    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在します（1個であるべき）"
    print("\n検証成功: 解は唯一です")
    return valid_solutions[0]


# ============================================================
# テンプレート2: グリッド論理演算問題（XOR, AND, OR等）
# ============================================================
def verify_grid_operation():
    """
    グリッド論理演算問題の検証テンプレート

    例: 2つの3x3グリッドにXOR演算を適用
    """
    # グリッドを定義（0=白, 1=黒）
    grid_a = [
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]

    grid_b = [
        [1, 1, 0],
        [0, 0, 1],
        [0, 0, 0]
    ]

    # XOR演算を適用
    def xor_grids(g1, g2):
        return [[g1[i][j] ^ g2[i][j] for j in range(3)] for i in range(3)]

    # AND演算
    def and_grids(g1, g2):
        return [[g1[i][j] & g2[i][j] for j in range(3)] for i in range(3)]

    # OR演算
    def or_grids(g1, g2):
        return [[g1[i][j] | g2[i][j] for j in range(3)] for i in range(3)]

    result = xor_grids(grid_a, grid_b)

    print("グリッドA:")
    for row in grid_a:
        print(f"  {['白' if c == 0 else '黒' for c in row]}")

    print("\nグリッドB:")
    for row in grid_b:
        print(f"  {['白' if c == 0 else '黒' for c in row]}")

    print("\n結果 (XOR):")
    for row in result:
        print(f"  {['白' if c == 0 else '黒' for c in row]}")

    return result


# ============================================================
# テンプレート3: パターン認識問題
# ============================================================
def verify_pattern_problem():
    """
    パターン認識問題の検証テンプレート

    例: 数列の次の値を求める
    """
    # 既知の数列
    sequence = [3, 5, 7, 9]  # 等差数列

    # 可能な規則を定義
    rules = [
        ("等差+2", lambda n: 3 + 2 * n),
        ("奇数列", lambda n: 2 * n + 3),
        ("等差+3", lambda n: 3 + 3 * n),
    ]

    valid_rules = []

    for name, rule in rules:
        # 規則が既存の数列に一致するかチェック
        matches = all(rule(i) == sequence[i] for i in range(len(sequence)))
        if matches:
            next_value = rule(len(sequence))
            valid_rules.append((name, next_value))
            print(f"規則「{name}」: 一致 -> 次の値 = {next_value}")
        else:
            print(f"規則「{name}」: 不一致")

    print(f"\n有効な規則の数: {len(valid_rules)}")
    return valid_rules


# ============================================================
# テンプレート4: 制約充足問題（CSP）
# ============================================================
def verify_csp_problem():
    """
    制約充足問題の検証テンプレート

    例: 複数の変数に値を割り当てる問題
    """
    # 変数とドメイン（取りうる値）
    variables = ['X', 'Y', 'Z']
    domains = {
        'X': [1, 2, 3, 4, 5],
        'Y': [1, 2, 3, 4, 5],
        'Z': [1, 2, 3, 4, 5],
    }

    valid_solutions = []

    # 全ての組み合わせを試す
    for x in domains['X']:
        for y in domains['Y']:
            for z in domains['Z']:
                assignment = {'X': x, 'Y': y, 'Z': z}

                # ===== ここに制約条件を記述 =====
                # 例: X + Y + Z = 10
                if not (x + y + z == 10):
                    continue

                # 例: X < Y < Z
                if not (x < y < z):
                    continue

                # 例: Zは偶数
                if z % 2 != 0:
                    continue

                # ===== 制約条件ここまで =====

                valid_solutions.append(assignment)

    print(f"有効な解の数: {len(valid_solutions)}")
    for sol in valid_solutions:
        print(f"  {sol}")

    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在します（1個であるべき）"
    print("\n検証成功: 解は唯一です")
    return valid_solutions[0]


# ============================================================
# テンプレート5: 天秤問題
# ============================================================
def verify_balance_problem():
    """
    天秤問題の検証テンプレート

    例: 3つのアイテムの重さを比較から推定
    """
    items = ['A', 'B', 'C', 'D']
    weight_range = range(1, 11)  # 1〜10の重さ

    valid_solutions = []

    for weights in product(weight_range, repeat=len(items)):
        w = dict(zip(items, weights))

        # ===== ここに制約条件を記述 =====
        # 例: A + B > C + D
        if not (w['A'] + w['B'] > w['C'] + w['D']):
            continue

        # 例: A < B
        if not (w['A'] < w['B']):
            continue

        # 例: C = D + 2
        if not (w['C'] == w['D'] + 2):
            continue

        # ===== 制約条件ここまで =====

        valid_solutions.append(w)

    print(f"有効な解の数: {len(valid_solutions)}")

    # 解が多すぎる場合は最初の10個だけ表示
    for sol in valid_solutions[:10]:
        print(f"  {sol}")
    if len(valid_solutions) > 10:
        print(f"  ... 他 {len(valid_solutions) - 10} 個")

    return valid_solutions


# ============================================================
# テンプレート6: 暗号解読問題
# ============================================================
def verify_cipher_problem():
    """
    暗号解読問題の検証テンプレート

    例: 文字を数字に置き換える暗号
    """
    # 暗号文と平文の対応
    # SEND + MORE = MONEY のような問題

    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    valid_solutions = []

    for perm in permutations(range(10), len(letters)):
        mapping = dict(zip(letters, perm))

        # 先頭文字は0ではない制約
        if mapping['S'] == 0 or mapping['M'] == 0:
            continue

        # SEND + MORE = MONEY を検証
        send = mapping['S'] * 1000 + mapping['E'] * 100 + mapping['N'] * 10 + mapping['D']
        more = mapping['M'] * 1000 + mapping['O'] * 100 + mapping['R'] * 10 + mapping['E']
        money = mapping['M'] * 10000 + mapping['O'] * 1000 + mapping['N'] * 100 + mapping['E'] * 10 + mapping['Y']

        if send + more == money:
            valid_solutions.append(mapping)

    print(f"有効な解の数: {len(valid_solutions)}")
    for sol in valid_solutions:
        print(f"  {sol}")

    return valid_solutions


# ============================================================
# メイン: 使用するテンプレートを選択して実行
# ============================================================
if __name__ == '__main__':
    print("="*60)
    print("解の一意性検証")
    print("="*60)

    # 使用するテンプレートをコメント解除して実行
    # verify_ordering_problem()
    # verify_grid_operation()
    # verify_pattern_problem()
    verify_csp_problem()
    # verify_balance_problem()
    # verify_cipher_problem()
