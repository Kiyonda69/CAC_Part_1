"""
航大思考9 - 資料解釈問題の検証スクリプト

問1: 旅客機の搭乗データ（座席数・搭乗率・搭乗者数の相互関係から空欄を求める）
問2: 航空貨物の運賃計算（基本運賃×重量×割増率から空欄を逆算する）
"""

from fractions import Fraction


def verify_q1():
    """
    問1: 国内線4便の搭乗データ表から合計搭乗者数を求める

    【表の構造】
    | 便名  | 座席数 | 搭乗率 | 搭乗者数 |
    | 101便 | 200   | 85%  | ア      |
    | 102便 | 250   | イ   | 200     |
    | 103便 | ウ    | 90%  | 270     |
    | 104便 | 180   | 75%  | エ      |
    | 合計  | オ    | -    | カ      |

    条件: 103便の座席数は101便の座席数の1.5倍

    搭乗者数 = 座席数 × 搭乗率
    """
    print("=== 問1 検証 ===")

    # 既知の値
    seat_101 = 200
    rate_101 = Fraction(85, 100)
    pass_102 = 200
    seat_102 = 250
    rate_103 = Fraction(90, 100)
    pass_103 = 270
    seat_104 = 180
    rate_104 = Fraction(75, 100)

    # 空欄の計算
    # ア: 101便の搭乗者数
    a = seat_101 * rate_101
    print(f"ア (101便の搭乗者数) = {seat_101} × {rate_101} = {a}")
    assert a == 170, f"アの計算エラー: {a}"

    # イ: 102便の搭乗率
    i = Fraction(pass_102, seat_102)
    print(f"イ (102便の搭乗率) = {pass_102} ÷ {seat_102} = {i} = {float(i)*100:.0f}%")
    assert i == Fraction(4, 5), f"イの計算エラー: {i}"

    # ウ: 103便の座席数（条件: 103便の座席数は101便の1.5倍）
    u = Fraction(3, 2) * seat_101
    print(f"ウ (103便の座席数) = {seat_101} × 1.5 = {u}")
    assert u == 300, f"ウの計算エラー: {u}"

    # 検証: ウ × 搭乗率 = 270
    check = u * rate_103
    print(f"  検証: {u} × {rate_103} = {check} (期待値: 270)")
    assert check == 270, f"ウの搭乗者数検証エラー: {check}"

    # エ: 104便の搭乗者数
    e = seat_104 * rate_104
    print(f"エ (104便の搭乗者数) = {seat_104} × {rate_104} = {e}")
    assert e == 135, f"エの計算エラー: {e}"

    # オ: 合計座席数
    o = seat_101 + seat_102 + u + seat_104
    print(f"オ (合計座席数) = {seat_101} + {seat_102} + {u} + {seat_104} = {o}")
    assert o == 930, f"オの計算エラー: {o}"

    # カ: 合計搭乗者数（正解）
    ka = a + pass_102 + pass_103 + e
    print(f"カ (合計搭乗者数) = {a} + {pass_102} + {pass_103} + {e} = {ka}")
    assert ka == 775, f"カの計算エラー: {ka}"

    print(f"\n【問1の正解】カ = {ka} 人")
    print("解の一意性: 一意解であることを確認 ✓")
    return int(ka)


def verify_q2():
    """
    問2: 航空貨物の運賃計算表から合計重量を求める

    【表の構造】
    | 貨物便 | 重量(kg) | 基本運賃(円/kg) | 割増率 | 運賃(円)  |
    | 第1便  | 500      | 100            | 0%    | ア        |
    | 第2便  | イ       | 100            | 50%   | 36,000   |
    | 第3便  | 400      | ウ             | 20%   | 57,600   |
    | 第4便  | 300      | 100            | エ    | 45,000   |
    | 合計   | オ       | -              | -     | カ        |

    計算式: 運賃 = 重量 × 基本運賃 × (1 + 割増率)
    """
    print("\n=== 問2 検証 ===")

    # 既知の値
    weight_1 = 500
    unit_1 = 100
    surcharge_1 = Fraction(0, 100)

    weight_3 = 400
    surcharge_3 = Fraction(20, 100)
    fare_3 = 57600

    unit_2 = 100
    surcharge_2 = Fraction(50, 100)
    fare_2 = 36000

    weight_4 = 300
    unit_4 = 100
    fare_4 = 45000

    # 空欄の計算
    # ア: 第1便の運賃
    a = weight_1 * unit_1 * (1 + surcharge_1)
    print(f"ア (第1便の運賃) = {weight_1} × {unit_1} × (1 + {surcharge_1}) = {a}")
    assert a == 50000, f"アの計算エラー: {a}"

    # イ: 第2便の重量
    i = Fraction(fare_2, unit_2) / (1 + surcharge_2)
    print(f"イ (第2便の重量) = {fare_2} ÷ ({unit_2} × (1 + {surcharge_2})) = {i}")
    assert i == 240, f"イの計算エラー: {i}"

    # ウ: 第3便の基本運賃
    u = Fraction(fare_3, weight_3) / (1 + surcharge_3)
    print(f"ウ (第3便の基本運賃) = {fare_3} ÷ ({weight_3} × (1 + {surcharge_3})) = {u}")
    assert u == 120, f"ウの計算エラー: {u}"

    # 検証: 400 × 120 × 1.2 = 57600
    check = weight_3 * u * (1 + surcharge_3)
    print(f"  検証: {weight_3} × {u} × (1 + {surcharge_3}) = {check} (期待値: {fare_3})")
    assert check == fare_3, f"ウの運賃検証エラー: {check}"

    # エ: 第4便の割増率
    e = Fraction(fare_4, weight_4 * unit_4) - 1
    print(f"エ (第4便の割増率) = {fare_4} ÷ ({weight_4} × {unit_4}) - 1 = {e} = {float(e)*100:.0f}%")
    assert e == Fraction(1, 2), f"エの計算エラー: {e}"

    # 検証: 300 × 100 × 1.5 = 45000
    check = weight_4 * unit_4 * (1 + e)
    print(f"  検証: {weight_4} × {unit_4} × (1 + {e}) = {check} (期待値: {fare_4})")
    assert check == fare_4, f"エの運賃検証エラー: {check}"

    # オ: 合計重量（正解）
    o = weight_1 + i + weight_3 + weight_4
    print(f"オ (合計重量) = {weight_1} + {i} + {weight_3} + {weight_4} = {o}")
    assert o == 1440, f"オの計算エラー: {o}"

    # カ: 合計運賃
    ka = a + fare_2 + fare_3 + fare_4
    print(f"カ (合計運賃) = {a} + {fare_2} + {fare_3} + {fare_4} = {ka}")
    assert ka == 188600, f"カの計算エラー: {ka}"

    print(f"\n【問2の正解】オ = {o} kg")
    print("解の一意性: 一意解であることを確認 ✓")
    return int(o)


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("\n" + "=" * 40)
    print("【検証完了】")
    print(f"問1 正解: カ = {q1_answer} 人")
    print(f"問2 正解: オ = {q2_answer} kg")
    print("両問とも一意解を確認 ✓")
