"""
航大思考55 検証スクリプト
問1: 燃料搭載量計算（標準）
問2: 2区間飛行の燃料計算（高難度）
"""

def verify_q1():
    """
    問1: 燃料搭載量の計算

    パイロットが空港Pから空港Qまでの飛行を計画している。
    以下の条件から、最低搭載燃料を計算せよ。

    条件:
    - 飛行距離 P→Q: 720 km
    - 巡航燃費: 2.5 kg/km
    - 上昇追加燃料: 200 kg
    - 降下節約量: 80 kg
    - 地上走行燃料: 60 kg
    - 不測事態燃料: 飛行燃料の5%（10 kg単位で切り上げ）
    - 予備燃料: 450 kg
    """
    import math

    # 基本データ
    distance = 720  # km
    cruise_rate = 2.5  # kg/km
    climb_extra = 200  # kg
    descent_savings = 80  # kg
    taxi_fuel = 60  # kg
    contingency_rate = 0.05
    reserve = 450  # kg

    # 計算
    cruise_fuel = distance * cruise_rate  # 720 × 2.5 = 1,800
    flight_fuel = cruise_fuel + climb_extra - descent_savings  # 1,800 + 200 - 80 = 1,920
    contingency_raw = flight_fuel * contingency_rate  # 1,920 × 0.05 = 96
    contingency = math.ceil(contingency_raw / 10) * 10  # 切り上げ → 100
    total = taxi_fuel + flight_fuel + contingency + reserve  # 60 + 1,920 + 100 + 450 = 2,530

    print(f"=== 問1 検証 ===")
    print(f"巡航燃料: {distance} × {cruise_rate} = {cruise_fuel} kg")
    print(f"飛行燃料: {cruise_fuel} + {climb_extra} - {descent_savings} = {flight_fuel} kg")
    print(f"不測事態燃料: {flight_fuel} × {contingency_rate} = {contingency_raw} → {contingency} kg（10kg単位切り上げ）")
    print(f"最低搭載燃料: {taxi_fuel} + {flight_fuel} + {contingency} + {reserve} = {total} kg")
    print()

    # 誤答パターンの検証
    # 誤答1: 上昇追加を忘れる
    err1_flight = cruise_fuel - descent_savings  # 1,720
    err1_cont = math.ceil(err1_flight * contingency_rate / 10) * 10  # 86 → 90
    err1_total = taxi_fuel + err1_flight + err1_cont + reserve  # 60 + 1720 + 90 + 450 = 2,320

    # 誤答2: 切り上げしない
    err2_total = taxi_fuel + flight_fuel + int(contingency_raw) + reserve  # 60 + 1920 + 96 + 450 = 2,526

    # 誤答3: 不測事態燃料を全体に適用
    err3_base = taxi_fuel + flight_fuel + reserve  # 2,430
    err3_cont = math.ceil(err3_base * contingency_rate / 10) * 10  # 121.5 → 130
    err3_total = err3_base + err3_cont  # 2,430 + 130 = 2,560

    # 誤答4: 降下節約を忘れる
    err4_flight = cruise_fuel + climb_extra  # 2,000
    err4_cont = math.ceil(err4_flight * contingency_rate / 10) * 10  # 100
    err4_total = taxi_fuel + err4_flight + err4_cont + reserve  # 60 + 2000 + 100 + 450 = 2,610

    print("--- 選択肢検証 ---")
    print(f"正解: {total} kg")
    print(f"誤答（上昇追加忘れ）: {err1_total} kg")
    print(f"誤答（切り上げなし）: {err2_total} kg")
    print(f"誤答（不測事態を全体に適用）: {err3_total} kg")
    print(f"誤答（降下節約忘れ）: {err4_total} kg")

    # 全て異なることを確認
    all_options = [total, err1_total, err2_total, err3_total, err4_total]
    assert len(set(all_options)) == 5, f"選択肢に重複あり: {all_options}"
    assert total == 2530, f"正解が想定と異なる: {total}"

    print("問1: 検証OK - 解は唯一\n")
    return total


