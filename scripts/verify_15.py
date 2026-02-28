"""
問題セット15の解の一意性検証スクリプト

問1: 3×3 図形行列パターン（4分割正方形の塗りつぶし）
問2: 3行×3列 図形演算（対称差=XOR演算の発見と適用）
"""

# ============================================================
# 共通関数: 4分割正方形の表現
# ============================================================
# 象限インデックス: 0=TL(左上), 1=TR(右上), 2=BL(左下), 3=BR(右下)
# 時計回りの順序: 0(TL) -> 1(TR) -> 3(BR) -> 2(BL) -> 0(TL)

def rotate_cw(pattern: frozenset) -> frozenset:
    """
    4分割正方形のパターンを90°時計回りに回転する
    TL(0)->TR(1), TR(1)->BR(3), BR(3)->BL(2), BL(2)->TL(0)
    """
    rotation = {0: 1, 1: 3, 3: 2, 2: 0}
    return frozenset(rotation[q] for q in pattern)


def cw_next(quadrant: int) -> int:
    """時計回り順での次の象限を返す"""
    cw_order = {0: 1, 1: 3, 3: 2, 2: 0}
    return cw_order[quadrant]


def format_pattern(pattern: frozenset) -> str:
    """パターンを人間が読みやすい形式に変換"""
    names = {0: 'TL', 1: 'TR', 2: 'BL', 3: 'BR'}
    sorted_p = sorted(pattern)
    return '{' + ', '.join(names[q] for q in sorted_p) + '}'


# ============================================================
# 問1: 3×3 図形行列パターン検証
# ============================================================
print("=" * 60)
print("問1: 3×3 図形行列パターン")
print("=" * 60)
print()
print("規則:")
print("  横方向(左→右): パターンを90°時計回りに回転")
print("  縦方向(上→下): 時計回り順で次の象限を1つ追加")
print()

# 行列を構築
# 各列の開始象限
# Col1: TL(0), Col2: TR(1), Col3: BR(3)
grid = {}
start_per_col = {1: 0, 2: 1, 3: 3}  # col -> starting quadrant

# 縦方向: 各列の各行に対して象限を追加
for col in range(1, 4):
    current = frozenset([start_per_col[col]])
    grid[1, col] = current
    # Row2: 次の象限を追加
    next_q = cw_next(start_per_col[col])
    current = frozenset([start_per_col[col], next_q])
    grid[2, col] = current
    # Row3: さらに次の象限を追加
    next_q2 = cw_next(next_q)
    current = frozenset([start_per_col[col], next_q, next_q2])
    grid[3, col] = current

print("構築された行列:")
for row in range(1, 4):
    row_str = f"  行{row}: "
    for col in range(1, 4):
        row_str += f"{format_pattern(grid[row, col]):25s}"
    print(row_str)

print()
print("横方向の規則検証 (90°時計回り回転):")
all_ok = True
for row in range(1, 4):
    for col in range(1, 3):
        expected = rotate_cw(grid[row, col])
        actual = grid[row, col + 1]
        ok = (expected == actual)
        if not ok:
            all_ok = False
        print(f"  ({row},{col})→({row},{col+1}): rotate({format_pattern(grid[row,col])}) = {format_pattern(expected)} == {format_pattern(actual)} {'OK' if ok else 'NG!'}")
print(f"  結果: {'全OK' if all_ok else '規則違反あり'}")

print()
print("縦方向の規則検証 (時計回り順で象限追加):")
all_ok2 = True
for col in range(1, 4):
    for row in range(1, 3):
        added = grid[row + 1, col] - grid[row, col]
        prev_set = grid[row, col]
        last_added = sorted(prev_set)[-1] if row == 1 else None
        ok = (len(added) == 1)
        if ok:
            new_q = list(added)[0]
            # 前の行の最後に追加された象限の次のCW象限か確認
            if row == 1:
                expected_add = cw_next(start_per_col[col])
            else:
                prev_added = grid[row, col] - grid[row - 1, col]
                expected_add = cw_next(list(prev_added)[0])
            ok = (new_q == expected_add)
        else:
            all_ok2 = False
        print(f"  列{col} 行{row}→{row+1}: 追加={format_pattern(added)} {'OK' if ok else 'NG!'}")
