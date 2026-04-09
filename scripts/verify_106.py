#!/usr/bin/env python3
"""
セット106: 資料穴埋め問題の解の一意性検証
問1: K市の通勤手段に関する住民調査報告書
問2: B市の5地区の人口動態に関する報告書
"""

def verify_q1():
    """問1: 交通手段調査の穴埋め検証"""
    print("=" * 60)
    print("問1: K市の通勤手段に関する住民調査報告書")
    print("=" * 60)
    
    # 与えられた情報
    total = 2000
    bus = 300
    car = 520
    bicycle = 360
    
    # テキストから: 鉄道は全体の34%
    railway_pct = 34.0
    railway = int(total * railway_pct / 100)
    print(f"ア（鉄道利用者数）: {total} × {railway_pct}% = {railway}人")
    
    # バスは全体の15%
    bus_pct = 15.0
    bus_calc = int(total * bus_pct / 100)
    assert bus_calc == bus, f"バス計算不一致: {bus_calc} != {bus}"
    
    # 自転車は全体の18%
    bicycle_pct = 18.0
    bicycle_calc = int(total * bicycle_pct / 100)
    assert bicycle_calc == bicycle, f"自転車計算不一致: {bicycle_calc} != {bicycle}"
    
    # 自家用車の割合
    car_pct = car / total * 100
    print(f"自家用車の割合: {car}/{total} × 100 = {car_pct}%")
    
    # 徒歩 = 残り
    walk = total - railway - bus - car - bicycle
    walk_pct = 100 - railway_pct - bus_pct - car_pct - bicycle_pct
    print(f"イ（徒歩利用者数）: {total} - {railway} - {bus} - {car} - {bicycle} = {walk}人")
    print(f"徒歩の割合: 100 - 34 - 15 - 26 - 18 = {walk_pct}%")
    
    # 徒歩の満足度 = 鉄道と同じ = 3.8
    railway_satisfaction = 3.8
    walk_satisfaction = railway_satisfaction
    print(f"ウ（徒歩の満足度）: 鉄道と同じ = {walk_satisfaction}")
    
    # 検証
    assert railway == 680, f"ア不正: {railway}"
    assert walk == 140, f"イ不正: {walk}"
    assert walk_satisfaction == 3.8, f"ウ不正: {walk_satisfaction}"
    assert railway + bus + car + bicycle + walk == total, "合計不一致"
    
    # バス(300) < 自転車(360) の確認
    assert bus < bicycle, "バスは自転車より少ないはず"
    
    print(f"\n正解: ア={railway}  イ={walk}  ウ={walk_satisfaction}")
    print("解の一意性: 確認OK")
    
    # 選択肢の確認
    choices = {
        1: (680, 140, 3.5),   # ウ: 自転車の満足度と混同
        2: (680, 140, 3.8),   # 正解
        3: (680, 160, 3.8),   # イ: 割合計算ミス(8%で計算)
        4: (660, 140, 3.8),   # ア: 33%で計算
        5: (680, 140, 2.9),   # ウ: バスの満足度と混同
    }
    
    correct_count = 0
    for num, (a, b, c) in choices.items():
        is_correct = (a == railway and b == walk and c == walk_satisfaction)
        if is_correct:
            correct_count += 1
            print(f"  選択肢({num}): ア={a} イ={b} ウ={c} ← 正解")
        else:
            print(f"  選択肢({num}): ア={a} イ={b} ウ={c}")
    
    assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
    print(f"\n正解番号: (2) — 唯一解であることを確認")


