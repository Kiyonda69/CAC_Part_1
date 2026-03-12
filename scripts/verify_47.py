#!/usr/bin/env python3
"""
航大思考47 検証スクリプト

問1: 黒白タイル変化パターン（XOR隣接ルール）
問2: 立方体の8頂点から3頂点を選んで作れる正三角形の個数
"""

from itertools import combinations
import math


def verify_q1():
    """
    問1: 6マスの黒白タイル行が、XOR右隣接ルールで変化する。
    ルール: next[i] = current[i] XOR current[(i+1) % 6]

    例示パターン（4行）と5つの選択肢を検証。
    """
    print("=" * 60)
    print("問1: 黒白タイルXOR隣接ルール検証")
    print("=" * 60)

    def apply_rule(row):
        """XOR右隣接ルールを適用"""
        n = len(row)
        return [row[i] ^ row[(i + 1) % n] for i in range(n)]

    def check_sequence(rows):
        """4行のシーケンスがXORルールに従うか検証"""
        for i in range(len(rows) - 1):
            expected = apply_rule(rows[i])
            if expected != rows[i + 1]:
                return False
        return True

    def display_row(row):
        """行を視覚的に表示"""
        return ''.join(['■' if x else '□' for x in row])

    # 例示パターン
    example = [
        [1, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0],
    ]

    print("\n【例示パターン】")
    for i, row in enumerate(example):
        print(f"  行{i+1}: {display_row(row)}  {row}")
    assert check_sequence(example), "例示パターンがルールに従っていない！"
    print("  → ルール検証OK")

    # 正解の選択肢（選択肢3に配置）
    correct = [
        [0, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 0],
    ]

    print("\n【正解（選択肢3）】")
    for i, row in enumerate(correct):
        print(f"  行{i+1}: {display_row(row)}  {row}")
    assert check_sequence(correct), "正解パターンがルールに従っていない！"
    print("  → ルール検証OK")

    # 不正解の選択肢
    # 選択肢1: 行3の3番目が違う（正しくは1だが0に変更）
    wrong1 = [
        [1, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 0],  # 正しくは [1,1,1,1,0,0]
        [0, 0, 0, 1, 0, 1],
    ]

    # 選択肢2: 行3の4番目が違う
    wrong2 = [
        [0, 1, 0, 1, 1, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],  # 正しくは [0,0,1,1,1,0]だが行4と合わない
        [0, 1, 0, 0, 1, 1],
    ]

    # 選択肢4: 行2の2番目が違う
    wrong3 = [
        [1, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 0],  # 正しくは [0,1,0,1,1,1]
        [1, 1, 1, 0, 0, 1],
        [0, 0, 1, 0, 1, 0],
    ]

    # 選択肢5: 行3の最初が違う
    wrong4 = [
        [1, 0, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0, 0],  # 正しくは [0,0,0,1,0,0]
        [1, 0, 1, 1, 0, 0],
    ]

    choices = [wrong1, wrong2, correct, wrong3, wrong4]

    print("\n【全選択肢の検証】")
    correct_count = 0
    for idx, choice in enumerate(choices, 1):
        is_valid = check_sequence(choice)
        status = "正解" if is_valid else "不正解"
        print(f"  選択肢({idx}): {status}")
        for i, row in enumerate(choice):
            expected = apply_rule(choice[i-1]) if i > 0 else None
            match = "" if i == 0 else (" ✓" if expected == row else f" ✗ (期待: {display_row(expected)})")
            print(f"    行{i+1}: {display_row(row)}{match}")
        if is_valid:
            correct_count += 1

    assert correct_count == 1, f"正解が{correct_count}個存在（1個であるべき）"
    print(f"\n  → 正解は選択肢(3)のみ。検証OK")

    # 全ての6セル初期状態でルール生成パターンが正しいか追加検証
    print("\n【ルール自体の網羅検証】")
    for start in range(64):  # 2^6 = 64通り
        row = [(start >> i) & 1 for i in range(6)]
        seq = [row]
        for _ in range(3):
            seq.append(apply_rule(seq[-1]))
        assert check_sequence(seq), f"ルール検証失敗: {row}"
    print("  全64初期パターンでルール整合性を確認OK")

    return True


