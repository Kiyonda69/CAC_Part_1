"""
航大思考184 - 資料読み取り問題の解の一意性検証

問1: 売上データから3条件を満たす商品を特定
問2: 部署別評価データから4条件を満たす部署を特定
"""


def verify_q1():
    """問1: 売上データ分析（標準難度）"""
    # 商品データ: { 商品名: [10月, 11月, 12月] }
    sales = {
        'A': [200, 180, 160],
        'B': [110, 140, 130],
        'C': [130, 150, 170],
        'D': [145, 135, 195],
        'E': [160, 170, 165],
    }

    # 条件:
    # 1. 3ヶ月の合計売上が400以上
    # 2. 12月の売上が前月（11月）より増加している
    # 3. 3ヶ月の中で最高売上月と最低売上月の差が50以下
    valid = []
    for name, data in sales.items():
        oct_, nov, dec = data
        total = oct_ + nov + dec
        cond1 = total >= 400
        cond2 = dec > nov
        cond3 = (max(data) - min(data)) <= 50
        print(f"  {name}: 合計={total}, 12月>{nov}={cond2}, 差={max(data)-min(data)}, "
              f"条件1={cond1}, 条件2={cond2}, 条件3={cond3}")
        if cond1 and cond2 and cond3:
            valid.append(name)

    print(f"\n問1 該当商品: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    return valid[0]


def verify_q2():
    """問2: 部署別総合評価分析（高難度）"""
    # 部署データ: { 部署名: [売上, 満足度, 効率, 革新性, コスト] }
    depts = {
        '営業': [70, 80, 75, 95, 70],
        '開発': [90, 75, 85, 70, 60],
        '企画': [80, 85, 70, 80, 75],
        '総務': [65, 90, 65, 60, 95],
        '人事': [85, 70, 80, 65, 80],
    }

    # 条件:
    # 1. 5指標の平均が75点以上
    # 2. 最高点と最低点の差が25以上
    # 3. 4つ以上の指標で70点以上を獲得
    # 4. 革新性が80点以上、または、コスト管理が80点以上
    valid = []
    for name, scores in depts.items():
        avg = sum(scores) / len(scores)
        diff = max(scores) - min(scores)
        above70 = sum(1 for s in scores if s >= 70)
        innovation, cost = scores[3], scores[4]
        cond1 = avg >= 75
        cond2 = diff >= 25
        cond3 = above70 >= 4
        cond4 = innovation >= 80 or cost >= 80
        print(f"  {name}: 平均={avg}, 差={diff}, 70以上={above70}つ, "
              f"革新性={innovation}, コスト={cost}, "
              f"条件1={cond1}, 条件2={cond2}, 条件3={cond3}, 条件4={cond4}")
        if cond1 and cond2 and cond3 and cond4:
            valid.append(name)

    print(f"\n問2 該当部署: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    return valid[0]


if __name__ == '__main__':
    print("===== 問1検証 =====")
    ans1 = verify_q1()
    print(f"\n問1正解: {ans1}\n")

    print("===== 問2検証 =====")
    ans2 = verify_q2()
    print(f"\n問2正解: {ans2}")
