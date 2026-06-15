# -*- coding: utf-8 -*-
"""航大思考225 立方体ULDコンテナの切断面検証
立方体 [0,L]^3 を平面で切断したときの断面多角形を求める。
平面: n・(x - p0) = 0  ->  a x + b y + c z = d
立方体の12辺と平面の交点を求め、面ごとに線分を集めて多角形を構成。
"""
import itertools, math

L = 6
verts = [(x,y,z) for x in (0,L) for y in (0,L) for z in (0,L)]

# 立方体の12辺（頂点インデックスのペア）
edges = []
for i in range(8):
    for j in range(i+1,8):
        # 1座標だけ異なる = 辺
        diff = sum(1 for a,b in zip(verts[i],verts[j]) if a!=b)
        if diff == 1:
            edges.append((i,j))

def cross_section(a,b,c,d):
    """平面 a x + b y + c z = d と立方体辺の交点集合"""
    pts = []
    def f(v): return a*v[0]+b*v[1]+c*v[2]-d
    for i,j in edges:
        vi, vj = verts[i], verts[j]
        fi, fj = f(vi), f(vj)
        if abs(fi) < 1e-9:
            pts.append(vi)
        if abs(fj) < 1e-9:
            pts.append(vj)
        if fi*fj < -1e-12:
            t = fi/(fi-fj)
            p = tuple(vi[k]+t*(vj[k]-vi[k]) for k in range(3))
            pts.append(p)
    # 重複除去
    uniq=[]
    for p in pts:
        if not any(all(abs(p[k]-q[k])<1e-6 for k in range(3)) for q in uniq):
            uniq.append(p)
    return uniq

def classify(pts):
    """断面多角形の頂点を平面内で角度順に並べ、辺長を返す"""
    n = len(pts)
    cx = sum(p[0] for p in pts)/n
    cy = sum(p[1] for p in pts)/n
    cz = sum(p[2] for p in pts)/n
    c = (cx,cy,cz)
    # 平面の基底を作る
    # 法線
    # 任意の2点で
    import numpy as np
    P = [np.array(p)-np.array(c) for p in pts]
    # 法線推定
    nv = np.cross(P[0], P[1])
    if np.linalg.norm(nv) < 1e-9:
        nv = np.cross(P[0], P[2])
    nv = nv/np.linalg.norm(nv)
    u = P[0]/np.linalg.norm(P[0])
    w = np.cross(nv,u)
    ang = []
    for p in P:
        ang.append((math.atan2(np.dot(p,w), np.dot(p,u)), p))
    ang.sort()
    ordered = [c + p for _,p in ang]
    sides=[]
    m=len(ordered)
    for i in range(m):
        d = np.linalg.norm(ordered[i]-ordered[(i+1)%m])
        sides.append(round(d,3))
    return m, sides

import numpy as np

print("== 問1: 平面が上面の1辺と底面の対辺を通る斜め切断 ==")
# 上面 z=L の辺 y=0 (x:0->L) と 底面 z=0 の辺 y=L
# 点(0,0,L),(L,0,L),(0,L,0),(L,L,0) を通る -> 平面 b y + c z = d
# (0,0,L): cL=d ; (0,L,0): bL=d => b=c, d=cL. 平面: y + z = L
pts1 = cross_section(0,1,1,L)
print("頂点数,辺長:", classify(pts1), " 頂点:", [tuple(round(x,2) for x in p) for p in pts1])

print("\n== 問2: 3辺の中点を通る切断（正六角形）==")
# 平面 x+y+z = 1.5L が立方体中心を通り正六角形
pts2 = cross_section(1,1,1,1.5*L)
print("頂点数,辺長:", classify(pts2), " 頂点:", [tuple(round(x,2) for x in p) for p in pts2])

print("\n== 参考: 1頂点近傍3中点を通る正三角形 ==")
# 原点付近の3辺中点 (L/2,0,0),(0,L/2,0),(0,0,L/2): x+y+z=L/2
pts3 = cross_section(1,1,1,0.5*L)
print("頂点数,辺長:", classify(pts3))

print("\n== 参考: 五角形になる切断 ==")
# x + y + z = 2L のような? 試す
for d in [0.5*L,1.0*L,1.5*L,2.0*L,2.5*L]:
    p = cross_section(1,1,1,d)
    print(f"x+y+z={d}:", classify(p)[0],"頂点")

print("\n== 五角形探索 ==")
found=False
# 整数/半整数係数の平面を総当たり
for a in range(1,4):
  for b in range(1,4):
    for c in range(1,4):
      for d2 in range(1,40):
        d = d2/2
        p = cross_section(a,b,c,d)
        if len(p)==5:
          try:
            m,sides=classify(p)
          except Exception:
            continue
          if m==5:
            print(f"五角形: 法線({a},{b},{c}) d={d} 辺長={sides}")
            print("  頂点:", [tuple(round(x,2) for x in q) for q in p])
            found=True
            break
      if found: break
    if found: break
  if found: break
