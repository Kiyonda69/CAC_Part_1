#!/usr/bin/env python3
"""航大思考249 検証スクリプト
資料読取（航空テーマ・離陸性能表）

資料1: 離陸距離表（基準: 無風・水平な乾燥舗装滑走路）
  気圧高度\気温   0℃    20℃   40℃
  0 ft           500    550    600
  2,000 ft       600    650    700
  4,000 ft       700    750    800

資料2: 運航規程
  1. 表にない気温・気圧高度は直線補間
  2. 向かい風10ktにつき10%減、追い風10ktにつき20%増
  3. 草地滑走路は20%増
  4. 湿潤滑走路はさらに15%増（本問では全空港乾燥＝ダミー規則）
  5. 必要滑走路長 = 補正後離陸距離 × 1.5
"""

TABLE = {0: {0: 500, 20: 550, 40: 600},
         2000: {0: 600, 20: 650, 40: 700},
         4000: {0: 700, 20: 750, 40: 800}}
PAS = [0, 2000, 4000]
TEMPS = [0, 20, 40]


def interp1(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def base_distance(pa, temp):
    """両軸直線補間で基準離陸距離を求める"""
    pa0 = max(p for p in PAS if p <= pa)
    pa1 = min(p for p in PAS if p >= pa)
    t0 = max(t for t in TEMPS if t <= temp)
    t1 = min(t for t in TEMPS if t >= temp)
    row = {}
    for p in (pa0, pa1):
        if t0 == t1:
            row[p] = TABLE[p][t0]
        else:
            row[p] = interp1(temp, t0, t1, TABLE[p][t0], TABLE[p][t1])
    if pa0 == pa1:
        return row[pa0]
    return interp1(pa, pa0, pa1, row[pa0], row[pa1])


def corrected(pa, temp, wind_kt, wind_type, surface):
    """補正後離陸距離。wind_type: 'head'/'tail'/None, surface: 'paved'/'grass'"""
    d = base_distance(pa, temp)
    if wind_type == 'head':
        d *= (1 - 0.10 * wind_kt / 10)
    elif wind_type == 'tail':
        d *= (1 + 0.20 * wind_kt / 10)
    if surface == 'grass':
        d *= 1.20
    return d


def required(pa, temp, wind_kt, wind_type, surface):
    return corrected(pa, temp, wind_kt, wind_type, surface) * 1.5


def verify_q1():
    """問1: PA2,000ft・30℃・向かい風20kt・草地 → 必要滑走路長"""
    base = base_distance(2000, 30)
    assert base == 675, base                      # (650+700)/2
    ans = required(2000, 30, 20, 'head', 'grass')
    assert ans == 972, ans                        # 675*0.8*1.2*1.5
    # 誤答（すべて正解と異なる値で、昇順に4番目が正解）
    d_no_safety = 675 * 0.8 * 1.2                 # 安全率忘れ → 648
    d_no_grass = 675 * 0.8 * 1.5                  # 草地忘れ → 810
    d_t20 = 650 * 0.8 * 1.2 * 1.5                 # 補間せず20℃値 → 936
    d_t40 = 700 * 0.8 * 1.2 * 1.5                 # 補間せず40℃値 → 1008
    opts = sorted([d_no_safety, d_no_grass, d_t20, ans, d_t40])
    assert opts == [648, 810, 936, 972, 1008], opts
    assert opts.index(ans) == 3                   # 正解は(4)
    print("問1 OK: 必要滑走路長 972 m / 選択肢", opts, "正解(4)")


def verify_q2():
    """問2: 5空港のうち離陸できるのはC空港のみ（正解(3)）"""
    airports = {
        'A': dict(pa=0,    temp=30, wind=10, wt='tail', sfc='paved', rwy=1000),
        'B': dict(pa=2000, temp=20, wind=20, wt='head', sfc='grass', rwy=900),
        'C': dict(pa=1000, temp=10, wind=0,  wt=None,   sfc='paved', rwy=900),
        'D': dict(pa=4000, temp=0,  wind=10, wt='head', sfc='paved', rwy=900),
        'E': dict(pa=2000, temp=40, wind=20, wt='head', sfc='grass', rwy=1000),
    }
    expected_req = {'A': 1035.0, 'B': 936.0, 'C': 862.5, 'D': 945.0, 'E': 1008.0}
    ok = []
    for name, a in airports.items():
        req = required(a['pa'], a['temp'], a['wind'], a['wt'], a['sfc'])
        assert abs(req - expected_req[name]) < 1e-9, (name, req)
        if req <= a['rwy']:
            ok.append(name)
        print(f"  {name}空港: 必要 {req:.1f} m / 滑走路 {a['rwy']} m → "
              f"{'離陸可' if req <= a['rwy'] else '離陸不可'}")
    assert ok == ['C'], f"解が一意でない: {ok}"
    # 罠の検証: 補正や補間を誤ると別の空港が可に見える/正解が不可に見える
    # (1) A: 追い風補正を忘れると 575*1.5=862.5<=1000 で可に見える
    assert base_distance(0, 30) * 1.5 <= 1000
    # (2) B/E: 草地補正を忘れると可に見える
    assert 650 * 0.8 * 1.5 <= 900 and 700 * 0.8 * 1.5 <= 1000
    # (3) C: 補間せず気圧高度2,000ft・20℃のセルを使うと 975>900 で不可に見える
    assert 650 * 1.5 > 900
    # (4) D: 安全率を忘れると 630<=900 で可に見える
    assert 700 * 0.9 <= 900
    print("問2 OK: 離陸可能はC空港のみ（正解(3)・罠4種を確認）")


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("全検証 OK")