def verify_q2():
    """
    問2: 2区間飛行の燃料計算

    航空機が P→Q→R の2区間を飛行する。Qでは給油できない。

    条件:
    | 項目          | P→Q区間   | Q→R区間   |
    |--------------|-----------|-----------|
    | 飛行距離      | 800 km    | 600 km    |
    | 基本燃費      | 2.0 kg/km | 2.0 kg/km |
    | 風の影響      | 向かい風+20% | 追い風-10% |
    | 上昇追加燃料   | 150 kg    | 150 kg    |
    | 降下節約量     | 50 kg     | 50 kg     |

    追加条件:
    - 地上走行燃料（P出発）: 40 kg
    - 地上走行燃料（Q出発）: 30 kg
    - 不測事態燃料: 全区間の飛行燃料合計の5%
    - 予備燃料（R到着時）: 300 kg
    """
    # 区間P→Q
    dist_pq = 800
    rate = 2.0
    wind_pq = 1.20  # 向かい風 +20%
    climb = 150
    descent = 50

    base_pq = dist_pq * rate  # 1,600
    wind_pq_fuel = base_pq * wind_pq  # 1,920
    flight_pq = wind_pq_fuel + climb - descent  # 1,920 + 150 - 50 = 2,020

    # 区間Q→R
    dist_qr = 600
    wind_qr = 0.90  # 追い風 -10%

    base_qr = dist_qr * rate  # 1,200
    wind_qr_fuel = base_qr * wind_qr  # 1,080
    flight_qr = wind_qr_fuel + climb - descent  # 1,080 + 150 - 50 = 1,180

    # 合計
    total_flight = flight_pq + flight_qr  # 3,200
    taxi_p = 40
    taxi_q = 30
    contingency = total_flight * 0.05  # 160
    reserve = 300

    total = taxi_p + taxi_q + total_flight + contingency + reserve
    # 40 + 30 + 3,200 + 160 + 300 = 3,730

    print(f"=== 問2 検証 ===")
    print(f"P→Q 基本燃料: {dist_pq} × {rate} = {base_pq} kg")
    print(f"P→Q 風補正後: {base_pq} × {wind_pq} = {wind_pq_fuel} kg")
    print(f"P→Q 飛行燃料: {wind_pq_fuel} + {climb} - {descent} = {flight_pq} kg")
    print(f"Q→R 基本燃料: {dist_qr} × {rate} = {base_qr} kg")
    print(f"Q→R 風補正後: {base_qr} × {wind_qr} = {wind_qr_fuel} kg")
    print(f"Q→R 飛行燃料: {wind_qr_fuel} + {climb} - {descent} = {flight_qr} kg")
    print(f"全飛行燃料: {flight_pq} + {flight_qr} = {total_flight} kg")
    print(f"不測事態燃料: {total_flight} × 0.05 = {contingency} kg")
    print(f"地上走行燃料: {taxi_p} + {taxi_q} = {taxi_p + taxi_q} kg")
    print(f"最低搭載燃料: {taxi_p} + {taxi_q} + {total_flight} + {contingency} + {reserve} = {total} kg")
    print()

    # 誤答パターン
    # 誤答1: 風の影響を無視
    err1_pq = base_pq + climb - descent  # 1,700
    err1_qr = base_qr + climb - descent  # 1,300
    err1_flight = err1_pq + err1_qr  # 3,000
    err1_cont = err1_flight * 0.05  # 150
    err1_total = taxi_p + taxi_q + err1_flight + err1_cont + reserve  # 3,520

    # 誤答2: Q出発の地上走行燃料を忘れる
    err2_total = taxi_p + total_flight + contingency + reserve  # 3,700

    # 誤答3: 降下節約を忘れる
    err3_pq = wind_pq_fuel + climb  # 2,070
    err3_qr = wind_qr_fuel + climb  # 1,230
    err3_flight = err3_pq + err3_qr  # 3,300
    err3_cont = err3_flight * 0.05  # 165
    err3_total = taxi_p + taxi_q + err3_flight + err3_cont + reserve  # 3,835

    # 誤答4: 追い風を向かい風と同じ方向（+10%）に計算
    err4_qr_fuel = base_qr * 1.10  # 1,320
    err4_qr = err4_qr_fuel + climb - descent  # 1,420
    err4_flight = flight_pq + err4_qr  # 3,440
    err4_cont = err4_flight * 0.05  # 172
    err4_total = taxi_p + taxi_q + err4_flight + err4_cont + reserve  # 3,982

    print("--- 選択肢検証 ---")
    print(f"正解: {total} kg")
    print(f"誤答（風の影響無視）: {err1_total} kg")
    print(f"誤答（Q地上走行忘れ）: {err2_total} kg")
    print(f"誤答（降下節約忘れ）: {err3_total} kg")
    print(f"誤答（追い風方向逆）: {err4_total} kg")

    all_options = [total, err1_total, err2_total, err3_total, err4_total]
    assert len(set(all_options)) == 5, f"選択肢に重複あり: {all_options}"
    assert total == 3730, f"正解が想定と異なる: {total}"

    print("問2: 検証OK - 解は唯一\n")
    return total


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全問題の検証が完了しました。")
