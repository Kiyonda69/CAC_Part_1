"""
verify_165.py - 立方体の正六角形断面と展開図の対応検証

問題: 立方体ABCD-EFGHを正六角形になるように切断したとき、
切り口の線が十字型展開図(前面ABFE中央)上のどの位置に現れるかを問う。

立方体座標:
  A=(0,1,1)  B=(1,1,1)  C=(1,1,0)  D=(0,1,0)
  E=(0,0,1)  F=(1,0,1)  G=(1,0,0)  H=(0,0,0)

正六角形断面は立方体の体対角線に垂直な平面で得られる。
体対角線は4本: BH, AG, CE, DF。それぞれ異なる頂点を「切り落とす」。

各面パネルの位置(十字型展開図, 前面中央):
  上面ABCD(前面の上):  A=BL B=BR C=TR D=TL
  前面ABFE(中央):      A=TL B=TR F=BR E=BL
  下面EFGH(前面の下):  E=TL F=TR G=BR H=BL
  左面ADHE(前面の左):  D=TL A=TR E=BR H=BL
  右面BCGF(前面の右):  B=TL C=TR G=BR F=BL
  後面DCGH(右面の右):  C=TL D=TR H=BR G=BL
"""

CUBE = {
    'A': (0, 1, 1), 'B': (1, 1, 1), 'C': (1, 1, 0), 'D': (0, 1, 0),
    'E': (0, 0, 1), 'F': (1, 0, 1), 'G': (1, 0, 0), 'H': (0, 0, 0),
}

EDGES = [
    ('A','B'),('B','C'),('C','D'),('D','A'),
    ('E','F'),('F','G'),('G','H'),('H','E'),
    ('A','E'),('B','F'),('C','G'),('D','H'),
]

FACES = {
    '上': ['A','B','C','D'],   # 上面 ABCD
    '前': ['A','B','F','E'],   # 前面 ABFE
    '下': ['E','F','G','H'],   # 下面 EFGH
    '左': ['A','D','H','E'],   # 左面 ADHE
    '右': ['B','C','G','F'],   # 右面 BCGF
    '後': ['D','C','G','H'],   # 後面 DCGH
}

NET_POS = {
    '上': {'A':'BL','B':'BR','C':'TR','D':'TL'},
    '前': {'A':'TL','B':'TR','F':'BR','E':'BL'},
    '下': {'E':'TL','F':'TR','G':'BR','H':'BL'},
    '左': {'D':'TL','A':'TR','E':'BR','H':'BL'},
    '右': {'B':'TL','C':'TR','G':'BR','F':'BL'},
    '後': {'C':'TL','D':'TR','H':'BR','G':'BL'},
}

DIAGONALS = {
    'BH': (('B','H'), (-1,-1,-1)),
    'AG': (('A','G'), ( 1,-1,-1)),
    'CE': (('C','E'), (-1,-1, 1)),
    'DF': (('D','F'), ( 1,-1, 1)),
}


def midpoint(p1, p2):
    return tuple((a+b)/2 for a, b in zip(p1, p2))


def plane_value(point, normal, center=(0.5,0.5,0.5)):
    return sum(n*(p-c) for n,p,c in zip(normal, point, center))


def cut_edges_for_diagonal(diag_key):
    """対角線に垂直な平面が中点で交差する6本の辺を返す"""
    _, normal = DIAGONALS[diag_key]
    cut = []
    for u, v in EDGES:
        pu, pv = CUBE[u], CUBE[v]
        vu, vv = plane_value(pu, normal), plane_value(pv, normal)
        # 平面通過判定: 中点で値0なら通過
        mid = midpoint(pu, pv)
        if abs(plane_value(mid, normal)) < 1e-9 and vu * vv < 0:
            cut.append((u, v))
    return cut


def cut_corner_per_face(cut_edges):
    """各面で切り落とされる頂点を求める(その面で切られる2辺の共通頂点)"""
    result = {}
    for face_name, verts in FACES.items():
        face_set = set(verts)
        face_cut_edges = [e for e in cut_edges if set(e).issubset(face_set)]
        if len(face_cut_edges) != 2:
            continue
        common = set(face_cut_edges[0]) & set(face_cut_edges[1])
        if len(common) == 1:
            result[face_name] = common.pop()
    return result


def hexagon_pattern(diag_key):
    """対角線に対応する展開図上の切り取り位置を返す"""
    edges = cut_edges_for_diagonal(diag_key)
    corners = cut_corner_per_face(edges)
    return {face: NET_POS[face][v] for face, v in corners.items()}


def is_regular_hexagon(diag_key):
    """切り口が正六角形であることを検証"""
    edges = cut_edges_for_diagonal(diag_key)
    pts = [midpoint(CUBE[u], CUBE[v]) for u, v in edges]
    # 重心からの距離が全て等しい
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    cz = sum(p[2] for p in pts) / len(pts)
    dists = [((p[0]-cx)**2 + (p[1]-cy)**2 + (p[2]-cz)**2)**0.5 for p in pts]
    return all(abs(d - dists[0]) < 1e-9 for d in dists), len(pts) == 6


def main():
    print("=== 4本の体対角線に対応する正六角形断面 ===\n")
    patterns = {}
    for diag in DIAGONALS:
        ok, six = is_regular_hexagon(diag)
        edges = cut_edges_for_diagonal(diag)
        corners = cut_corner_per_face(edges)
        pat = hexagon_pattern(diag)
        patterns[diag] = pat
        print(f"⊥ {diag}: 正六角形={ok}, 6点={six}")
        print(f"  切断辺: {[u+v for u,v in edges]}")
        print(f"  各面で切り落とされる頂点: {corners}")
        print(f"  展開図上の切り取り位置: {pat}\n")

    # 一意性: 4パターンが全て異なることを確認
    sigs = {d: tuple(sorted(p.items())) for d, p in patterns.items()}
    unique = len(set(sigs.values())) == 4
    print(f"4対角線パターンが全て異なる: {unique}")

    # 問1正解(⊥BH)と問2正解(⊥AG)を出力
    print("\n=== 問1正解(⊥BH) ===")
    for f, pos in patterns['BH'].items():
        print(f"  {f}面パネル: {pos}コーナーをカット")
    print("\n=== 問2正解(⊥AG) ===")
    for f, pos in patterns['AG'].items():
        print(f"  {f}面パネル: {pos}コーナーをカット")

    assert unique, "4パターンが重複しています"
    assert all(is_regular_hexagon(d)[0] for d in DIAGONALS), "全断面が正六角形であるべき"
    print("\n✓ 検証完了: 4パターンは全て異なる正六角形断面")


if __name__ == '__main__':
    main()
