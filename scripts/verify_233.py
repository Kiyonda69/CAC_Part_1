# -*- coding: utf-8 -*-
"""
航大思考233 検証コード
テーマ: 滑走路の方位番号 + 回転したコンパス（方位盤）による空間方位認識
規則:
  滑走路番号 = (滑走路が向く磁方位[度]) / 10 を四捨五入(0.5切り上げ)した2桁数。
  北=360->36, 東=090->09, 南=180->18, 西=270->27。
  滑走路の両端には、その端から進入する向きの方位に対応する番号が描かれる。
"""
import math

def heading_to_number(bearing):
    """方位(度, 0-360)を滑走路番号(1-36)に変換。0.5は切り上げ。"""
    b = bearing % 360
    if b == 0:
        b = 360
    # 10で割り四捨五入(round half up)
    n = math.floor(b / 10 + 0.5)
    if n == 0:
        n = 36
    if n > 36:
        n -= 36
    return n

def fmt(n):
    return f"{n:02d}"

# ---- 確認: 基本対応 ----
assert heading_to_number(360) == 36
assert heading_to_number(180) == 18
assert heading_to_number(90) == 9
assert heading_to_number(270) == 27
assert heading_to_number(45) == 5    # 4.5 -> 5
assert heading_to_number(225) == 23  # 22.5 -> 23
assert heading_to_number(315) == 32  # 31.5 -> 32
assert heading_to_number(135) == 14  # 13.5 -> 14

print("=== 問1 (北が上の地図) ===")
# 滑走路ア: 北東-南西 の対角線(45度/225度)
# 滑走路イ: 南北(縦, 0/180度)
# 航空機は南西側から進入し、北東へ向かって着陸 -> 進行方位=045度
travel = 45
num1 = heading_to_number(travel)
print(f"進行方位 {travel}度 -> 着陸端の番号 {fmt(num1)}")
# 反対側端
opp1 = heading_to_number((travel+180) % 360)
print(f"反対側端(北東側の番号) = {fmt(opp1)}  ※罠")
# 南北滑走路の番号
print(f"南北滑走路 = {fmt(heading_to_number(360))}/{fmt(heading_to_number(180))}")
ans1 = fmt(num1)
print(f"問1 正解 = {ans1}")

print()
print("=== 問2 (回転した方位盤: 真北が紙面の右を指す) ===")
# 紙面上で 真北 = +x(右), 方位は時計回り。
# 紙面ベクトル(dx,dy) (画面座標は y下向きだが、ここでは数学座標 y上向きで扱う)
def page_dir_to_bearing(dx, dy):
    """紙面方向(数学座標, y上)から真方位を求める。真北=+x, 時計回り。"""
    alpha = math.degrees(math.atan2(dy, dx)) % 360  # +xからの反時計回り角
    bearing = (360 - alpha) % 360                    # 時計回り角=真方位
    return bearing

# 滑走路は紙面の左下-右上の対角線。航空機は右上へ向かって進む。
b_upper_right = page_dir_to_bearing(1, 1)   # 右上
b_lower_left  = page_dir_to_bearing(-1, -1) # 左下
print(f"紙面 右上 方向 = 真方位 {b_upper_right}度 -> 番号 {fmt(heading_to_number(b_upper_right))}")
print(f"紙面 左下 方向 = 真方位 {b_lower_left}度 -> 番号 {fmt(heading_to_number(b_lower_left))}")
num2 = heading_to_number(b_upper_right)
ans2 = fmt(num2)
# 罠: 回転を無視して紙面上を北上と誤認 -> 右上=北東=045=05
trap_naive = heading_to_number(45)
print(f"罠(回転無視, 右上を北東と誤認) = {fmt(trap_naive)}")
print(f"問2 正解 = {ans2}")

print()
print("=== 選択肢の一意性確認 ===")
opts1 = [fmt(5), fmt(23), fmt(36), fmt(18), fmt(14)]
opts2 = [fmt(32), fmt(5), fmt(14), fmt(9), fmt(27)]
assert len(set(opts1)) == 5, "問1選択肢に重複"
assert len(set(opts2)) == 5, "問2選択肢に重複"
assert ans1 in opts1 and opts1.count(ans1) == 1
assert ans2 in opts2 and opts2.count(ans2) == 1
print(f"問1 選択肢 {opts1}  正解 {ans1} (位置 {opts1.index(ans1)+1})")
print(f"問2 選択肢 {opts2}  正解 {ans2} (位置 {opts2.index(ans2)+1})")
print("検証OK: 各問の正解は選択肢中ただ1つ")
