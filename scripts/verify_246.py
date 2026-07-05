#!/usr/bin/env python3
"""航大思考246 検証: 気象電文解読＋着陸可否判定問題の解の一意性を確認

着陸最低気象条件:
 1. 視程 5000m以上 (9999は10km以上)
 2. シーリング(BKN/OVCの最低雲底) 1000ft以上 (BKN/OVCなしは制限なし)
 3. 風速 20kt以下 (ガストがある場合はガスト値で判定)
"""

VIS_MIN = 5000
CEIL_MIN = 1000   # ft
WIND_MAX = 20     # kt


def judge(wind_mean, gust, vis, clouds):
    """clouds: [(amount, base_ft), ...]  戻り値: 不適合条件のリスト"""
    fails = []
    if vis < VIS_MIN:
        fails.append("視程")
    ceilings = [b for a, b in clouds if a in ("BKN", "OVC")]
    if ceilings and min(ceilings) < CEIL_MIN:
        fails.append("雲底")
    w = gust if gust is not None else wind_mean
    if w > WIND_MAX:
        fails.append("風速")
    return fails


def q1():
    # (空港, 平均風速, ガスト, 視程m, 雲)  9999→10000扱い
    airports = [
        ("A", 12, None, 6000, [("BKN", 800)]),
        ("B", 22, None, 10000, [("SCT", 3000)]),
        ("C", 10, None, 10000, [("FEW", 500), ("BKN", 2000)]),  # 正解(3)
        ("D", 15, None, 4000, [("BKN", 1500)]),
        ("E", 8, 25, 8000, [("SCT", 2500)]),
    ]
    ok = []
    for name, wm, g, vis, cl in airports:
        fails = judge(wm, g, vis, cl)
        print(f"問1 {name}空港: {'適合' if not fails else '不適合 ' + str(fails)}")
        if not fails:
            ok.append(name)
        else:
            assert len(fails) == 1, f"{name}は1条件のみ不適合にする設計: {fails}"
    assert ok == ["C"], f"唯一解でない: {ok}"
    print("問1: C空港のみ適合 → 正解(3) 検証OK\n")


ARRIVAL = 9.5  # 09:30 UTC


def forecast_state(obs, becmg, tempo):
    """到着時刻の判定用気象状態を返す
    obs: dict(wind, gust, vis, clouds)
    becmg: (start, end, 変更dict) 終了時刻以降は新値が持続
    tempo: (start, end, 変更dict) 時間帯内に到着する場合は記載値で判定
    """
    st = dict(obs)
    if becmg and ARRIVAL >= becmg[1]:
        st.update(becmg[2])
    if tempo and tempo[0] <= ARRIVAL <= tempo[1]:
        st.update(tempo[2])
    return st


def q2():
    airports = [
        ("P", dict(wind=10, gust=None, vis=10000, clouds=[("SCT", 3000)]),
         (6, 8, dict(vis=4000)), None),                       # 悪化が到着前に完了→視程NG
        ("Q", dict(wind=14, gust=None, vis=8000, clouds=[("BKN", 3000)]),
         None, (8, 12, dict(wind=25))),                       # TEMPO 25kt→風速NG
        ("R", dict(wind=12, gust=None, vis=4000, clouds=[("BKN", 2500)]),
         (7, 9, dict(vis=10000)), None),                      # 改善が到着前に完了→適合 正解(3)
        ("S", dict(wind=16, gust=None, vis=3000, clouds=[("BKN", 1500)]),
         (10, 12, dict(vis=10000)), None),                    # 改善が到着後→視程NG
        ("T", dict(wind=8, gust=None, vis=10000, clouds=[("BKN", 800)]),
         None, None),                                         # 変化なし→雲底NG
    ]
    ok = []
    for name, obs, becmg, tempo in airports:
        st = forecast_state(obs, becmg, tempo)
        fails = judge(st["wind"], st["gust"], st["vis"], st["clouds"])
        print(f"問2 {name}空港 到着時: {'適合' if not fails else '不適合 ' + str(fails)}")
        if not fails:
            ok.append(name)
    assert ok == ["R"], f"唯一解でない: {ok}"
    # 罠の検証: 現況のみで判定するとRは不適合・P/Qは適合に見える
    r_now = judge(12, None, 4000, [("BKN", 2500)])
    p_now = judge(10, None, 10000, [("SCT", 3000)])
    assert r_now and not p_now, "現況判定の罠が成立していない"
    # 罠の検証: BECMG終了時刻を無視して先取りするとSも適合に見える
    s_early = judge(16, None, 10000, [("BKN", 1500)])
    assert not s_early, "S空港の改善先取り罠が成立していない"
    print("問2: R空港のみ適合 → 正解(3) 検証OK")


if __name__ == "__main__":
    q1()
    q2()
    print("\n全検証OK: 問1正解(3)C空港 / 問2正解(3)R空港")
