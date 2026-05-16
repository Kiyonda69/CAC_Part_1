"""
航大思考173 - 立方体組み合わせ問題の検証

問1: 2×2×2立方体（8個）から、立体A（4個のtripod）と組み合わせて
     大きな立方体になる立体を5つの候補から選ぶ。
問2: 3×3×3立方体（27個）から、立体A（18個の階段ピラミッド）と
     組み合わせて大きな立方体になる立体を5つの候補から選ぶ。

検証内容:
- 立体Aと欠けた部分（missing）が互いに排他で、合わせて全体になることを確認
- 候補のうち、回転により missing と一致するものが正解1つだけであることを確認
"""

import itertools

# ===== 回転群の生成（24個の3D回転） =====

def rotate_x(p):
    x, y, z = p
    return (x, -z, y)

def rotate_y(p):
    x, y, z = p
    return (z, y, -x)

def rotate_z(p):
    x, y, z = p
    return (-y, x, z)

def apply_rotations(shape, rotations):
    """shape の各点に rotations の回転を順に適用"""
    result = shape
    for r in rotations:
        result = frozenset(r(p) for p in result)
    return result

def normalize(shape):
    """形状を平行移動して原点に正規化（最小座標を0,0,0に）"""
    if not shape:
        return frozenset()
    min_x = min(p[0] for p in shape)
    min_y = min(p[1] for p in shape)
    min_z = min(p[2] for p in shape)
    return frozenset((p[0]-min_x, p[1]-min_y, p[2]-min_z) for p in shape)

def all_rotations(shape):
    """形状の24個の回転すべてを列挙（正規化済み）"""
    rotations_list = []
    # 24個の回転を生成
    rotation_sequences = [
        [],
        [rotate_x],
        [rotate_x, rotate_x],
        [rotate_x, rotate_x, rotate_x],
        [rotate_y],
        [rotate_y, rotate_x],
        [rotate_y, rotate_x, rotate_x],
        [rotate_y, rotate_x, rotate_x, rotate_x],
        [rotate_y, rotate_y],
        [rotate_y, rotate_y, rotate_x],
        [rotate_y, rotate_y, rotate_x, rotate_x],
        [rotate_y, rotate_y, rotate_x, rotate_x, rotate_x],
        [rotate_y, rotate_y, rotate_y],
        [rotate_y, rotate_y, rotate_y, rotate_x],
        [rotate_y, rotate_y, rotate_y, rotate_x, rotate_x],
        [rotate_y, rotate_y, rotate_y, rotate_x, rotate_x, rotate_x],
        [rotate_z],
        [rotate_z, rotate_x],
        [rotate_z, rotate_x, rotate_x],
        [rotate_z, rotate_x, rotate_x, rotate_x],
        [rotate_z, rotate_z, rotate_z],
        [rotate_z, rotate_z, rotate_z, rotate_x],
        [rotate_z, rotate_z, rotate_z, rotate_x, rotate_x],
        [rotate_z, rotate_z, rotate_z, rotate_x, rotate_x, rotate_x],
    ]
    seen = set()
    for seq in rotation_sequences:
        rotated = apply_rotations(shape, seq)
        normalized = normalize(rotated)
        if normalized not in seen:
            seen.add(normalized)
            rotations_list.append(normalized)
    return rotations_list

def shapes_equal_under_rotation(shape1, shape2):
    """2つの形状が回転で一致するか確認"""
    norm1 = normalize(shape1)
    for r in all_rotations(shape2):
        if r == norm1:
            return True
    return False


# ===== 問1: 2×2×2立方体 =====
print("=" * 60)
print("問1: 2×2×2立方体（8個）")
print("=" * 60)

cube_2x2x2 = frozenset((x, y, z) for x in [0, 1] for y in [0, 1] for z in [0, 1])

# 立体A: 原点(0,0,0)を中心とする tripod（4個）
A1 = frozenset({(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)})
missing1 = cube_2x2x2 - A1
print(f"立体A: {sorted(A1)}")
print(f"  個数: {len(A1)}")
print(f"欠けた部分（missing）: {sorted(missing1)}")
print(f"  個数: {len(missing1)}")
assert A1 | missing1 == cube_2x2x2
assert A1 & missing1 == frozenset()
print("✓ AとmissingがちょうどA cube全体を構成")

