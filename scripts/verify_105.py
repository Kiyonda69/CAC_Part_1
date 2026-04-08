"""
航大思考105 検証スクリプト

問1（標準）: 図書館月次貸出データの空欄穴埋め
問2（高難度）: 物流センター配送実績の空欄穴埋め（複数空欄＋合計）
"""


def verify_q1():
    """
    問1: 市立図書館の月次貸出データ

    長文の条件:
    - 当月の総貸出冊数は2,400冊
    - 文学は全体の30%
    - 実用書は文学より96冊少ない
    - 児童書は実用書の1.5倍
    - 専門書は残り
    """
    total = 2400

    # 条件1: 文学は全体の30%
    bungaku = int(total * 0.3)
    assert bungaku == 720, f"文学の冊数が想定外: {bungaku}"

    # 条件2: 実用書は文学より96冊少ない
    jitsuyo = bungaku - 96
    assert jitsuyo == 624

    # 条件3: 児童書は実用書の1.5倍
    jido = int(jitsuyo * 1.5)
    assert jido == 936

    # 条件4: 専門書は残り
    senmon = total - bungaku - jitsuyo - jido
    assert senmon == 120

    # 検算: 合計が一致
    assert bungaku + jitsuyo + jido + senmon == total

    # 表中の他の数値が条件と整合するか確認
    # 前月比+5% → 前月は720/1.05 ≒ 685.7（参考値）
    print(f"問1: 文学={bungaku}, 実用書={jitsuyo}, 児童書={jido}, 専門書={senmon}")
    print(f"問1 答え: ア = {bungaku}")

    # 選択肢
    choices = [600, 660, 680, 700, 720]
    correct_idx = choices.index(bungaku) + 1
    assert correct_idx == 5, f"正解番号が想定外: {correct_idx}"
    print(f"問1 正解番号: ({correct_idx})")
    return bungaku


def verify_q2():
    """
    問2: 物流センターの月次配送実績

    長文の条件:
    【北部ルート】
    - 2台のトラック
    - 配送日数25日
    - 1台あたり1日平均120個
    - 両トラックとも全日稼働

    【中部ルート】
    - 3台のトラック
    - うち1台は前半14日間のみ稼働、後半は整備停止
    - 残り2台は通常通り月間28日稼働
    - 1台あたり1日平均150個

    【南部ルート】
    - 2台のトラック
    - 通常22日稼働予定
    - 月末3日間は1台が停止、もう1台のみで継続
    - 1台あたり1日平均180個
    """
    # 北部ルート
    hokubu = 2 * 25 * 120
    assert hokubu == 6000

    # 中部ルート
    chubu_truck1 = 14 * 150  # 前半14日のみ
    chubu_truck23 = 2 * 28 * 150  # 残り2台が月間28日
    chubu = chubu_truck1 + chubu_truck23
    assert chubu == 2100 + 8400 == 10500

    # 南部ルート
    nanbu_truck_full = 22 * 180  # フル稼働
    nanbu_truck_partial = (22 - 3) * 180  # 月末3日間停止
    nanbu = nanbu_truck_full + nanbu_truck_partial
    assert nanbu == 3960 + 3420 == 7380

    # 合計
    total = hokubu + chubu + nanbu
    assert total == 6000 + 10500 + 7380 == 23880

    print(f"問2: 北部={hokubu}, 中部={chubu}(ア), 南部={nanbu}(イ), 合計={total}(ウ)")

    # ア + イ + ウ
    answer = chubu + nanbu + total
    print(f"問2 答え: ア+イ+ウ = {chubu} + {nanbu} + {total} = {answer}")

    # 選択肢
    choices = [41260, 41500, 41760, 42000, 42260]
    assert answer in choices, f"答え {answer} が選択肢にない"
    correct_idx = choices.index(answer) + 1
    assert correct_idx == 3, f"正解番号が想定外: {correct_idx}"
    print(f"問2 正解番号: ({correct_idx})")
    return answer


if __name__ == "__main__":
    print("=" * 60)
    print("航大思考105 検証")
    print("=" * 60)
    q1 = verify_q1()
    print()
    q2 = verify_q2()
    print()
    print("=" * 60)
    print("すべての検証に合格しました")
    print("=" * 60)
