"""
セット28 解の一意性検証スクリプト
アジア太平洋地域の主要航空会社 経営指標読み取り問題
"""

def verify_q1():
    """
    問1: 4社の経営指標表読み取り（標準難度）
    表: P航空・Q航空・R航空・S航空の2021〜2023年 旅客数/営業収入/営業利益率/座席利用率
    問い: ア〜オのうち正しいものの組み合わせを選べ
    """
    print("=" * 60)
    print("【問1 検証】")
    print("=" * 60)

    data = {
        'P航空': {
            '旅客数':     [280,  320,  350 ],  # 万人 [2021, 2022, 2023]
            '営業収入':   [1200, 1450, 1600],  # 億円
            '営業利益率': [5.0,  8.0,  10.0],  # %
            '座席利用率': [70,   78,   82  ],   # %
        },
        'Q航空': {
            '旅客数':     [210,  180,  230 ],
            '営業収入':   [900,  820,  980 ],
            '営業利益率': [4.0,  2.0,  6.0 ],
            '座席利用率': [72,   65,   79  ],
        },
        'R航空': {
            '旅客数':     [150,  130,  140 ],
            '営業収入':   [650,  700,  620 ],
            '営業利益率': [3.0,  5.0,  2.0 ],
            '座席利用率': [68,   74,   70  ],
        },
        'S航空': {
            '旅客数':     [80,   90,   100 ],
            '営業収入':   [380,  420,  460 ],
            '営業利益率': [1.0,  3.0,  5.0 ],
            '座席利用率': [55,   62,   68  ],
        },
    }

    years = [2021, 2022, 2023]
    companies = list(data.keys())

    # ア: 2022年において旅客数が前年より減少した航空会社はQ航空とR航空の2社である
    decreased_2022 = [c for c in companies if data[c]['旅客数'][1] < data[c]['旅客数'][0]]
    a_correct = set(decreased_2022) == {'Q航空', 'R航空'}
    print(f"\nア: 2022年に旅客数が前年より減少した会社 = {decreased_2022}")
    print(f"    期待: [Q航空, R航空] → {'正しい ○' if a_correct else '誤り ×'}")

    # イ: 3年間を通じてP航空の座席利用率は全4社の中で常に最も高かった
    i_correct = True
    for yi, year in enumerate(years):
        p_rate = data['P航空']['座席利用率'][yi]
        max_rate = max(data[c]['座席利用率'][yi] for c in companies)
        if p_rate < max_rate:
            i_correct = False
            max_company = [c for c in companies if data[c]['座席利用率'][yi] == max_rate]
            print(f"\nイ: {year}年 P航空({p_rate}%) < 最高({max_rate}%)→{max_company}")
    if i_correct:
        print(f"\nイ: 全年P航空が最高")
    print(f"    → {'正しい ○' if i_correct else '誤り ×'}")

    # ウ: 2023年において営業利益（営業収入×営業利益率）が最も大きい航空会社はP航空である
    profits_2023 = {c: data[c]['営業収入'][2] * data[c]['営業利益率'][2] / 100
                    for c in companies}
    max_profit_company = max(profits_2023, key=lambda x: profits_2023[x])
    u_correct = max_profit_company == 'P航空'
    print(f"\nウ: 2023年 営業利益 = {profits_2023}")
    print(f"    最大 = {max_profit_company} → {'正しい ○' if u_correct else '誤り ×'}")

    # エ: 調査期間中にR航空の営業収入が前年を下回った年は存在しない
    r_rev = data['R航空']['営業収入']
    r_decreased_years = [years[i] for i in range(1, 3) if r_rev[i] < r_rev[i-1]]
    e_correct = len(r_decreased_years) == 0
    print(f"\nエ: R航空 営業収入 = {r_rev}")
    print(f"    前年比減少年 = {r_decreased_years} → {'正しい ○' if e_correct else '誤り ×'}")

    # オ: 2023年において座席利用率が75%を超えた航空会社は2社である
    over75_2023 = [c for c in companies if data[c]['座席利用率'][2] > 75]
    o_correct = len(over75_2023) == 2
    print(f"\nオ: 2023年 座席利用率75%超の会社 = {over75_2023}")
    print(f"    社数 = {len(over75_2023)} → {'正しい ○' if o_correct else '誤り ×'}")

    # 結果集計
    results = {'ア': a_correct, 'イ': i_correct, 'ウ': u_correct, 'エ': e_correct, 'オ': o_correct}
    correct_labels = [label for label, val in results.items() if val]
    print(f"\n{'='*60}")
    print(f"【問1 結果】正しい文: {correct_labels}")
    print(f"  正解の組み合わせ: {'・'.join(correct_labels)}")
    assert len(correct_labels) == 3, f"正しい文が{len(correct_labels)}個（3個であるべき）"
    print("  解の一意性: OK（3文が正しい）")
    return correct_labels


