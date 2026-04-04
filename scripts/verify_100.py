"""
セット100: 資料読み取り問題の検証スクリプト
問1: 社内研修プログラムの実施結果報告（読解力問題）
問2: 5都市の観光客動向調査報告書（読解力問題）
"""

def verify_q1():
    """問1: 社内研修プログラムの実施結果報告 - 正解(5)"""

    # 各部門の所属人数
    departments = {
        '営業部': 40,
        '技術部': 40,
        '総務部': 20,
        '企画部': 25,
    }

    # 各研修の参加者数 [営業部, 技術部, 総務部, 企画部]
    trainings = {
        '第1回': {'営業部': 28, '技術部': 35, '総務部': 12, '企画部': 15, '満足度': 3.8},
        '第2回': {'営業部': 32, '技術部': 36, '総務部': 15, '企画部': 18, '満足度': 4.2},
        '第3回': {'営業部': 35, '技術部': 20, '総務部': 8, '企画部': 22, '満足度': 3.5},
        '第4回': {'営業部': 20, '技術部': 38, '総務部': 10, '企画部': 16, '満足度': 4.0},
        '第5回': {'営業部': 25, '技術部': 30, '総務部': 14, '企画部': 20, '満足度': 3.6},
    }

    # 参加率を計算
    print("=== 問1 検証 ===")
    print("\n各研修の参加率:")
    for name, data in trainings.items():
        total = sum(data[d] for d in departments)
        print(f"  {name}: 合計{total}名, 満足度{data['満足度']}")
        for dept, count in departments.items():
            rate = data[dept] / count * 100
            print(f"    {dept}: {data[dept]}名 ({rate:.1f}%)")

    # 延べ参加者数
    print("\n延べ参加者数:")
    for dept in departments:
        total = sum(t[dept] for t in trainings.values())
        print(f"  {dept}: {total}名")

    grand_total = sum(sum(t[dept] for dept in departments) for t in trainings.values())
    print(f"  合計: {grand_total}名")

    # 選択肢の検証
    print("\n--- 選択肢の検証 ---")

    # (1) 技術部は全5回の研修を通じて、毎回30名以上が参加した
    tech_all_30 = all(t['技術部'] >= 30 for t in trainings.values())
    print(f"(1) 技術部が毎回30名以上: {tech_all_30}")
    print(f"    → 第3回は{trainings['第3回']['技術部']}名 → 不正解")
    assert not tech_all_30

    # (2) 満足度が4.0以上の研修は、いずれも受講者数が90名を超えている
    high_satisfaction = [(name, sum(t[d] for d in departments))
                        for name, t in trainings.items() if t['満足度'] >= 4.0]
    all_over_90 = all(total > 90 for _, total in high_satisfaction)
    print(f"(2) 満足度4.0以上の研修が全て90名超: {all_over_90}")
    for name, total in high_satisfaction:
        print(f"    {name}: {total}名")
    assert not all_over_90  # 第4回は84名

    # (3) 総務部の参加率が最も高かったのは第5回である
    somu_rates = {name: t['総務部'] / departments['総務部'] * 100
                  for name, t in trainings.items()}
    max_somu = max(somu_rates, key=somu_rates.get)
    print(f"(3) 総務部参加率が最高の研修: {max_somu} ({somu_rates[max_somu]:.1f}%)")
    print(f"    第5回の参加率: {somu_rates['第5回']:.1f}%")
    assert max_somu != '第5回'  # 第2回(75%)が最高

    # (4) 受講者数が最も少なかった研修は、満足度も最も低かった
    totals = {name: sum(t[d] for d in departments) for name, t in trainings.items()}
    min_total = min(totals, key=totals.get)
    min_satisfaction = min(trainings, key=lambda x: trainings[x]['満足度'])
    print(f"(4) 受講者数最少: {min_total}({totals[min_total]}名), 満足度最低: {min_satisfaction}({trainings[min_satisfaction]['満足度']})")
    assert min_total != min_satisfaction

    # (5) 企画部の上半期の平均参加率は、営業部の上半期の平均参加率より高い（正解）
    eigyo_avg_rate = sum(t['営業部'] / departments['営業部'] * 100 for t in trainings.values()) / 5
    kikaku_avg_rate = sum(t['企画部'] / departments['企画部'] * 100 for t in trainings.values()) / 5
    print(f"(5) 営業部平均参加率: {eigyo_avg_rate:.1f}%, 企画部平均参加率: {kikaku_avg_rate:.1f}%")
    print(f"    企画部 > 営業部: {kikaku_avg_rate > eigyo_avg_rate}")
    assert kikaku_avg_rate > eigyo_avg_rate  # 正解

    # 正解確認
    results = [tech_all_30, all_over_90, max_somu == '第5回', min_total == min_satisfaction, kikaku_avg_rate > eigyo_avg_rate]
    correct_indices = [i+1 for i, r in enumerate(results) if r]
    assert correct_indices == [5], f"正解が(5)のみであること: {correct_indices}"
    print(f"\n問1: 正解は(5)のみ ✓")


