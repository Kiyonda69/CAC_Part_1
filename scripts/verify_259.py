#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考259 検証スクリプト
テーマ: 航空気象電文（METAR/TAF）の解読による資料空欄穴埋め問題

問1: METAR RJAA 210745Z 33008G21KT 4000 -SN BKN012 OVC040 M01/M04 Q0996
     の解読表の空欄（ア）〜（エ）を求める
問2: TAF RJBB 210500Z 2106/2212 24012KT 9999 FEW030
     BECMG 2108/2110 17016G28KT 6000 -RA SCT015
     TEMPO 2113/2118 2500 +SHRA BKN008
     における21日23時JST（=21日14時UTC）の予想の空欄（ア）〜（エ）を求める
"""


def verify_q1():
    """問1: METAR解読の検証"""
    # 電文の要素（資料の定義に従い機械的に解読）
    metar = {
        "day": 21, "hour_utc": 7, "minute": 45,
        "wind_dir": 330, "wind_mean": 8, "wind_gust": 21,
        "visibility": 4000,
        "weather": "-SN",
        "clouds": [("BKN", 12), ("OVC", 40)],  # 高度は100ft単位の3桁値
        "temp": -1, "dewpoint": -4, "qnh": 996,
    }

    # ガスト付加規則の整合性: 最大瞬間風速が平均より10kt以上大きい場合のみ付加
    assert metar["wind_gust"] - metar["wind_mean"] >= 10, "ガスト付加規則に違反"

    # (ア) 観測時刻のJST時: JST = UTC + 9
    a = metar["hour_utc"] + 9
    assert 0 <= a <= 23, "日付をまたぐ設定は不可"
    # (イ) 最大瞬間風速 [kt]
    b = metar["wind_gust"]
    # (ウ) 最も低い雲の雲底高度 [ft]: 3桁値 × 100
    c = min(h for _, h in metar["clouds"]) * 100
    # (エ) 気温と露点の差 [℃]
    d = metar["temp"] - metar["dewpoint"]

    truth = (a, b, c, d)
    expected = (16, 21, 1200, 3)
    assert truth == expected, f"想定解と不一致: {truth}"

    # 選択肢（ア, イ, ウ, エ）: 正解番号ランダム化前の候補タプル
    options = {
        "correct": (16, 21, 1200, 3),
        "err_no_tz_conv": (7, 21, 1200, 3),       # JST変換忘れ
        "err_mean_wind_temp": (16, 8, 1200, 5),   # 平均風速を採用・温度差を-1+(-4)と誤算
        "err_cloud_x1000": (16, 21, 12000, 3),    # 雲底高度を1000ft単位と誤読
        "err_multiple": (7, 8, 120, 5),           # 複合的な誤り
    }
    tuples = list(options.values())
    assert len(set(tuples)) == 5, "選択肢に重複あり"
    matches = [t for t in tuples if t == truth]
    assert len(matches) == 1, f"正解が{len(matches)}個存在"
    print(f"問1 OK: (ア,イ,ウ,エ) = {truth}, 唯一解を確認")
    return truth


def verify_q2():
    """問2: TAF変化群の適用判定の検証"""
    # 有効期間: 21日06時UTC 〜 22日12時UTC
    # 本文（期間開始時の卓越状態）
    base = {"wind": (240, 12, None), "vis": 9999,
            "wx": None, "clouds": [("FEW", 30)]}
    # BECMG 2108/2110: 期間終了時刻(10Z)以降は新状態が卓越
    becmg = {"period": (8, 10),
             "state": {"wind": (170, 16, 28), "vis": 6000,
                       "wx": "-RA", "clouds": [("SCT", 15)]}}
    # TEMPO 2113/2118: 期間中に一時的に現れる状態
    tempo = {"period": (13, 18),
             "state": {"vis": 2500, "wx": "+SHRA", "clouds": [("BKN", 8)]}}

    # ガスト付加規則の整合性
    assert becmg["state"]["wind"][2] - becmg["state"]["wind"][1] >= 10

    # 評価時刻: 21日23時JST = 21日14時UTC
    t_utc = 23 - 9
    assert t_utc == 14

    # 卓越状態の決定: BECMGは期間終了時刻以降に完了（14Z > 10Z なので新状態）
    assert t_utc >= becmg["period"][1], "BECMG未完了の時刻設定"
    prevailing = dict(base)
    prevailing.update(becmg["state"])

    # TEMPOの適用判定: 13Z <= 14Z < 18Z なので一時的変化あり
    assert tempo["period"][0] <= t_utc < tempo["period"][1], "TEMPO期間外"

    # (ア) 卓越風向 [度]
    a = prevailing["wind"][0]
    # (イ) 卓越視程 [m]
    b = prevailing["vis"]
    # (ウ) 一時的悪化時の視程 [m]
    c = tempo["state"]["vis"]
    # (エ) 一時的悪化時のBKN雲の雲底高度 [ft]: 3桁値 × 100
    d = tempo["state"]["clouds"][0][1] * 100

    truth = (a, b, c, d)
    expected = (170, 6000, 2500, 800)
    assert truth == expected, f"想定解と不一致: {truth}"

    # 視程9999は「10km以上」の意味（選択肢表では「10km以上」と表記）
    options = {
        "correct": (170, 6000, 2500, 800),
        "err_ignore_becmg": (240, 9999, 2500, 800),  # BECMG完了を見落とし
        "err_tempo_swap": (170, 6000, 6000, 800),    # 卓越視程と一時的視程の混同
        "err_vis_keep": (170, 9999, 2500, 800),      # 視程のみ本文から引継ぎと誤解
        "err_cloud_x10": (170, 6000, 2500, 8000),    # 雲底高度の桁誤り
    }
    tuples = list(options.values())
    assert len(set(tuples)) == 5, "選択肢に重複あり"
    matches = [t for t in tuples if t == truth]
    assert len(matches) == 1, f"正解が{len(matches)}個存在"
    print(f"問2 OK: (ア,イ,ウ,エ) = {truth}, 唯一解を確認")
    return truth


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 問1・問2とも解が一意に定まる")
