"""
航大思考183 検証スクリプト - 箱ひげ図問題

問1（標準）: 5つの箱ひげ図と4つの条件からクラスCを特定
問2（高難度）: 5つの箱ひげ図と5つの条件からクラスCを特定（連鎖推論）
"""
import random
from itertools import permutations


# ============================================================
# 問1: 5クラス（A-E）の箱ひげ図、4条件でCを特定
# ============================================================
def verify_q1():
    # クラスごとの真の箱ひげ図統計値 (min, Q1, med, Q3, max)
    classes = {
        'A': (5, 15, 30, 50, 70),    # 中央値最小
        'B': (10, 20, 45, 65, 90),   # 範囲最大
        'C': (15, 35, 50, 70, 85),   # 残り（目標）
        'D': (20, 40, 55, 60, 80),   # IQR最小
        'E': (25, 45, 60, 75, 85),   # 最小値最大
    }

    # 条件
    # ア. Aの中央値が5クラスで最も小さい
    # イ. Bの範囲が5クラスで最も大きい
    # ウ. Dの四分位範囲(IQR)が5クラスで最も小さい
    # エ. Eの最小値が5クラスで最も大きい
    # → C は残り

    # 全順列で割り当てを試し、条件を満たす唯一の割り当てを確認
    labels = ['A', 'B', 'C', 'D', 'E']
    stats = list(classes.values())

    valid_assignments = []
    for perm in permutations(stats):
        # perm[i] が labels[i] に対応
        assigned = dict(zip(labels, perm))

        # ア: A.med が最小
        meds = {k: v[2] for k, v in assigned.items()}
        if assigned['A'][2] != min(meds.values()):
            continue
        # メディアンが最小のクラスが唯一Aである
        if list(meds.values()).count(min(meds.values())) != 1:
            continue

        # イ: B.range が最大
        ranges = {k: v[4] - v[0] for k, v in assigned.items()}
        if assigned['B'][4] - assigned['B'][0] != max(ranges.values()):
            continue
        if list(ranges.values()).count(max(ranges.values())) != 1:
            continue

        # ウ: D.IQR が最小
        iqrs = {k: v[3] - v[1] for k, v in assigned.items()}
        if assigned['D'][3] - assigned['D'][1] != min(iqrs.values()):
            continue
        if list(iqrs.values()).count(min(iqrs.values())) != 1:
            continue

        # エ: E.min が最大
        mins = {k: v[0] for k, v in assigned.items()}
        if assigned['E'][0] != max(mins.values()):
            continue
        if list(mins.values()).count(max(mins.values())) != 1:
            continue

        valid_assignments.append(assigned)

    # 唯一の割り当てを確認
    assert len(valid_assignments) == 1, f"問1: 解が{len(valid_assignments)}個存在"
    answer = valid_assignments[0]

    # 真の割り当てと一致
    for k in labels:
        assert answer[k] == classes[k], f"問1: 割り当て不一致 {k}"

    print("問1: 検証成功 - クラスCの箱ひげ図統計値 =", classes['C'])
    print("       (min, Q1, med, Q3, max) = (15, 35, 50, 70, 85)")
    return classes


# ============================================================
# 問2: 5クラス（A-E）の箱ひげ図、5条件（連鎖推論）でCを特定
# ============================================================
def verify_q2():
    classes = {
        'A': (10, 20, 35, 55, 70),   # range=60, IQR=35
        'B': (15, 25, 40, 60, 80),   # range=65, IQR=35
        'C': (20, 35, 50, 65, 90),   # range=70, IQR=30
        'D': (5,  30, 45, 70, 85),   # range=80, IQR=40
        'E': (25, 40, 55, 75, 95),   # range=70, IQR=35
    }

    # 条件
    # ア. Eの最小値はAの最小値より15大きい (E.min - A.min = 15)
    # イ. Bの第1四分位数はDの第1四分位数より5小さい (B.Q1 = D.Q1 - 5)
    # ウ. Cの中央値はEの中央値より5小さい (C.med = E.med - 5)
    # エ. Dの範囲が5クラスで最も大きい
    # オ. Eの第3四分位数はAの第3四分位数より20大きい (E.Q3 - A.Q3 = 20)

    labels = ['A', 'B', 'C', 'D', 'E']
    stats = list(classes.values())

    valid_assignments = []
    for perm in permutations(stats):
        assigned = dict(zip(labels, perm))
        A = assigned['A']
        B = assigned['B']
        C = assigned['C']
        D = assigned['D']
        E = assigned['E']

        # ア
        if E[0] - A[0] != 15:
            continue
        # イ
        if B[1] != D[1] - 5:
            continue
        # ウ
        if C[2] != E[2] - 5:
            continue
        # エ: Dの範囲が最大、唯一
        ranges = {k: v[4] - v[0] for k, v in assigned.items()}
        d_range = D[4] - D[0]
        if d_range != max(ranges.values()):
            continue
        if list(ranges.values()).count(d_range) != 1:
            continue
        # オ
        if E[3] - A[3] != 20:
            continue

        valid_assignments.append(assigned)

    assert len(valid_assignments) == 1, f"問2: 解が{len(valid_assignments)}個存在"
    answer = valid_assignments[0]

    for k in labels:
        assert answer[k] == classes[k], f"問2: 割り当て不一致 {k}"

    print("問2: 検証成功 - クラスCの箱ひげ図統計値 =", classes['C'])
    print("       (min, Q1, med, Q3, max) = (20, 35, 50, 65, 90)")
    return classes


def randomize_positions(seed=None):
    """各問のクラス→表示位置(1)-(5)へのランダム割り当て"""
    if seed is not None:
        random.seed(seed)

    pos_q1 = list(range(1, 6))
    random.shuffle(pos_q1)
    pos_q2 = list(range(1, 6))
    random.shuffle(pos_q2)

    # A, B, C, D, E の表示位置
    labels = ['A', 'B', 'C', 'D', 'E']
    map_q1 = dict(zip(labels, pos_q1))
    map_q2 = dict(zip(labels, pos_q2))

    print("\n=== 問1 表示位置 ===")
    for k in labels:
        print(f"  クラス{k} → 位置({map_q1[k]})")
    print(f"  ★問1の正解（Cの位置）: ({map_q1['C']})")

    print("\n=== 問2 表示位置 ===")
    for k in labels:
        print(f"  クラス{k} → 位置({map_q2[k]})")
    print(f"  ★問2の正解（Cの位置）: ({map_q2['C']})")

    return map_q1, map_q2


if __name__ == "__main__":
    print("=" * 60)
    print("航大思考183 検証")
    print("=" * 60)
    cls_q1 = verify_q1()
    print()
    cls_q2 = verify_q2()
    randomize_positions(seed=183)