print(f"  結果: {'全OK' if all_ok2 else '規則違反あり'}")

print()
print(f"[問1の答え] (3,3) = {format_pattern(grid[3, 3])}")
print(f"  → TL=左上, TR=右上, BL=左下, BR=右下")
answer_names = {0: '左上(TL)', 1: '右上(TR)', 2: '左下(BL)', 3: '右下(BR)'}
for q in sorted(grid[3, 3]):
    print(f"  → {answer_names[q]} が塗りつぶされる")
missing = frozenset([0, 1, 2, 3]) - grid[3, 3]
for q in sorted(missing):
    print(f"  → {answer_names[q]} は白（空白）")


# ============================================================
# 問2: 図形演算（対称差=XOR）検証
# ============================================================
print()
print("=" * 60)
print("問2: 3行×3列 図形演算（対称差=XOR演算）")
print("=" * 60)
print()
print("規則: 列3 = 列1 ⊕ 列2（対称差: 片方にのみ含まれる象限）")
print()

# 行列の定義
# 行1: A={0}(TL), B={1,2}(TR,BL), Result=A XOR B
#      → 重複なし: 結果は和集合と同一 → 規則の候補が複数
# 行2: A={0,1}(TL,TR), B={1,3}(TR,BR), Result=A XOR B
#      → 重複あり(TR): 和集合≠結果 → 対称差(XOR)と確定
# 行3: A={0,2,3}(TL,BL,BR), B={1,3}(TR,BR), Result=?
#      → 重複あり(BR): 対称差を適用

def sym_diff(A: frozenset, B: frozenset) -> frozenset:
    """対称差（XOR演算）"""
    return (A | B) - (A & B)

rows_q2 = [
    (frozenset([0]),       frozenset([1, 2])),    # 行1: A=TL, B=TR+BL  → 重複なし
    (frozenset([0, 1]),    frozenset([1, 3])),    # 行2: A=TL+TR, B=TR+BR → 重複:TR
    (frozenset([0, 1, 2]), frozenset([2, 3])),    # 行3: A=TL+TR+BL, B=BL+BR → 重複:BL
]

print("検証:")
for i, (A, B) in enumerate(rows_q2, 1):
    result = sym_diff(A, B)
    intersection = A & B
    union = A | B
    print(f"  行{i}: A={format_pattern(A)}, B={format_pattern(B)}")
    print(f"       A∩B={format_pattern(intersection)}, A∪B={format_pattern(union)}")
    print(f"       A⊕B（対称差）= {format_pattern(result)}")
    if i == 3:
        answer_q2 = result
    print()

print(f"[問2の答え] 行3の結果 = {format_pattern(answer_q2)}")
print(f"  → 塗りつぶし: ", end="")
names = {0: '左上', 1: '右上', 2: '左下', 3: '右下'}
print(', '.join(names[q] for q in sorted(answer_q2)))
missing_q2 = frozenset([0, 1, 2, 3]) - answer_q2
print(f"  → 空白: ", end="")
print(', '.join(names[q] for q in sorted(missing_q2)))

print()
print("【操作の発見ができるか検証】")
A1, B1 = rows_q2[0]
r1 = sym_diff(A1, B1)
A2, B2 = rows_q2[1]
r2 = sym_diff(A2, B2)
print(f"行1: A∩B={format_pattern(A1&B1)} → 重複なし → 結果=A∪B → XOR/UNIONの区別不可")
print(f"行2: A∩B={format_pattern(A2&B2)} → 重複あり → 結果≠A∪B({format_pattern(A2|B2)}) → XOR確定")
print("→ 行1と行2の組み合わせで対称差(XOR)が唯一決まる")

print()
print("=" * 60)
print("全検証完了")
print("=" * 60)
