"""
航大思考208 解の一意性検証スクリプト
問1: 商品データ表から条件を満たす商品の6月販売数合計を求める
問2: 支店業績データから条件を満たす唯一の支店を選ぶ
"""


def verify_q1():
    """問1: 8商品の販売データから条件を満たす商品の6月販売数合計"""
    # 商品データ: (コード, カテゴリ, 単価, 4月, 5月, 6月, 評価, 在庫)
    products = [
        ("P-101", "食品", 850, 320, 380, 410, 4.2, 50),
        ("P-102", "雑貨", 1200, 180, 210, 245, 3.8, 120),
        ("P-103", "電子", 3500, 95, 145, 200, 4.5, 25),
        ("P-104", "家電", 2800, 145, 160, 175, 4.0, 80),
        ("P-105", "食品", 950, 280, 295, 325, 4.3, 60),
        ("P-106", "電子", 4200, 75, 85, 95, 4.6, 30),
        ("P-107", "雑貨", 1500, 200, 220, 250, 4.1, 90),
        ("P-108", "家電", 3200, 130, 150, 165, 4.4, 55),
    ]

    # 条件:
    # 1. 単価が1500円以上
    # 2. 4-6月の合計販売数が400個以上
    # 3. 6月販売数が4月販売数の1.2倍以上
    # 4. 評価が4.3以上
    matched = []
    for p in products:
        code, cat, price, m4, m5, m6, rate, stock = p
        c1 = price >= 1500
        c2 = (m4 + m5 + m6) >= 400
        c3 = m6 >= m4 * 1.2
        c4 = rate >= 4.3
        if c1 and c2 and c3 and c4:
            matched.append(p)

    print(f"問1: 該当商品 = {[p[0] for p in matched]}")
    total_june = sum(p[5] for p in matched)
    print(f"問1: 該当商品の6月販売数合計 = {total_june}")
    return total_june, matched


def verify_q2():
    """問2: 5支店の業績データから条件を満たす唯一の支店"""
    # 店舗A-Eの順序で並べ、店舗C(=3番目)が正解になるよう調整
    # (名前, 売上万円, 経費万円, 社員数, 顧客数, 平均評価, 前年比成長率%)
    branches = [
        ("店舗A", 8500, 6800, 12, 4200, 4.1, 4),   # 成長4% で NG
        ("店舗B", 12000, 9200, 18, 5800, 3.9, 12), # 評価3.9 NG
        ("店舗C", 11000, 8700, 16, 5200, 4.0, 6),  # ★全条件OK → 選択肢(3)
        ("店舗D", 9800, 7500, 14, 4800, 4.3, 3),   # 成長3% NG
        ("店舗E", 7200, 5900, 10, 3600, 4.4, 10),  # 利益1300 NG
    ]

    # 条件:
    # 1. 利益（売上-経費）が1500万円以上
    # 2. 社員あたり顧客数が300人以上
    # 3. 平均評価が4.0以上
    # 4. 前年比成長率が5%以上
    matched = []
    for b in branches:
        name, sales, cost, staff, cust, rate, growth = b
        c1 = (sales - cost) >= 1500
        c2 = (cust / staff) >= 300
        c3 = rate >= 4.0
        c4 = growth >= 5
        if c1 and c2 and c3 and c4:
            matched.append(b)

    print(f"問2: 該当支店 = {[b[0] for b in matched]}")
    assert len(matched) == 1, f"問2の解が{len(matched)}個存在"

    # 正解が選択肢(3)の位置にあることを確認
    correct_idx = branches.index(matched[0]) + 1
    print(f"問2: 正解の選択肢番号 = ({correct_idx})")

    # 全支店の指標一覧（参考用）
    print("\n全支店の指標:")
    for b in branches:
        name, sales, cost, staff, cust, rate, growth = b
        print(f"  {name}: 利益={sales-cost}, 顧客/社員={cust/staff:.1f}, "
              f"評価={rate}, 成長={growth}%")
    return matched[0], correct_idx


if __name__ == "__main__":
    print("=" * 50)
    print("問1 検証")
    print("=" * 50)
    total, m1 = verify_q1()
    print(f"\n該当商品詳細:")
    for p in m1:
        print(f"  {p[0]}: カテゴリ={p[1]}, 単価={p[2]}, 4-6月合計={p[3]+p[4]+p[5]}, "
              f"6月/4月={p[5]/p[3]:.2f}, 評価={p[6]}, 6月={p[5]}")

    print("\n" + "=" * 50)
    print("問2 検証")
    print("=" * 50)
    branch, idx = verify_q2()
    assert idx == 3, f"問2正解番号が3ではない: {idx}"
    print("\n両問とも検証成功！")
