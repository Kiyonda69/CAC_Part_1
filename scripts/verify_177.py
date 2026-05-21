"""
航大思考177 解の一意性検証

問1: 東京(東経135°)を5月20日 20:00(日本時間)に出発し、ロサンゼルス(西経120°)へ
     10時間のフライト。ロサンゼルス到着時の現地日時を求める。

問2: 東京(東経135°)を3月10日 21:00(日本時間)に出発し、シカゴ(西経90°)に
     3月10日 18:30(現地時間)に到着した。所要時間を求める。
"""
from datetime import datetime, timedelta


def utc_offset_from_longitude(deg_east):
    """経度からUTCオフセット(時間)を返す。東経正、西経負。"""
    return deg_east / 15


def verify_q1():
    """問1: 東京→ロサンゼルス 10時間飛行、現地到着日時"""
    tokyo_offset = utc_offset_from_longitude(135)   # +9
    la_offset = utc_offset_from_longitude(-120)     # -8
    diff = tokyo_offset - la_offset                 # 17時間 LAが遅い

    # 出発: 5月20日 20:00 東京時間
    dep_tokyo = datetime(2026, 5, 20, 20, 0)
    flight = timedelta(hours=10)
    arr_tokyo = dep_tokyo + flight                  # 5月21日 06:00 東京
    arr_la = arr_tokyo - timedelta(hours=diff)      # LAローカル時刻

    print(f"問1: 東京UTC{tokyo_offset:+.0f} / LA UTC{la_offset:+.0f} / 時差{diff:.0f}時間")
    print(f"  東京出発(JST): {dep_tokyo}")
    print(f"  東京基準到着(JST): {arr_tokyo}")
    print(f"  LA到着(現地): {arr_la}")
    assert arr_la == datetime(2026, 5, 20, 13, 0), f"想定外: {arr_la}"
    return arr_la


def verify_q2():
    """問2: 東京→シカゴ、東京21:00発→シカゴ18:30着、所要時間"""
    tokyo_offset = utc_offset_from_longitude(135)   # +9
    chi_offset = utc_offset_from_longitude(-90)     # -6
    diff = tokyo_offset - chi_offset                # 15時間 シカゴが遅い

    dep_tokyo = datetime(2026, 3, 10, 21, 0)
    arr_chi_local = datetime(2026, 3, 10, 18, 30)
    arr_chi_tokyo = arr_chi_local + timedelta(hours=diff)
    flight = arr_chi_tokyo - dep_tokyo

    print(f"問2: 東京UTC{tokyo_offset:+.0f} / シカゴ UTC{chi_offset:+.0f} / 時差{diff:.0f}時間")
    print(f"  東京出発(JST): {dep_tokyo}")
    print(f"  シカゴ到着(現地): {arr_chi_local}")
    print(f"  シカゴ到着(東京基準): {arr_chi_tokyo}")
    print(f"  所要時間: {flight}")
    assert flight == timedelta(hours=12, minutes=30), f"想定外: {flight}"
    return flight


def verify_uniqueness_q1():
    """問1の選択肢の中で正解が一つだけであることを確認"""
    candidates = [
        ("5月20日 13:00", datetime(2026, 5, 20, 13, 0)),
        ("5月20日 23:00", datetime(2026, 5, 20, 23, 0)),
        ("5月21日 06:00", datetime(2026, 5, 21, 6, 0)),
        ("5月21日 13:00", datetime(2026, 5, 21, 13, 0)),
        ("5月19日 13:00", datetime(2026, 5, 19, 13, 0)),
    ]
    answer = verify_q1()
    matches = [c for c in candidates if c[1] == answer]
    print(f"問1正解候補一致: {[m[0] for m in matches]}")
    assert len(matches) == 1, f"一意解でない: {matches}"


def verify_uniqueness_q2():
    candidates = [
        ("12時間30分", timedelta(hours=12, minutes=30)),
        ("11時間30分", timedelta(hours=11, minutes=30)),
        ("13時間30分", timedelta(hours=13, minutes=30)),
        ("12時間", timedelta(hours=12)),
        ("14時間", timedelta(hours=14)),
    ]
    answer = verify_q2()
    matches = [c for c in candidates if c[1] == answer]
    print(f"問2正解候補一致: {[m[0] for m in matches]}")
    assert len(matches) == 1, f"一意解でない: {matches}"


if __name__ == "__main__":
    verify_uniqueness_q1()
    print()
    verify_uniqueness_q2()
    print("\n検証成功: 解は一意")
