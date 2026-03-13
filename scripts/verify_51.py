#!/usr/bin/env python3
"""
セット51 検証スクリプト
問1: 正六角形の頂点操作（対称群）
問2: バス路線と停留所の論理推論
"""

from itertools import permutations, combinations

# ===== 問1: 正六角形の対称性 =====
print("=" * 60)
print("問1: 正六角形の頂点操作")
print("=" * 60)

# 正六角形 A,B,C,D,E,F（時計回り）の対称群 D6
# 頂点を 0=A, 1=B, 2=C, 3=D, 4=E, 5=F とする

def apply_perm(perm, state):
    """permutation を state に適用"""
    result = [None] * len(state)
    for i, p in enumerate(perm):
        result[p] = state[i]
    return tuple(result)

def compose_perms(p1, p2):
    """p2 を適用してから p1 を適用（p1 ∘ p2）"""
    return tuple(p1[p2[i]] for i in range(len(p1)))

# 正六角形の隣接関係 (0=A, 1=B, 2=C, 3=D, 4=E, 5=F)
# A-B, B-C, C-D, D-E, E-F, F-A
adjacency = {
    (0,1), (1,2), (2,3), (3,4), (4,5), (5,0),
    (1,0), (2,1), (3,2), (4,3), (5,4), (0,5)
}

def is_hexagon_symmetry(perm):
    """置換が正六角形の対称性かどうかを判定"""
    for i, j in adjacency:
        if (perm[i], perm[j]) not in adjacency:
            return False
    return True

# 全対称操作を列挙
symmetries = []
for perm in permutations(range(6)):
    if is_hexagon_symmetry(perm):
        symmetries.append(perm)

print(f"正六角形の対称操作の数: {len(symmetries)} (D6 = 12であるべき)")
assert len(symmetries) == 12, "対称操作は12個のはず"

# 対称操作を表示
labels = "ABCDEF"
print("\n対称操作一覧:")
for s in symmetries:
    mapping = ", ".join(f"{labels[i]}→{labels[s[i]]}" for i in range(6))
    print(f"  ({', '.join(labels[s[i]] for i in range(6))}) : {mapping}")

# 各操作を検証
print("\n--- 各操作の検証 ---")

# ア: A→C, C→E, E→A, B→D, D→F, F→B (120° 回転)
op_a = (2, 3, 4, 5, 0, 1)  # A(0)→C(2), B(1)→D(3), C(2)→E(4), D(3)→F(5), E(4)→A(0), F(5)→B(1)
print(f"ア (ACE)(BDF): {tuple(labels[op_a[i]] for i in range(6))}")
print(f"  対称性: {is_hexagon_symmetry(op_a)}")

# イ: A↔D, B↔E, C↔F (180° 回転)
op_b = (3, 4, 5, 0, 1, 2)  # A→D, B→E, C→F, D→A, E→B, F→C
print(f"イ (AD)(BE)(CF): {tuple(labels[op_b[i]] for i in range(6))}")
print(f"  対称性: {is_hexagon_symmetry(op_b)}")

# ウ: A↔C, B↔F (DとEはそのまま)
op_c = (2, 5, 0, 3, 4, 1)  # A→C, B→F, C→A, D→D, E→E, F→B
print(f"ウ (AC)(BF): {tuple(labels[op_c[i]] for i in range(6))}")
print(f"  対称性: {is_hexagon_symmetry(op_c)}")

# エ: B↔F, C↔E (AとDはそのまま) - 反射 A-D軸
op_d = (0, 5, 4, 3, 2, 1)  # A→A, B→F, C→E, D→D, E→C, F→B
print(f"エ (BF)(CE): {tuple(labels[op_d[i]] for i in range(6))}")
print(f"  対称性: {is_hexagon_symmetry(op_d)}")

# オ: A↔B, D↔E (CとFはそのまま)
op_e = (1, 0, 2, 4, 3, 5)  # A→B, B→A, C→C, D→E, E→D, F→F
print(f"オ (AB)(DE): {tuple(labels[op_e[i]] for i in range(6))}")
print(f"  対称性: {is_hexagon_symmetry(op_e)}")

# 正解の確認
correct_ops = []
for name, op in [("ア", op_a), ("イ", op_b), ("ウ", op_c), ("エ", op_d), ("オ", op_e)]:
    if is_hexagon_symmetry(op):
        correct_ops.append(name)

print(f"\n正解の操作: {', '.join(correct_ops)}")
print(f"答え: ア、イ、エ (3つの操作が対称性)")

# ===== 問2: バス路線と停留所の論理推論 =====
print("\n" + "=" * 60)
print("問2: バス路線と停留所の論理推論")
print("=" * 60)

"""
6つの停留所 P, Q, R, S, T, U
3つの路線 X, Y, Z
条件:
(I) 各停留所には少なくとも1つの路線が通る
(II) Xは3つ、Yは3つ、Zは2つの停留所を通る
(III) PとQには路線Xのみが通る
(IV) Rには路線XとYが通る
(V) Sには路線Yのみが通る
(VI) TとUには路線Xは通らない
"""