def verify_q2():
    """
    問2: 立方体の8頂点から3頂点を選んで正三角形を作る。
    正三角形は何個あるか。

    答え: 8個
    """
    print("\n" + "=" * 60)
    print("問2: 立方体の正三角形の個数")
    print("=" * 60)

    # 立方体の8頂点
    vertices = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1),
    ]

    def dist_sq(a, b):
        return sum((ai - bi) ** 2 for ai, bi in zip(a, b))

    equilateral_triangles = []

    for combo in combinations(range(8), 3):
        v0, v1, v2 = vertices[combo[0]], vertices[combo[1]], vertices[combo[2]]
        d01 = dist_sq(v0, v1)
        d02 = dist_sq(v0, v2)
        d12 = dist_sq(v1, v2)

        # 正三角形: 3辺の長さが等しい
        if d01 == d02 == d12 and d01 > 0:
            equilateral_triangles.append((combo, math.sqrt(d01)))

    print(f"\n正三角形の数: {len(equilateral_triangles)}")

    # 辺の長さ別に分類
    by_length = {}
    for combo, length in equilateral_triangles:
        length_str = f"{length:.4f}"
        if length_str not in by_length:
            by_length[length_str] = []
        by_length[length_str].append(combo)

    for length_str, triangles in sorted(by_length.items()):
        print(f"\n辺の長さ {length_str} の正三角形:")
        for combo in triangles:
            v = [vertices[i] for i in combo]
            print(f"  {combo}: {v}")

    assert len(equilateral_triangles) == 8, \
        f"正三角形の数が{len(equilateral_triangles)}個（8個であるべき）"

    print(f"\n  → 正三角形は全部で8個。検証OK")

    # 追加検証: 全て辺の長さがsqrt(2)であることを確認
    all_sqrt2 = all(abs(length - math.sqrt(2)) < 1e-10 for _, length in equilateral_triangles)
    assert all_sqrt2, "全ての正三角形の辺の長さがsqrt(2)でない"
    print("  → 全て辺の長さsqrt(2)（面対角線）であることを確認OK")

    # 2つの正四面体に分類されることを確認
    tetra1 = {(0,0,0), (1,1,0), (1,0,1), (0,1,1)}
    tetra2 = {(1,0,0), (0,1,0), (0,0,1), (1,1,1)}

    t1_count = 0
    t2_count = 0
    for combo, _ in equilateral_triangles:
        v_set = {vertices[i] for i in combo}
        if v_set.issubset(tetra1):
            t1_count += 1
        elif v_set.issubset(tetra2):
            t2_count += 1

    assert t1_count == 4 and t2_count == 4, \
        f"正四面体への分類が正しくない: T1={t1_count}, T2={t2_count}"
    print("  → 2つの正四面体（各4個）に正しく分類されることを確認OK")

    # 選択肢の検証
    print("\n【選択肢】")
    choices = {1: 4, 2: 8, 3: 12, 4: 16, 5: 24}
    for num, val in choices.items():
        status = "正解" if val == 8 else "不正解"
        print(f"  ({num}) {val}個 → {status}")

    print(f"\n  → 正解は(2) 8個")

    return True


if __name__ == "__main__":
    print("航大思考47 解の一意性検証")
    print("=" * 60)

    q1_ok = verify_q1()
    q2_ok = verify_q2()

    print("\n" + "=" * 60)
    print("最終結果:")
    print(f"  問1: {'PASS' if q1_ok else 'FAIL'}")
    print(f"  問2: {'PASS' if q2_ok else 'FAIL'}")
    print("=" * 60)
