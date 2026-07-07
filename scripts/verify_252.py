#!/usr/bin/env python3
"""航大思考252: 洋上航法計画（PNR/ETP）の検証

資料設定:
- A空港 → B空港: 総距離 800 NM、A→B方向の風成分は向かい風30kt（一定）
- 通常巡航: TAS 180 kt, 燃料流量 360 lb/h
- OEI(1発不作動)巡航: TAS 150 kt, 燃料流量 300 lb/h
- 搭載燃料 2,700 lb、最終予備燃料 540 lb（使用不可）

問1: PNR距離（通常巡航で往復する前提）
問2: ETP(OEI基準)まで通常巡航で進み、直後に1発停止して
     OEIで引き返した場合の総飛行時間
"""

from fractions import Fraction as F

# ---------- 共通データ ----------
D_TOTAL = 800          # NM
WIND = 30              # kt 向かい風(A→B方向)
TAS_NORM = 180         # kt
FF_NORM = 360          # lb/h
TAS_OEI = 150          # kt
FUEL_TOTAL = 2700      # lb
FUEL_RESERVE = 540     # lb

# ---------- 問1: PNR ----------
def q1():
    endurance = F(FUEL_TOTAL - FUEL_RESERVE, FF_NORM)   # 滞空可能時間
    gs_out = TAS_NORM - WIND    # 150
    gs_ret = TAS_NORM + WIND    # 210
    # 検証: 距離Dを総当たり(0.5NM刻み)し、往復時間==enduranceとなるDが唯一か
    solutions = []
    d = F(0)
    while d <= 700:
        t = d / gs_out + d / gs_ret
        if t == endurance:
            solutions.append(d)
        d += F(1, 2)
    assert len(solutions) == 1, f"問1: 解が{len(solutions)}個"
    d_pnr = solutions[0]
    # 公式との一致確認
    formula = endurance * gs_out * gs_ret / (gs_out + gs_ret)
    assert d_pnr == formula == 525
    print(f"問1 PNR = {float(d_pnr)} NM (E={float(endurance)}h, GS往={gs_out}, GS復={gs_ret})")
    return d_pnr

# ---------- 問2: ETP + 総飛行時間 ----------
def q2():
    gs_cont = TAS_OEI - WIND    # ETP以降Bへ続行(OEI): 120
    gs_ret = TAS_OEI + WIND     # ETPからAへ帰投(OEI): 180
    gs_norm_out = TAS_NORM - WIND  # A→ETPは通常巡航: 150
    # 検証: Xを総当たりし、続行時間==帰投時間となるXが唯一か
    solutions = []
    x = F(0)
    while x <= D_TOTAL:
        if (D_TOTAL - x) / F(gs_cont) == x / F(gs_ret):
            solutions.append(x)
        x += F(1, 2)
    assert len(solutions) == 1, f"問2: ETP解が{len(solutions)}個"
    x_etp = solutions[0]
    assert x_etp == F(D_TOTAL * gs_ret, gs_cont + gs_ret) == 480
    t_out = x_etp / gs_norm_out          # 3.2 h
    t_back = x_etp / gs_ret              # 2h40m
    total = t_out + t_back
    h = int(total)
    m = (total - h) * 60
    assert m == int(m), "分が整数でない"
    # 整合確認: ETPから続行した場合の時間 == 帰投時間
    assert (D_TOTAL - x_etp) / F(gs_cont) == t_back
    print(f"問2 ETP = {float(x_etp)} NM, 往路{float(t_out)}h + 帰投{float(t_back):.4f}h = {h}時間{int(m)}分")
    return h, int(m)

# ---------- 誤答選択肢の検算 ----------
def distractors():
    E = F(2160, 360)
    print("--- 問1 誤答由来 ---")
    print(f"往路GSで単純折返し E*150/2 = {float(E*150/2)}")          # 450
    print(f"TAS基準 E*180/2 = {float(E*180/2)}")                     # 540
    print(f"復路GSで E*210/2 = {float(E*210/2)}")                    # 630
    print(f"全燃料使用 7.5h公式 = {float(F(75,10)*150*210/360)}")    # 656.25
    print("--- 問2 誤答由来 ---")
    print(f"中間点400NM使用: {float(F(400,150)+F(400,180))*60:.1f}分")   # 4h53m
    print(f"全区間そのまま 800/150: {float(F(800,150))*60:.1f}分")        # 5h20m
    print(f"帰投を通常巡航GS210と誤る: {float(F(480,150)+F(480,210))*60:.1f}分")  # 5h29m
    print(f"A→ETPもOEIと誤る: {float(F(480,120)+F(480,180))*60:.1f}分")  # 6h40m

if __name__ == "__main__":
    q1()
    q2()
    distractors()
    print("検証OK: 問1・問2とも唯一解")
