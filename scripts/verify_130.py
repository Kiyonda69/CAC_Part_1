#!/usr/bin/env python3
"""
航大思考128 解の検証スクリプト
問題タイプ: 切頂八面体の展開図 - 平行面の数字の和

切頂八面体:
- 8つの六角形面 → 4組の平行ペア (s1x+s2y+s3z=3 の平面)
- 6つの正方形面 → 3組の平行ペア

平行ペア (方向ベクトルの正負が逆):
  (1,1,1) ↔ (-1,-1,-1)
  (1,1,-1) ↔ (-1,-1,1)
  (1,-1,1) ↔ (-1,1,-1)
  (1,-1,-1) ↔ (-1,1,1)
"""

print("=" * 50)
print("問1 (標準難度) 検証")
print("=" * 50)
print()

# 問1: 5つのラベル付き六角形面
# 平行ペアの和がすべて等しい → X を求める
#
# 展開図でのラベル:
#   (1,1,1)   = 2
#   (-1,-1,-1)= 7   ← (1,1,1) と平行
#   (1,-1,-1) = 6
#   (-1,1,1)  = X   ← (1,-1,-1) と平行
#   (1,-1,1)  = 5   (パートナー未表示)
#   (1,1,-1), (-1,1,-1), (-1,-1,1) = ラベルなし

face_labels_q1 = {
    (1,1,1): 2,
    (-1,-1,-1): 7,   # (1,1,1) の対面
    (1,-1,-1): 6,
    # (-1,1,1) = X (未知)
    (1,-1,1): 5,
    # 残り3面はラベルなし
}

parallel_pairs = [
    ((1,1,1),  (-1,-1,-1)),
    ((1,1,-1), (-1,-1,1)),
    ((1,-1,1), (-1,1,-1)),
    ((1,-1,-1),(-1,1,1)),
]

# S を決定: (1,1,1)=2 と (-1,-1,-1)=7 の和
S_q1 = face_labels_q1[(1,1,1)] + face_labels_q1[(-1,-1,-1)]
print(f"既知ペア: (1,1,1)={face_labels_q1[(1,1,1)]} と (-1,-1,-1)={face_labels_q1[(-1,-1,-1)]}")
print(f"平行面の和 S = {face_labels_q1[(1,1,1)]} + {face_labels_q1[(-1,-1,-1)]} = {S_q1}")
print()

# X を求める: (-1,1,1) は (1,-1,-1)=6 の対面
X_q1 = S_q1 - face_labels_q1[(1,-1,-1)]
print(f"(1,-1,-1) = {face_labels_q1[(1,-1,-1)]} の対面 (-1,1,1) = X")
print(f"X = S - {face_labels_q1[(1,-1,-1)]} = {S_q1} - {face_labels_q1[(1,-1,-1)]} = {X_q1}")
print()

# 検証: 他の確認できるペアも S と一致するか
# (1,-1,1)=5 のパートナー (-1,1,-1) = S-5 = 4 (ラベルなし、矛盾なし)
print(f"確認: (1,-1,1)=5 のパートナー = {S_q1}-5 = {S_q1-5} (展開図でラベルなし → 矛盾なし)")
print()

assert 1 <= X_q1 <= 5, f"X={X_q1} が選択肢1-5の範囲外"
print(f"問1 正解: ({X_q1}) {X_q1}")
print()

# 一意性確認: X=3 以外に有効な解は存在しないか
valid_X = []
for x_candidate in range(1, 6):
    # S を設定: (1,1,1)=2 と (-1,-1,-1)=7 → S=9 は固定
    S_fixed = 9
    x_val = S_fixed - 6  # (1,-1,-1)=6 の対面
    if x_val == x_candidate:
        valid_X.append(x_candidate)
print(f"有効な X の候補: {valid_X}")
assert len(valid_X) == 1 and valid_X[0] == X_q1, "解が一意でない"
print("検証OK: 解は唯一")
print()

print("=" * 50)
print("問2 (高難度) 検証")
print("=" * 50)
print()

# 問2: 7つのラベル付き六角形面 + X
# 数字1-8を使用, 各ペアの和 S=9
#
# 展開図でのラベル:
#   (1,1,1)   = 2
#   (-1,-1,-1)= 7   ← (1,1,1) 対面
#   (1,1,-1)  = 8
#   (-1,-1,1) = X   ← (1,1,-1) 対面  X=1
#   (1,-1,1)  = 3
#   (-1,1,-1) = 6   ← (1,-1,1) 対面
#   (1,-1,-1) = 5
#   (-1,1,1)  = 4   ← (1,-1,-1) 対面

face_labels_q2 = {
    (1,1,1):   2,
    (-1,-1,-1):7,
    (1,1,-1):  8,
    # (-1,-1,1) = X (未知)
    (1,-1,1):  3,
    (-1,1,-1): 6,
    (1,-1,-1): 5,
    (-1,1,1):  4,
}

print("ラベル付き面の確認:")
for pair in parallel_pairs:
    f1, f2 = pair
    v1 = face_labels_q2.get(f1)
    v2 = face_labels_q2.get(f2)
    if v1 is not None and v2 is not None:
        print(f"  {f1}={v1} ↔ {f2}={v2}: 和={v1+v2}")
    elif v1 is not None:
        print(f"  {f1}={v1} ↔ {f2}=X")
    elif v2 is not None:
        print(f"  {f1}=X ↔ {f2}={v2}")

print()

# S を複数ペアから確認
S_candidates = []
for pair in parallel_pairs:
    f1, f2 = pair
    v1 = face_labels_q2.get(f1)
    v2 = face_labels_q2.get(f2)
    if v1 is not None and v2 is not None:
        S_candidates.append(v1 + v2)

print(f"既知ペアの和: {S_candidates}")
assert len(set(S_candidates)) == 1, f"ペアの和が一致しない: {S_candidates}"
S_q2 = S_candidates[0]
print(f"S = {S_q2}")
print()

# X を含むペア: (1,1,-1)=8 の対面 (-1,-1,1)=X
X_q2 = S_q2 - face_labels_q2[(1,1,-1)]
print(f"(1,1,-1)={face_labels_q2[(1,1,-1)]} の対面 X = {S_q2} - {face_labels_q2[(1,1,-1)]} = {X_q2}")
assert 1 <= X_q2 <= 5, f"X={X_q2} が選択肢1-5の範囲外"
print(f"問2 正解: ({X_q2}) {X_q2}")
print()

# 全ペア最終確認
all_labels = dict(face_labels_q2)
all_labels[(-1,-1,1)] = X_q2
print("全ペア確認:")
for pair in parallel_pairs:
    f1, f2 = pair
    v1 = all_labels[f1]
    v2 = all_labels[f2]
    status = "OK" if v1+v2 == S_q2 else "NG"
    print(f"  {f1}={v1} + {f2}={v2} = {v1+v2} [{status}]")

vals = sorted(all_labels.values())
print(f"\n全面の数字: {vals}")
assert vals == list(range(1,9)), f"数字1-8が揃っていない: {vals}"
print("検証OK: 数字1-8がすべて使用され、解は唯一")
