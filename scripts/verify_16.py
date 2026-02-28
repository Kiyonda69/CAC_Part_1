#!/usr/bin/env python3
"""
問題16 解の一意性検証
問題タイプ: 資料読み取り
"""

def verify_q1():
    """
    問1: 棒グラフの読み取り
    5都市の年間訪問者数から上位2都市と下位2都市の比率を求める
    正解: (4) 2倍
    """
    visitors = {
        '札幌': 850,
        '仙台': 420,
        '名古屋': 680,
        '広島': 390,
        '福岡': 760
    }

    sorted_vals = sorted(visitors.values(), reverse=True)
    print(f"訪問者数順位: {sorted_vals}")

    top2_sum = sorted_vals[0] + sorted_vals[1]   # 850 + 760 = 1610
    bottom2_sum = sorted_vals[-2] + sorted_vals[-1]  # 420 + 390 = 810
    ratio = top2_sum / bottom2_sum

    print(f"上位2都市の合計: {top2_sum}万人 ({sorted([k for k,v in visitors.items() if v in sorted_vals[:2]])})")
    print(f"下位2都市の合計: {bottom2_sum}万人 ({sorted([k for k,v in visitors.items() if v in sorted_vals[-2:]])})")
    print(f"比率: {ratio:.4f}")

    options = [1.5, 2.5, 1.75, 2.0, 2.25]
    labels = ['(1)', '(2)', '(3)', '(4)', '(5)']
    diffs = [abs(opt - ratio) for opt in options]
    closest_idx = diffs.index(min(diffs))
    print(f"最も近い選択肢: {labels[closest_idx]} = {options[closest_idx]}倍")
    print(f"差: {[f'{d:.4f}' for d in diffs]}")

    assert options[closest_idx] == 2.0, f"正解が{options[closest_idx]}になっている"
    assert closest_idx == 3, f"正解が選択肢(4)ではなく({closest_idx+1})になっている"
    print("✓ 問1: 正解は選択肢(4) 2倍 — 唯一解確認\n")
    return True


def verify_q2():
    """
    問2: 整備記録表の複合読み取り
    2項目以上の整備基準を満たす機体の飛行時間合計を求める
    正解: (1) 1,640時間
    """
    aircraft = {
        '1号機': {'days': 85, 'hours': 520, 'landings': 330},
        '2号機': {'days': 95, 'hours': 480, 'landings': 370},
        '3号機': {'days': 110, 'hours': 650, 'landings': 420},
        '4号機': {'days': 65, 'hours': 390, 'landings': 260},
        '5号機': {'days': 92, 'hours': 510, 'landings': 345},
    }

    thresholds = {'days': 90, 'hours': 500, 'landings': 350}

    qualifying = []
    print("各機体の整備基準チェック:")
    for name, data in aircraft.items():
        c_days = data['days'] >= thresholds['days']
        c_hours = data['hours'] >= thresholds['hours']
        c_landings = data['landings'] >= thresholds['landings']
        count = sum([c_days, c_hours, c_landings])
        print(f"  {name}: 経過日数{data['days']}日({'○' if c_days else '×'}), "
              f"飛行時間{data['hours']}h({'○' if c_hours else '×'}), "
              f"着陸{data['landings']}回({'○' if c_landings else '×'}) → {count}項目")
        if count >= 2:
            qualifying.append((name, data['hours']))

    total_hours = sum(h for _, h in qualifying)
    print(f"\n2項目以上満たす機体: {[n for n,_ in qualifying]}")
    print(f"各機体の飛行時間: {[f'{n}:{h}h' for n,h in qualifying]}")
    print(f"合計飛行時間: {total_hours}時間")

    options = [1640, 1130, 1160, 1510, 2160]
    labels = ['(1)', '(2)', '(3)', '(4)', '(5)']
    correct_idx = options.index(total_hours)
    print(f"正解選択肢: {labels[correct_idx]} = {options[correct_idx]}時間")

    assert total_hours == 1640, f"合計が{total_hours}になっている"
    assert correct_idx == 0, f"正解が選択肢(1)ではなく({correct_idx+1})になっている"
    print("✓ 問2: 正解は選択肢(1) 1,640時間 — 唯一解確認\n")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("問題16 解の一意性検証")
    print("=" * 50)
    print()
    verify_q1()
    verify_q2()
    print("=" * 50)
    print("全問題の検証完了")
