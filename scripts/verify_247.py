#!/usr/bin/env python3
"""セット247: NOTAM（航空情報）読解問題の検証

問1: 到着 7/10 11:30 JST（NOTAM時刻もJST）で着陸できない空港が唯一か
問2: 到着 7/10 08:30 JST = 7/9 23:30 UTC（NOTAM時刻はUTC）で着陸できる空港が唯一か
"""

NIGHT_START = 19 * 60   # 夜間: JST 19:00〜翌5:00
NIGHT_END = 5 * 60


def notam_active(notam, day, minute):
    """NOTAMが (day, minute) 時点で有効か。時刻はNOTAMと同じ基準系で渡す。"""
    s, e = notam["start_day"], notam["end_day"]
    win = notam.get("window")  # None=終日, (ws, we) 分単位。we>1440は日またぎ
    if win is None:
        return s <= day <= e
    ws, we = win
    if we <= 1440:  # 日をまたがない時間帯
        return s <= day <= e and ws <= minute < we
    # 日をまたぐ時間帯（例 23:00〜翌06:00）
    if s <= day <= e and minute >= ws:
        return True
    return s <= day - 1 <= e and minute < (we - 1440)


def can_land(airport, day, minute, jst_minute):
    """到着時点で着陸可能か。day/minuteはNOTAM基準系、jst_minuteは夜間判定用JST時刻。"""
    closed_runways = set()
    for n in airport["notams"]:
        if not notam_active(n, day, minute):
            continue
        if n["kind"] == "TWY_CLSD":
            continue  # 誘導路閉鎖は離着陸可
        if n["kind"] == "LGT_US":
            is_night = jst_minute >= NIGHT_START or jst_minute < NIGHT_END
            if is_night:
                closed_runways.update(airport["runways"])
            continue
        if n["kind"] == "RWY_CLSD":
            closed_runways.add(n.get("rwy", airport["runways"][0]))
    return any(r not in closed_runways for r in airport["runways"])


# ---------- 問1: JST 7/10 11:30、全空港滑走路1本 ----------
Q1_AIRPORTS = {
    "A": {"runways": ["R"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 1, "end_day": 9, "window": None}]},
    "B": {"runways": ["R"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 8, "end_day": 12,
         "window": (13 * 60, 17 * 60)}]},
    "C": {"runways": ["R"], "notams": [
        {"kind": "TWY_CLSD", "start_day": 10, "end_day": 15, "window": None}]},
    "D": {"runways": ["R"], "notams": [
        {"kind": "LGT_US", "start_day": 5, "end_day": 20, "window": None}]},
    "E": {"runways": ["R"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 9, "end_day": 11,
         "window": (9 * 60, 15 * 60)}]},
}

# ---------- 問2: UTC 7/9 23:30（= JST 7/10 08:30）----------
Q2_AIRPORTS = {
    "A": {"runways": ["16L/34R", "16R/34L"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "16L/34R", "start_day": 1, "end_day": 31, "window": None},
        {"kind": "TWY_CLSD", "start_day": 9, "end_day": 12, "window": None}]},
    "B": {"runways": ["R"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 9, "end_day": 11,
         "window": (21 * 60, 24 * 60)},
        {"kind": "LGT_US", "start_day": 1, "end_day": 20, "window": None}]},
    "C": {"runways": ["R"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 5, "end_day": 9, "window": None},
        {"kind": "TWY_CLSD", "start_day": 10, "end_day": 12, "window": None}]},
    "D": {"runways": ["R"], "notams": [
        {"kind": "LGT_US", "start_day": 1, "end_day": 20, "window": None},
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 9, "end_day": 10,
         "window": (23 * 60, 30 * 60)}]},  # 23:00〜翌06:00
    "E": {"runways": ["R"], "notams": [
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 10, "end_day": 15, "window": None},
        {"kind": "RWY_CLSD", "rwy": "R", "start_day": 6, "end_day": 9,
         "window": (12 * 60, 24 * 60)}]},
}


def verify_q1():
    day, minute = 10, 11 * 60 + 30  # JST 7/10 11:30
    result = {k: can_land(v, day, minute, jst_minute=minute) for k, v in Q1_AIRPORTS.items()}
    blocked = [k for k, ok in result.items() if not ok]
    print("問1 着陸可否:", result)
    assert blocked == ["E"], f"着陸不可空港が一意でない: {blocked}"
    print("問1 OK: 着陸できない空港は E のみ → 正解(5)")


def verify_q2():
    day, minute = 9, 23 * 60 + 30       # UTC 7/9 23:30
    jst_minute = 8 * 60 + 30            # JST 08:30（昼間）
    result = {k: can_land(v, day, minute, jst_minute) for k, v in Q2_AIRPORTS.items()}
    usable = [k for k, ok in result.items() if ok]
    print("問2 着陸可否:", result)
    assert usable == ["A"], f"着陸可能空港が一意でない: {usable}"
    print("問2 OK: 着陸できる空港は A のみ → 正解(1)")


def verify_all_conditions_needed():
    """問2: 各妨害NOTAMを外すと当該空港が着陸可能になる（条件がすべて効いている）ことを確認"""
    day, minute, jst = 9, 23 * 60 + 30, 8 * 60 + 30
    for name, blocker_idx in [("B", 0), ("C", 0), ("D", 1), ("E", 1)]:
        ap = Q2_AIRPORTS[name]
        reduced = {"runways": ap["runways"],
                   "notams": [n for i, n in enumerate(ap["notams"]) if i != blocker_idx]}
        assert can_land(reduced, day, minute, jst), f"{name}: 妨害NOTAM以外で閉塞している"
    print("問2 OK: 各空港の閉鎖はそれぞれ1件のNOTAMのみに依存")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    verify_all_conditions_needed()
    print("\n全検証パス: 問1正解=(5) E空港 / 問2正解=(1) A空港")
