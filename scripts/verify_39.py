#!/usr/bin/env python3
"""
セット39 検証コード
問1: 正方形ABCDの頂点操作（対称群）
問2: 町・施設・バス路線の論理パズル
"""

from itertools import permutations, combinations, product

print("=" * 60)
print("問1: 正方形ABCDの頂点操作")
print("=" * 60)
print()

# 正方形ABCDの頂点: A=0, B=1, C=2, D=3
# 正方形の配置:
#   A --- B
#   |     |
#   D --- C
# 
# 正方形の対称群 D4 (位数8):
# 恒等変換: (A,B,C,D)
# 90度回転: (B,C,D,A)
# 180度回転: (C,D,A,B)
# 270度回転: (D,A,B,C)
# 水平軸反転(AB-DC): (D,C,B,A)
# 垂直軸反転(AD-BC): (B,A,D,C)
# 対角線AC反転: (A,D,C,B)
# 対角線BD反転: (C,B,A,D)

# 正方形の対称操作群
D4 = [
    (0,1,2,3),  # 恒等
    (1,2,3,0),  # 90度回転
    (2,3,0,1),  # 180度回転
    (3,0,1,2),  # 270度回転
    (3,2,1,0),  # 水平軸反転
    (1,0,3,2),  # 垂直軸反転
    (0,3,2,1),  # 対角線AC反転
    (2,1,0,3),  # 対角線BD反転
]

def apply_perm(state, perm):
    """置換permを状態stateに適用"""
    return tuple(state[i] for i in perm)

def compose_perms(p1, p2):
    """置換p1の後にp2を適用"""
    return tuple(p1[i] for i in p2)

# 問題: 正方形ABCDに操作ア〜オのいずれか1つを行ったとき、
# A,B,C,Dの並びが元の正方形と必ず一致する操作はどれか。
#
# ただし「一致する」とは、正方形の対称操作で重ね合わせられることを意味する

# 操作の候補を定義
# ア: AとCを入れ替える → (C,B,A,D) = (2,1,0,3)
op_a = (2,1,0,3)
# イ: BとD、AとCをそれぞれ入れ替える → (C,D,A,B) = (2,3,0,1)  
op_b = (2,3,0,1)
# ウ: AとBを入れ替えた後、CとDを入れ替える → まずAB交換(B,A,C,D)=(1,0,2,3)、次にCD交換(B,A,D,C)=(1,0,3,2)
op_c_step1 = (1,0,2,3)  # AB交換
op_c = tuple(op_c_step1[i] if i < 2 else op_c_step1[i] for i in range(4))
# AB交換: (1,0,2,3)、CD交換を適用: position 2と3を交換
op_c = (1,0,3,2)
# エ: AをB、BをC、CをD、DをAにそれぞれ移す → (D,A,B,C) ... wait
# A→B位置, B→C位置, C→D位置, D→A位置
# つまり position B に A の値, position C に B の値, etc.
# 新しい配置: position 0(A) ← D, position 1(B) ← A, position 2(C) ← B, position 3(D) ← C
# = (3,0,1,2) ... これは270度回転 = (D,A,B,C)
# Wait, let me think more carefully.
# "AをBに、BをCに、CをDに、DをAに移す" means:
# The element at position A goes to position B
# The element at position B goes to position C
# etc.
# So if we start with (A,B,C,D) = (0,1,2,3):
# new[1] = old[0] = 0(A), new[2] = old[1] = 1(B), new[3] = old[2] = 2(C), new[0] = old[3] = 3(D)
# Result: (3, 0, 1, 2) → (D, A, B, C)
op_d = (3,0,1,2)

# オ: ランダムに二つの頂点を選び、それらを入れ替える。これを4回行う。
# → 必ず一致するとは限らない（反例があればNG）

print("操作の定義:")
names = ['A', 'B', 'C', 'D']

def perm_to_str(p):
    return '(' + ','.join(names[i] for i in p) + ')'

print(f"  ア: AとCを入れ替える → {perm_to_str(op_a)}")
print(f"  イ: BとDを、AとCをそれぞれ入れ替える → {perm_to_str(op_b)}")
print(f"  ウ: AとBを入れ替えた後、CとDを入れ替える → {perm_to_str(op_c)}")
print(f"  エ: AをB、BをC、CをD、DをAに移す → {perm_to_str(op_d)}")
print()

def is_in_D4(perm):
    """置換が正方形の対称群D4に含まれるか"""
    return perm in D4

print("各操作が正方形の対称操作か判定:")
ops = {'ア': op_a, 'イ': op_b, 'ウ': op_c, 'エ': op_d}
for name, op in ops.items():
    result = is_in_D4(op)
    print(f"  {name}: {perm_to_str(op)} → {'D4に含まれる (一致)' if result else 'D4に含まれない (不一致)'}")

