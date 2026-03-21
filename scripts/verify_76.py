"""
航大思考76 検証スクリプト
問1: 5地区の統計データから1世帯あたり人口を計算し順位付け
問2: 5事業部の2年度分データから利益率変化を計算し順位付け
"""

def verify_q1():
    """問1: 1世帯あたり人口の順位付け"""
    data = {
        'A': {'population': 24500, 'households': 9800,  'area': 8.5,  'facilities': 12},
        'B': {'population': 31200, 'households': 12000, 'area': 11.2, 'facilities': 18},
        'C': {'population': 18900, 'households': 7000,  'area': 6.8,  'facilities': 9},
        'D': {'population': 42000, 'households': 15000, 'area': 15.5, 'facilities': 24},
        'E': {'population': 27600, 'households': 11500, 'area': 9.3,  'facilities': 15},
    }

    # 1世帯あたり人口を計算
    ratios = {}
    for district, d in data.items():
        ratio = d['population'] / d['households']
        ratios[district] = ratio
        print(f"  {district}地区: {d['population']}/{d['households']} = {ratio:.2f}")

    # 全て一意であることを確認
    values = list(ratios.values())
    assert len(values) == len(set(values)), "重複する値があります"

    # 降順にソート
    ranking = sorted(ratios.keys(), key=lambda x: ratios[x], reverse=True)
    print(f"  順位（多い順）: {'→'.join(ranking)}")

    # 選択肢の検証
    options = {
        1: ['D', 'C', 'A', 'B', 'E'],
        2: ['C', 'D', 'B', 'A', 'E'],
        3: ['D', 'B', 'C', 'A', 'E'],
        4: ['D', 'C', 'B', 'E', 'A'],
        5: ['D', 'C', 'B', 'A', 'E'],  # 正解
    }

    correct_count = 0
    for opt_num, opt_order in options.items():
        is_correct = opt_order == ranking
        if is_correct:
            correct_count += 1
            print(f"  選択肢({opt_num}): {'→'.join(opt_order)} ← 正解")
        else:
            print(f"  選択肢({opt_num}): {'→'.join(opt_order)}")

    assert correct_count == 1, f"正解が{correct_count}個あります（1個であるべき）"
    assert options[5] == ranking, "正解は(5)であるべき"
    print("  問1: 検証OK - 正解は(5)")
    return ranking


def verify_q2():
    """問2: 利益率変化の順位付け"""
    data = {
        'P': {'r5_sales': 50, 'r5_cost': 40, 'r7_sales': 60, 'r7_cost': 45},
        'Q': {'r5_sales': 80, 'r5_cost': 60, 'r7_sales': 100, 'r7_cost': 72},
        'R': {'r5_sales': 40, 'r5_cost': 30, 'r7_sales': 48, 'r7_cost': 36},
        'S': {'r5_sales': 60, 'r5_cost': 48, 'r7_sales': 75, 'r7_cost': 54},
        'T': {'r5_sales': 120, 'r5_cost': 96, 'r7_sales': 140, 'r7_cost': 98},
    }

    changes = {}
    for dept, d in data.items():
        r5_margin = (d['r5_sales'] - d['r5_cost']) / d['r5_sales'] * 100
        r7_margin = (d['r7_sales'] - d['r7_cost']) / d['r7_sales'] * 100
        change = r7_margin - r5_margin
        changes[dept] = change
        print(f"  {dept}: R5利益率={r5_margin:.1f}%, R7利益率={r7_margin:.1f}%, 変化={change:+.1f}%")

    # 全て一意であることを確認
    values = list(changes.values())
    assert len(values) == len(set(values)), "重複する値があります"

    # 降順にソート
    ranking = sorted(changes.keys(), key=lambda x: changes[x], reverse=True)
    print(f"  順位（変化が大きい順）: {'→'.join(ranking)}")

    # 選択肢の検証
    options = {
        1: ['T', 'P', 'S', 'Q', 'R'],
        2: ['S', 'T', 'P', 'Q', 'R'],
        3: ['T', 'S', 'Q', 'P', 'R'],
        4: ['T', 'S', 'P', 'Q', 'R'],  # 正解
        5: ['T', 'S', 'P', 'R', 'Q'],
    }

    correct_count = 0
    for opt_num, opt_order in options.items():
        is_correct = opt_order == ranking
        if is_correct:
            correct_count += 1
            print(f"  選択肢({opt_num}): {'→'.join(opt_order)} ← 正解")
        else:
            print(f"  選択肢({opt_num}): {'→'.join(opt_order)}")

    assert correct_count == 1, f"正解が{correct_count}個あります（1個であるべき）"
    assert options[4] == ranking, "正解は(4)であるべき"
    print("  問2: 検証OK - 正解は(4)")
    return ranking


if __name__ == '__main__':
    print("=" * 60)
    print("航大思考76 検証")
    print("=" * 60)
    print("\n問1: 1世帯あたり人口の多い順")
    verify_q1()
    print("\n問2: 利益率変化が大きい順")
    verify_q2()
    print("\n" + "=" * 60)
    print("全検証完了")
    print("=" * 60)
