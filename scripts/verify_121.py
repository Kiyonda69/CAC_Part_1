#!/usr/bin/env python3
"""
セット121 の検証スクリプト

問1: 書店8店舗 × 5ジャンルの売上データ（穴埋め4箇所）
問2: 観光8地域 × 4四半期 × 2指標 の統計データ（穴埋め5箇所）
"""


def verify_q1():
    """問1: 書店8店舗 × 5ジャンル"""
    # 売上（万円）
    data = {
        '札幌': {'文芸': 320, '実用': 240, '専門': 180, '児童': 120, 'コミック': 380},
        '仙台': {'文芸': 280, '実用': 220, '専門': 160, '児童': 140, 'コミック': 360},
        '東京': {'文芸': 480, '実用': 380, '専門': 320, '児童': 200, 'コミック': 520},
        '横浜': {'文芸': 360, '実用': 280, '専門': 200, '児童': 180, 'コミック': 420},
        '名古屋': {'文芸': 340, '実用': 260, '専門': 220, '児童': 160, 'コミック': 400},
        '大阪': {'文芸': 420, '実用': 320, '専門': 260, '児童': 180, 'コミック': 460},
        '広島': {'文芸': 240, '実用': 200, '専門': 140, '児童': 100, 'コミック': 320},
        '福岡': {'文芸': 320, '実用': 240, '専門': 180, '児童': 140, 'コミック': 360},
    }
    genres = ['文芸', '実用', '専門', '児童', 'コミック']
    stores = list(data.keys())

    # 店舗別合計
    store_total = {s: sum(data[s].values()) for s in stores}
    # ジャンル別合計
    genre_total = {g: sum(data[s][g] for s in stores) for g in genres}
    # 全合計
    total = sum(store_total.values())
    total2 = sum(genre_total.values())
    assert total == total2, f"合計不一致: {total} vs {total2}"

    print('=== 問1 検証 ===')
    print(f'店舗別合計: {store_total}')
    print(f'ジャンル別合計: {genre_total}')
    print(f'全体合計: {total}')

    # （ア）店舗別売上で最大の店舗
    max_store = max(stores, key=lambda s: store_total[s])
    # （イ）コミック比率（コミック÷店舗合計）が最大の店舗
    comic_ratio = {s: data[s]['コミック'] / store_total[s] for s in stores}
    max_comic_store = max(stores, key=lambda s: comic_ratio[s])
    # （ウ）専門書ジャンルの売上合計
    specialty_total = genre_total['専門']
    # （エ）全合計
    grand_total = total

    print(f'\n（ア）店舗別売上で最大の店舗: {max_store}（{store_total[max_store]}万円）')
    print(f'（イ）コミック比率最大の店舗: {max_comic_store}（{comic_ratio[max_comic_store]*100:.2f}%）')
    print(f'   全店舗のコミック比率:')
    for s in stores:
        print(f'     {s}: {comic_ratio[s]*100:.2f}%')
    print(f'（ウ）専門書ジャンルの売上合計: {specialty_total}万円')
    print(f'（エ）全合計: {grand_total}万円')

    # 期待値の確認
    assert max_store == '東京'
    assert max_comic_store == '広島'
    assert specialty_total == 1660
    assert grand_total == 11000

    print('\n問1 検証OK')
    return {
        'ア': grand_total if False else '東京',  # ア = 東京
        'イ': '広島',
        'ウ': 1660,
        'エ': 11000,
    }


def verify_q2():
    """問2: 観光8地域 × 4四半期 × 2指標"""
    # (来訪千人, 消費百万円)
    data = {
        '北海道': {'Q1': (80, 120), 'Q2': (100, 160), 'Q3': (140, 240), 'Q4': (180, 320)},
        '東北':   {'Q1': (60, 90),  'Q2': (90, 140),  'Q3': (110, 180), 'Q4': (120, 200)},
        '関東':   {'Q1': (200, 360), 'Q2': (240, 460), 'Q3': (280, 560), 'Q4': (320, 660)},
        '中部':   {'Q1': (120, 200), 'Q2': (140, 240), 'Q3': (160, 280), 'Q4': (180, 320)},
        '近畿':   {'Q1': (180, 320), 'Q2': (200, 380), 'Q3': (220, 420), 'Q4': (240, 460)},
        '中国':   {'Q1': (70, 100),  'Q2': (80, 120),  'Q3': (90, 140),  'Q4': (100, 160)},
        '四国':   {'Q1': (50, 70),   'Q2': (60, 90),   'Q3': (70, 110),  'Q4': (80, 130)},
        '九州':   {'Q1': (100, 160), 'Q2': (120, 200), 'Q3': (140, 240), 'Q4': (160, 280)},
    }
    regions = list(data.keys())
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    # 地域別の年間来訪・消費
    region_visit = {r: sum(data[r][q][0] for q in quarters) for r in regions}
    region_spend = {r: sum(data[r][q][1] for q in quarters) for r in regions}
    # 四半期別の8地域合計
    q_visit = {q: sum(data[r][q][0] for r in regions) for q in quarters}
    q_spend = {q: sum(data[r][q][1] for r in regions) for q in quarters}
    # 全体合計
    total_visit = sum(region_visit.values())
    total_spend = sum(region_spend.values())

    print('\n=== 問2 検証 ===')
    print(f'地域別 年間来訪者: {region_visit}')
    print(f'地域別 年間消費額: {region_spend}')
    print(f'四半期別 来訪者合計: {q_visit}')
    print(f'四半期別 消費額合計: {q_spend}')
    print(f'全体 来訪者: {total_visit}, 消費: {total_spend}')

    # （ア）8地域の年間来訪者数合計
    a = total_visit
    # （イ）来訪者1人あたり消費額が最大の地域
    per_capita = {r: region_spend[r] / region_visit[r] for r in regions}
    b = max(regions, key=lambda r: per_capita[r])
    # （ウ）Q4消費額がQ1消費額の2倍以上の地域数
    c = sum(1 for r in regions if data[r]['Q4'][1] >= 2 * data[r]['Q1'][1])
    # （エ）地域別年間消費額の最大値
    d = max(region_spend.values())
    # （オ）8地域の年間消費額合計
    e = total_spend

    print(f'\n（ア）年間来訪者合計: {a}千人')
    print(f'（イ）1人あたり消費額が最大の地域: {b}')
    print(f'   1人あたり消費額（千円/人）:')
    for r in regions:
        print(f'     {r}: {per_capita[r]*1000/1000:.3f} (= {region_spend[r]}/{region_visit[r]})')
    print(f'（ウ）Q4消費額 ≥ 2 × Q1消費額 の地域数: {c}')
    for r in regions:
        ratio = data[r]['Q4'][1] / data[r]['Q1'][1]
        mark = '○' if ratio >= 2 else '×'
        print(f'     {r}: Q4={data[r]["Q4"][1]} / Q1={data[r]["Q1"][1]} = {ratio:.3f} {mark}')
    print(f'（エ）年間消費額が最大の地域の値: {d}百万円')
    print(f'（オ）年間消費額合計: {e}百万円')

    # 期待値の確認
    assert a == 4480
    assert b == '関東'
    assert c == 2
    assert d == 2040
    assert e == 7910

    print('\n問2 検証OK')


if __name__ == '__main__':
    verify_q1()
    verify_q2()
