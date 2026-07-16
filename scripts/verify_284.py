#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考284 検証スクリプト
テーマ: 小立方体の切断個数（分割した立方体を平面で切ると何個切られるか）

1辺3cmの立方体を1cm角の小立方体27個に分割（切り離さず目印線のみ）。
小立方体 (i,j,k) は [i,i+1]x[j,j+1]x[k,k+1]  (i,j,k in 0..2)

問1: 頂点A(0,0,0)から出る3辺の反対端 B(3,0,0)・D(0,3,0)・E(0,0,3)
     を通る平面 x+y+z=3 で切断 → 切断される小立方体の個数
問2: 対角線AG(A(0,0,0)-G(3,3,3))に垂直で立方体の中心を通る平面
     x+y+z=4.5（6本の辺の中点を通り断面は正六角形）
     → 切断されない小立方体の個数

「切断される」= 平面が小立方体の内部を通り2つの部分に分ける
（頂点や辺で接するだけのものは切断されない）
"""
from itertools import product


def count_cut(plane_value):
    """平面 x+y+z = plane_value に内部を切られる小立方体の数"""
    cut = []
    for i, j, k in product(range(3), repeat=3):
        smin = i + j + k          # 最小頂点の座標和
        smax = i + j + k + 3      # 最大頂点の座標和
        # 内部を通る ⇔ smin < plane_value < smax
        if smin < plane_value < smax:
            cut.append((i, j, k))
    return cut


def layer_breakdown(cubes):
    """z方向の層(k=0,1,2)ごとの個数"""
    return [sum(1 for c in cubes if c[2] == k) for k in range(3)]


def main():
    # ---- 問1: 平面 x+y+z=3 ----
    cut1 = count_cut(3)
    print("問1 平面 x+y+z=3 (B・D・Eを通る)")
    print(f"  切断される小立方体: {len(cut1)}個")
    print(f"  層別(下・中・上): {layer_breakdown(cut1)}")
    # 頂点で接するだけの小立方体（切断されない）を確認
    touch1 = [(i, j, k) for i, j, k in product(range(3), repeat=3)
              if (i + j + k == 3 or i + j + k + 3 == 3)
              and not (i + j + k < 3 < i + j + k + 3)]
    print(f"  頂点で接するのみ(非切断): {touch1}")
    assert len(cut1) == 9, f"問1: 期待9個, 実際{len(cut1)}個"
    assert layer_breakdown(cut1) == [5, 3, 1]

    # ---- 問2: 平面 x+y+z=4.5 ----
    cut2 = count_cut(4.5)
    uncut2 = [(i, j, k) for i, j, k in product(range(3), repeat=3)
              if (i, j, k) not in cut2]
    print("\n問2 平面 x+y+z=4.5 (辺の中点6つ・断面正六角形)")
    print(f"  切断される小立方体: {len(cut2)}個")
    print(f"  層別(下・中・上): {layer_breakdown(cut2)}")
    print(f"  切断されない小立方体: {len(uncut2)}個")
    print(f"  非切断の内訳: {sorted(uncut2)}")
    assert len(cut2) == 19, f"問2: 切断19個のはず, 実際{len(cut2)}個"
    assert len(uncut2) == 8, f"問2: 非切断8個のはず, 実際{len(uncut2)}個"
    assert layer_breakdown(cut2) == [6, 7, 6]
    # 非切断はA側4個(座標和0,1)とG側4個(座標和5,6)
    a_side = [c for c in uncut2 if sum(c) <= 1]
    g_side = [c for c in uncut2 if sum(c) >= 5]
    assert len(a_side) == 4 and len(g_side) == 4
    print(f"  A側(頂点A周り): {sorted(a_side)} = 4個")
    print(f"  G側(頂点G周り): {sorted(g_side)} = 4個")

    # 断面が正六角形であることの確認（辺の中点6つが平面上）
    midpoints = [(3, 1.5, 0), (1.5, 3, 0), (0, 3, 1.5),
                 (0, 1.5, 3), (1.5, 0, 3), (3, 0, 1.5)]
    for p in midpoints:
        assert abs(sum(p) - 4.5) < 1e-9
    print("\n  辺の中点6点はすべて平面 x+y+z=4.5 上 → 断面は正六角形")

    print("\n検証OK: 問1=9個(切断) / 問2=8個(非切断・切断は19個)")


if __name__ == "__main__":
    main()
