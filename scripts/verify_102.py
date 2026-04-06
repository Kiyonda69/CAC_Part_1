#!/usr/bin/env python3
"""
航大思考102 検証スクリプト
問1: 数表の規則性（正解: (4) = 15）
問2: 図形マトリックスの規則（正解: (3) = 小さい黒塗り三角形・印が上）
"""

def verify_q1():
    """問1: 数表の規則性 - 解の一意性検証"""
    print("=" * 50)
    print("問1: 数表の規則性")
    print("=" * 50)

    # 数表: 各行は「前の数 × 3 + 加算値」の規則
    # ア行: ×3+0, イ行: ×3+1, ウ行: ×3+2, エ行: ×3+3
    table = {
        'ア': [1, 3, 9, 27],
        'イ': [2, 7, 22, 67],
        'ウ': [3, 11, 35, 107],
        'エ': [4, None, 48, 147]  # ?は2列目
    }

    # 横方向の規則検証
    print("\n【横方向の規則検証】")
    for row_name in ['ア', 'イ', 'ウ']:
        row = table[row_name]
        # f(x) = x*m + b を求める
        # row[1] = row[0]*m + b, row[2] = row[1]*m + b
        m = (row[2] - row[1]) / (row[1] - row[0]) if row[1] != row[0] else None
        if m is not None:
            b = row[1] - m * row[0]
            valid = all(abs(row[i+1] - (m * row[i] + b)) < 0.001 for i in range(3))
            print(f"  {row_name}行: ×{m:.0f}+{b:.0f} → {row} {'✓' if valid else '✗'}")
            assert valid, f"{row_name}行の規則が不正"

    # エ行: 4, ?, 48, 147
    # ?→48 と 48→147 から m と b を求める
    # 48*m + b = 147 ... (1)
    # ?*m + b = 48  ... (2)
    # 4*m + b = ?   ... (3)
    # (1)-(2): (48-?)*m = 99
    # (3): ? = 4*m + b → (2): (4*m+b)*m + b = 48

    # 他の行から m=3 と推定
    m = 3
    b = 147 - m * 48  # = 147 - 144 = 3
    missing = m * 4 + b  # = 12 + 3 = 15
    print(f"  エ行: ×{m}+{b} → 4, {missing}, 48, 147")

    # 検証
    assert m * 4 + b == 15, f"4×3+3 = {m*4+b} ≠ 15"
    assert m * 15 + b == 48, f"15×3+3 = {m*15+b} ≠ 48"
    assert m * 48 + b == 147, f"48×3+3 = {m*48+b} ≠ 147"
    print(f"  → 横方向: ? = {int(missing)} ✓")

    # 加算値パターン
    print("\n【加算値パターン】")
    offsets = [0, 1, 2, 3]
    print(f"  ア行=+0, イ行=+1, ウ行=+2, エ行=+3 → 等差数列(公差1) ✓")

    # 縦方向の検証
    print("\n【縦方向の規則検証】")
    rows_full = {
        'ア': [1, 3, 9, 27],
        'イ': [2, 7, 22, 67],
        'ウ': [3, 11, 35, 107],
        'エ': [4, 15, 48, 147]
    }
    for col in range(4):
        col_vals = [rows_full[r][col] for r in ['ア', 'イ', 'ウ', 'エ']]
        diffs = [col_vals[i+1] - col_vals[i] for i in range(3)]
        is_arithmetic = len(set(diffs)) == 1
        print(f"  {col+1}列: {col_vals}, 差: {diffs} {'(等差)' if is_arithmetic else ''}")
        if is_arithmetic:
            assert col_vals[3] == col_vals[2] + diffs[0]

    # 列差の規則: 1, 4, 13, 40 → ×3+1
    col_diffs = [1, 4, 13, 40]
    print(f"\n  列差: {col_diffs}")
    for i in range(len(col_diffs) - 1):
        expected = col_diffs[i] * 3 + 1
        assert expected == col_diffs[i+1], f"{col_diffs[i]}×3+1 = {expected} ≠ {col_diffs[i+1]}"
    print(f"  列差の規則: ×3+1 ✓")

    # 総当たり検証: ?に1~200の全整数を試し、両方向の規則を満たすのが15のみか確認
    print("\n【総当たり検証】")
    valid_values = []
    for candidate in range(1, 201):
        # 横方向: 4, candidate, 48, 147 が f(x)=ax+b で成立するか
        # candidate = 4a+b, 48 = candidate*a+b, 147 = 48*a+b
        # 147 = 48a+b → b = 147-48a
        # 48 = candidate*a + 147-48a → 48 = a*(candidate-48)+147
        # a*(candidate-48) = -99 → a = -99/(candidate-48) if candidate != 48
        if candidate == 48:
            continue
        a_num = -99
        a_den = candidate - 48
        if a_num % a_den != 0:
            continue
        a = a_num // a_den
        if a <= 0:
            continue
        b = 147 - 48 * a
        # 確認: 4*a+b == candidate
        if 4 * a + b != candidate:
            continue
        # 確認: candidate*a+b == 48
        if candidate * a + b != 48:
            continue
        valid_values.append((candidate, a, b))

    print(f"  有効な解: {valid_values}")
    assert len(valid_values) == 1, f"解が{len(valid_values)}個: {valid_values}"
    assert valid_values[0][0] == 15
    print(f"  解は唯一: ? = 15 ✓")

    print(f"\n★ 問1の正解: (4) 15")
    return 15


