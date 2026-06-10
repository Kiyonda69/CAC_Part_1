"""
航大思考201 検証スクリプト
航空資料解釈問題

問1: 機種別燃料効率比較
問2: 路線別収益効率比較
"""

def verify_q1():
    """機種別の旅客1人あたり燃料消費を計算"""
    # (機種名, 1便燃料消費kL, 座席数, 搭乗率)
    aircraft = [
        ('A型', 24, 280, 0.80),
        ('B型', 18, 220, 0.75),
        ('C型', 15, 180, 0.85),
        ('D型', 21, 240, 0.70),
        ('E型', 12, 160, 0.90),
    ]
    results = []
    for name, fuel_kL, seats, load in aircraft:
        passengers = seats * load
        # 1人あたり燃料消費（L）
        per_passenger = (fuel_kL * 1000) / passengers
        results.append((name, per_passenger))
        print(f'{name}: {per_passenger:.2f} L/人')
    results.sort(key=lambda x: x[1])
    print(f'\n最も少ない: {results[0][0]} ({results[0][1]:.2f} L/人)')
    assert results[0][0] == 'E型', f'予想と異なる: {results[0][0]}'
    return results

def verify_q2():
    """路線別の1便あたり利益と距離あたり効率を計算"""
    # (路線名, 距離km, 運航コスト万円, 座席数, 搭乗率, 平均運賃円)
    routes = [
        ('A路線',  800, 250, 200, 0.80, 22000),
        ('B路線', 1200, 350, 250, 0.75, 28000),
        ('C路線', 1500, 420, 280, 0.70, 32000),
        ('D路線',  600, 200, 180, 0.85, 18000),
        ('E路線', 1000, 300, 220, 0.78, 25000),
    ]
    results = []
    for name, dist, cost_man, seats, load, fare in routes:
        revenue = seats * load * fare
        cost = cost_man * 10000
        profit = revenue - cost
        per_km = profit / dist
        results.append((name, profit, per_km))
        print(f'{name}: 利益={profit:>10,.0f}円, 効率={per_km:>7.1f}円/km')
    results.sort(key=lambda x: -x[2])
    print(f'\n最も効率高: {results[0][0]} ({results[0][2]:.1f} 円/km)')
    # 最も高い路線を確認
    return results

if __name__ == '__main__':
    print('=== 問1: 機種別燃料効率 ===')
    r1 = verify_q1()
    print('\n=== 問2: 路線別収益効率 ===')
    r2 = verify_q2()