def verify_q2():
    """問2: 人口動態の穴埋め検証"""
    print("\n" + "=" * 60)
    print("問2: B市の5地区の人口動態に関する報告書")
    print("=" * 60)
    
    # 与えられた情報
    # 甲: 世帯1200, 人口3000, 高齢化率28.0%
    # 乙: 世帯900, 人口(ア), 高齢化率22.0%
    # 丙: 世帯(イ), 人口2400, 高齢化率32.0%
    # 丁: 世帯1500, 人口3600, 高齢化率(ウ)%
    # 戊: 世帯800, 人口1800, 高齢化率35.0%
    
    total_pop = 12960
    kou_household, kou_pop, kou_aging = 1200, 3000, 28.0
    otsu_household = 900
    hei_pop, hei_aging = 2400, 32.0
    tei_household, tei_pop = 1500, 3600
    bo_household, bo_pop, bo_aging = 800, 1800, 35.0
    otsu_aging = 22.0
    
    # ア: 乙の1世帯あたり人口 = 丁の1世帯あたり人口
    tei_per_household = tei_pop / tei_household
    print(f"丁の1世帯あたり人口: {tei_pop}/{tei_household} = {tei_per_household}")
    
    otsu_pop = otsu_household * tei_per_household
    print(f"ア（乙の人口）: {otsu_household} × {tei_per_household} = {otsu_pop}")
    
    # 人口合計の検証
    actual_total = kou_pop + otsu_pop + hei_pop + tei_pop + bo_pop
    print(f"人口合計検証: {kou_pop}+{otsu_pop}+{hei_pop}+{tei_pop}+{bo_pop} = {actual_total}")
    assert actual_total == total_pop, f"人口合計不一致: {actual_total} != {total_pop}"
    
    # イ: 丙の1世帯あたり人口 = 甲の1世帯あたり人口
    kou_per_household = kou_pop / kou_household
    print(f"\n甲の1世帯あたり人口: {kou_pop}/{kou_household} = {kou_per_household}")
    
    hei_household = hei_pop / kou_per_household
    print(f"イ（丙の世帯数）: {hei_pop}/{kou_per_household} = {hei_household}")
    
    # 世帯数の制約: 甲(1200) > 丙 > 戊(800)
    assert kou_household > hei_household > bo_household, \
        f"世帯数制約違反: 甲({kou_household}) > 丙({hei_household}) > 戊({bo_household})"
    print(f"世帯数制約: 甲({kou_household}) > 丙({int(hei_household)}) > 戊({bo_household}) ✓")
    
    # ウ: 高齢化率の平均 = 28.0%
    avg_aging = 28.0
    known_aging_sum = kou_aging + otsu_aging + hei_aging + bo_aging
    tei_aging = avg_aging * 5 - known_aging_sum
    print(f"\nウ（丁の高齢化率）: {avg_aging}×5 - ({kou_aging}+{otsu_aging}+{hei_aging}+{bo_aging})")
    print(f"  = {avg_aging * 5} - {known_aging_sum} = {tei_aging}%")
    
    # 検証
    all_aging = [kou_aging, otsu_aging, hei_aging, tei_aging, bo_aging]
    calc_avg = sum(all_aging) / 5
    print(f"高齢化率平均検証: {all_aging} → 平均 = {calc_avg}%")
    assert abs(calc_avg - avg_aging) < 0.001, f"平均不一致: {calc_avg}"
    
    # 最高: 戊(35.0), 最低: 乙(22.0) の確認
    assert max(all_aging) == bo_aging, "最高高齢化率は戊のはず"
    assert min(all_aging) == otsu_aging, "最低高齢化率は乙のはず"
    print(f"最高: 戊({bo_aging}%), 最低: 乙({otsu_aging}%) ✓")
    
    print(f"\n正解: ア={int(otsu_pop)}  イ={int(hei_household)}  ウ={tei_aging}")
    print("解の一意性: 確認OK")
    
    # 選択肢の確認
    choices = {
        1: (2160, 960, 25.0),   # ウ: 算術ミス
        2: (2400, 960, 23.0),   # ア: 丙の人口と混同
        3: (2160, 960, 23.0),   # 正解
        4: (2160, 1000, 23.0),  # イ: 丁の世帯あたり人口で計算
        5: (2160, 960, 21.0),   # ウ: 算術ミス(加算間違い)
    }
    
    correct_count = 0
    for num, (a, b, c) in choices.items():
        is_correct = (a == int(otsu_pop) and b == int(hei_household) and c == tei_aging)
        if is_correct:
            correct_count += 1
            print(f"  選択肢({num}): ア={a} イ={b} ウ={c} ← 正解")
        else:
            print(f"  選択肢({num}): ア={a} イ={b} ウ={c}")
    
    assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
    print(f"\n正解番号: (3) — 唯一解であることを確認")
    
    # 誤答の検証（それぞれが不正解である理由）
    print("\n【誤答の検証】")
    # (1) ウ=25.0: 平均 = (28+22+32+25+35)/5 = 142/5 = 28.4 ≠ 28.0
    avg1 = (28+22+32+25+35)/5
    print(f"  (1) ウ=25.0 → 平均={avg1} ≠ 28.0 ✗")
    
    # (2) ア=2400: 合計 = 3000+2400+2400+3600+1800 = 13200 ≠ 12960
    total2 = 3000+2400+2400+3600+1800
    print(f"  (2) ア=2400 → 合計={total2} ≠ 12960 ✗")
    
    # (4) イ=1000: 1世帯あたり = 2400/1000 = 2.4 ≠ 甲の2.5
    per4 = 2400/1000
    print(f"  (4) イ=1000 → 1世帯あたり={per4} ≠ 甲の{kou_per_household} ✗")
    
    # (5) ウ=21.0: 平均 = (28+22+32+21+35)/5 = 138/5 = 27.6 ≠ 28.0
    avg5 = (28+22+32+21+35)/5
    print(f"  (5) ウ=21.0 → 平均={avg5} ≠ 28.0 ✗")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 60)
    print("全問の解の一意性検証: 完了")
    print("=" * 60)
