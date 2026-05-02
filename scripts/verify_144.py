#!/usr/bin/env python3
"""航大思考144の検証スクリプト"""

def verify_q1():
    """問1: 5都市の交通統計表読み取り"""
    # データ定義
    cities = {
        'P': {'人口': 350, '鉄道': 285, 'バス': 46, '自動車': 180, '自転車': 290},
        'Q': {'人口': 120, '鉄道':  58, 'バス': 31, '自動車':  74, '自転車':  88},
        'R': {'人口':  85, '鉄道':  12, 'バス': 28, '自動車':  72, '自転車':  70},
        'S': {'人口': 210, '鉄道': 145, 'バス': 38, '自動車':  98, '自転車': 164},
        'T': {'人口': 160, '鉄道':  96, 'バス': 44, '自動車':  88, '自転車': 130},
    }

    print("=== 問1 検証 ===")
    print("\n鉄道利用者数/人口:")
    for c, d in cities.items():
        ratio = d['鉄道'] / d['人口']
        print(f"  {c}: {d['鉄道']}/{d['人口']} = {ratio:.3f} ({ratio*100:.1f}%)")

    print("\nバス利用者数ランキング:")
    bus_rank = sorted(cities.items(), key=lambda x: x[1]['バス'], reverse=True)
    for c, d in bus_rank:
        print(f"  {c}: {d['バス']}")

    print("\n自動車 vs 自転車:")
    for c, d in cities.items():
        diff = d['自動車'] - d['自転車']
        print(f"  {c}: 自動車{d['自動車']} vs 自転車{d['自転車']} → {'自動車多い' if diff > 0 else '自転車多い'}")

    total_rail = sum(d['鉄道'] for d in cities.values())
    print(f"\n5都市の鉄道利用者数合計: {total_rail}万人/日")

    print("\n人口当たり自転車保有台数:")
    bike_ratio = {c: d['自転車']/d['人口'] for c, d in cities.items()}
    for c, r in sorted(bike_ratio.items(), key=lambda x: x[1], reverse=True):
        print(f"  {c}: {r:.4f}")

    print("\n各選択肢の検証:")
    # (1) バス最多はT？
    max_bus_city = max(cities, key=lambda c: cities[c]['バス'])
    print(f"(1) バス最多: {max_bus_city}都市 → {'T' if max_bus_city=='T' else 'T以外'}なので {'TRUE' if max_bus_city=='T' else 'FALSE'}")

    # (2) 自動車>自転車の都市なし？
    auto_more = [c for c in cities if cities[c]['自動車'] > cities[c]['自転車']]
    print(f"(2) 自動車>自転車の都市: {auto_more} → なし={'TRUE' if not auto_more else 'FALSE'}")

    # (3) 鉄道/人口>80%はPのみ？
    rail_80 = [c for c in cities if cities[c]['鉄道']/cities[c]['人口'] > 0.80]
    print(f"(3) 鉄道>80%の都市: {rail_80} → Pのみ={'TRUE' if rail_80==['P'] else 'FALSE'}")

    # (4) 鉄道合計>600？
    print(f"(4) 鉄道合計={total_rail} > 600 → {'TRUE' if total_rail > 600 else 'FALSE'}")

    # (5) 人口当たり自転車最高はR？
    max_bike_city = max(bike_ratio, key=bike_ratio.get)
    print(f"(5) 人口当たり自転車最高: {max_bike_city}都市 → R='TRUE' if {max_bike_city=='R'} else FALSE")

    correct = []
    if max_bus_city == 'T': correct.append(1)
    if not auto_more: correct.append(2)
    if rail_80 == ['P']: correct.append(3)
    if total_rail > 600: correct.append(4)
    if max_bike_city == 'R': correct.append(5)

    print(f"\n正解選択肢: {correct}")
    assert correct == [3], f"期待する正解は[3]だが実際は{correct}"
    print("検証OK: 唯一解 (3)")


def verify_q2():
    """問2: 工場生産効率データ読み取り"""
    factories = {
        'A': {'1月': (8400, 252), '2月': (7600, 304), '3月': (9200, 230)},
        'B': {'1月': (5600, 112), '2月': (6200, 186), '3月': (5800, 116)},
        'C': {'1月': (7200, 360), '2月': (7800, 234), '3月': (8100, 405)},
        'D': {'1月': (4800,  96), '2月': (5400, 162), '3月': (4600, 138)},
        'E': {'1月': (6500, 195), '2月': (7100, 284), '3月': (6800, 204)},
    }

    print("\n=== 問2 検証 ===")

    quarterly = {}
    for f, months in factories.items():
        total_prod = sum(v[0] for v in months.values())
        total_def  = sum(v[1] for v in months.values())
        rate = total_def / total_prod
        quarterly[f] = {'生産': total_prod, '不良': total_def, '率': rate}
        print(f"工場{f}: 生産={total_prod:,} 不良={total_def} 率={rate*100:.2f}%")

    print("\n各月不良品率:")
    for f, months in factories.items():
        for m, (prod, defect) in months.items():
            print(f"  工場{f} {m}: {defect}/{prod} = {defect/prod*100:.2f}%")

    print("\n各選択肢の検証:")
    # (1) C工場四半期不良品率>5%？
    c_rate = quarterly['C']['率']
    print(f"(1) C工場四半期不良品率={c_rate*100:.2f}% > 5% → {'TRUE' if c_rate > 0.05 else 'FALSE'}")

    # (2) A工場3月不良品率 > 1月？
    a1 = 252/8400
    a3 = 230/9200
    print(f"(2) A工場 3月({a3*100:.2f}%) > 1月({a1*100:.2f}%) → {'TRUE' if a3 > a1 else 'FALSE'}")

    # (3) 3月生産最多はA工場 かつ その不良品率<2.5%？
    march_prod = {f: factories[f]['3月'][0] for f in factories}
    max_march = max(march_prod, key=march_prod.get)
    a3_rate = 230/9200
    cond3 = (max_march == 'A') and (a3_rate < 0.025)
    print(f"(3) 3月最多生産={max_march}工場, A工場3月率={a3_rate*100:.2f}% < 2.5% → {'TRUE' if cond3 else 'FALSE'}")

    # (4) D工場四半期生産>20000？
    d_prod = quarterly['D']['生産']
    print(f"(4) D工場四半期生産={d_prod:,} > 20000 → {'TRUE' if d_prod > 20000 else 'FALSE'}")

    # (5) 四半期不良品率最低はB工場？
    min_rate_factory = min(quarterly, key=lambda f: quarterly[f]['率'])
    print(f"(5) 四半期不良品率最低={min_rate_factory}工場 → B='TRUE' if {min_rate_factory=='B'} else FALSE")

    correct = []
    if c_rate > 0.05: correct.append(1)
    if a3 > a1: correct.append(2)
    if cond3: correct.append(3)
    if d_prod > 20000: correct.append(4)
    if min_rate_factory == 'B': correct.append(5)

    print(f"\n正解選択肢: {correct}")
    assert correct == [5], f"期待する正解は[5]だが実際は{correct}"
    print("検証OK: 唯一解 (5)")


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("\n両問の検証完了")
