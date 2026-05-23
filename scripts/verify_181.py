"""航大思考181 解の一意性検証"""

def verify_q1():
    """問1: 4店舗の月次売上レポート"""
    stores = {
        '東店': {'visitors': 8500, 'buyers': 2720, 'sales': 4080000},
        '西店': {'visitors': 6000, 'buyers': 1800, 'sales': 3150000},
        '南店': {'visitors': 7500, 'buyers': 2400, 'sales': 3360000},
        '北店': {'visitors': 5000, 'buyers': 1400, 'sales': 2100000},
    }

    for name, d in stores.items():
        d['buy_rate'] = d['buyers'] / d['visitors'] * 100
        d['avg_price'] = d['sales'] / d['buyers']
        d['per_visitor'] = d['sales'] / d['visitors']
        print(f"{name}: 購入率={d['buy_rate']:.2f}%, 客単価={d['avg_price']:.0f}円, "
              f"1人あたり={d['per_visitor']:.2f}円")

    print()
    # 選択肢の検証
    options = []
    # (1) 売上総額が最も高いのは西店
    top_sales = max(stores, key=lambda k: stores[k]['sales'])
    options.append(('(1)', top_sales == '西店', f"売上最大={top_sales}"))

    # (2) 購入率が最も高いのは東店のみ
    max_rate = max(d['buy_rate'] for d in stores.values())
    top_rate_stores = [k for k, d in stores.items() if d['buy_rate'] == max_rate]
    options.append(('(2)', top_rate_stores == ['東店'], f"購入率最大={top_rate_stores}"))

    # (3) 客単価が最も低いのは北店
    min_price = min(stores, key=lambda k: stores[k]['avg_price'])
    options.append(('(3)', min_price == '北店', f"客単価最低={min_price}"))

    # (4) 来店者1人あたり売上が最も高いのは西店
    top_per = max(stores, key=lambda k: stores[k]['per_visitor'])
    options.append(('(4)', top_per == '西店', f"1人あたり最大={top_per}"))

    # (5) 4店舗の購入率はすべて30%以上
    all_30 = all(d['buy_rate'] >= 30 for d in stores.values())
    options.append(('(5)', all_30, f"購入率<30%の店={[k for k,d in stores.items() if d['buy_rate']<30]}"))

    correct = [opt for opt, ok, _ in options if ok]
    for opt, ok, info in options:
        print(f"{opt}: {'正' if ok else '誤'} - {info}")
    assert len(correct) == 1, f"問1: 正解が{len(correct)}個 {correct}"
    print(f"問1正解: {correct[0]}\n")


def verify_q2():
    """問2: 5生産ラインの月次品質報告書"""
    lines = {
        'A': {'produced': 12000, 'defects': 240, 'insp_hour': 60},
        'B': {'produced': 8000, 'defects': 120, 'insp_hour': 50},
        'C': {'produced': 15000, 'defects': 450, 'insp_hour': 75},
        'D': {'produced': 6000, 'defects': 90, 'insp_hour': 30},
        'E': {'produced': 10000, 'defects': 200, 'insp_hour': 40},
    }

    for name, d in lines.items():
        d['defect_rate'] = d['defects'] / d['produced'] * 100
        d['insp_eff'] = d['produced'] / d['insp_hour']
        print(f"{name}: 不良率={d['defect_rate']:.2f}%, 検査効率={d['insp_eff']:.1f}個/h")
    print()

    options = []
    # (1) 不良品率が最も低いのはBのみ
    min_rate = min(d['defect_rate'] for d in lines.values())
    min_lines = [k for k, d in lines.items() if d['defect_rate'] == min_rate]
    options.append(('(1)', min_lines == ['B'], f"不良率最低={min_lines}"))

    # (2) 検査効率が最も高いのはA
    top_eff = max(lines, key=lambda k: lines[k]['insp_eff'])
    options.append(('(2)', top_eff == 'A', f"検査効率最大={top_eff}"))

    # (3) 生産数の合計は52,000個
    total = sum(d['produced'] for d in lines.values())
    options.append(('(3)', total == 52000, f"生産数合計={total}"))

    # (4) 不良品数が最も多いのはA
    top_def = max(lines, key=lambda k: lines[k]['defects'])
    options.append(('(4)', top_def == 'A', f"不良品最多={top_def}"))

    # (5) 検査効率が250個/hを超える生産ラインはない
    over250 = [k for k, d in lines.items() if d['insp_eff'] > 250]
    options.append(('(5)', len(over250) == 0, f"250個/h超ライン={over250}"))

    correct = [opt for opt, ok, _ in options if ok]
    for opt, ok, info in options:
        print(f"{opt}: {'正' if ok else '誤'} - {info}")
    assert len(correct) == 1, f"問2: 正解が{len(correct)}個 {correct}"
    print(f"問2正解: {correct[0]}")


if __name__ == '__main__':
    verify_q1()
    verify_q2()
