"""
問題セット10 解の一意性検証
問1: 航空機部品の年間調達コスト管理データ（保管費用率を発見して(ア)を求める）
問2: パイロット訓練コスト管理データ（教官単価・機体使用単価・消耗品費率を発見して(ア)を求める）
"""

def verify_q1():
    """問1: 部品調達コストデータの検証"""
    print("=" * 60)
    print("問1: 航空機部品の年間調達コスト管理データ")
    print("=" * 60)

    # データ: (部品名, 年間発注回数, 1回の発注数量, 単価(円), 保管費用(万円), 総コスト(万円))
    parts = [
        ('A', 12, 100, 5000, 90,  690),
        ('B',  6, 200, 8000, 144, 1104),
        ('C',  4, 300, 6000, 108,  828),
    ]

    print("\n【既知データの検証】")
    rates = []
    for name, orders, qty, unit_price, storage_fee, total_cost in parts:
        annual_qty = orders * qty
        procurement = annual_qty * unit_price / 10000  # 万円
        rate = storage_fee / procurement
        calc_total = procurement + storage_fee
        rates.append(rate)
        print(f"部品{name}: 年間調達量={annual_qty:,}個, 調達費={procurement:.0f}万円, "
              f"保管費率={rate*100:.1f}%, 総コスト={calc_total:.0f}万円 (表={total_cost}万円)")
        assert abs(calc_total - total_cost) < 0.01, f"部品{name}の総コストが一致しない"

    # 保管費率の一意性確認
    assert all(abs(r - rates[0]) < 1e-9 for r in rates), "保管費率が一定でない"
    storage_rate = rates[0]
    print(f"\n→ 保管費用率 = {storage_rate*100:.0f}% (全部品で一定)")

    # 部品D（問の対象）
    orders_D, qty_D, unit_price_D = 3, 500, 4000
    annual_qty_D = orders_D * qty_D
    procurement_D = annual_qty_D * unit_price_D / 10000
    storage_D = procurement_D * storage_rate

    print(f"\n【部品D（問の対象）】")
    print(f"年間調達量 = {orders_D} × {qty_D} = {annual_qty_D:,}個")
    print(f"調達費用 = {annual_qty_D:,} × {unit_price_D:,}円 ÷ 10,000 = {procurement_D:.0f}万円")
    print(f"保管費用（ア）= {procurement_D:.0f} × {storage_rate*100:.0f}% = {storage_D:.0f}万円")
    print(f"\n→ 正解: （ア）= {storage_D:.0f}万円")

    # 解の一意性を確認（他の保管費率では成立しない）
    print("\n【解の一意性確認】")
    valid_rates = []
    for r_test in [i/100 for i in range(5, 30)]:
        ok = all(
            abs(parts[i][4] - (parts[i][1]*parts[i][2]*parts[i][3]/10000)*r_test) < 0.01
            for i in range(3)
        )
        if ok:
            valid_rates.append(r_test)
    print(f"整数%での有効な保管費率: {[f'{r*100:.0f}%' for r in valid_rates]}")
    assert len(valid_rates) == 1, f"解が一意でない: {valid_rates}"
    print("✓ 解は唯一（15%のみ）")
    return storage_D


def verify_q2():
    """問2: パイロット訓練コストデータの検証"""
    print("\n" + "=" * 60)
    print("問2: パイロット訓練コスト管理データ")
    print("=" * 60)

    # データ: (候補生, 飛行時間h, 教官費万円, 飛行機使用料万円, 消耗品費万円, 合計万円)
    trainees = [
        ('P1', 20, 100, 160, 24,  284),
        ('P2', 30, 150, 240, 36,  426),
        ('P3', 25, 125, 200, 30,  355),
    ]

    print("\n【既知データの検証】")
    instructor_rates = []
    machine_rates = []
    consumable_rates = []

    for name, hours, instructor, machine, consumable, total in trainees:
        ins_rate = instructor / hours       # 万円/時間
        mac_rate = machine / hours          # 万円/時間
        con_rate = consumable / machine     # 消耗品費率
        calc_total = instructor + machine + consumable
        instructor_rates.append(ins_rate)
        machine_rates.append(mac_rate)
        consumable_rates.append(con_rate)
        print(f"候補生{name}: 飛行{hours}h, 教官単価={ins_rate:.1f}万/h, "
              f"機体単価={mac_rate:.1f}万/h, 消耗品費率={con_rate*100:.0f}%, "
              f"合計={calc_total:.0f}万円 (表={total}万円)")
        assert abs(calc_total - total) < 0.01, f"候補生{name}の合計が一致しない"

    # 各レートの一意性確認
    assert all(abs(r - instructor_rates[0]) < 1e-9 for r in instructor_rates), "教官単価が一定でない"
    assert all(abs(r - machine_rates[0]) < 1e-9 for r in machine_rates), "機体使用単価が一定でない"
    assert all(abs(r - consumable_rates[0]) < 1e-9 for r in consumable_rates), "消耗品費率が一定でない"

    ins_rate = instructor_rates[0]
    mac_rate = machine_rates[0]
    con_rate = consumable_rates[0]
    print(f"\n→ 教官単価 = {ins_rate:.0f}万円/時間（全候補生で一定）")
    print(f"→ 機体使用単価 = {mac_rate:.0f}万円/時間（全候補生で一定）")
    print(f"→ 消耗品費率 = {con_rate*100:.0f}%（全候補生で一定）")

    # 候補生P4（問の対象）
    hours_P4 = 40
    machine_P4 = hours_P4 * mac_rate
    consumable_P4 = machine_P4 * con_rate

    print(f"\n【候補生P4（問の対象）】")
    print(f"飛行時間 = {hours_P4}時間")
    print(f"飛行機使用料 = {hours_P4} × {mac_rate:.0f} = {machine_P4:.0f}万円")
    print(f"消耗品費（ア）= {machine_P4:.0f} × {con_rate*100:.0f}% = {consumable_P4:.0f}万円")
    print(f"\n→ 正解: （ア）= {consumable_P4:.0f}万円")

    # 解の一意性確認
    print("\n【解の一意性確認】")
    valid_solutions = []
    for ins_test in [i*0.5 for i in range(2, 20)]:
        for mac_test in [i*0.5 for i in range(2, 30)]:
            for con_test in [i/100 for i in range(5, 40)]:
                ok = all(
                    abs(trainees[i][2] - trainees[i][1] * ins_test) < 0.01 and
                    abs(trainees[i][3] - trainees[i][1] * mac_test) < 0.01 and
                    abs(trainees[i][4] - trainees[i][3] * con_test) < 0.01
                    for i in range(3)
                )
                if ok:
                    valid_solutions.append((ins_test, mac_test, con_test))
    print(f"有効な解の数: {len(valid_solutions)}")
    if valid_solutions:
        print(f"有効な解: 教官単価={valid_solutions[0][0]}万/h, "
              f"機体単価={valid_solutions[0][1]}万/h, "
              f"消耗品費率={valid_solutions[0][2]*100}%")
    assert len(valid_solutions) == 1, f"解が一意でない"
    print("✓ 解は唯一")
    return consumable_P4


if __name__ == "__main__":
    ans1 = verify_q1()
    ans2 = verify_q2()
    print(f"\n{'='*60}")
    print(f"問1の正解: （ア）= {ans1:.0f}万円 → 選択肢(4)")
    print(f"問2の正解: （ア）= {ans2:.0f}万円 → 選択肢(2)")
    print("✓ 両問とも解の一意性を確認")