# オの検証: 4回のランダム交換で必ずD4に含まれるか？
# 2つの頂点の交換 = 互換
# 4回の互換の合成 = 偶置換
# D4の偶置換: 恒等, 90度回転, 180度回転, 270度回転 → すべて偶置換
# D4の奇置換: 4つの反転 → 奇置換
# 4回の互換の積は必ず偶置換になる
# しかし偶置換でもD4に含まれないものがある
# S4の偶置換群A4は位数12: 恒等(1) + 3つの(ab)(cd)型 + 8つの(abc)型
# D4の偶置換は: 恒等, (ABCD), (AC)(BD), (ADCB) = 4つ
# A4にはD4に含まれない偶置換がある（例: (ABC) = (0,2,1,3)ではなく(1,2,0,3)）
# (A,B,C) = (1,2,0,3) はD4に含まれるか？
test_perm = (1,2,0,3)
print(f"\n  (ABC)巡回 = {perm_to_str(test_perm)} → D4に{'含まれる' if is_in_D4(test_perm) else '含まれない'}")

# 4回の互換で(1,2,0,3)を作れるか？
# (1,2,0,3) は3-巡回置換 = 奇数長巡回 = 偶置換
# (ABC) = (AB)(AC) = 2回の互換で作れる → 4回にするには恒等互換2回追加
# 例: (AB)(AC)(AB)(AB) = (AB)(AC) = (ABC) = (1,2,0,3)
swap_AB = (1,0,2,3)
swap_AC = (2,1,0,3)

result = (0,1,2,3)  # 恒等
result = apply_perm(result, swap_AB)  # (AB)
result = apply_perm(result, swap_AB)  # (AB)(AB) = 恒等
result = apply_perm(result, swap_AC)  # (AC)
result = apply_perm(result, swap_AB)  # (AB)(AC) = ?

# Actually let me redo. apply_perm means we permute the positions.
# Let me reconsider.
# State = (s0, s1, s2, s3) where s_i is the label at position i
# Initial: (A, B, C, D) = (0, 1, 2, 3)
# swap_AB: swap positions 0 and 1 → (s1, s0, s2, s3)
# As a permutation on positions: (1, 0, 2, 3)

def swap(state, i, j):
    """Swap elements at positions i and j"""
    lst = list(state)
    lst[i], lst[j] = lst[j], lst[i]
    return tuple(lst)

# Try to get (1,2,0,3) with 4 swaps
state = (0,1,2,3)
state = swap(state, 0, 1)  # (1,0,2,3)
state = swap(state, 0, 2)  # (2,0,1,3)
state = swap(state, 0, 1)  # (0,2,1,3) - not what we want

# Let me brute force: can we get (1,2,0,3) with exactly 4 swaps?
pairs = list(combinations(range(4), 2))
found_non_D4 = False
# Check all possible 4-swap sequences
for s1 in pairs:
    for s2 in pairs:
        for s3 in pairs:
            for s4 in pairs:
                state = (0,1,2,3)
                state = swap(state, *s1)
                state = swap(state, *s2)
                state = swap(state, *s3)
                state = swap(state, *s4)
                if not is_in_D4(state):
                    if not found_non_D4:
                        print(f"\n  オの反例: swaps={s1},{s2},{s3},{s4} → {perm_to_str(state)} (D4に含まれない)")
                        found_non_D4 = True
                        break
            if found_non_D4:
                break
        if found_non_D4:
            break
    if found_non_D4:
        break

if not found_non_D4:
    print("  オ: 4回の交換で常にD4に含まれる")
else:
    print("  オ: 必ずしもD4に含まれない → 「必ず一致」とは言えない")

print()

# 結論
print("結論:")
d4_ops = []
non_d4_ops = []
for name, op in ops.items():
    if is_in_D4(op):
        d4_ops.append(name)
    else:
        non_d4_ops.append(name)
print(f"  D4に含まれる（必ず一致する）: {', '.join(d4_ops)}")
print(f"  D4に含まれない（一致しない）: {', '.join(non_d4_ops)}")
print(f"  オ: 必ずしも一致しない")

# Hmm, let me reconsider the problem. The original 問9 asks about tetrahedron.
# The key insight is which operations are symmetries of the shape.
# Let me redesign to make the answer unique (exactly one correct pair of operations)

# Actually, for the answer format like the original (picking 2 correct operations out of 5),
# let me check which operations map to D4 elements.

print("\n" + "=" * 60)
print("問1の最終設計")  
print("=" * 60)

# Let me redesign with clearer operations for a cube problem instead.
# Actually, let me stick with the square (正方形) as it's cleaner and similar to the tetrahedron problem.

