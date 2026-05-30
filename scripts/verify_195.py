# -*- coding: utf-8 -*-
"""セット195 箱ひげ図問題の検証 + SVG生成
問1(標準): 4つの最大/最小条件でクラスCを特定
問2(高難度): 5つの相対値・連鎖条件でクラスCを特定
"""
import itertools, random

def x(v):
    return round(80 + v * 4.8, 1)

def stats(d):
    mn, q1, md, q3, mx = d
    return dict(mn=mn, q1=q1, md=md, q3=q3, mx=mx,
                rng=mx - mn, iqr=q3 - q1)

# ---------- 問1 各箱ひげ図の素データ(min,Q1,med,Q3,max) ----------
Q1_data = {
    (1): (20, 35, 45, 70, 90),
    (2): (10, 25, 40, 55, 65),
    (3): (30, 45, 55, 65, 85),
    (4): (5, 30, 50, 60, 95),
    (5): (25, 40, 60, 75, 80),
}

def check_q1(assign):
    """assign: dict role->plot_index。条件を全て満たすか"""
    S = {r: stats(Q1_data[p]) for r, p in assign.items()}
    allp = [stats(Q1_data[i]) for i in range(1, 6)]
    # ア. Aの範囲が最大
    if S['A']['rng'] != max(s['rng'] for s in allp): return False
    if sum(s['rng'] == S['A']['rng'] for s in allp) != 1: return False
    # イ. Bの最小値が最大
    if S['B']['mn'] != max(s['mn'] for s in allp): return False
    if sum(s['mn'] == S['B']['mn'] for s in allp) != 1: return False
    # ウ. Dの中央値が最小
    if S['D']['md'] != min(s['md'] for s in allp): return False
    if sum(s['md'] == S['D']['md'] for s in allp) != 1: return False
    # エ. Eの第3四分位数が最大
    if S['E']['q3'] != max(s['q3'] for s in allp): return False
    if sum(s['q3'] == S['E']['q3'] for s in allp) != 1: return False
    return True

# ---------- 問2 各箱ひげ図の素データ ----------
Q2_data = {
    (1): (15, 30, 45, 60, 85),
    (2): (25, 40, 50, 70, 90),
    (3): (5, 20, 35, 50, 75),
    (4): (20, 35, 55, 65, 80),
    (5): (10, 25, 40, 55, 95),
}

def check_q2(assign):
    S = {r: stats(Q2_data[p]) for r, p in assign.items()}
    allp = [stats(Q2_data[i]) for i in range(1, 6)]
    # ア. Dの範囲が最大
    if S['D']['rng'] != max(s['rng'] for s in allp): return False
    if sum(s['rng'] == S['D']['rng'] for s in allp) != 1: return False
    # イ. BのQ1 = DのQ1 + 10
    if S['B']['q1'] != S['D']['q1'] + 10: return False
    # ウ. Aの最小値 = Eの最小値 - 10
    if S['A']['mn'] != S['E']['mn'] - 10: return False
    # エ. Eの中央値 = Cの中央値 - 5
    if S['E']['md'] != S['C']['md'] - 5: return False
    # オ. EのQ3 = AのQ3 + 10
    if S['E']['q3'] != S['A']['q3'] + 10: return False
    return True

def solve(check):
    roles = ['A', 'B', 'C', 'D', 'E']
    sols = []
    for perm in itertools.permutations(range(1, 6)):
        assign = dict(zip(roles, perm))
        if check(assign):
            sols.append(assign)
    return sols

for name, check, data in [("問1", check_q1, Q1_data), ("問2", check_q2, Q2_data)]:
    sols = solve(check)
    assert len(sols) == 1, f"{name}: 解が{len(sols)}個"
    C = sols[0]['C']
    print(f"{name}: 唯一解 {sols[0]}  → クラスC = ({C})")

print("検証OK: 両問とも解が一意")
