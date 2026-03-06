"""
航大思考41 検証スクリプト
北海道乳製品輸出データ読み取り問題

問1: 2022年の生産量の前年比増加率（正解: (4) 3.5%）
問2: 輸出量1500t以上かつ比率8%未満の年の生産量平均（正解: (2) 約29500t）
"""

def verify():
    years = list(range(2014, 2023))
    export_volume = [820, 1050, 1380, 1560, 1890, 2150, 2480, 1870, 2960]
    export_ratio = [3.2, 3.8, 4.5, 5.1, 6.3, 7.2, 8.5, 6.8, 10.4]
    prods = [export_volume[i] / export_ratio[i] * 100 for i in range(len(years))]

    # 問1: 2022年の生産量の前年比増加率
    prod_2021 = export_volume[7] / export_ratio[7] * 100
    prod_2022 = export_volume[8] / export_ratio[8] * 100
    growth = (prod_2022 - prod_2021) / prod_2021 * 100

    choices_q1 = [1.5, 2.5, 3.0, 3.5, 4.5]
    closest_q1 = min(choices_q1, key=lambda x: abs(x - growth))
    assert closest_q1 == 3.5, f"問1: 最も近い選択肢が3.5%でない: {closest_q1}"

    distances_q1 = sorted([(abs(x - growth), x) for x in choices_q1])
    assert distances_q1[1][0] > 0.3, f"問1: 2番目に近い選択肢が近すぎ"
    print(f"問1: 前年比増加率 = {growth:.2f}% → 正解(4) 3.5% [OK]")

    # 問2: 輸出量1500t以上かつ比率8%未満の年の生産量平均
    matching = []
    for i in range(len(years)):
        if export_volume[i] >= 1500 and export_ratio[i] < 8.0:
            matching.append(i)

    assert len(matching) == 4, f"問2: 該当年数が4でない: {len(matching)}"
    assert [years[i] for i in matching] == [2017, 2018, 2019, 2021]

    avg_prod = sum(prods[i] for i in matching) / len(matching)
    choices_q2 = [27500, 29500, 30500, 31500, 32500]
    closest_q2 = min(choices_q2, key=lambda x: abs(x - avg_prod))
    assert closest_q2 == 29500, f"問2: 最も近い選択肢が29500でない: {closest_q2}"

    distances_q2 = sorted([(abs(x - avg_prod), x) for x in choices_q2])
    assert distances_q2[1][0] > 500, f"問2: 2番目に近い選択肢が近すぎ"
    print(f"問2: 平均生産量 = {avg_prod:.0f}t → 正解(2) 約29500t [OK]")

    print("\n検証完了: 両問題とも解は一意")


if __name__ == "__main__":
    verify()