# 正方形ABCD (A=上左, B=上右, C=下右, D=下左)
# Symmetries D4:
# e: (0,1,2,3)
# r90: (3,0,1,2) - 90度時計回り: A→B, B→C, C→D, D→A... wait
# Let me use a clearer convention.
# Positions: 0=top-left(A), 1=top-right(B), 2=bottom-right(C), 3=bottom-left(D)
# 
# 90° clockwise rotation: what was at position 3(D) goes to 0(A), 0(A)→1(B), 1(B)→2(C), 2(C)→3(D)
# new[0]=old[3], new[1]=old[0], new[2]=old[1], new[3]=old[2]
# = (3,0,1,2) = (D,A,B,C) ← this is what エ does!

# OK so my analysis is correct. Let me check:
# ア: (2,1,0,3) = AC swap = diagonal BD reflection? 
# D4 diagonal BD reflection swaps A↔C = (2,1,0,3) ← YES, this is in D4!

# Wait, I said op_a is NOT in D4 earlier. Let me recheck.
print("\nD4 elements:")
for i, elem in enumerate(D4):
    print(f"  {i}: {perm_to_str(elem)}")

print(f"\n  ア (2,1,0,3) in D4? {(2,1,0,3) in D4}")

# (2,1,0,3) is the last element! It IS in D4. Let me re-examine.
# D4[7] = (2,1,0,3) - this is the BD diagonal reflection
# So ア IS in D4.

# Let me recount which are in D4:
# ア: (2,1,0,3) → YES (BD対角線反転)
# イ: (2,3,0,1) → YES (180度回転)  
# ウ: (1,0,3,2) → YES (垂直軸反転)
# エ: (3,0,1,2) → YES (90度回転)

# ALL of ア through エ are in D4! That's a problem - the question needs to distinguish.

# I need to redesign. Let me use a different shape or different operations.

# Let me try: 正三角柱の頂点操作 or just redesign the operations.

# Actually, looking at the original problem more carefully:
# 問9 uses a tetrahedron (4 vertices), and asks which operations ALWAYS match.
# The symmetry group of tetrahedron is S4 (order 24)... no wait.
# Regular tetrahedron symmetry group has order 12 (A4, the alternating group on 4 elements).
# Actually the full symmetry group including reflections is S4 (order 24).

# Hmm, for a regular tetrahedron, ALL permutations of vertices are symmetries.
# No that's not right either. The rotation group is A4 (order 12).
# The full symmetry group (including improper rotations) is S4 (order 24).
# Wait, for a REGULAR tetrahedron, every permutation of the 4 vertices 
# corresponds to a symmetry. So the symmetry group IS S4.
# So ANY permutation of ABCD preserves the tetrahedron.

# Hmm but the original problem says "必ず一致する" which might mean something different.
# Let me re-read: "A,B,C,Dの並びが元の四面体と必ず一致する操作はどれか"
# 
# Oh wait - for a REGULAR tetrahedron, every permutation of the vertices 
# maps the tetrahedron to itself (since all vertices are equivalent).
# But the answer choices include ア through オ with specific operations,
# and the answer is a PAIR (2 correct out of 5).
# 
# Actually, for 操作オ "ランダムに二つの頂点を選び、それらを入れ替える。これを4回行う。"
# The result is always an even permutation (product of 4 transpositions).
# If the tetrahedron's symmetry group is S4, then ALL permutations are symmetries,
# so オ would always work too...
# 
# Unless "必ず一致する" means the result is always the SAME as the original 
# (identity permutation), not just a symmetry... No, that doesn't make sense either.
# 
# Let me reconsider. Looking at the image again:
# 問9: 正四面体ABCD
# The operations are on the vertices labeled A,B,C,D
# "A,B,C,Dの並びが元の四面体と必ず一致する"
# 
# I think the question is: after the operation, does the labeled tetrahedron 
# look the same? I.e., is the permutation a symmetry of the tetrahedron?
# 
# For a regular tetrahedron, ALL 24 permutations of vertices are symmetries.
# So that can't be it...
# 
# Actually wait - maybe not all permutations. Let me think again.
# A regular tetrahedron has vertices A(top), B, C, D (bottom three).
# The symmetry group has:
# - Identity
# - 8 rotations around vertex-to-opposite-face axes (120° and 240° each, 4 axes × 2 = 8)
# - 3 rotations around edge midpoint axes (180°, 3 axes)
# Total rotations: 1 + 8 + 3 = 12
# Including reflections: 12 more → 24 total
# 
# S4 has order 24, so YES, the symmetry group of a regular tetrahedron is S4.
# Every permutation of 4 vertices is a symmetry.
# 
# So the question must be about something else. Let me re-read.
# 
# Oh! "操作のいずれか1つを行ったとき、A,B,C,Dの並びが元の四面体と必ず一致する操作"
# 
# Wait, operation オ says "ランダムに二つの頂点を選び、それらを入れ替える。これを4回行う。"
# Since the tetrahedron symmetry group is ALL of S4, any permutation works.
# 4 random transpositions give SOME permutation, which is always in S4.
# So even オ would always work...
# 
# I think I'm misunderstanding the problem. Perhaps the problem is asking about a 
# LABELED tetrahedron (with specific edges), not just vertex positions.
# Or perhaps the question is about a specific property like "the same face is on top".
# 
# Without fully understanding the original, let me just design my OWN problem 
# that's similar in spirit but with a clear unique answer.

