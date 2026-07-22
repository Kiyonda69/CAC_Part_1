#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""航大思考297 検証スクリプト
問1: 公共施設利用者数表の空欄穴埋め（増減率の順算・集計・増減率算出）
問2: 輸出額表の空欄穴埋め（構成比からの逆算・指数算出・連鎖計算）
"""


def verify_q1():
    """問1: ある市の公共施設利用者数"""
    # (施設, 2023年度, 2024年度, 増減率%)  ア=図書館2024年度
    data = [
        ("体育館", 12400, 13640, 10.0),
        ("図書館", 25600, None, 12.5),
        ("美術館", 8500, 7820, -8.0),
        ("公民館", 18300, 19215, 5.0),
        ("プール", 9200, 10580, 15.0),
    ]
    # 既知セルの増減率が表と厳密に一致するか検証
    for name, y23, y24, rate in data:
        if y24 is not None:
            actual = (y24 - y23) / y23 * 100
            assert abs(actual - rate) < 1e-9, f"{name}: {actual} != {rate}"

    # ア: 図書館2024年度 = 25600 × 1.125（整数で割り切れることを確認）
    a = 25600 * 1.125
    assert a == int(a), f"アが整数でない: {a}"
    a = int(a)
    assert a == 28800

    # イ: 2024年度合計
    total23 = sum(d[1] for d in data)
    assert total23 == 74000
    total24 = sum(d[2] if d[2] is not None else a for d in data)
    assert total24 == 80055  # イ

    # ウ: 合計の増減率（小数第2位を四捨五入）
    rate_total = (total24 - total23) / total23 * 100
    w = round(rate_total, 1)
    assert w == 8.2, f"ウ: {rate_total}"

    # 選択肢（ア, イ, ウ）: 正解が唯一であることを確認
    options = [
        (28800, 80055, 8.2),   # 正解
        (28160, 79415, 7.3),   # 増減率10%を誤用した連鎖誤り
        (28160, 80055, 8.2),   # 不整合肢
        (28800, 80055, 6.9),   # 増減率の単純平均の罠
        (28800, 79415, 8.2),   # 不整合肢
    ]
    correct = [o for o in options if o == (a, total24, w)]
    assert len(correct) == 1, f"問1: 正解が{len(correct)}個"
    print(f"問1 OK: ア={a:,} イ={total24:,} ウ={w}%")


def verify_q2():
    """問2: ある県の輸出額（構成比＋指数）"""
    # 化学: 11,000億円が構成比20.0% → 2022年合計を逆算
    total22 = 11000 / 0.20
    assert total22 == 55000

    # ア: 機械の2022年輸出額（構成比40.0%）
    a = total22 * 0.40
    assert a == int(a) and int(a) == 22000
    a = int(a)

    # イ: 機械の指数（2024年23,760億円 ÷ ア × 100、整数で割り切れる）
    b = 23760 / a * 100
    assert b == int(b) and int(b) == 108
    b = int(b)

    # 食品・繊維の2022年値の整合検証
    food22 = 13200 / 0.96      # 指数96から逆算
    assert food22 == 13750 and food22 / total22 == 0.25  # 構成比25.0%と一致
    fiber22 = total22 * 0.15
    assert fiber22 == 8250 and abs(fiber22 * 0.92 - 7590) < 1e-9  # 指数92と一致

    # ウ: 2024年合計 — 2通りの計算が一致（二重整合）
    w_index = total22 * 1.04            # 合計指数104から
    w_sum = 23760 + 13200 + 12650 + 7590  # 各品目の加算から
    assert w_index == w_sum == 57200
    w = int(w_sum)

    # 化学の指数115の整合検証
    assert abs(11000 * 1.15 - 12650) < 1e-9

    # 構成比合計100%
    assert abs((a + food22 + 11000 + fiber22) - total22) < 1e-9

    # 選択肢（ア, イ, ウ）: 正解が唯一であることを確認
    options = [
        (22000, 108, 57200),   # 正解
        (21120, 113, 54912),   # 2024年食品から合計を誤逆算した連鎖誤り
        (22000, 104, 57200),   # イを合計指数と混同
        (22000, 108, 57750),   # ウを5%増と誤計算
        (21120, 108, 57200),   # 不整合肢
    ]
    correct = [o for o in options if o == (a, b, w)]
    assert len(correct) == 1, f"問2: 正解が{len(correct)}個"
    print(f"問2 OK: ア={a:,} イ={b} ウ={w:,}")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証パス: 両問とも解は一意")
