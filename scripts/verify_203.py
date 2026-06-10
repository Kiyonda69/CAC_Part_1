"""航大思考203 検証スクリプト
資料穴埋め問題（読解力＋計算力）
"""


def verify_q1():
    """問1: 市役所環境対策予算の穴埋め"""
    # 与件
    total = 5000
    waste_total = 2400
    waste_general = 1500
    waste_illegal = 350
    energy = 1300
    education = 600

    # (ア) 資源化推進費 = 廃棄物対策費 − 一般廃棄物処理費 − 不法投棄対策費
    a = waste_total - waste_general - waste_illegal
    # (イ) 環境調査費 = 総予算 − 廃棄物対策費 − エネルギー対策費 − 環境教育費
    b = total - waste_total - energy - education

    print(f"問1: (ア)={a}万円, (イ)={b}万円")

    options = {
        1: (450, 800),
        2: (550, 600),
        3: (650, 700),
        4: (450, 700),
        5: (550, 700),
    }

    correct = [k for k, v in options.items() if v == (a, b)]
    assert len(correct) == 1, f"正解候補が{len(correct)}個: {correct}"
    assert correct[0] == 5, f"正解は(5)であるべき: {correct[0]}"
    print(f"  → 正解: ({correct[0]})  唯一解確認")


def verify_q2():
    """問2: 食品メーカー売上報告の穴埋め"""
    # 与件
    total_sales = 30000
    domestic_ratio = 0.6
    overseas_ratio = 0.4
    profit = 4500

    # 国内
    north_jp = 4800
    kanto = 8400
    west_jp = 3600

    # 海外
    asia = 7200
    north_am = 2400

    domestic_total = total_sales * domestic_ratio
    overseas_total = total_sales * overseas_ratio

    # (ア) 関西 = 国内合計 − 北日本 − 関東 − 西日本
    a = int(domestic_total - north_jp - kanto - west_jp)
    # (イ) 欧州 = 海外合計 − アジア − 北米
    b = int(overseas_total - asia - north_am)
    # (ウ) 営業利益率 = 営業利益 / 全体売上 * 100
    c = int(profit / total_sales * 100)

    print(f"問2: (ア)={a}万円, (イ)={b}万円, (ウ)={c}%")

    options = {
        1: (1200, 2400, 15),
        2: (1200, 2400, 20),
        3: (1200, 1800, 15),
        4: (1800, 2400, 15),
        5: (1800, 1800, 20),
    }

    correct = [k for k, v in options.items() if v == (a, b, c)]
    assert len(correct) == 1, f"正解候補が{len(correct)}個: {correct}"
    assert correct[0] == 1, f"正解は(1)であるべき: {correct[0]}"
    print(f"  → 正解: ({correct[0]})  唯一解確認")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\nすべての検証に成功しました。")
