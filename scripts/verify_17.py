"""
verify_17.py - セット17 解の一意性検証

問1: 1人の嘘つき特定問題
  5人(A,B,C,D,E)のうちちょうど1人が嘘つき。
  各人の発言から嘘つきを特定する。

問2: 2人の嘘つき特定問題（高難度版）
  5人(A,B,C,D,E)のうちちょうど2人が嘘つき。
  各人の発言から嘘つきの組み合わせを特定する。
"""

from itertools import combinations


def verify_problem1():
    """
    問1: 5人の中の1人の嘘つきを特定する

    発言:
    A: 「Bは嘘をついている」
    B: 「Aは嘘をついている」
    C: 「BかDのどちらかが嘘をついている」
    D: 「Cは正直者だ」
    E: 「Cは正直者だ」
    """
    people = ['A', 'B', 'C', 'D', 'E']
    valid_solutions = []

    for liar in people:
        ok = True

        # A の発言: 「Bは嘘をついている」
        a_statement = (liar == 'B')
        if liar == 'A' and a_statement:      # 嘘つきが真を言っている → 矛盾
            ok = False
        if liar != 'A' and not a_statement:  # 正直者が偽を言っている → 矛盾
            ok = False
        if not ok:
            continue

        # B の発言: 「Aは嘘をついている」
        b_statement = (liar == 'A')
        if liar == 'B' and b_statement:
            ok = False
        if liar != 'B' and not b_statement:
            ok = False
        if not ok:
            continue

        # C の発言: 「BかDのどちらかが嘘をついている」
        c_statement = (liar in ['B', 'D'])
        if liar == 'C' and c_statement:
            ok = False
        if liar != 'C' and not c_statement:
            ok = False
        if not ok:
            continue

        # D の発言: 「Cは正直者だ」
        d_statement = (liar != 'C')
        if liar == 'D' and d_statement:
            ok = False
        if liar != 'D' and not d_statement:
            ok = False
        if not ok:
            continue

        # E の発言: 「Cは正直者だ」
        e_statement = (liar != 'C')
        if liar == 'E' and e_statement:
            ok = False
        if liar != 'E' and not e_statement:
            ok = False

        if ok:
            valid_solutions.append(liar)

    print(f"[問1] 有効な嘘つき: {valid_solutions}")
    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在 (期待: 1)"
    print(f"[問1] 正解: {valid_solutions[0]} が嘘をついている")
    return valid_solutions[0]


def verify_problem2():
    """
    問2: 5人の中の2人の嘘つきを特定する（高難度）

    発言:
    A: 「BかEのどちらかが嘘をついている」
    B: 「CかDのどちらかが嘘をついている」
    C: 「EとDはともに正直者だ」
    D: 「AとBはともに正直者だ」
    E: 「AかBのどちらかが嘘をついている」
    """
    people = ['A', 'B', 'C', 'D', 'E']
    valid_solutions = []

    for pair in combinations(people, 2):
        liars = set(pair)
        ok = True

        for person in people:
            is_liar = person in liars

            # 各人の発言を評価
            if person == 'A':
                statement = ('B' in liars or 'E' in liars)
            elif person == 'B':
                statement = ('C' in liars or 'D' in liars)
            elif person == 'C':
                statement = ('E' not in liars and 'D' not in liars)
            elif person == 'D':
                statement = ('A' not in liars and 'B' not in liars)
            elif person == 'E':
                statement = ('A' in liars or 'B' in liars)

            if is_liar and statement:      # 嘘つきが真を言っている → 矛盾
                ok = False
                break
            if not is_liar and not statement:  # 正直者が偽を言っている → 矛盾
                ok = False
                break

        if ok:
            valid_solutions.append(tuple(sorted(pair)))

    print(f"[問2] 有効な嘘つき組み合わせ: {valid_solutions}")
    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在 (期待: 1)"
    print(f"[問2] 正解: {valid_solutions[0][0]} と {valid_solutions[0][1]} が嘘をついている")
    return valid_solutions[0]


if __name__ == '__main__':
    print("=" * 50)
    print("セット17 解の一意性検証")
    print("=" * 50)
    ans1 = verify_problem1()
    print()
    ans2 = verify_problem2()
    print()
    print("=" * 50)
    print("検証完了: 両問題とも唯一解を確認")
    print("=" * 50)