# NEW DESIGN: 正六角形ABCDEF with D6 symmetry group

# Actually, let me keep it simpler. Let me do a problem about 
# a 2x2 grid with labeled cells.

# NEW PROBLEM DESIGN:
# 下図のような正三角形ABCの各辺の中点をD, E, Fとする。
# 6つの点に対して操作ア〜オを行ったとき、
# 元の図形と完全に一致する操作はどれか。
#
# Actually this is getting complicated. Let me go with a simpler approach.

# SIMPLER DESIGN - Similar to original but with a cube:
# 正方形ABCDの各頂点にア〜オの操作を行い、
# 元の正方形と一致するかどうか

# The key issue is: not all permutations of 4 vertices are in D4 (only 8 out of 24).
# So many operations WON'T be in D4.

# Let me pick operations where exactly 2 are in D4 and 3 are not:

# ア: AとBを入れ替える (0,1交換) → (1,0,2,3) = 垂直軸反転? 
# D4 vertical axis: swaps A↔B and D↔C → (1,0,3,2) ≠ (1,0,2,3)
# So (1,0,2,3) is NOT in D4
print(f"\n(1,0,2,3) in D4? {(1,0,2,3) in D4}")  # False

# イ: AとC、BとDをそれぞれ入れ替える → (2,3,0,1) = 180度回転 → IN D4
print(f"(2,3,0,1) in D4? {(2,3,0,1) in D4}")  # True

# ウ: AとBを入れ替えた後、CとDを入れ替える → (1,0,2,3)→(1,0,3,2) = 垂直軸反転 → IN D4
print(f"(1,0,3,2) in D4? {(1,0,3,2) in D4}")  # True

# エ: AをC、BをA、CをD、DをBにそれぞれ移す → 
# A→C位置, B→A位置, C→D位置, D→B位置
# new[2]=old[0]=A, new[0]=old[1]=B, new[3]=old[2]=C, new[1]=old[3]=D
# = (B, D, A, C) = (1, 3, 0, 2)
print(f"(1,3,0,2) in D4? {(1,3,0,2) in D4}")  # ?

# オ: ランダムに二つの頂点を選び入れ替える。これを2回行う。
# 2 transpositions = even permutation
# Even permutations in S4: A4 = {e, (12)(34), (13)(24), (14)(23), (123), (132), (124), (142), (134), (143), (234), (243)}
# = 12 elements
# D4 ∩ A4 = {e, r90, r180, r270} = 4 elements (rotations)
# So NOT all even permutations are in D4
# Example: swap(0,1) then swap(2,3) → (1,0,3,2) which IS in D4
# Example: swap(0,1) then swap(0,2) → first (1,0,2,3), then swap pos 0 and 2: (2,0,1,3)
print(f"(2,0,1,3) in D4? {(2,0,1,3) in D4}")  # Probably not

# So オ doesn't ALWAYS give a D4 element.

# Let me verify all results:
print("\n最終チェック:")
final_ops = {
    'ア': (1,0,2,3),   # AとBの交換のみ
    'イ': (2,3,0,1),   # AとC、BとDの交換 (180度回転)
    'ウ': (1,0,3,2),   # ABを入れ替え、CDを入れ替え (垂直軸反転)
    'エ': (1,3,0,2),   # A→C, B→A, C→D, D→B
    'オ': None          # ランダム2回交換
}

for name, op in final_ops.items():
    if op is not None:
        print(f"  {name}: {perm_to_str(op)} → D4に{'含まれる' if is_in_D4(op) else '含まれない'}")
    else:
        # Check all possible 2-swap results
        all_in_d4 = True
        counterexample = None
        for s1 in pairs:
            for s2 in pairs:
                state = (0,1,2,3)
                state = swap(state, *s1)
                state = swap(state, *s2)
                if not is_in_D4(state):
                    all_in_d4 = False
                    counterexample = (s1, s2, state)
                    break
            if not all_in_d4:
                break
        if all_in_d4:
            print(f"  {name}: 2回交換で常にD4 → D4に含まれる")
        else:
            print(f"  {name}: 反例 swaps={counterexample[0]},{counterexample[1]} → {perm_to_str(counterexample[2])} → D4に含まれない場合がある")

