#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""セット250: 使用滑走路の選定問題（風の成分計算）の検証

資料1（運航規程）:
- 滑走路番号は磁方位を10で割った値。各滑走路は両方向から使用可能。
- 風向と滑走路方位の角度差（0〜180°）から係数表で成分を計算。
  正面風成分 = 風速 × 正面風係数（負の値は追い風）
  横風成分   = 風速 × 横風係数
- 使用条件: 横風成分 12kt以下、追い風成分 5kt以下（問1）
- 複数方向が使用可能な場合、正面風成分が最大の方向を使用する。

問2追加規程:
- ガストがある場合、横風成分はガスト値、正面・追い風成分は平均風速で計算。
- 横風制限 15kt、追い風制限 5kt。
"""

# 係数表（角度差: (正面風係数, 横風係数)）
COEF = {
    0: (1.00, 0.00),
    30: (0.87, 0.50),
    45: (0.71, 0.71),
    60: (0.50, 0.87),
    90: (0.00, 1.00),
    120: (-0.50, 0.87),
    135: (-0.71, 0.71),
    150: (-0.87, 0.50),
    180: (-1.00, 0.00),
}

RUNWAYS = {"09": 90, "18": 180, "27": 270, "36": 360}


def angle_diff(wind_dir, rwy_hdg):
    d = abs(wind_dir - rwy_hdg) % 360
    return min(d, 360 - d)


def components(wind_dir, mean, gust, rwy_hdg):
    """(正面風成分[平均風], 横風成分[ガスト優先]) を返す"""
    diff = angle_diff(wind_dir, rwy_hdg)
    assert diff in COEF, f"角度差{diff}が係数表にない"
    h_coef, x_coef = COEF[diff]
    head = mean * h_coef
    cross = (gust if gust else mean) * x_coef
    return head, cross


def usable(wind_dir, mean, gust, rwy_hdg, cross_limit, tail_limit=5):
    head, cross = components(wind_dir, mean, gust, rwy_hdg)
    return cross <= cross_limit and head >= -tail_limit


def verify_q1():
    """問1: 風向120°・風速12kt（ガストなし）、横風制限12kt・追い風制限5kt"""
    wind_dir, mean = 120, 12
    results = {}
    for rwy, hdg in RUNWAYS.items():
        head, cross = components(wind_dir, mean, None, hdg)
        ok = usable(wind_dir, mean, None, hdg, cross_limit=12)
        results[rwy] = (head, cross, ok)
        print(f"  RWY{rwy}: 正面風={head:+.2f}kt 横風={cross:.2f}kt "
              f"{'使用可' if ok else '使用不可'}")
    usable_rwys = [(r, v[0]) for r, v in results.items() if v[2]]
    assert len(usable_rwys) == 2, f"使用可能滑走路が{len(usable_rwys)}本（2本の想定）"
    best = max(usable_rwys, key=lambda x: x[1])
    ties = [r for r, h in usable_rwys if abs(h - best[1]) < 1e-9]
    assert len(ties) == 1, "正面風成分が最大の滑走路が複数存在"
    print(f"  → 使用滑走路: RWY{best[0]} 正面風成分 約{best[1]:.1f}kt")
    assert best[0] == "09" and abs(best[1] - 10.44) < 0.01
    return best


def verify_q2():
    """問2: 5時刻の風予報のうち、どの滑走路も使用できない時刻が唯一か
    制限: 横風15kt（ガストで計算）、追い風5kt（平均風で計算）
    正解(2) = 10時 の行のみ全滑走路使用不可となること
    """
    forecast = [
        ("09時", 90, 10, None),
        ("10時", 135, 12, 22),   # 正解: 全方向使用不可
        ("11時", 180, 14, 20),
        ("12時", 225, 10, 16),
        ("13時", 330, 16, 24),
    ]
    no_rwy_times = []
    for label, wd, mean, gust in forecast:
        oks = []
        detail = []
        for rwy, hdg in RUNWAYS.items():
            head, cross = components(wd, mean, gust, hdg)
            ok = usable(wd, mean, gust, hdg, cross_limit=15)
            oks.append(ok)
            detail.append(f"RWY{rwy}:H{head:+.1f}/X{cross:.1f}{'○' if ok else '×'}")
        print(f"  {label} 風向{wd:03d}° {mean}kt"
              f"{f' G{gust}kt' if gust else '':7s} | " + " ".join(detail))
        if not any(oks):
            no_rwy_times.append(label)
    assert no_rwy_times == ["10時"], f"全滑走路使用不可の時刻: {no_rwy_times}"
    print(f"  → どの滑走路も使用できない時刻: {no_rwy_times[0]}（唯一）")
    return no_rwy_times[0]


if __name__ == "__main__":
    print("=== 問1 検証 ===")
    verify_q1()
    print("\n=== 問2 検証 ===")
    verify_q2()
    print("\n検証OK: 問1・問2とも解は一意")
