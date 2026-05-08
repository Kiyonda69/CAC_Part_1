"""
航大思考153 解の一意性検証
- 問1: 5カフェの文章情報＋営業時間表から4条件を満たす店舗を特定
- 問2: 5医療保険プランの文章情報＋料金/保障表から5条件を満たすプランを特定
"""


def verify_q1():
    """問1: カフェ選定問題（標準難度）

    条件:
      C1: 終日Wi-Fi利用可能
      C2: 22時以降も営業
      C3: 個室席またはブース席あり
      C4: ランチタイム以外でも食事メニューあり
    """
    cafes = {
        "A": {"wifi_all_day": True,  "close_hour": 24, "private_or_booth": True,  "food_anytime": True},
        "B": {"wifi_all_day": True,  "close_hour": 20, "private_or_booth": True,  "food_anytime": True},
        "C": {"wifi_all_day": False, "close_hour": 24, "private_or_booth": True,  "food_anytime": True},
        "D": {"wifi_all_day": True,  "close_hour": 23, "private_or_booth": False, "food_anytime": True},
        "E": {"wifi_all_day": True,  "close_hour": 24, "private_or_booth": True,  "food_anytime": False},
    }

    valid = []
    for name, c in cafes.items():
        if (c["wifi_all_day"]
            and c["close_hour"] >= 22
            and c["private_or_booth"]
            and c["food_anytime"]):
            valid.append(name)

    print("問1 適合店舗:", valid)
    assert len(valid) == 1, f"問1: 解が{len(valid)}個存在"
    return valid[0]


def verify_q2():
    """問2: 医療保険プラン選定問題（高難度）

    被保険者: 45歳
    条件:
      C1: 月額保険料 ≦ 3,500円
      C2: 入院日額 ≧ 5,000円
      C3: 通院給付金（1日あたり） ≧ 2,500円
      C4: がん診断一時金 ≧ 100万円
      C5: 先進医療特約あり
    """
    plans = {
        "P": {"monthly": 3800, "hospital": 5000, "outpatient": 2500, "cancer": 100, "advanced": True},
        "Q": {"monthly": 3200, "hospital": 5000, "outpatient": 3000, "cancer": 100, "advanced": True},
        "R": {"monthly": 2800, "hospital": 4000, "outpatient": 3000, "cancer": 100, "advanced": True},
        "S": {"monthly": 3500, "hospital": 6000, "outpatient": 2000, "cancer": 100, "advanced": True},
        "T": {"monthly": 3500, "hospital": 5000, "outpatient": 2500, "cancer": 80,  "advanced": True},
    }

    valid = []
    for name, p in plans.items():
        if (p["monthly"] <= 3500
            and p["hospital"] >= 5000
            and p["outpatient"] >= 2500
            and p["cancer"] >= 100
            and p["advanced"]):
            valid.append(name)

    print("問2 適合プラン:", valid)
    assert len(valid) == 1, f"問2: 解が{len(valid)}個存在"
    return valid[0]


if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"\n問1 正解: {a1} (選択肢(1)=A)")
    print(f"問2 正解: {a2} (選択肢(2)=Q)")
