#!/usr/bin/env python3
"""航大思考294 検証: 資料解釈（大量計算型）
問1: 5市の観光統計表 / 問2: 5部門の対前年増加率表
各問とも「正しい記述は1つだけ」であることを検証する。
"""

def verify_q1():
    # 市: (2023客数[万人], 2024客数, 2023消費額[億円], 2024消費額)
    data = {
        'A': (620, 682, 372, 409),
        'B': (540, 513, 297, 308),
        'C': (380, 418, 209, 230),
        'D': (760, 798, 456, 503),
        'E': (300, 342, 186, 205),
    }
    # (1) 客数の対前年増加率が最大なのはC市 → E市(14%)なので誤り
    rates = {c: (v[1] - v[0]) / v[0] for c, v in data.items()}
    s1 = max(rates, key=rates.get) == 'C'
    # (2) 2024年の1人当たり消費額が最高なのはE市 → D市なので誤り
    per = {c: v[3] / v[1] for c, v in data.items()}
    s2 = max(per, key=per.get) == 'E'
    # (3) 合計消費額は10%以上増加 → 8.88%なので誤り
    t23 = sum(v[2] for v in data.values())
    t24 = sum(v[3] for v in data.values())
    s3 = (t24 - t23) / t23 >= 0.10
    # (4) 客数・消費額とも増加した市は3つ → 4つ(A,C,D,E)なので誤り
    both = sum(1 for v in data.values() if v[1] > v[0] and v[3] > v[2])
    s4 = both == 3
    # (5) D市の客数構成比は2023年より低下 → 29.23%→28.99% 正しい
    n23 = sum(v[0] for v in data.values())
    n24 = sum(v[1] for v in data.values())
    s5 = data['D'][1] / n24 < data['D'][0] / n23

    stmts = [s1, s2, s3, s4, s5]
    print('問1 各選択肢の真偽:', stmts)
    print('  増加率:', {c: f'{r:.4f}' for c, r in rates.items()})
    print('  1人当たり消費額(万円):', {c: f'{p*10000/10000:.4f}' for c, p in per.items()})
    print(f'  合計消費額: {t23}→{t24} ({(t24-t23)/t23*100:.2f}%)')
    print(f'  両方増加した市の数: {both}')
    print(f'  D市構成比: {data["D"][0]/n23*100:.2f}% → {data["D"][1]/n24*100:.2f}%')
    assert stmts.count(True) == 1, f'正しい選択肢が{stmts.count(True)}個存在'
    assert stmts.index(True) == 4, '正解は(5)のはず'
    print('問1 OK: 正解は(5)のみ\n')


def verify_q2():
    # 部門: 2021年生産額[億円], 対前年増加率% (2022, 2023, 2024)
    base = {'食品': 2400, '化学': 1800, '金属': 1500, '機械': 3200, '繊維': 900}
    growth = {
        '食品': (5.0, -2.0, 4.0),
        '化学': (-3.0, 6.0, 2.5),
        '金属': (8.0, 2.5, -4.0),
        '機械': (2.5, 5.0, 6.0),
        '繊維': (-5.0, -2.5, 8.0),
    }
    val = {}
    for k in base:
        v = [base[k]]
        for g in growth[k]:
            v.append(v[-1] * (1 + g / 100))
        val[k] = v  # [2021, 2022, 2023, 2024]
        print(f'  {k}: ' + ' '.join(f'{x:.2f}' for x in v))

    # (1) 2024年が2021年を下回る部門は2つ → 0部門なので誤り
    below = sum(1 for k in base if val[k][3] < val[k][0])
    s1 = below == 2
    # (2) 2023年の機械は食品の1.4倍を上回る → 1.3946倍なので誤り
    ratio = val['機械'][2] / val['食品'][2]
    s2 = ratio > 1.4
    # (3) 2022年の減少額合計は増加額合計の半分以下 → 99 vs 320 正しい
    dec = sum(val[k][0] - val[k][1] for k in base if val[k][1] < val[k][0])
    inc = sum(val[k][1] - val[k][0] for k in base if val[k][1] > val[k][0])
    s3 = dec <= inc / 2
    # (4) 2021→2024の増加率最大は金属 → 機械(+14.08%)なので誤り
    tot = {k: (val[k][3] - val[k][0]) / val[k][0] for k in base}
    s4 = max(tot, key=tot.get) == '金属'
    # (5) 2024年合計に占める機械の構成比は35%超 → 34.41%なので誤り
    total24 = sum(val[k][3] for k in base)
    share = val['機械'][3] / total24
    s5 = share > 0.35

    stmts = [s1, s2, s3, s4, s5]
    print('問2 各選択肢の真偽:', stmts)
    print(f'  2021年割れ部門数: {below} (繊維2024={val["繊維"][3]:.3f})')
    print(f'  機械/食品(2023): {ratio:.4f}')
    print(f'  2022年 減少額計: {dec:.1f} / 増加額計: {inc:.1f}')
    print('  2021→2024増加率:', {k: f'{r*100:.2f}%' for k, r in tot.items()})
    print(f'  機械の2024構成比: {share*100:.2f}%')
    assert stmts.count(True) == 1, f'正しい選択肢が{stmts.count(True)}個存在'
    assert stmts.index(True) == 2, '正解は(3)のはず'
    print('問2 OK: 正解は(3)のみ')


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print('\n検証完了: 両問とも唯一解')