def verify_q2():
    """問2: 5都市の観光客動向調査報告書 - 正解(2)"""

    # 各都市・各四半期のデータ [来訪者数, 一人あたり消費額]
    data = {
        '甲市': {
            'Q1': (45000, 3200), 'Q2': (52000, 3500),
            'Q3': (48000, 3800), 'Q4': (25000, 2800),
        },
        '乙市': {
            'Q1': (28000, 5800), 'Q2': (65000, 4200),
            'Q3': (35000, 5500), 'Q4': (32000, 6200),
        },
        '丙市': {
            'Q1': (32000, 4100), 'Q2': (30000, 4800),
            'Q3': (40000, 4300), 'Q4': (28000, 3900),
        },
        '丁市': {
            'Q1': (38000, 3600), 'Q2': (55000, 4000),
            'Q3': (42000, 3900), 'Q4': (36000, 4500),
        },
        '戊市': {
            'Q1': (15000, 4500), 'Q2': (22000, 5200),
            'Q3': (18000, 4800), 'Q4': (12000, 4200),
        },
    }

    print("\n=== 問2 検証 ===")

    # 年間来訪者数
    annual_visitors = {}
    annual_revenue = {}
    for city, quarters in data.items():
        visitors = sum(q[0] for q in quarters.values())
        revenue = sum(q[0] * q[1] for q in quarters.values())
        annual_visitors[city] = visitors
        annual_revenue[city] = revenue
        print(f"{city}: 年間来訪者数={visitors:,}人, 年間消費総額={revenue:,}円")

    # 選択肢検証
    print("\n--- 選択肢の検証 ---")

    # (1) 年間の総来訪者数が最も多い都市は甲市
    max_visitor_city = max(annual_visitors, key=annual_visitors.get)
    print(f"(1) 年間来訪者数最多: {max_visitor_city}({annual_visitors[max_visitor_city]:,}人)")
    print(f"    甲市: {annual_visitors['甲市']:,}人")
    assert max_visitor_city != '甲市'  # 丁市が最多

    # (2) 年間の観光消費総額が最も大きい都市は乙市（正解）
    max_revenue_city = max(annual_revenue, key=annual_revenue.get)
    print(f"(2) 年間消費総額最大: {max_revenue_city}({annual_revenue[max_revenue_city]:,}円)")
    assert max_revenue_city == '乙市'

    # (3) 丙市は全四半期を通じて来訪者数の変動が最も小さい
    ranges = {}
    for city, quarters in data.items():
        visitors = [q[0] for q in quarters.values()]
        ranges[city] = max(visitors) - min(visitors)
    min_range_city = min(ranges, key=ranges.get)
    print(f"(3) 来訪者数の変動幅:")
    for city, r in sorted(ranges.items(), key=lambda x: x[1]):
        print(f"    {city}: {r:,}人")
    print(f"    最小変動: {min_range_city}")
    assert min_range_city != '丙市'  # 戊市が最小

    # (4) 第3四半期の5都市合計来訪者数は第1四半期より50,000人以上多い
    q1_total = sum(d['Q1'][0] for d in data.values())
    q3_total = sum(d['Q3'][0] for d in data.values())
    diff = q3_total - q1_total
    print(f"(4) Q1合計: {q1_total:,}人, Q3合計: {q3_total:,}人, 差: {diff:,}人")
    assert diff < 50000

    # (5) 戊市の年間平均消費額は甲市の1.4倍以上
    bo_avg = annual_revenue['戊市'] / annual_visitors['戊市']
    ko_avg = annual_revenue['甲市'] / annual_visitors['甲市']
    ratio = bo_avg / ko_avg
    print(f"(5) 戊市年間平均消費額: {bo_avg:.1f}円, 甲市: {ko_avg:.1f}円")
    print(f"    比率: {ratio:.4f}")
    assert ratio < 1.4  # 1.4倍未満

    # 正解確認
    results = [
        max_visitor_city == '甲市',
        max_revenue_city == '乙市',
        min_range_city == '丙市',
        diff >= 50000,
        ratio >= 1.4,
    ]
    correct_indices = [i+1 for i, r in enumerate(results) if r]
    assert correct_indices == [2], f"正解が(2)のみであること: {correct_indices}"
    print(f"\n問2: 正解は(2)のみ ✓")


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("\n========================================")
    print("全問題の検証完了: 解の一意性を確認しました")
    print("========================================")
