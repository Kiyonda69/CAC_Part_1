"""航大思考188 図表用: 立方体の斜投影座標を計算してSVG用座標を出力"""

# 斜投影パラメータ
OX, OY = 70, 255      # E=(0,0,0) のスクリーン位置
SX, SZ = 72, 72       # X, Z 1単位あたりのpx
DYX, DYY = 34, 30     # 奥行きY 1単位あたりの (右, 上) px


def proj(p):
    x, y, z = p
    sx = OX + x*SX + y*DYX
    sy = OY - z*SZ - y*DYY
    return (round(sx, 1), round(sy, 1))


V = {
    'A': (0, 0, 2), 'B': (2, 0, 2), 'C': (2, 2, 2), 'D': (0, 2, 2),
    'E': (0, 0, 0), 'F': (2, 0, 0), 'G': (2, 2, 0), 'H': (0, 2, 0),
}

print("頂点:")
for k in 'ABCDEFGH':
    print(f"  {k} {V[k]} -> {proj(V[k])}")

pts = {
    'midAB': (1, 0, 2),
    'midAD': (0, 1, 2),
    'P_BF': (2, 0, 4/3),
    'P_DH': (0, 2, 4/3),
}
print("問2の追加点:")
for k, p in pts.items():
    print(f"  {k} {tuple(round(x,3) for x in p)} -> {proj(p)}")

xs = [proj(V[k])[0] for k in V] + [proj(p)[0] for p in pts.values()]
ys = [proj(V[k])[1] for k in V] + [proj(p)[1] for p in pts.values()]
print(f"範囲 x:[{min(xs)},{max(xs)}] y:[{min(ys)},{max(ys)}]")