# 正解: イとウ → 選択肢で(イ, ウ)の組み合わせを正解にする

print()
print("=" * 60)
print("問2: 町と施設のバス路線パズル")
print("=" * 60)
print()

# 5つの町 P, Q, R, S, T にそれぞれ施設がある。
# バス会社 X, Y, Z がこれらの町の間で直行バスを運行している。
# いくつかの町は山間部に位置している。
# 
# 条件:
# (I) P〜Tのうち、山間部でない町は隣接しており、山間部の町はほかのどの町とも隣接しない。
# (II) X社は隣接する2つの町と、1つの山間部の町の間で直行バスを運行している。
# (III) Y社は1つの山間部でない町と、2つの山間部の町の間で直行バスを運行しており、そのうち1つはTである。
# (IV) Z社は隣接する2つの町の間でのみ直行バスを運行している。
# (V) Pは山間部ではなく、どのバス会社もPとそのほかの町の間で直行バスを運行している。
# (VI) すべての町で、いずれかの会社がバスを運行している。
#
# 選択肢:
# ア 2社の直行バスが運航されている町の組は1組である
# イ Tは山間部である
# ウ Q R間はいずれかのバス会社が直行バスを運行している
# エ Z社の便のみ発着している町がある

# Let's model this properly.
# Towns: P, Q, R, S, T (indices 0-4)
# Mountain towns: some subset
# Non-mountain towns: adjacent to each other, mountain towns not adjacent to any other town

# An airline/bus company connects specific pairs of towns.
# "Adjacent" means non-mountain (mainland) towns that are neighbors.
# Mountain towns are isolated (not adjacent to any other town).

# Condition (I): Non-mountain towns are adjacent to each other (fully connected among themselves).
#                Mountain towns are not adjacent to any town.
# Condition (II): X operates between 2 adjacent (non-mountain) towns and 1 mountain town.
#   → X has routes: {non-mountain1, non-mountain2} (adjacent) and {non-mountain?, mountain1}
#   Wait, "2つの隣接する町と1つの山間部の町の間で" means X operates routes connecting
#   2 adjacent towns AND routes connecting to 1 mountain town.
#   Probably: X serves 3 towns total (2 non-mountain + 1 mountain), with routes between them.
#   But since mountain towns aren't adjacent, the routes would be:
#   - non-mountain1 ↔ non-mountain2 (adjacent)
#   - non-mountain1 ↔ mountain1 and/or non-mountain2 ↔ mountain1
#   
#   Actually, re-reading the original 問10 more carefully:
#   "(II)S社は陸続きの2つの地点と、1つの離島の地点の間で直行便を運航している。"
#   This means S airline operates direct flights between:
#   - 2 mainland points AND 1 island point
#   So S airline serves 3 points, connecting them pairwise? Or specific connections?
#   
#   I think it means: X operates between {2 non-mountain towns} and {1 mountain town}
#   i.e., X has routes connecting these 3 towns. The 2 non-mountain towns are adjacent.
#   Routes: between each pair of the 3 towns = 3 routes.

# Let me reformulate for clarity.
# Each bus company operates routes between specific sets of towns.
# "A社はXつの町とYつの町の間で運行" = A operates routes between X towns of type1 and Y towns of type2

# Let me think about it differently. Each company has a set of towns it serves,
# and operates direct routes between certain pairs.

# Simplified model:
# - Each company serves a set of towns
# - Routes exist between certain pairs of served towns
# - "隣接する2つの町と1つの山間部の町の間" = connects 2 adjacent non-mountain towns to 1 mountain town
#   → Routes: nm1↔nm2, nm1↔m1, nm2↔m1 (all pairs among the 3)

# OK let me just design a concrete puzzle and verify it.

# Setup: 5 towns P,Q,R,S,T
# Let's say mountain towns = {S, T} (2 mountain towns)
# Non-mountain towns = {P, Q, R} (3 non-mountain towns, all adjacent to each other)

# Now assign bus companies:
# (V) P is non-mountain, every company operates between P and some other town.
# (II) X: 2 adjacent non-mountain + 1 mountain → e.g., X serves {P, Q, S}
#   Routes: P↔Q, P↔S, Q↔S
# (III) Y: 1 non-mountain + 2 mountain, one of which is T → e.g., Y serves {P, S, T}  
#   Wait, but (V) says every company serves P. So Y must serve P.
#   Y: {P, S, T} - routes: P↔S, P↔T, S↔T
#   But S and T are both mountain, they're not adjacent. Can there be a route between non-adjacent towns?
#   In the airline model, yes - direct flights exist between islands and mainland.
#   
#   Hmm wait - "直行バス" means direct bus. In the original, direct flights go between mainland and islands.
#   For buses: mountain towns are remote, but you can still have a direct bus route to them.