def verify_q2():
    """
    問2: 5社の経営指標表読み取り（高難度）
    表: A航空〜E航空の2021〜2023年 旅客数/営業収入/営業利益率/座席利用率
    問い: ア〜オのうち正しいものの組み合わせを選べ（営業利益の計算が必要）
    """
    print("\n" + "=" * 60)
    print("【問2 検証】")
    print("=" * 60)

    data = {
        'A航空': {
            '旅客数':     [520,  580,  620 ],  # 万人
            '営業収入':   [2400, 2800, 3000],  # 億円
            '営業利益率': [6.0,  9.0,  11.0],  # %
            '座席利用率': [72,   80,   84  ],   # %
        },
        'B航空': {
            '旅客数':     [380,  350,  410 ],
            '営業収入':   [1800, 1650, 1950],
            '営業利益率': [4.0,  2.0,  7.0 ],
            '座席利用率': [68,   62,   75  ],
        },
        'C航空': {
            '旅客数':     [250,  270,  280 ],
            '営業収入':   [1100, 1200, 1250],
            '営業利益率': [3.0,  4.0,  5.0 ],
            '座席利用率': [65,   70,   74  ],
        },
        'D航空': {
            '旅客数':     [160,  180,  200 ],
            '営業収入':   [750,  850,  950 ],
            '営業利益率': [2.0,  4.0,  6.0 ],
            '座席利用率': [60,   66,   72  ],
        },
        'E航空': {
            '旅客数':     [90,   110,  100 ],
            '営業収入':   [420,  480,  450 ],
            '営業利益率': [-1.0, 1.0,  3.0 ],
            '座席利用率': [50,   58,   62  ],
        },
    }

    years = [2021, 2022, 2023]
    companies = list(data.keys())

    # ア: 2022年から2023年にかけて旅客数が前年より減少した航空会社はE航空のみである
    decreased_2223 = [c for c in companies if data[c]['旅客数'][2] < data[c]['旅客数'][1]]
    a_correct = set(decreased_2223) == {'E航空'}
    print(f"\nア: 2022→2023年に旅客数が減少した会社 = {decreased_2223}")
    print(f"    → {'正しい ○' if a_correct else '誤り ×'}")

    # イ: 2023年における全5社の営業利益の合計は600億円を超える
    profits_2023 = {c: data[c]['営業収入'][2] * data[c]['営業利益率'][2] / 100
                    for c in companies}
    total_profit_2023 = sum(profits_2023.values())
    i_correct = total_profit_2023 > 600
    print(f"\nイ: 2023年 各社の営業利益(億円) = {profits_2023}")
    print(f"    合計 = {total_profit_2023:.1f}億円")
    print(f"    600億円超か？ → {'正しい ○' if i_correct else '誤り ×'}")

    # ウ: 3年間を通じてB航空の旅客数はC航空の旅客数を常に上回っていた
    u_correct = all(data['B航空']['旅客数'][i] > data['C航空']['旅客数'][i]
                    for i in range(3))
    print(f"\nウ: B航空旅客数 = {data['B航空']['旅客数']}")
    print(f"    C航空旅客数 = {data['C航空']['旅客数']}")
    print(f"    常にB>C？ → {'正しい ○' if u_correct else '誤り ×'}")

    # エ: 2023年において座席利用率が最も高い会社と最も低い会社の差は20ポイント以上
    rates_2023 = {c: data[c]['座席利用率'][2] for c in companies}
    max_rate = max(rates_2023.values())
    min_rate = min(rates_2023.values())
    diff = max_rate - min_rate
    e_correct = diff >= 20
    print(f"\nエ: 2023年 座席利用率 = {rates_2023}")
    print(f"    最高={max_rate}%, 最低={min_rate}%, 差={diff}pt")
    print(f"    20pt以上か？ → {'正しい ○' if e_correct else '誤り ×'}")

    # オ: 調査期間を通じてE航空は一度も黒字にならなかった
    e_profitable_years = [years[i] for i in range(3) if data['E航空']['営業利益率'][i] > 0]
    o_correct = len(e_profitable_years) == 0
    print(f"\nオ: E航空の黒字年 = {e_profitable_years}")
    print(f"    一度も黒字なし？ → {'正しい ○' if o_correct else '誤り ×'}")

    # 結果集計
    results = {'ア': a_correct, 'イ': i_correct, 'ウ': u_correct, 'エ': e_correct, 'オ': o_correct}
    correct_labels = [label for label, val in results.items() if val]
    print(f"\n{'='*60}")
    print(f"【問2 結果】正しい文: {correct_labels}")
    print(f"  正解の組み合わせ: {'・'.join(correct_labels)}")
    assert len(correct_labels) == 3, f"正しい文が{len(correct_labels)}個（3個であるべき）"
    print("  解の一意性: OK（3文が正しい）")
    return correct_labels


if __name__ == '__main__':
    q1_correct = verify_q1()
    q2_correct = verify_q2()
    print(f"\n{'='*60}")
    print(f"【最終確認】")
    print(f"  問1 正解: {'・'.join(q1_correct)}")
    print(f"  問2 正解: {'・'.join(q2_correct)}")
