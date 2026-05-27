"""
航大思考190 解の一意性検証
資料空欄穴埋め問題（情報量が多い資料の読み取り）

問1（標準）: カフェチェーン来客数表。前年同期 × 前年比 から当期合計を求め、
            空欄の月別値を逆算する2段階の読み取り。
問2（高難度）: 4部署×4四半期の経費表。行・列合計と脚注条件から
            連立方程式を解いて空欄を確定する。
"""


def verify_q1():
    """問1: かえで店の3月来客数（空欄）を求める。

    与えられた資料:
    - かえで店: 1月=40, 2月=36, 3月=空欄
    - かえで店 前年同期合計=125, 前年比=96%
    （他店・他列は読み取りの撹乱情報）
    """
    candidates = []
    zenki = 125          # かえで店 前年同期合計
    ratio = 0.96         # 前年比 96%
    jan, feb = 40, 36
    # 3月来客数を総当たり（百人単位、0〜100の整数）
    for march in range(0, 101):
        touki = jan + feb + march           # 当期合計
        # 前年比 = 当期 / 前年 が 96% に一致するか
        if abs(touki - zenki * ratio) < 1e-9:
            candidates.append(march)
    assert len(candidates) == 1, f"問1: 解が{len(candidates)}個 -> {candidates}"
    assert candidates[0] == 44, f"問1: 期待値44だが{candidates[0]}"
    return candidates[0]


def verify_q2():
    """問2: 開発部の第4四半期(エ)を求める。

    表（万円）の確定済み:
      営業部: Q1=180, Q3=220, 部門計=760
      開発部: Q1=150, Q3=140, 部門計=650
      総務部: Q2=100, Q4=120
      製造部: Q2=230, Q4=200
      四半期計: Q2=700, Q4=670
    空欄: a=営業Q2, b=開発Q2, c=営業Q4, d=開発Q4
    脚注: 営業部の第2四半期は第4四半期より40多い (a = c + 40)
    """
    sols = []
    rng = range(0, 401)   # 各空欄の探索範囲
    for a in rng:
        # 営業部 行合計: 180 + a + 220 + c = 760
        c = 760 - 180 - 220 - a
        if c < 0:
            continue
        # 脚注: a = c + 40
        if a != c + 40:
            continue
        for b in rng:
            # 開発部 行合計: 150 + b + 140 + d = 650
            d = 650 - 150 - 140 - b
            if d < 0:
                continue
            # Q2列合計: a + b + 100 + 230 = 700
            if a + b + 100 + 230 != 700:
                continue
            # Q4列合計: c + d + 120 + 200 = 670
            if c + d + 120 + 200 != 670:
                continue
            sols.append((a, b, c, d))
    assert len(sols) == 1, f"問2: 解が{len(sols)}個 -> {sols}"
    a, b, c, d = sols[0]
    assert (a, b, c, d) == (200, 170, 160, 190), f"問2: 想定外 {sols[0]}"
    return d  # エ = 開発部Q4 = 190


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    print(f"問1 一意解: かえで店3月 = {q1}（百人 = {q1*100}人）")
    print(f"問2 一意解: 開発部Q4(エ) = {q2}（万円）")
    print("両問とも解は一意。検証OK")
