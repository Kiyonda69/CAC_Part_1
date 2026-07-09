#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考263 検証コード
テーマ: 速度の換算（CAS→TAS→マッハ数・対地速度）の資料空欄穴埋め

規則:
  規則1: TAS = CAS × (1 + 0.02 × 気圧高度[千ft])
  規則2: GS = TAS + 風成分（追い風+、向かい風−）
  規則3: マッハ数 = TAS ÷ 音速（音速は外気温の表から）
  規則4: 所要時間[分] = 距離 ÷ GS × 60
音速表: +15℃:660 / 0℃:645 / −15℃:625 / −25℃:615 / −35℃:600 / −45℃:590 / −55℃:575
"""

LSS = {15: 660, 0: 645, -15: 625, -25: 615, -35: 600, -45: 590, -55: 575}


def tas_from_cas(cas, alt_ft):
    return cas * (1 + 0.02 * alt_ft / 1000)


def verify_q1():
    """問1: 順方向の連鎖計算（CAS→TAS→マッハ→GS→所要時間）"""
    alt, cas, oat, headwind, dist = 25000, 200, -35, 50, 175

    a = tas_from_cas(cas, alt)          # (ア) TAS
    b = a / LSS[oat]                    # (イ) マッハ数
    c = a - headwind                    # (ウ) GS
    d = dist / c * 60                   # (エ) 所要時間[分]

    assert a == 300, a
    assert abs(b - 0.50) < 1e-9, b
    assert c == 250, c
    assert d == 42, d

    # 誤答トレースの検証
    # 換算忘れ（TAS=CAS）: 200 / 0.33 / 150 / 70分
    t2 = cas
    assert round(t2 / LSS[oat], 2) == 0.33
    assert t2 - headwind == 150
    assert dist / (t2 - headwind) * 60 == 70
    # 風符号逆: GS=350 → 30分
    assert a + headwind == 350 and dist / 350 * 60 == 30
    # マッハにCAS代入: 0.33
    assert round(cas / LSS[oat], 2) == 0.33
    # 所要時間にTAS使用: 35分
    assert dist / a * 60 == 35

    # 選択肢5組の一意性（正解は1組のみ）
    options = [
        (300, 0.50, 250, 42),   # 正解
        (200, 0.33, 150, 70),   # 換算忘れ
        (300, 0.50, 350, 30),   # 風符号逆
        (300, 0.33, 250, 42),   # マッハにCAS代入
        (300, 0.50, 250, 35),   # 所要時間にTAS使用
    ]
    truth = (a, round(b, 2), c, d)
    matches = [o for o in options if o == truth]
    assert len(set(options)) == 5, "選択肢に重複あり"
    assert len(matches) == 1, f"正解が{len(matches)}個"
    print("問1 OK:", truth)


def verify_q2():
    """問2: 逆算（締切→必要GS→必要TAS→必要CAS）＋マッハ判定"""
    alt, oat, headwind, dist, limit_min, mach_limit = 30000, -45, 40, 432, 60, 0.80
    factor = 1 + 0.02 * alt / 1000      # 1.6

    a = dist / limit_min * 60           # (ア) 必要GS
    b = a + headwind                    # (イ) 必要TAS（向かい風の分だけ大きく）
    c = b / factor                      # (ウ) 必要CAS
    d = b / LSS[oat]                    # (エ) マッハ数

    assert a == 432, a
    assert b == 472, b
    assert c == 295, c
    assert abs(d - 0.80) < 1e-9, d
    feasible = d <= mach_limit
    assert feasible, "制限マッハちょうどで到着可能のはず"

    # 誤答トレースの検証
    # 風符号逆: TAS=392 → CAS=245 → M=0.66
    t2 = a - headwind
    assert t2 == 392 and t2 / factor == 245
    assert round(t2 / LSS[oat], 2) == 0.66
    # 換算忘れ（CAS=TAS）: 472
    # 音速表の行誤り（−55℃:575）: M=0.82 → 制限超過で「到着できない」に見える
    assert round(b / LSS[-55], 2) == 0.82
    assert b / LSS[-55] > mach_limit
    # マッハにCAS代入: 295/590=0.50
    assert round(c / LSS[oat], 2) == 0.50

    options = [
        (432, 472, 295, 0.80, True),    # 正解（ちょうど制限・到着できる）
        (432, 392, 245, 0.66, True),    # 風符号逆
        (432, 472, 472, 0.80, True),    # 換算忘れ CAS=TAS
        (432, 472, 295, 0.82, False),   # 音速表の行誤り
        (432, 472, 295, 0.50, True),    # マッハにCAS代入
    ]
    truth = (a, b, c, round(d, 2), feasible)
    matches = [o for o in options if o == truth]
    assert len(set(options)) == 5, "選択肢に重複あり"
    assert len(matches) == 1, f"正解が{len(matches)}個"
    print("問2 OK:", truth)


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 問1・問2とも唯一解")
