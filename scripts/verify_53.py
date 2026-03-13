#!/usr/bin/env python3
"""
航大思考53 検証スクリプト
問1: 日本酒の輸出量・輸出比率から生産量の前年比増加率を求める
問2: 4つの記述の正誤を判定し正しい組み合わせを選ぶ
"""

def verify_q1():
    """問1: 2022年の生産量の前年比増加率"""
    # データ: (年, 輸出量kL, 輸出比率%)
    data = [
        (2014, 800, 3.2),
        (2015, 1100, 4.0),
        (2016, 1350, 4.5),
        (2017, 1500, 5.0),
        (2018, 1920, 6.0),
        (2019, 2380, 7.0),
        (2020, 1680, 6.0),
        (2021, 2560, 8.0),
        (2022, 3240, 9.0),
    ]
    
    # 生産量 = 輸出量 / (輸出比率/100)
    productions = {}
    for year, export, ratio in data:
        prod = export / (ratio / 100)
        productions[year] = prod
        print(f"  {year}年: 輸出量{export}kL, 比率{ratio}%, 生産量={prod:.0f}kL")
    
    # 2022年の前年比増加率
    growth = (productions[2022] - productions[2021]) / productions[2021] * 100
    print(f"\n  2022年前年比増加率: ({productions[2022]:.0f} - {productions[2021]:.0f}) / {productions[2021]:.0f} * 100 = {growth:.1f}%")
    
    # 選択肢
    choices = {1: 12.5, 2: 15.0, 3: 18.4, 4: 22.5, 5: 26.6}
    correct = None
    for k, v in choices.items():
        if abs(v - growth) < 0.5:
            correct = k
    
    print(f"  正解: ({correct}) {choices[correct]}%")
    assert correct == 1, f"正解が(1)でない: ({correct})"
    return True

def verify_q2():
    """問2: 4つの記述の正誤判定"""
    data = [
        (2014, 800, 3.2),
        (2015, 1100, 4.0),
        (2016, 1350, 4.5),
        (2017, 1500, 5.0),
        (2018, 1920, 6.0),
        (2019, 2380, 7.0),
        (2020, 1680, 6.0),
        (2021, 2560, 8.0),
        (2022, 3240, 9.0),
    ]
    
    productions = {}
    for year, export, ratio in data:
        productions[year] = export / (ratio / 100)
    
    # ア. 2017年と2018年の生産量の差は3000kL以上である
    diff_17_18 = productions[2018] - productions[2017]
    a_result = diff_17_18 >= 3000
    print(f"  ア. 2017-2018差 = {diff_17_18:.0f}kL >= 3000? -> {a_result}")
    
    # イ. 2020年の生産量は2016年の生産量より少ない
    b_result = productions[2020] < productions[2016]
    print(f"  イ. 2020年({productions[2020]:.0f}) < 2016年({productions[2016]:.0f})? -> {b_result}")
    
    # ウ. 期間中で生産量が最も大きい年は2022年である
    max_year = max(productions, key=productions.get)
    c_result = max_year == 2022
    print(f"  ウ. 最大生産年 = {max_year}年({productions[max_year]:.0f}kL) -> 2022年? {c_result}")
    
    # エ. 輸出量の前年比増加率が最も大きい年は2022年である
    export_growth = {}
    for i in range(1, len(data)):
        year = data[i][0]
        prev_export = data[i-1][1]
        curr_export = data[i][1]
        rate = (curr_export - prev_export) / prev_export * 100
        export_growth[year] = rate
        print(f"    輸出量増加率 {year}年: {rate:.1f}%")
    
    max_growth_year = max(export_growth, key=export_growth.get)
    d_result = max_growth_year == 2022
    print(f"  エ. 輸出量増加率最大年 = {max_growth_year}年({export_growth[max_growth_year]:.1f}%) -> 2022年? {d_result}")
    
    print(f"\n  結果: ア={a_result}, イ={b_result}, ウ={c_result}, エ={d_result}")
    
    # 正しいのはイとウ → 選択肢(2)
    assert not a_result, "ア should be FALSE"
    assert b_result, "イ should be TRUE"
    assert c_result, "ウ should be TRUE"
    assert not d_result, "エ should be FALSE"
    
    # 選択肢の組み合わせ
    print("  正しい組み合わせ: イ、ウ → 正解: (2)")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("航大思考53 検証")
    print("=" * 60)
    
    print("\n【問1】2022年の生産量の前年比増加率")
    assert verify_q1()
    print("  -> 問1 検証OK")
    
    print("\n【問2】4つの記述の正誤判定")
    assert verify_q2()
    print("  -> 問2 検証OK")
    
    print("\n" + "=" * 60)
    print("全検証完了: 解は一意")
    print("=" * 60)