stops = ['P', 'Q', 'R', 'S', 'T', 'U']
routes = ['X', 'Y', 'Z']

valid_configs = []

# 路線Xの停留所: 3つ。P,Q,R は確定（条件III,IV）
# 条件VI: T,U はXに含まれない → X = {P, Q, R}
X_stops = {'P', 'Q', 'R'}

# 路線Yの停留所: 3つ。R,S は確定（条件IV,V）
# Yの3つ目: P,Qは条件IIIで「Xのみ」なので除外。R,Sは既に含む。残りはT,U
# → Yの3つ目は T または U
for y_third in ['T', 'U']:
    Y_stops = {'R', 'S', y_third}
    
    # 路線Zの停留所: 2つ
    # 条件III: PはXのみ → Zに含まない。QはXのみ → Zに含まない。
    # 条件V: SはYのみ → Zに含まない。
    # → Z ⊆ {R, T, U}
    possible_z = ['R', 'T', 'U']
    for z_combo in combinations(possible_z, 2):
        Z_stops = set(z_combo)
        
        # 条件(I): 各停留所に少なくとも1路線
        all_covered = True
        for stop in stops:
            if stop not in X_stops and stop not in Y_stops and stop not in Z_stops:
                all_covered = False
                break
        
        if not all_covered:
            continue
        
        # 条件(II): X=3, Y=3, Z=2 を確認
        assert len(X_stops) == 3
        assert len(Y_stops) == 3
        assert len(Z_stops) == 2
        
        # 条件(III): PとQはXのみ
        if 'P' in Y_stops or 'P' in Z_stops:
            continue
        if 'Q' in Y_stops or 'Q' in Z_stops:
            continue
        
        # 条件(V): SはYのみ
        if 'S' in X_stops or 'S' in Z_stops:
            continue
        
        # 条件(VI): TとUはXに含まれない（既に保証）
        
        config = {
            'X': X_stops.copy(),
            'Y': Y_stops.copy(),
            'Z': Z_stops.copy()
        }
        
        # 各停留所の路線を計算
        stop_routes = {}
        for stop in stops:
            sr = set()
            if stop in X_stops:
                sr.add('X')
            if stop in Y_stops:
                sr.add('Y')
            if stop in Z_stops:
                sr.add('Z')
            stop_routes[stop] = sr
        
        config['stop_routes'] = stop_routes
        valid_configs.append(config)

print(f"\n有効な配置の数: {len(valid_configs)}")
for i, cfg in enumerate(valid_configs):
    print(f"\n配置{i+1}:")
    print(f"  X = {sorted(cfg['X'])}")
    print(f"  Y = {sorted(cfg['Y'])}")
    print(f"  Z = {sorted(cfg['Z'])}")
    for stop in stops:
        routes_str = ', '.join(sorted(cfg['stop_routes'][stop]))
        print(f"  {stop}: {{{routes_str}}}")

# 命題の検証
print("\n--- 命題の検証 ---")

statements = {
    "ア: 路線Yと路線Zの両方が通る停留所が存在する": [],
    "イ: 路線Zが通る停留所のうち少なくとも1つは路線Yも通る": [],
    "ウ: TまたはUの少なくとも一方に路線Zが通る": [],
    "エ: 3つの路線すべてが通る停留所がある": [],
}

for i, cfg in enumerate(valid_configs):
    sr = cfg['stop_routes']
    
    # ア: Y∩Zが通る停留所が存在
    a_result = any('Y' in sr[s] and 'Z' in sr[s] for s in stops)
    statements["ア: 路線Yと路線Zの両方が通る停留所が存在する"].append(a_result)
    
    # イ: Zの停留所のうち少なくとも1つにYも通る
    z_stops = [s for s in stops if 'Z' in sr[s]]
    b_result = any('Y' in sr[s] for s in z_stops)
    statements["イ: 路線Zが通る停留所のうち少なくとも1つは路線Yも通る"].append(b_result)
    
    # ウ: TまたはUに路線Z
    c_result = 'Z' in sr['T'] or 'Z' in sr['U']
    statements["ウ: TまたはUの少なくとも一方に路線Zが通る"].append(c_result)
    
    # エ: 3路線すべてが通る停留所
    d_result = any(len(sr[s]) == 3 for s in stops)
    statements["エ: 3つの路線すべてが通る停留所がある"].append(d_result)

print()
for stmt, results in statements.items():
    always_true = all(results)
    always_false = not any(results)
    status = "常に真" if always_true else ("常に偽" if always_false else "場合による")
    true_count = sum(results)
    print(f"{stmt}")
    print(f"  → {status} (真: {true_count}/{len(results)})")

# 確実にいえるもの
certain = [k.split(":")[0] for k, v in statements.items() if all(v)]
print(f"\n確実にいえるもの: {', '.join(certain)}")
print("答え: ア、イ、ウ")

