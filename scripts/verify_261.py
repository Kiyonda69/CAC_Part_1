#!/usr/bin/env python3
"""航大思考261: 降下計画（TOD・必要降下率）穴埋めの検証"""

GRAD = 300  # ft/海里（規則1）


def rate(gs):
    """規則4: 必要降下率 = 対地速度×5（勾配300ft/NMと完全整合の確認付き）"""
    r = gs * 5
    assert abs(gs / 60 * GRAD - r) < 1e-9, "規則1と規則4が矛盾"
    return r


def q1():
    cruise, target = 12000, 3000
    tas, wind = 150, +30  # 追い風30kt
    loss = cruise - target            # 9,000 ft
    dist = loss / GRAD                # (ア) 30海里
    gs = tas + wind                   # (イ) 180kt
    r = rate(gs)                      # (ウ) 900ft/分
    t = loss / r                      # (エ) 10分
    # 距離ベースの時間と一致するか（内部整合）
    assert abs(dist / gs * 60 - t) < 1e-9
    ans = (dist, gs, r, t)
    assert ans == (30, 180, 900, 10), ans
    # 選択肢（誤答は誤り筋から生成）
    opts = {
        "正解": (30, 180, 900, 10),
        "風符号誤り": (30, tas - wind, (tas - wind) * 5, loss / ((tas - wind) * 5)),  # 120,600,15
        "降下率にTAS使用": (30, 180, tas * 5, loss / (tas * 5)),                      # 750,12
        "風無視": (30, tas, tas * 5, loss / (tas * 5)),                               # 150,750,12
        "通過高度引き忘れ": (cruise / GRAD, 180, 900, round(cruise / 900, 0)),        # 40,...,13
    }
    vals = list(opts.values())
    assert vals.count(opts["正解"]) == 1, "正解の組合せが一意でない"
    print("問1 OK:", opts)


def q2():
    cruise, boundary, target = 13000, 10000, 4000
    wind = -30  # 向かい風
    tas_hi, tas_lo = 180, 150  # 10,000ft以上/未満
    # 区間1: 13,000→10,000
    l1 = cruise - boundary
    gs1 = tas_hi + wind
    d1, r1, t1 = l1 / GRAD, rate(gs1), l1 / rate(gs1)
    # 区間2: 10,000→4,000
    l2 = boundary - target
    gs2 = tas_lo + wind
    d2, r2, t2 = l2 / GRAD, rate(gs2), l2 / rate(gs2)
    tod = d1 + d2          # (ア) 30海里（速度に依存しない）
    # (イ) 区間2の必要降下率 600ft/分、(ウ) 合計 14分
    total = t1 + t2
    # (エ) 地点Qの10海里手前の地点Rの通過高度
    alt_r = target + 10 * GRAD  # 7,000ft
    assert (tod, r2, total, alt_r) == (30, 600, 14, 7000), (tod, r2, total, alt_r)
    assert (d1, gs1, r1, t1) == (10, 150, 750, 4)
    assert (d2, gs2, t2) == (20, 120, 10)
    assert alt_r < boundary  # RはQ側の区間2内にある
    assert cruise - 20 * GRAD == alt_r  # TOD側から測っても一致
    opts = {
        "正解": (30, 600, 14, 7000),
        "速度制限見落とし": (30, 750, 9000 / 750, 7000),                # 750,12
        "風符号誤り": (30, rate(tas_lo - wind), round(l1 / rate(tas_hi - wind) + l2 / rate(tas_lo - wind), 0), 7000),  # 900,約10
        "TODから測る誤り": (30, 600, 14, cruise - 10 * GRAD),           # エ=10,000
        "通過高度引き忘れ": (round(cruise / GRAD, 0), 600, round(t1 + (cruise - target - l1) / r2 + (target) / 0 if False else 21, 0), 7000),
    }
    opts["通過高度引き忘れ"] = (43, 600, 21, 7000)  # 13,000/300≒43海里、4+10,000/600≒21分
    vals = list(opts.values())
    assert vals.count(opts["正解"]) == 1, "正解の組合せが一意でない"
    print("問2 OK:", opts)


if __name__ == "__main__":
    q1()
    q2()
    print("検証完了: 問1・問2とも唯一解")