# 5つの候補（すべて4個の立方体の形状）
candidates1 = {
    1: frozenset({(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)}),  # 2×2×1スラブ
    2: frozenset({(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}),  # トリポッド ✓
    3: frozenset({(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0)}),  # L字（平面）
    4: frozenset({(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0)}),  # T字（平面）
    5: frozenset({(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)}),  # S字（平面）
}

print("\n【候補と missing との一致確認】")
correct_count = 0
correct_idx = None
for idx, cand in candidates1.items():
    match = shapes_equal_under_rotation(cand, missing1)
    print(f"  ({idx}): {'✓ 一致' if match else '✗ 不一致'}  個数={len(cand)}")
    if match:
        correct_count += 1
        correct_idx = idx

assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
print(f"\n✓ 正解: ({correct_idx})")
assert correct_idx == 2, f"問1の正解は2であるべき（実際: {correct_idx}）"


# ===== 問2: 3×3×3立方体 =====
print("\n" + "=" * 60)
print("問2: 3×3×3立方体（27個）")
print("=" * 60)

cube_3x3x3 = frozenset((x, y, z) for x in range(3) for y in range(3) for z in range(3))

# 立体A: 階段ピラミッド（18個）
# z=0: 3×3 (9個)
# z=1: 2×3 (y=0,1, 6個)
# z=2: 1×3 (y=0, 3個)
A2 = frozenset(
    [(x, y, 0) for x in range(3) for y in range(3)] +
    [(x, y, 1) for x in range(3) for y in [0, 1]] +
    [(x, 0, 2) for x in range(3)]
)
missing2 = cube_3x3x3 - A2
print(f"立体A: {len(A2)}個")
print(f"欠けた部分: {len(missing2)}個")
assert A2 | missing2 == cube_3x3x3
assert A2 & missing2 == frozenset()
print("✓ AとmissingがちょうどA cube全体を構成")

# 5つの候補（すべて9個の立方体の形状）
# 正解候補(1): missing2と同じ形（階段の小さい方）
correct_shape = frozenset(
    [(x, 0, 0) for x in range(3)] +
    [(x, y, 1) for x in range(3) for y in [0, 1]]
)
assert len(correct_shape) == 9
assert shapes_equal_under_rotation(correct_shape, missing2), "正解候補がmissingと一致しません"

candidates2 = {
    1: correct_shape,  # ✓ 正解（missing2の回転）
    2: frozenset([(x, y, 0) for x in range(3) for y in range(3)]),  # 3×3×1スラブ（正方形板）
    3: frozenset(
        [(x, y, z) for x in [0, 1] for y in [0, 1] for z in [0, 1]] +
        [(2, 0, 0)]
    ),  # 2×2×2立方体 + 1個の突起（合計9個）
    4: frozenset(
        [(x, 0, 0) for x in range(5)] +
        [(x, 0, 1) for x in [1, 2, 3]] +
        [(2, 0, 2)]
    ),  # 5+3+1のピラミッド階段（平面内、9個）
    5: frozenset(
        [(x, 0, 0) for x in range(3)] +
        [(2, y, 1) for y in range(3)] +
        [(x, 2, 2) for x in range(3)]
    ),  # 3D螺旋ジグザグ（3層×3個ずつ）
}

print("\n【候補と missing との一致確認】")
correct_count = 0
correct_idx = None
for idx, cand in candidates2.items():
    assert len(cand) == 9, f"候補({idx})の個数が9でない: {len(cand)}"
    match = shapes_equal_under_rotation(cand, missing2)
    print(f"  ({idx}): {'✓ 一致' if match else '✗ 不一致'}  個数={len(cand)}")
    if match:
        correct_count += 1
        correct_idx = idx

assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
print(f"\n✓ 正解: ({correct_idx})")
assert correct_idx == 1, f"問2の正解は1であるべき（実際: {correct_idx}）"

print("\n" + "=" * 60)
print("✓ 全検証クリア")
print("=" * 60)
