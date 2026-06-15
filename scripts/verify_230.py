# -*- coding: utf-8 -*-
"""
航大思考230 解の一意性検証
問1: 3店舗×3曜日 売上表の穴埋め（目標セル ア = 店舗R水曜）
問2: 4部門 売上・原価率・原価・利益表の穴埋め（全社利益率）
"""

def verify_q1():
    """問1: 表の合計制約から ア を一意に決定できるか検証"""
    # 完全な正解グリッド
    # 行: P, Q, R / 列: 月, 火, 水
    grid = {
        'P': {'月': 120, '火': 150, '水': 150},
        'Q': {'月': 110, '火': 100, '水': 140},
        'R': {'月': 90,  '火': 140, '水': 130},
    }
    days = ['月', '火', '水']
    rows = ['P', 'Q', 'R']

    # 行合計・列合計の整合性確認
    row_tot = {r: sum(grid[r][d] for d in days) for r in rows}
    col_tot = {d: sum(grid[r][d] for r in rows) for d in days}
    assert row_tot == {'P': 420, 'Q': 350, 'R': 360}, row_tot
    assert col_tot == {'月': 320, '火': 390, '水': 420}, col_tot
    grand = sum(row_tot.values())
    assert grand == sum(col_tot.values()) == 1130, grand

    # 与える情報: P水・R水を空欄、それ以外のセルと各種合計のうち必要分を提示
    # 提示: P月120 P火150 P行合計420 / Q水140 / R火140 / 水列合計420
    # ステップ1: P水 = P行合計420 - 120 - 150 = 150
    p_sui = 420 - 120 - 150
    assert p_sui == grid['P']['水'] == 150
    # ステップ2: ア(R水) = 水列合計420 - P水150 - Q水140 = 130
    a = col_tot['水'] - p_sui - grid['Q']['水']
    assert a == grid['R']['水'] == 130

    # 一意性: ア を未知数として制約を満たす整数解が一つか
    solutions = set()
    for p in range(0, 421):          # P水
        if 120 + 150 + p != 420:     # P行合計
            continue
        for x in range(0, 421):      # R水(ア)
            if 150 + 140 + p + x != 420 + 140:  # 列整合を分解した形
                pass
            # 水列合計制約
            if p + 140 + x == 420:
                solutions.add(x)
    assert solutions == {130}, solutions
    print(f"問1: ア = {a} (一意解) OK")
    return a


def verify_q2():
    """問2: 利益逆算・原価率逆算を経て全社利益率を一意に決定できるか検証"""
    # 利益 = 売上 × (1 - 原価率)
    dept = {
        'A': {'売上': 2000, '原価率': 0.60},
        'B': {'売上': 3000, '原価率': 0.55},
        'C': {'売上': 1500, '原価率': 0.80},
        'D': {'売上': 2500, '原価率': 0.72},
    }
    for d in dept:
        dept[d]['利益'] = round(dept[d]['売上'] * (1 - dept[d]['原価率']))
    assert dept['A']['利益'] == 800
    assert dept['B']['利益'] == 1350
    assert dept['C']['利益'] == 300
    assert dept['D']['利益'] == 700

    # ステップ1: B売上(ア) = 利益1350 / (1-0.55)
    b_uri = round(1350 / (1 - 0.55))
    assert b_uri == 3000
    # ステップ2: C原価率(イ) = 1 - 利益300/売上1500
    c_rate = 1 - 300 / 1500
    assert abs(c_rate - 0.80) < 1e-9
    # ステップ3: D利益 = 2500 × (1-0.72)
    d_rieki = round(2500 * (1 - 0.72))
    assert d_rieki == 700

    uri_total = sum(dept[d]['売上'] for d in dept)
    rieki_total = sum(dept[d]['利益'] for d in dept)
    assert uri_total == 9000, uri_total
    assert rieki_total == 3150, rieki_total
    ritsu = rieki_total / uri_total * 100
    assert abs(ritsu - 35.0) < 1e-9, ritsu

    # 誤答候補の確認
    avg_genka = sum(dept[d]['原価率'] for d in dept) / 4  # 単純平均原価率の罠
    trap = (1 - avg_genka) * 100
    print(f"問2: 全社利益率 = {ritsu:.1f}% (一意解) OK / 単純平均利益率の罠={trap:.2f}%")
    return ritsu


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("全検証パス")