# (IV) Z: only between 2 adjacent non-mountain towns → e.g., Z serves {P, R}
#   Route: P↔R
# (V) P is served by all companies: X serves P ✓, Y serves P ✓, Z serves P ✓
# (VI) All towns have at least one company: 
#   P: X,Y,Z ✓; Q: X ✓; R: Z ✓; S: X,Y ✓; T: Y ✓

# Check condition (V) more carefully: "どのバス会社もPとそのほかの町の間で直行バスを運行している"
# This means EVERY company operates BETWEEN P AND some other town.
# X: P↔Q, P↔S ✓
# Y: P↔S, P↔T ✓  
# Z: P↔R ✓
# All good!

# Now verify all conditions:
# (I) Non-mountain: {P,Q,R} - adjacent to each other ✓. Mountain: {S,T} - not adjacent to any ✓
# (II) X: 2 adjacent non-mountain (P,Q) + 1 mountain (S) ✓
# (III) Y: 1 non-mountain (P) + 2 mountain (S,T), one is T ✓
# (IV) Z: 2 adjacent non-mountain (P,R) only ✓
# (V) P is non-mountain, all companies connect to P ✓
# (VI) All towns served ✓

# Now check choices:
# ア: 2社の直行バスが運航されている町の組は1組である
# Town pairs with 2+ companies:
# P-Q: X only
# P-R: Z only
# P-S: X and Y → 2 companies!
# P-T: Y only
# Q-S: X only
# S-T: Y only (if Y connects S-T)
# Actually, does Y connect S↔T? Y serves {P, S, T}.
# Y operates "1つの山間部でない町と、2つの山間部の町の間で直行バスを運行"
# So Y's routes are: P↔S, P↔T, and S↔T
# But S and T are both mountain and not adjacent...
# In the airline problem, flights between two islands would be unusual.
# Let me re-read: "1つの離島でない地点と、2つの離島の地点の間で直行便を運航"
# I think this means routes are between the non-island point and each island point.
# So: P↔S and P↔T (but NOT S↔T)
# That makes more sense logistically.

# Similarly for X: "陸続きの2つの地点と、1つの離島の地点の間で"
# Routes: between each of the 2 mainland and the 1 island, plus between the 2 mainland
# So X: P↔Q, P↔S, Q↔S

# Actually wait, for X: the route is "between" the set of {2 adjacent towns} and {1 mountain town}
# So routes connect the set to the mountain town: nm1↔m and nm2↔m
# And also nm1↔nm2 (since they're adjacent)?
# 
# Hmm, in the original, S airline "陸続きの2つの地点と、1つの離島の地点の間で直行便を運航"
# I think "の間で" means the company operates flights connecting these 3 points.
# So all pairs: nm1↔nm2, nm1↔m, nm2↔m. That's 3 routes for 3 points.

# For Y: "1つの離島でない地点と、2つの離島の地点の間で直行便を運航"
# Similarly, all pairs: nm↔m1, nm↔m2, m1↔m2. 3 routes for 3 points.

# OK let me go with all-pairs interpretation.

print("設定:")
print("  山間部: S, T")
print("  非山間部(隣接): P, Q, R")
print()
print("バス路線:")
print("  X社: {P, Q, S} → P↔Q, P↔S, Q↔S")
print("  Y社: {P, S, T} → P↔S, P↔T, S↔T")
print("  Z社: {P, R} → P↔R")
print()

# Let me also check: is this the ONLY valid configuration?
# We need to verify uniqueness.

# Variables:
# - Which towns are mountain? (subset of {P,Q,R,S,T}, excluding P since P is non-mountain by (V))
# - Which towns does each company serve?

# Constraints:
# - P is non-mountain (V)
# - At least 1 mountain town (since Y serves 2 mountain towns (III))
# - Non-mountain towns form a clique (I)
# - Mountain towns have no adjacency (I)

# Let M = set of mountain towns, NM = set of non-mountain towns
# |NM| >= 1 (P), P ∈ NM
# |M| >= 2 (Y needs 2 mountain towns (III))
# T might or might not be mountain

# (II) X: serves 2 NM towns + 1 M town, the 2 NM are adjacent (always true since all NM are adjacent)
# (III) Y: serves 1 NM town + 2 M towns, one M town is T → T ∈ M
# (IV) Z: serves 2 NM towns (adjacent), only operates between them
# (V) P ∈ NM, all companies have routes involving P
#   → P must be one of X's NM towns
#   → P must be Y's NM town
#   → P must be one of Z's NM towns

