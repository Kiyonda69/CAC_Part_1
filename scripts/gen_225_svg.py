# -*- coding: utf-8 -*-
import math
L=6
# キャビネット投影: 前面(Y=0)は正方形、奥行きYは右上45°へ0.5倍
def cab(X,Y,Z,k=26,d=0.5,ox=70,oy=235):
    a=math.radians(45)
    sx = ox + X*k + Y*d*k*math.cos(a)
    sy = oy - Z*k - Y*d*k*math.sin(a)
    return (round(sx,1), round(sy,1))
def P(x,y,z): return cab(x,y,z)
v = {n:P(x,y,z) for n,(x,y,z) in {
 'A':(0,0,0),'B':(L,0,0),'C':(L,L,0),'D':(0,L,0),
 'E':(0,0,L),'F':(L,0,L),'G':(L,L,L),'H':(0,L,L)}.items()}
print("頂点:")
for n,p in v.items(): print(f"  {n}: {p}")
print("\n問1断面(E,F,C,D):", " ".join(f"{v[n][0]},{v[n][1]}" for n in ['E','F','C','D']))
mid = {'M1':P(3,0,6),'M2':P(0,3,6),'M3':P(0,6,3),'M4':P(3,6,0),'M5':P(6,3,0),'M6':P(6,0,3)}
print("\n問2 6中点:")
for n,p in mid.items(): print(f"  {n}: {p}")
print("六角形ポリゴン:", " ".join(f"{mid[n][0]},{mid[n][1]}" for n in ['M1','M6','M5','M4','M3','M2']))
print("指定3点 P=M1,Q=M3,R=M5:", mid['M1'],mid['M3'],mid['M5'])
# 範囲確認
xs=[p[0] for p in list(v.values())+list(mid.values())]
ys=[p[1] for p in list(v.values())+list(mid.values())]
print(f"\nX範囲 {min(xs)}-{max(xs)}  Y範囲 {min(ys)}-{max(ys)}")
