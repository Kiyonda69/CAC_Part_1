"""
verify_43.py - 航大思考43の解の一意性検証

問1（標準）: 鋼材の地域別入荷量・消費量・在庫量データ
  - 前月の在庫量 = 今月の在庫量 - 今月の入荷量 + 今月の消費量
  - 2月の関東と中部の在庫量の差を求める

問2（高難度）: 主要品目別貿易額データ
  - 前年値 = 当年値 - 対前年差
  - 前年に貿易黒字（輸出額＞輸入額）であった品目を特定
  - それらの前年の貿易黒字額の合計を求める
"""


def verify_q1():
    """問1: 鋼材データの検証"""
    print("=" * 60)
    print("問1: 鋼材の地域別入荷量・消費量・在庫量")
    print("=" * 60)

    # 3月のデータ（千トン）
    # 形式: (地域, 入荷量当月値, 入荷量対前月差, 消費量当月値, 消費量対前月差, 在庫量当月値)
    data = {
        "全国":   (856, 63, 812, -18, 1425),
        "北海道": (38, 2, 35, -1, 72),
        "関東":   (285, 25, 264, -7, 498),
        "中部":   (196, 14, 188, -3, 312),
        "近畿":   (152, -5, 148, 2, 205),
        "中国":   (108, 18, 96, -6, 187),
        "九州":   (77, 9, 81, -3, 151),
    }

    # 注: 今月の在庫量 = 前月の在庫量 + 今月の入荷量 - 今月の消費量
    # 前月の在庫量 = 今月の在庫量 - 今月の入荷量 + 今月の消費量

    print("\n各地域の2月（前月）在庫量:")
    prev_stock = {}
    for region, (incoming, inc_diff, consume, con_diff, stock) in data.items():
        prev = stock - incoming + consume
        prev_stock[region] = prev
        print(f"  {region}: {stock} - {incoming} + {consume} = {prev} 千トン")

    kanto_prev = prev_stock["関東"]
    chubu_prev = prev_stock["中部"]
    diff = kanto_prev - chubu_prev

    print(f"\n関東の2月在庫量: {kanto_prev} 千トン")
    print(f"中部の2月在庫量: {chubu_prev} 千トン")
    print(f"差: {kanto_prev} - {chubu_prev} = {diff} 千トン")

    # 全国の整合性チェック
    total_incoming = sum(v[0] for k, v in data.items() if k != "全国")
    total_consume = sum(v[2] for k, v in data.items() if k != "全国")
    total_stock = sum(v[4] for k, v in data.items() if k != "全国")
    print(f"\n【整合性チェック】")
    print(f"  入荷量合計: {total_incoming} (全国値: {data['全国'][0]})")
    print(f"  消費量合計: {total_consume} (全国値: {data['全国'][2]})")
    print(f"  在庫量合計: {total_stock} (全国値: {data['全国'][4]})")

    # 正解は173千トン → 選択肢(4)に配置
    assert diff == 173, f"差が{diff}千トン（期待値: 173）"

    # 選択肢の配置（正解は(4)）
    choices = [161, 167, 170, 173, 179]
    print(f"\n選択肢: {['({}) {}千トン'.format(i+1, c) for i, c in enumerate(choices)]}")
    print(f"正解: (4) 173千トン")

    return diff


def verify_q2():
    """問2: 貿易データの検証"""
    print("\n" + "=" * 60)
    print("問2: 主要品目別貿易額")
    print("=" * 60)

    # 令和7年のデータ（億ドル）
    # 形式: (品目, 輸出額, 輸出対前年差, 輸入額, 輸入対前年差)
    data = {
        "自動車":   (1350, 90, 340, 25),
        "電子部品": (920, -55, 1080, 45),
        "化学製品": (780, 130, 710, -20),
        "一般機械": (1150, 60, 880, 75),
        "食料品":   (95, -12, 750, 110),
    }

    # 前年値 = 当年値 - 対前年差
    print("\n前年（令和6年）の貿易データ:")
    prev_data = {}
    for item, (exp, exp_diff, imp, imp_diff) in data.items():
        prev_exp = exp - exp_diff
        prev_imp = imp - imp_diff
        balance = prev_exp - prev_imp
        surplus = balance > 0
        prev_data[item] = (prev_exp, prev_imp, balance, surplus)
        status = "黒字" if surplus else "赤字"
        print(f"  {item}: 輸出{prev_exp} - 輸入{prev_imp} = {balance}億ドル ({status})")

    # 黒字品目の特定
    surplus_items = {k: v for k, v in prev_data.items() if v[3]}
    print(f"\n前年に貿易黒字の品目: {list(surplus_items.keys())}")

    # 黒字額の合計
    total_surplus = sum(v[2] for v in surplus_items.values())
    print(f"\n黒字額の合計:")
    for item, (prev_exp, prev_imp, balance, _) in surplus_items.items():
        print(f"  {item}: {balance}億ドル")
    print(f"  合計: {total_surplus}億ドル")

    # 正解は1230億ドル → 選択肢(3)に配置
    assert total_surplus == 1230, f"合計が{total_surplus}億ドル（期待値: 1230）"

    # 選択肢の配置（正解は(3)）
    choices = [1170, 1200, 1230, 1260, 1290]
    print(f"\n選択肢: {['({}) {}億ドル'.format(i+1, c) for i, c in enumerate(choices)]}")
    print(f"正解: (3) 1230億ドル")

    return total_surplus


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()
    print("\n" + "=" * 60)
    print("検証完了")
    print(f"  問1正解: 173千トン → 選択肢(4)")
    print(f"  問2正解: 1230億ドル → 選択肢(3)")
    print("=" * 60)