# From (III) and T ∈ M: T is mountain.
# From (III): Y serves {P, T, m2} where m2 is another mountain town.
# |M| >= 2: T and at least one more.

# Possible M sets (T ∈ M, P ∉ M):
# {T, Q}, {T, R}, {T, S}, {T, Q, R}, {T, Q, S}, {T, R, S}, {T, Q, R, S}

# (IV) Z serves 2 NM towns including P.
# If NM = {P} only (M = {Q,R,S,T}), Z can't have 2 NM towns → impossible.
# If NM = {P, one_other}, Z = {P, one_other}. 
# Need |NM| >= 2.
# (II) X serves 2 NM + 1 M, so |NM| >= 2 as well.

# Case 1: |M| = 2 → |NM| = 3
# M contains T and one of {Q, R, S}
# NM = 5 - 2 = 3 towns including P

# Case 1a: M = {S, T}, NM = {P, Q, R}
# X: 2 from {P,Q,R} including P + 1 from {S,T}
#   X pairs including P: {P,Q} or {P,R}
#   X mountain: S or T
# Y: {P} + 2 from {S,T} = {P, S, T}
# Z: 2 from {P,Q,R} including P: {P,Q} or {P,R}
# 
# (VI) All towns served:
# Q must be served by someone. X serves {P, ?, ?} and Z serves {P, ?}.
# If X = {P, Q, S} and Z = {P, R}: Q served by X ✓, R served by Z ✓, S served by X,Y ✓, T served by Y ✓
# If X = {P, Q, T} and Z = {P, R}: S needs to be served. Y serves {P, S, T} → S served by Y ✓. OK.
# If X = {P, R, S} and Z = {P, Q}: All served ✓
# If X = {P, R, T} and Z = {P, Q}: S served by Y ✓. OK.

# Hmm there are multiple possibilities. I need to add more constraints.

# Let me add: "(VII) X社とY社がともに運行する路線がちょうど1つある"
# This constrains things further.

# Case 1a: M = {S, T}, NM = {P, Q, R}
# Y = {P, S, T}, routes: P↔S, P↔T, S↔T
# 
# If X = {P, Q, S}: X routes: P↔Q, P↔S, Q↔S
#   Common with Y: P↔S → 1 common route ✓
# If X = {P, Q, T}: X routes: P↔Q, P↔T, Q↔T
#   Common with Y: P↔T → 1 common route ✓
# If X = {P, R, S}: X routes: P↔R, P↔S, R↔S
#   Common with Y: P↔S → 1 common route ✓
# If X = {P, R, T}: X routes: P↔R, P↔T, R↔T
#   Common with Y: P↔T → 1 common route ✓

# Still too many. Let me add another constraint or modify existing ones.

# Let me try a completely different approach and just verify the configuration I want.

# Actually, let me redesign the problem to be cleaner. I'll model it directly 
# based on the original 問10 structure.

print()
print("問2 再設計")
print("=" * 60)

# 5つの地区 P, Q, R, S, T にはそれぞれ学校がある。
# バス会社 X, Y, Z がこれらの地区間で直通バスを運行している。
# これらの地区のうちいくつかは山岳地帯に位置している。
# 次のことがわかっているとき、各地区と直通バスについて確実にいえるものはどれか。
#
# (I) P〜Tのうち、山岳地帯でない地区は平野部に位置して互いに隣接しており、
#     山岳地帯の地区はほかのどの地区とも隣接していない。
# (II) X社は平野部の2地区と、山岳地帯の1地区の間で直通バスを運行している。
# (III) Y社は平野部の1地区と、山岳地帯の2地区の間で直通バスを運行しており、
#      そのうち1地区はTである。
# (IV) Z社は平野部の2地区の間でのみ直通バスを運行している。
# (V) Pは平野部であり、どのバス会社もPとそのほかの地区の間で直通バスを運行している。
# (VI) すべての地区で、いずれかの会社が直通バスを運行している。
#
# Let me solve this systematically.

towns = ['P', 'Q', 'R', 'S', 'T']

# P is non-mountain (V)
# T is mountain (from III: Y serves 2 mountain towns, one is T)
# At least 2 mountain towns (for III)

# Enumerate all possible mountain sets
solutions = []

