"""
verify_81.py - 航大思考81 検証スクリプト

問1: 透明シート重ね合わせ（回転なし）
問2: 透明シート重ね合わせ（回転あり・高難度版）
"""
from itertools import combinations

def overlay_sheets(sheet_list, size=3):
    """複数シートを重ねた結果を返す。衝突があればNone"""
    result = [[None]*size for _ in range(size)]
    for sheet in sheet_list:
        for r in range(size):
            for c in range(size):
                if sheet[r][c] is not None:
                    if result[r][c] is not None and result[r][c] != sheet[r][c]:
                        return None
                    result[r][c] = sheet[r][c]
    return result

def grids_equal(g1, g2, size=3):
    for r in range(size):
        for c in range(size):
            if g1[r][c] != g2[r][c]:
                return False
    return True

def rotate_90cw(grid):
    """3x3グリッドを90度時計回りに回転"""
    n = len(grid)
    return [[grid[n-1-c][r] for c in range(n)] for r in range(n)]

def all_rotations(grid):
    """0°, 90°, 180°, 270°の4つの回転を返す"""
    r90 = rotate_90cw(grid)
    r180 = rotate_90cw(r90)
    r270 = rotate_90cw(r180)
    return [grid, r90, r180, r270]

def print_grid(grid):
    for row in grid:
        print("  ", [x if x else '·' for x in row])

# ============================================================
# 問1: 透明シート重ね合わせ（回転なし）
# ============================================================
print("=" * 60)
print("問1: 透明シート重ね合わせ（回転なし）")
print("=" * 60)

sheets_q1 = {
    'ア': [
        ['●', None, None],
        [None, '○', None],
        [None, None, '●'],
    ],
    'イ': [
        [None, '□', None],
        ['◇', None, None],
        ['△', None, None],
    ],
    'ウ': [
        [None, None, '▲'],
        [None, None, '■'],
        [None, '▼', None],
    ],
    'エ': [
        [None, None, '▲'],
        [None, '○', None],
        ['△', None, None],
    ],
    'オ': [
        ['●', '□', None],
        [None, None, '■'],
        [None, '▼', None],
    ],
}

target_q1 = [
    ['●', '□', '▲'],
    ['◇', '○', '■'],
    ['△', '▼', '●'],
]

names = list(sheets_q1.keys())
valid_q1 = []
for combo in combinations(names, 3):
    sheet_list = [sheets_q1[n] for n in combo]
    result = overlay_sheets(sheet_list)
    if result is not None and grids_equal(result, target_q1):
        valid_q1.append(combo)
        print(f"  一致: {' + '.join(combo)}")

print(f"解の数: {len(valid_q1)}")
assert len(valid_q1) == 1, f"解が{len(valid_q1)}個存在"
print(f"唯一解: {' + '.join(valid_q1[0])}")

# 各シートの内容を表示
print("\n各シート:")
for name, sheet in sheets_q1.items():
    print(f"\nシート{name}:")
    print_grid(sheet)

print("\n目標パターン:")
print_grid(target_q1)

# ============================================================
# 問2: 透明シート重ね合わせ（回転あり・高難度版）
# ============================================================
print("\n" + "=" * 60)
print("問2: 透明シート重ね合わせ（回転あり）")
print("=" * 60)

# 問2: 回転が必要な問題
# ア(0°) + イ(90°CW) + ウ(0°) で目標パターンを作る
# イは回転が必要

sheets_q2 = {
    'ア': [
        ['■', None, None],
        [None, None, '○'],
        [None, None, None],
    ],
    'イ': [
        # 90°CW回転すると: · ▲ · / · · · / ● · · になる
        [None, None, None],
        ['▲', None, None],
        [None, None, '●'],
    ],
    'ウ': [
        [None, None, '◇'],
        ['△', None, None],
        [None, '□', None],
    ],
    'エ': [
        [None, '▲', None],
        [None, None, None],
        ['●', None, '◇'],
    ],
    'オ': [
        ['■', None, '◇'],
        [None, None, None],
        [None, '□', None],
    ],
}

target_q2 = [
    ['■', '▲', '◇'],
    ['△', None, '○'],
    ['●', '□', None],
]

# イの回転確認
print("\nシートイの各回転:")
for i, rot in enumerate(all_rotations(sheets_q2['イ'])):
    print(f"\n  {i*90}°:")
    print_grid(rot)

# 全組み合わせ × 全回転をチェック
rotation_labels = ['0°', '90°', '180°', '270°']
valid_q2 = []

for combo in combinations(names, 3):
    base_sheets = [sheets_q2[n] for n in combo]
    for r0 in range(4):
        for r1 in range(4):
            for r2 in range(4):
                rotated = [
                    all_rotations(base_sheets[0])[r0],
                    all_rotations(base_sheets[1])[r1],
                    all_rotations(base_sheets[2])[r2],
                ]
                result = overlay_sheets(rotated)
                if result is not None and grids_equal(result, target_q2):
                    rots = (rotation_labels[r0], rotation_labels[r1], rotation_labels[r2])
                    valid_q2.append((combo, rots))
                    print(f"  一致: {combo[0]}({rots[0]}) + {combo[1]}({rots[1]}) + {combo[2]}({rots[2]})")

print(f"\n解の数: {len(valid_q2)}")
unique_combos = set(s[0] for s in valid_q2)
print(f"シート組み合わせの数: {len(unique_combos)}")
assert len(unique_combos) == 1, f"異なるシート組み合わせが{len(unique_combos)}個存在"
print(f"唯一のシート組み合わせ: {' + '.join(list(unique_combos)[0])}")

print("\n各シート:")
for name, sheet in sheets_q2.items():
    print(f"\nシート{name}:")
    print_grid(sheet)

print("\n目標パターン:")
print_grid(target_q2)

print("\n検証完了!")
