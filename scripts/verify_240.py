#!/usr/bin/env python3
"""航大思考240: 曲技飛行の機体姿勢追跡問題の検証

機体の姿勢を直交する3つの単位ベクトル（機首n・上面u・右翼r）で表し、
ロール・ピッチ操作を機体軸まわりの90°回転として厳密にシミュレートする。
正解の一意性（正解手順の結果が選択肢のうち1つだけに一致すること）と、
各誤答が典型的な誤り手順に対応することを確認する。
"""

# 方向ベクトル（x=東, y=北, z=上）
DIRS = {
    (1, 0, 0): "東", (-1, 0, 0): "西",
    (0, 1, 0): "北", (0, -1, 0): "南",
    (0, 0, 1): "真上", (0, 0, -1): "真下",
}
E, W = (1, 0, 0), (-1, 0, 0)
N, S = (0, 1, 0), (0, -1, 0)
U, D = (0, 0, 1), (0, 0, -1)


def neg(v):
    return (-v[0], -v[1], -v[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


class Plane:
    """姿勢: nose(機首), up(上面=垂直尾翼側), right(右翼) の正規直交系"""

    def __init__(self, nose, up):
        self.n, self.u = nose, up
        self.r = cross(nose, up)  # 右翼方向

    def check(self):
        assert cross(self.n, self.u) == self.r
        assert sum(x * x for x in self.n) == 1
        assert sum(x * x for x in self.u) == 1

    def roll_right(self):   # 機首軸まわり: 上面→旧右翼, 右翼→旧上面の逆
        self.u, self.r = self.r, neg(self.u)
        self.check()

    def roll_left(self):
        self.u, self.r = neg(self.r), self.u
        self.check()

    def pitch_up(self):     # 右翼軸まわり: 機首→旧上面, 上面→旧機首の逆
        self.n, self.u = self.u, neg(self.n)
        self.check()

    def pitch_down(self):
        self.n, self.u = neg(self.u), self.n
        self.check()

    def state(self):
        return (DIRS[self.n], DIRS[self.u])


def run(nose, up, ops):
    p = Plane(nose, up)
    for op in ops:
        getattr(p, op)()
    return p.state()


def verify_q(label, nose, up, procedures, options, correct_key):
    """procedures: {手順名: 操作列}。正解手順の結果が唯一の選択肢に一致するか検証"""
    results = {name: run(nose, up, ops) for name, ops in procedures.items()}
    ans = results[correct_key]
    matched = [no for no, st in options.items() if st == ans]
    assert len(matched) == 1, f"{label}: 正解一致の選択肢が{len(matched)}個"
    # 全選択肢が互いに異なること
    assert len(set(options.values())) == len(options), f"{label}: 選択肢に重複"
    print(f"{label}: 正解手順の結果 = 機首{ans[0]}・尾翼{ans[1]} → 選択肢({matched[0]})")
    for name, st in results.items():
        hit = [no for no, s in options.items() if s == st]
        print(f"  手順[{name}] → 機首{st[0]}・尾翼{st[1]} → 選択肢{hit or 'なし'}")
    return matched[0]


# ===== 問1 =====
# 初期: 機首=北, 上面=真上。操作: 右ロール90° → 引き起こし90°
q1_proc = {
    "正解(右ロール→引き起こし)": ["roll_right", "pitch_up"],
    "罠:ロール無視": ["pitch_up"],
    "罠:左ロールと取り違え": ["roll_left", "pitch_up"],
    "罠:引き起こしを機首下げと誤解": ["roll_right", "pitch_down"],
    "罠:操作を逆順に適用": ["pitch_up", "roll_right"],
}
q1_options = {
    1: ("東", "真上"),   # 尾翼の変化を忘れる
    2: ("真上", "南"),   # ロール無視
    3: ("西", "南"),     # 左ロール
    4: ("東", "南"),     # 正解
    5: ("真上", "東"),   # 逆順適用
}
a1 = verify_q("問1", N, U, q1_proc, q1_options, "正解(右ロール→引き起こし)")

# ===== 問2 =====
# 初期: 機首=東, 上面=真上。操作: 引き起こし90° → 右ロール90° → 引き起こし90°
q2_proc = {
    "正解(引き起こし→右ロール→引き起こし)": ["pitch_up", "roll_right", "pitch_up"],
    "罠:ロール無視(引き起こし2回)": ["pitch_up", "pitch_up"],
    "罠:左ロールと取り違え": ["pitch_up", "roll_left", "pitch_up"],
    "罠:最後を機首下げと誤解": ["pitch_up", "roll_right", "pitch_down"],
}
q2_options = {
    1: ("北", "真上"),   # 最後を機首下げ
    2: ("西", "真下"),   # ロール無視
    3: ("北", "真下"),   # 左ロール
    4: ("南", "真下"),   # 正解（背面飛行で南進）
    5: ("南", "真上"),   # 尾翼の変化を忘れる
}
a2 = verify_q("問2", E, U, q2_proc, q2_options, "正解(引き起こし→右ロール→引き起こし)")

print(f"\n検証OK: 問1の正解=({a1}), 問2の正解=({a2})（正解番号は後でランダム配置に差し替え）")