for mountain_mask in range(32):
    mountain = set()
    for i in range(5):
        if mountain_mask & (1 << i):
            mountain.add(towns[i])
    
    non_mountain = set(towns) - mountain
    
    # P is non-mountain
    if 'P' in mountain:
        continue
    
    # T is mountain (from III)
    if 'T' not in mountain:
        continue
    
    # Need at least 2 mountain towns for Y
    if len(mountain) < 2:
        continue
    
    # Need at least 2 non-mountain for X (II) and Z (IV)
    if len(non_mountain) < 2:
        continue
    
    # X: 2 non-mountain + 1 mountain, P must be in X's non-mountain (V)
    for x_nm2 in non_mountain - {'P'}:
        for x_m in mountain:
            x_towns_nm = {'P', x_nm2}
            x_towns_m = {x_m}
            x_routes = set()
            for a in x_towns_nm | x_towns_m:
                for b in x_towns_nm | x_towns_m:
                    if a < b:
                        x_routes.add((a, b))
            
            # Y: 1 non-mountain (must be P) + 2 mountain (one is T)
            y_nm = {'P'}
            for y_m2 in mountain - {'T'}:
                y_towns_m = {'T', y_m2}
                y_routes = set()
                for a in y_nm | y_towns_m:
                    for b in y_nm | y_towns_m:
                        if a < b:
                            y_routes.add((a, b))
                
                # Z: 2 non-mountain including P (V)
                for z_nm2 in non_mountain - {'P'}:
                    z_towns = {'P', z_nm2}
                    z_routes = set()
                    for a in z_towns:
                        for b in z_towns:
                            if a < b:
                                z_routes.add((a, b))
                    
                    # Check (V): P connected to other towns via each company
                    p_x = any('P' in r for r in x_routes)
                    p_y = any('P' in r for r in y_routes)
                    p_z = any('P' in r for r in z_routes)
                    if not (p_x and p_y and p_z):
                        continue
                    
                    # Check (VI): all towns served
                    all_served_towns = set()
                    for route_set in [x_routes, y_routes, z_routes]:
                        for a, b in route_set:
                            all_served_towns.add(a)
                            all_served_towns.add(b)
                    
                    if all_served_towns != set(towns):
                        continue
                    
                    sol = {
                        'mountain': mountain,
                        'non_mountain': non_mountain,
                        'X': (x_towns_nm, x_towns_m, x_routes),
                        'Y': (y_nm, y_towns_m, y_routes),
                        'Z': (z_towns, z_routes),
                    }
                    solutions.append(sol)

print(f"解の数: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"\n解{i+1}:")
    print(f"  山岳: {sol['mountain']}, 平野: {sol['non_mountain']}")
    print(f"  X社: 平野{sol['X'][0]}, 山岳{sol['X'][1]}, 路線{sol['X'][2]}")
    print(f"  Y社: 平野{sol['Y'][0]}, 山岳{sol['Y'][1]}, 路線{sol['Y'][2]}")
    print(f"  Z社: 町{sol['Z'][0]}, 路線{sol['Z'][1]}")

# Check which statements are always true
if solutions:
    print("\n選択肢の検証:")
    
    # ア: 2社の直通バスが運行されている地区の組は1組である
    print("\nア: 2社の直通バスが運行されている路線の組は1組である")
    for i, sol in enumerate(solutions):
        x_r = sol['X'][2]
        y_r = sol['Y'][2]
        z_r = sol['Z'][1]
        
        # Count routes served by exactly 2 companies
        all_routes = x_r | y_r | z_r
        two_company_routes = []
        for route in all_routes:
            count = (route in x_r) + (route in y_r) + (route in z_r)
            if count >= 2:
                two_company_routes.append(route)
        print(f"  解{i+1}: 2社以上の路線: {two_company_routes} ({len(two_company_routes)}組)")
    
    # イ: Tは山岳地帯である
    print("\nイ: Tは山岳地帯である")
    all_T_mountain = all('T' in sol['mountain'] for sol in solutions)
    print(f"  常に真: {all_T_mountain}")
    
    # ウ: QR間はいずれかのバス会社が直通バスを運行している
    print("\nウ: QR間はいずれかのバス会社が直通バスを運行している")
    for i, sol in enumerate(solutions):
        qr = ('Q', 'R')
        x_has = qr in sol['X'][2]
        y_has = qr in sol['Y'][2]
        z_has = qr in sol['Z'][1]
        print(f"  解{i+1}: X={x_has}, Y={y_has}, Z={z_has}, いずれか={x_has or y_has or z_has}")
    
    # エ: Z社の便のみ発着している地区がある
    print("\nエ: Z社の便のみ発着している地区がある")
    for i, sol in enumerate(solutions):
        x_towns_served = set()
        for a, b in sol['X'][2]:
            x_towns_served.add(a)
            x_towns_served.add(b)
        y_towns_served = set()
        for a, b in sol['Y'][2]:
            y_towns_served.add(a)
            y_towns_served.add(b)
        z_towns_served = set()
        for a, b in sol['Z'][1]:
            z_towns_served.add(a)
            z_towns_served.add(b)
        
        z_only = z_towns_served - x_towns_served - y_towns_served
        print(f"  解{i+1}: Z社のみ={z_only}")

