#!/usr/bin/env python3
"""
verify_21.py - 航大思考21の解の一意性検証

問1: 正六角形の扇形回転パターン（平面図形規則性）
問2: 3×3 X分割正方形行列（複合規則性）
"""

import random

# ──────────────────────────────────────────────
# 問1: 正六角形の扇形回転パターン
# ──────────────────────────────────────────────

def verify_q1():
    """
    正六角形を6等分した扇形のうち、隣接する2つが塗りつぶされている。
    各ステップで塗りつぶし領域が時計回りに1扇形ずつ移動する。
    A→B→C→D→? のパターンから?を求める。

    扇形番号 (時計回り):
      1: 右上 (V0-V1)
      2: 右   (V1-V2)
      3: 右下 (V2-V3)
      4: 左下 (V3-V4)
      5: 左   (V4-V5)
      6: 左上 (V5-V0)
    """
    def get_filled_sectors(step):
        """step=0→A, 1→B, 2→C, 3→D, 4→?"""
        s1 = (step % 6) + 1
        s2 = ((step + 1) % 6) + 1
        return (s1, s2)

    print("=" * 50)
    print("問1: 正六角形扇形回転パターン")
    print("=" * 50)

    labels = ['A', 'B', 'C', 'D', '?']
    sector_names = {
        1: '右上', 2: '右', 3: '右下',
        4: '左下', 5: '左', 6: '左上'
    }
    for i in range(5):
        s = get_filled_sectors(i)
        print(f"  {labels[i]}: 扇形{s[0]}({sector_names[s[0]]}) + 扇形{s[1]}({sector_names[s[1]]})")

    answer_sectors = get_filled_sectors(4)
    print(f"\n  正解: 扇形{answer_sectors[0]}({sector_names[answer_sectors[0]]}) "
          f"+ 扇形{answer_sectors[1]}({sector_names[answer_sectors[1]]})")

    # 選択肢の定義（正解は位置2に配置）
    options = {
        1: (4, 5),  # 左下+左 (D=直前)
        2: (5, 6),  # 左+左上 ← 正解
        3: (6, 1),  # 左上+右上 (1つ多く回った)
        4: (3, 4),  # 右下+左下 (C=2ステップ前)
        5: (1, 2),  # 右上+右 (A=最初)
    }

    correct_answers = [
        k for k, v in options.items()
        if set(v) == set(answer_sectors)
    ]

    print("\n  選択肢:")
    for k, v in options.items():
        mark = "← 正解" if set(v) == set(answer_sectors) else ""
        print(f"    ({k}): 扇形{v[0]}+{v[1]}  {mark}")

    assert len(correct_answers) == 1, f"正解が{len(correct_answers)}個存在"
    assert correct_answers[0] == 2, \
        f"正解は選択肢{correct_answers[0]} (期待値: 2)"

    print(f"\n  [検証OK] 唯一解 = 選択肢({correct_answers[0]})")
    return correct_answers[0]


# ──────────────────────────────────────────────
# 問2: 3×3 X分割正方形行列
# ──────────────────────────────────────────────

def verify_q2():
    """
    正方形を対角線で4分割（三角形: 上・右・下・左）した図形を3×3に配置。
    行ルール: 塗りつぶし開始位置が行ごとに1つずつ時計回りにずれる
      行1: 上から開始
      行2: 右から開始
      行3: 下から開始
    列ルール: 塗りつぶし三角形の数が列番号に等しい
      列1: 1個
      列2: 2個
      列3: 3個
    """
    triangles = ['上', '右', '下', '左']  # 時計回り順

    def get_filled(row, col):
        """行row・列colのセルの塗りつぶし三角形セットを返す"""
        start = (row - 1) % 4  # 行1→0(上), 行2→1(右), 行3→2(下)
        return frozenset(triangles[(start + k) % 4] for k in range(col))

    print("\n" + "=" * 50)
    print("問2: 3×3 X分割正方形行列")
    print("=" * 50)

    print("  マトリクス全体:")
    for r in range(1, 4):
        cells = []
        for c in range(1, 4):
            f = sorted(get_filled(r, c),
                       key=lambda x: triangles.index(x))
            cells.append(f"+".join(f) if f else "-")
        print(f"  行{r}: {' | '.join(cells)}")

    answer = get_filled(3, 3)
    not_filled = set(triangles) - answer
    print(f"\n  正解 (行3, 列3):")
    print(f"    塗りつぶし: {'+'.join(sorted(answer, key=lambda x: triangles.index(x)))}")
    print(f"    未塗り:    {'+'.join(sorted(not_filled, key=lambda x: triangles.index(x)))}")

    # 選択肢の定義（3個塗りつぶしの4通り + 全塗り1通り）
    options = {
        1: frozenset(['上', '右', '下']),         # 左が未塗り
        2: frozenset(['右', '下', '左']),         # 上が未塗り
        3: frozenset(['下', '左', '上']),         # 右が未塗り ← 正解
        4: frozenset(['左', '上', '右']),         # 下が未塗り
        5: frozenset(['上', '右', '下', '左']),   # 全塗り
    }

    correct_answers = [k for k, v in options.items() if v == answer]

    print("\n  選択肢:")
    for k, v in options.items():
        mark = "← 正解" if v == answer else ""
        label = '+'.join(sorted(v, key=lambda x: triangles.index(x)))
        print(f"    ({k}): {label}  {mark}")

    assert len(correct_answers) == 1, f"正解が{len(correct_answers)}個存在"
    assert correct_answers[0] == 3, \
        f"正解は選択肢{correct_answers[0]} (期待値: 3)"  # 問2の正解位置=3

    print(f"\n  [検証OK] 唯一解 = 選択肢({correct_answers[0]})")
    return correct_answers[0]


# ──────────────────────────────────────────────
# 正解番号のランダム化確認
# ──────────────────────────────────────────────

def check_answer_distribution():
    print("\n" + "=" * 50)
    print("正解番号の確認")
    print("=" * 50)
    print("  問1 正解: (2)  ← ランダム化後の配置")
    print("  問2 正解: (3)  ← ランダム化後の配置")


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()
    check_answer_distribution()

    print("\n" + "=" * 50)
    print("最終確認")
    print("=" * 50)
    print(f"  問1 正解: ({q1_answer})  [期待値: 2]")
    print(f"  問2 正解: ({q2_answer})  [期待値: 3]")
    print("  解の一意性: 両問とも唯一解を確認")
    print("=" * 50)
