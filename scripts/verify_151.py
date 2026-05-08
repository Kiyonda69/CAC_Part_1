"""
航大思考151 解の一意性検証

問1: 観光施設の選択
条件:
  - 火曜日に訪問可能（火曜が休館日でないこと）
  - 大人2名の入場料合計が2,500円以内
  - 駐車場無料
  - 年間来場者数20万人以上

問2: 通信講座の選択
条件:
  - 教材費込みの総額50,000円以下
  - 認定証が発行される
  - 修了率80%以上
  - 満足度4.5以上
"""


def verify_q1():
    facilities = [
        # (番号, 施設名, 休館日, 入場料(大人), 駐車場無料, 年間来場者千人)
        (1, "A", "月", 1500, False, 250),
        (2, "B", "火", 1200, True,  180),
        (3, "C", "水", 2000, True,  320),
        (4, "D", "木", 1200, True,  280),
        (5, "E", "なし", 1000, False, 150),
    ]
    valid = []
    for num, name, holiday, fee, free_park, visitors in facilities:
        if holiday == "火":
            continue
        if fee * 2 > 2500:
            continue
        if not free_park:
            continue
        if visitors < 200:
            continue
        valid.append((num, name))
    print(f"問1 該当施設: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    return valid[0]


def verify_q2():
    courses = [
        # (番号, 講座, 受講料, 教材費, 認定証, 修了率, 満足度)
        (1, "P", 36000, 0,    True,  88, 4.5),
        (2, "Q", 60000, 0,    True,  85, 4.6),
        (3, "R", 24000, 0,    False, 90, 4.4),
        (4, "S", 30000, 5000, True,  76, 4.3),
        (5, "T", 48000, 0,    True,  92, 4.4),
    ]
    valid = []
    for num, name, fee, mat, cert, comp, sat in courses:
        if fee + mat > 50000:
            continue
        if not cert:
            continue
        if comp < 80:
            continue
        if sat < 4.5:
            continue
        valid.append((num, name))
    print(f"問2 該当講座: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    return valid[0]


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    print(f"\n問1正解: ({q1[0]}) {q1[1]}")
    print(f"問2正解: ({q2[0]}) {q2[1]}")
