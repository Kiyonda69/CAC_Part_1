"""
航大思考211 検証スクリプト

問1: テーマパークのアトラクション利用者数表から条件を満たすものを特定
問2: 部署別売上グラフと経費表から条件を満たす部署を特定
"""


def verify_q1():
    """問1: 5つのアトラクション(A-E)の利用者数表"""
    # データ: 平日午前, 平日午後, 休日午前, 休日午後, 待ち時間(4時間帯)
    data = {
        "A": {"users": [180, 240, 320, 400], "wait": [25, 35, 50, 70]},
        "B": {"users": [300, 250, 250, 350], "wait": [15, 20, 30, 35]},
        "C": {"users": [150, 180, 280, 300], "wait": [10, 15, 25, 30]},
        "D": {"users": [220, 300, 290, 280], "wait": [20, 30, 40, 45]},
        "E": {"users": [280, 270, 180, 350], "wait": [30, 40, 60, 50]},
    }

    valid = []
    for name, d in data.items():
        u = d["users"]
        w = d["wait"]
        weekday_sum = u[0] + u[1]
        weekend_sum = u[2] + u[3]
        avg_wait = sum(w) / 4
        # 条件1: 平日合計 >= 500
        # 条件2: 休日午後 > 休日午前
        # 条件3: 平均待ち時間 <= 30
        # 条件4: 休日合計 > 平日合計
        c1 = weekday_sum >= 500
        c2 = u[3] > u[2]
        c3 = avg_wait <= 30
        c4 = weekend_sum > weekday_sum
        print(f"  {name}: 平日={weekday_sum}({c1}) 休日午後>午前({c2}) 平均待ち={avg_wait}({c3}) 休日>平日({c4})")
        if c1 and c2 and c3 and c4:
            valid.append(name)

    print(f"問1 valid: {valid}")
    assert len(valid) == 1, f"問1の解が{len(valid)}個存在: {valid}"
    return valid[0]


def verify_q2():
    """問2: 5部署の四半期売上(棒グラフ) + 経費表"""
    # 売上(百万円): Q1, Q2, Q3, Q4
    sales = {
        "営業1課": [80, 100, 120, 140],
        "営業2課": [110, 90, 100, 130],
        "企画課": [60, 70, 80, 90],
        "開発課": [50, 60, 70, 120],
        "管理課": [40, 50, 60, 50],
    }
    expense = {
        "営業1課": 300,
        "営業2課": 350,
        "企画課": 240,
        "開発課": 280,
        "管理課": 180,
    }

    valid = []
    for name, s in sales.items():
        total = sum(s)
        e = expense[name]
        profit = total - e
        rate = profit / total * 100 if total > 0 else 0
        # 条件1: 年間売上 >= 400
        # 条件2: Q4 >= Q1 * 1.5
        # 条件3: 利益率 >= 20%
        # 条件4: 売上単調増加 Q1<Q2<Q3<Q4
        c1 = total >= 400
        c2 = s[3] >= s[0] * 1.5
        c3 = rate >= 20
        c4 = s[0] < s[1] < s[2] < s[3]
        print(f"  {name}: 売上計={total}({c1}) Q4/Q1={s[3]/s[0]:.2f}({c2}) 利益率={rate:.1f}%({c3}) 単調増({c4})")
        if c1 and c2 and c3 and c4:
            valid.append(name)

    print(f"問2 valid: {valid}")
    assert len(valid) == 1, f"問2の解が{len(valid)}個存在: {valid}"
    return valid[0]


if __name__ == "__main__":
    print("=== 問1 検証 ===")
    ans1 = verify_q1()
    print(f"問1 正解: {ans1}\n")

    print("=== 問2 検証 ===")
    ans2 = verify_q2()
    print(f"問2 正解: {ans2}")
