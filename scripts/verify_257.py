#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""航大思考257 検証: 滑走路公示距離（TORA/TODA/ASDA/LDA）の空欄穴埋め

資料の定義:
  TORA = 滑走路長
  TODA = TORA + 離陸方向先のクリアウェイ長
  ASDA = TORA + 離陸方向先のストップウェイ長
  LDA  = 滑走路長 - 着陸方向の移設しきい値距離
"""


def declared(rwy_len, cwy, swy, disp):
    return {
        "TORA": rwy_len,
        "TODA": rwy_len + cwy,
        "ASDA": rwy_len + swy,
        "LDA": rwy_len - disp,
    }


def q1():
    """問1: A空港 RWY18/36 の公示距離を順算で求める"""
    L = 2500
    # 南側末端(RWY36しきい値側): RWY18方向の離陸で使用
    swy_s, cwy_s = 100, 300
    # 北側末端(RWY18しきい値側): RWY36方向の離陸で使用
    swy_n, cwy_n = 60, 150
    disp_18 = 200  # RWY18着陸時の移設距離(北側)
    disp_36 = 0

    d18 = declared(L, cwy_s, swy_s, disp_18)
    d36 = declared(L, cwy_n, swy_n, disp_36)

    # 空欄: (ア)=RWY18 TODA, (イ)=RWY18 ASDA, (ウ)=RWY18 LDA, (エ)=RWY36 TODA
    truth = (d18["TODA"], d18["ASDA"], d18["LDA"], d36["TODA"])
    assert truth == (2800, 2600, 2300, 2650), truth

    # 誤答パターン(定義の取り違え)も含む選択肢群
    options = {
        1: (2800, 2600, 2300, 2650),  # 正解
        2: (2600, 2800, 2300, 2560),  # TODAとASDAを取り違え
        3: (2800, 2600, 2500, 2650),  # LDAで移設距離を引き忘れ
        4: (2900, 2600, 2300, 2710),  # TODAにSWYまで加算
        5: (2800, 2560, 2300, 2650),  # ASDAに反対側のSWYを使用
    }
    matches = [k for k, v in options.items() if v == truth]
    assert len(matches) == 1, f"問1: 解が{len(matches)}個"
    return matches[0], truth


def q2():
    """問2: B空港 RWY09/27 公示距離からの逆算 + 運航可否判定"""
    L = 2400
    pub = {
        "09": {"TORA": 2400, "TODA": 2760, "ASDA": 2520, "LDA": 2400},
        "27": {"TORA": 2400, "TODA": 2580, "ASDA": 2460, "LDA": 2100},
    }
    # 逆算(方向ごとに総当たりで一意性確認)
    # RWY09方向: 東側CWY/東側SWY/西側移設距離が公示値を決める
    sols09 = [(c, s, d) for c in range(0, 501, 10) for s in range(0, 501, 10)
              for d in range(0, 501, 10) if declared(L, c, s, d) == pub["09"]]
    # RWY27方向: 西側CWY/西側SWY/東側移設距離が公示値を決める
    sols27 = [(c, s, d) for c in range(0, 501, 10) for s in range(0, 501, 10)
              for d in range(0, 501, 10) if declared(L, c, s, d) == pub["27"]]
    assert len(sols09) == 1 and len(sols27) == 1, \
        f"問2逆算: 解が09側{len(sols09)}個/27側{len(sols27)}個"
    cwy_e, swy_e, dw = sols09[0]
    cwy_w, swy_w, de = sols27[0]
    assert (cwy_e, swy_w, de) == (360, 60, 300), sols[0]

    # 運航可否: 所要離陸距離2700(≦TODA), 所要加速停止2500(≦ASDA), 所要着陸2050(≦LDA)
    def ops(r):
        to = pub[r]["TODA"] >= 2700 and pub[r]["ASDA"] >= 2500
        ldg = pub[r]["LDA"] >= 2050
        return to, ldg

    to09, ldg09 = ops("09")
    to27, ldg27 = ops("27")
    assert (to09, ldg09, to27, ldg27) == (True, True, False, True)
    verdict = "離陸はRWY09のみ可、着陸は両方向可"

    truth = (cwy_e, swy_w, de, verdict)
    options = {
        1: (360, 60, 300, "離陸・着陸とも両方向可"),
        2: (360, 60, 300, "離陸はRWY09のみ可、着陸は両方向可"),  # 正解
        3: (360, 120, 300, "離陸はRWY09のみ可、着陸は両方向可"),
        4: (180, 60, 300, "離陸はRWY09のみ可、着陸はRWY27のみ可"),
        5: (360, 60, 150, "離陸・着陸ともRWY09のみ可"),
    }
    matches = [k for k, v in options.items() if v == truth]
    assert len(matches) == 1, f"問2: 解が{len(matches)}個"
    return matches[0], truth


if __name__ == "__main__":
    a1, t1 = q1()
    a2, t2 = q2()
    print(f"問1 正解値: (ア){t1[0]} (イ){t1[1]} (ウ){t1[2]} (エ){t1[3]}")
    print(f"問2 正解値: (ア){t2[0]} (イ){t2[1]} (ウ){t2[2]} (エ){t2[3]}")
    print(f"検証用の正解位置: 問1={a1}, 問2={a2} (HTML作成時にランダム化して並べ替え)")