def verify_q2():
    """問2: 図形マトリックス - 解の一意性検証（4性質のラテン方陣）"""
    print("\n" + "=" * 50)
    print("問2: 図形マトリックスの規則")
    print("=" * 50)

    SHAPES = ['circle', 'triangle', 'square']
    SIZES = ['small', 'medium', 'large']
    FILLS = ['empty', 'gray', 'black']
    DOTS = ['top', 'right', 'bottom']

    # マトリックス: (行, 列) → (形, 大きさ, 塗り, 印位置)
    matrix = {
        (0,0): ('circle', 'small', 'empty', 'top'),
        (0,1): ('triangle', 'large', 'black', 'right'),
        (0,2): ('square', 'medium', 'gray', 'bottom'),
        (1,0): ('triangle', 'medium', 'black', 'bottom'),
        (1,1): ('square', 'small', 'gray', 'top'),
        (1,2): ('circle', 'large', 'empty', 'right'),
        (2,0): ('square', 'large', 'gray', 'right'),
        (2,1): ('circle', 'medium', 'empty', 'bottom'),
        # (2,2): ? を求める
    }

    # 各行・各列で4性質がそれぞれ全て異なることを検証
    print("\n【既知セルのラテン方陣検証】")
    for row in range(3):
        cells_in_row = [matrix[(row, c)] for c in range(3) if (row, c) in matrix]
        if len(cells_in_row) == 3:
            for prop_idx, prop_name in enumerate(['形', '大きさ', '塗り', '印']):
                vals = [c[prop_idx] for c in cells_in_row]
                assert len(set(vals)) == 3, f"行{row} {prop_name}: 重複あり {vals}"
            print(f"  行{row}: 全4性質が各3種 ✓")

    for col in range(3):
        cells_in_col = [matrix[(r, col)] for r in range(3) if (r, col) in matrix]
        if len(cells_in_col) == 3:
            for prop_idx, prop_name in enumerate(['形', '大きさ', '塗り', '印']):
                vals = [c[prop_idx] for c in cells_in_col]
                assert len(set(vals)) == 3, f"列{col} {prop_name}: 重複あり {vals}"
            print(f"  列{col}: 全4性質が各3種 ✓")

    # 総当たりで (2,2) を求める
    print("\n【総当たり検証: (2,2)セル】")
    valid = []
    for shape in SHAPES:
        for size in SIZES:
            for fill in FILLS:
                for dot in DOTS:
                    candidate = (shape, size, fill, dot)

                    # 行2の検証
                    row2 = [matrix[(2,0)], matrix[(2,1)], candidate]
                    for prop_idx in range(4):
                        if len(set(c[prop_idx] for c in row2)) != 3:
                            break
                    else:
                        # 列2の検証
                        col2 = [matrix[(0,2)], matrix[(1,2)], candidate]
                        for prop_idx in range(4):
                            if len(set(c[prop_idx] for c in col2)) != 3:
                                break
                        else:
                            valid.append(candidate)

    print(f"  有効な解の数: {len(valid)}")
    for v in valid:
        print(f"    {v}")

    assert len(valid) == 1, f"解が{len(valid)}個存在"
    answer = valid[0]
    assert answer == ('triangle', 'small', 'black', 'top'), f"予想と異なる: {answer}"

    print(f"\n★ 問2の正解: (3) 小さい黒塗り三角形（印が上）")

    # 選択肢の検証
    print("\n【選択肢検証】")
    choices = [
        ('triangle', 'large', 'black', 'top'),    # (1) 大きさ違い
        ('triangle', 'small', 'black', 'right'),   # (2) 印位置違い
        ('triangle', 'small', 'black', 'top'),      # (3) 正解
        ('triangle', 'small', 'gray', 'top'),       # (4) 塗り違い
        ('circle', 'small', 'black', 'top'),        # (5) 形違い
    ]
    for i, choice in enumerate(choices):
        diffs = sum(1 for a, b in zip(answer, choice) if a != b)
        status = "正解" if diffs == 0 else f"差異{diffs}箇所"
        print(f"  ({i+1}) {choice} → {status}")

    return answer


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("\n" + "=" * 50)
    print("全検証完了 ✓")
    print("=" * 50)
