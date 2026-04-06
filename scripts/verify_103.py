"""
セット103 検証スクリプト
問1: 立方体の展開図（十字型）の頂点Pに集まる3面の特定
問2: T字型展開図の4頂点マーク(P,Q,R,S)の頂点一致判定
"""

from itertools import product

def verify_q1():
    """
    問1: 十字型展開図の頂点Pに集まる3面を特定する

    展開図レイアウト:
              [イ]
    [ア][ウ][エ][オ]
              [カ]

    各面は1x1の正方形。座標:
    - ア: x=[0,1], y=[1,2]
    - ウ: x=[1,2], y=[1,2]
    - エ: x=[2,3], y=[1,2] (中心)
    - オ: x=[3,4], y=[1,2]
    - イ: x=[2,3], y=[0,1]
    - カ: x=[2,3], y=[2,3]

    エを正面に置いた場合の折り畳み:
    - エ = front (y=0)
    - イ = top (z=1) - エの上
    - カ = bottom (z=0) - エの下
    - ウ = left (x=0) - エの左
    - オ = right (x=1) - エの右
    - ア = back (y=1) - ウの左から折り返し

    対面: エ↔ア, イ↔カ, ウ↔オ
    """

    # 面の3D位置定義
    faces = {
        'エ': 'front',  # y=0
        'ア': 'back',   # y=1
        'イ': 'top',    # z=1
        'カ': 'bottom', # z=0
        'ウ': 'left',   # x=0
        'オ': 'right',  # x=1
    }

    opposite_pairs = {
        'エ': 'ア', 'ア': 'エ',
        'イ': 'カ', 'カ': 'イ',
        'ウ': 'オ', 'オ': 'ウ',
    }

    # 8つの立方体頂点に集まる3面
    vertices_3d = {
        (0, 0, 0): {'エ', 'ウ', 'カ'},  # front-left-bottom
        (1, 0, 0): {'エ', 'オ', 'カ'},  # front-right-bottom
        (0, 0, 1): {'エ', 'ウ', 'イ'},  # front-left-top
        (1, 0, 1): {'エ', 'オ', 'イ'},  # front-right-top
        (0, 1, 0): {'ア', 'ウ', 'カ'},  # back-left-bottom
        (1, 1, 0): {'ア', 'オ', 'カ'},  # back-right-bottom
        (0, 1, 1): {'ア', 'ウ', 'イ'},  # back-left-top
        (1, 1, 1): {'ア', 'オ', 'イ'},  # back-right-top
    }

    # 展開図上の各面の頂点 → 3D座標のマッピング
    # エ(front): (2,1)→(0,0,1), (3,1)→(1,0,1), (3,2)→(1,0,0), (2,2)→(0,0,0)
    # イ(top):   (2,0)→(0,1,1), (3,0)→(1,1,1), (3,1)→(1,0,1), (2,1)→(0,0,1)
    # ウ(left):  (1,1)→(0,0,1), (2,1)→already mapped, (2,2)→(0,0,0), (1,2)→(0,1,0)
    #   Actually: ウ folds left from エ's left edge
    #   (1,1)→(0,1,1)? No...

    # Let me redo this carefully.
    # エ = front face at y=0, corners:
    #   (0,0,0), (1,0,0), (1,0,1), (0,0,1)  [BL, BR, TR, TL in front view]
    # Net エ: (2,1)=TL→(0,0,1), (3,1)=TR→(1,0,1), (3,2)=BR→(1,0,0), (2,2)=BL→(0,0,0)

    net_to_3d = {}

    # エ (front face)
    net_to_3d[('エ', 2, 1)] = (0, 0, 1)  # top-left
    net_to_3d[('エ', 3, 1)] = (1, 0, 1)  # top-right
    net_to_3d[('エ', 3, 2)] = (1, 0, 0)  # bottom-right
    net_to_3d[('エ', 2, 2)] = (0, 0, 0)  # bottom-left

    # イ (top face) - folds up from エ's top edge
    # Hinge: (2,1)→(0,0,1) and (3,1)→(1,0,1) at z=1, y=0
    # イ folds backward: y increases
    net_to_3d[('イ', 2, 1)] = (0, 0, 1)  # on hinge
    net_to_3d[('イ', 3, 1)] = (1, 0, 1)  # on hinge
    net_to_3d[('イ', 2, 0)] = (0, 1, 1)  # folded to back
    net_to_3d[('イ', 3, 0)] = (1, 1, 1)  # folded to back

    # ウ (left face) - folds left from エ's left edge
    # Hinge: (2,1)→(0,0,1) and (2,2)→(0,0,0) at x=0, y=0
    # ウ folds to left: going in +y direction from front face
    net_to_3d[('ウ', 2, 1)] = (0, 0, 1)  # on hinge
    net_to_3d[('ウ', 2, 2)] = (0, 0, 0)  # on hinge
    net_to_3d[('ウ', 1, 1)] = (0, 1, 1)  # folded
    net_to_3d[('ウ', 1, 2)] = (0, 1, 0)  # folded

    # オ (right face) - folds right from エ's right edge
    # Hinge: (3,1)→(1,0,1) and (3,2)→(1,0,0) at x=1, y=0
    net_to_3d[('オ', 3, 1)] = (1, 0, 1)  # on hinge
    net_to_3d[('オ', 3, 2)] = (1, 0, 0)  # on hinge
    net_to_3d[('オ', 4, 1)] = (1, 1, 1)  # folded
    net_to_3d[('オ', 4, 2)] = (1, 1, 0)  # folded

    # カ (bottom face) - folds down from エ's bottom edge
    # Hinge: (2,2)→(0,0,0) and (3,2)→(1,0,0) at z=0, y=0
    net_to_3d[('カ', 2, 2)] = (0, 0, 0)  # on hinge
    net_to_3d[('カ', 3, 2)] = (1, 0, 0)  # on hinge
    net_to_3d[('カ', 2, 3)] = (0, 1, 0)  # folded
    net_to_3d[('カ', 3, 3)] = (1, 1, 0)  # folded

    # ア (back face) - folds from ウ's left edge
    # ウ's left edge: (1,1)→(0,1,1) and (1,2)→(0,1,0) at x=0, y=1
    # ア folds inward: going in +x direction
    net_to_3d[('ア', 1, 1)] = (0, 1, 1)  # on hinge
    net_to_3d[('ア', 1, 2)] = (0, 1, 0)  # on hinge
    net_to_3d[('ア', 0, 1)] = (1, 1, 1)  # folded
    net_to_3d[('ア', 0, 2)] = (1, 1, 0)  # folded

    # Verify all 8 cube vertices are covered
    all_3d = set()
    for v in net_to_3d.values():
        all_3d.add(v)
    assert len(all_3d) == 8, f"Expected 8 unique 3D vertices, got {len(all_3d)}: {all_3d}"

    # Verify opposite faces don't share vertices
    for face1, face2 in [('エ', 'ア'), ('イ', 'カ'), ('ウ', 'オ')]:
        verts1 = {v for (f, _, _), v in net_to_3d.items() if f == face1}
        verts2 = {v for (f, _, _), v in net_to_3d.items() if f == face2}
        shared = verts1 & verts2
        assert len(shared) == 0, f"Opposite faces {face1} and {face2} share vertices: {shared}"

    # P is at the top-left corner of イ in the net: (2, 0)
    P_net = (2, 0)
    P_3d = net_to_3d[('イ', 2, 0)]
    print(f"P net position: {P_net}")
    print(f"P 3D position: {P_3d}")

    # Find which 3 faces meet at P_3d
    P_faces = vertices_3d[P_3d]
    print(f"Faces at P: {P_faces}")

    assert P_faces == {'ア', 'ウ', 'イ'}, f"Expected {{ア, ウ, イ}}, got {P_faces}"

    # Verify choices
    choices = {
        1: {'ア', 'オ', 'イ'},  # valid vertex (1,1,1), not P
        2: {'ウ', 'エ', 'イ'},  # valid vertex (0,0,1), not P
        3: {'ア', 'エ', 'イ'},  # impossible (ア↔エ opposite)
        4: {'ア', 'ウ', 'イ'},  # CORRECT
        5: {'ア', 'ウ', 'カ'},  # valid vertex (0,1,0), not P
    }

    # Verify choice 3 is impossible
    assert choices[3] not in vertices_3d.values(), "Choice 3 should be impossible"

    # Verify choice 4 is correct
    assert choices[4] == P_faces, "Choice 4 should be correct"

    # Verify other valid choices are at different vertices
    for i in [1, 2, 5]:
        assert choices[i] in vertices_3d.values(), f"Choice {i} should be a valid vertex"
        assert choices[i] != P_faces, f"Choice {i} should not be at P"

    # Verify unique answer
    correct_count = sum(1 for c in choices.values() if c == P_faces)
    assert correct_count == 1, f"Expected exactly 1 correct answer, got {correct_count}"

    print("\n問1 検証結果: OK")
    print(f"正解: (4) ア, ウ, イ")
    return True


def verify_q2():
    """
    問2: T字型展開図の4頂点マーク一致判定

    展開図レイアウト:
    [ア][イ][ウ]
        [エ]
        [オ]
        [カ]

    座標:
    - ア: x=[0,1], y=[0,1]
    - イ: x=[1,2], y=[0,1]
    - ウ: x=[2,3], y=[0,1]
    - エ: x=[1,2], y=[1,2]
    - オ: x=[1,2], y=[2,3]
    - カ: x=[1,2], y=[3,4]

    エを正面に置いた場合の折り畳み:
    - エ = front
    - イ = top (エの上)
    - ア = left (イの左→top左辺から折り下げ)
    - ウ = right (イの右→top右辺から折り下げ)
    - オ = bottom (エの下)
    - カ = back (オの下→bottom奥辺から折り上げ)

    対面: エ↔カ, イ↔オ, ア↔ウ
    """

    # Net vertex → 3D coordinate mapping
    net_to_3d = {}

    # エ (front): y_3d=0 plane
    # Net: (1,1)TL, (2,1)TR, (2,2)BR, (1,2)BL
    # 3D: (0,0,1)TL, (1,0,1)TR, (1,0,0)BR, (0,0,0)BL
    net_to_3d[(1, 1)] = (0, 0, 1)
    net_to_3d[(2, 1)] = (1, 0, 1)
    net_to_3d[(2, 2)] = (1, 0, 0)
    net_to_3d[(1, 2)] = (0, 0, 0)

    # イ (top): z_3d=1 plane - folds up from エ's top edge
    # Hinge at y_net=1: (1,1)→(0,0,1), (2,1)→(1,0,1)
    # (1,0) → back-left = (0,1,1)
    # (2,0) → back-right = (1,1,1)
    net_to_3d[(1, 0)] = (0, 1, 1)
    net_to_3d[(2, 0)] = (1, 1, 1)
    # (1,1) and (2,1) already mapped

    # ア (left): x_3d=0 plane - folds from イ's left edge
    # İ's left edge: (1,0)→(0,1,1) and (1,1)→(0,0,1) at x_3d=0, z_3d=1
    # ア folds down:
    # (0,0) → (0,1,0) - 1 unit down from (0,1,1)
    # (0,1) → (0,0,0) - 1 unit down from (0,0,1)
    net_to_3d[(0, 0)] = (0, 1, 0)
    net_to_3d[(0, 1)] = (0, 0, 0)
    # (1,0) and (1,1) already mapped

    # ウ (right): x_3d=1 plane - folds from イ's right edge
    # İ's right edge: (2,0)→(1,1,1) and (2,1)→(1,0,1) at x_3d=1, z_3d=1
    # ウ folds down:
    # (3,0) → (1,1,0) - 1 unit down from (1,1,1)
    # (3,1) → (1,0,0) - 1 unit down from (1,0,1)
    net_to_3d[(3, 0)] = (1, 1, 0)
    net_to_3d[(3, 1)] = (1, 0, 0)
    # (2,0) and (2,1) already mapped

    # オ (bottom): z_3d=0 plane - folds from エ's bottom edge
    # Hinge at y_net=2: (1,2)→(0,0,0), (2,2)→(1,0,0)
    # (1,3) → (0,1,0) - 1 unit back
    # (2,3) → (1,1,0) - 1 unit back
    net_to_3d[(1, 3)] = (0, 1, 0)
    net_to_3d[(2, 3)] = (1, 1, 0)
    # (1,2) and (2,2) already mapped

    # カ (back): y_3d=1 plane - folds from オ's back edge
    # オ's back edge: (1,3)→(0,1,0), (2,3)→(1,1,0) at z_3d=0, y_3d=1
    # カ folds up:
    # (1,4) → (0,1,1) - 1 unit up from (0,1,0)
    # (2,4) → (1,1,1) - 1 unit up from (1,1,0)
    net_to_3d[(1, 4)] = (0, 1, 1)
    net_to_3d[(2, 4)] = (1, 1, 1)
    # (1,3) and (2,3) already mapped

    # Verify consistency: net vertices shared by multiple faces should map to same 3D
    # Check some shared vertices
    print("Net vertex → 3D mapping:")
    for nv, v3d in sorted(net_to_3d.items()):
        print(f"  {nv} → {v3d}")

    # All unique 3D vertices
    all_3d = set(net_to_3d.values())
    print(f"\nUnique 3D vertices: {len(all_3d)}")
    assert len(all_3d) == 8, f"Expected 8, got {len(all_3d)}"

    # P, Q, R, S positions
    P = (0, 0)  # top-left corner of ア
    Q = (2, 0)  # top-right corner of イ (= top-left of ウ)
    R = (1, 3)  # bottom-left of オ (= top-left of カ)
    S = (2, 4)  # bottom-right of カ

    P_3d = net_to_3d[P]
    Q_3d = net_to_3d[Q]
    R_3d = net_to_3d[R]
    S_3d = net_to_3d[S]

    print(f"\nP at net {P} → 3D {P_3d}")
    print(f"Q at net {Q} → 3D {Q_3d}")
    print(f"R at net {R} → 3D {R_3d}")
    print(f"S at net {S} → 3D {S_3d}")

    # Check which points coincide with P
    same_as_P = []
    if Q_3d == P_3d:
        same_as_P.append('Q')
    if R_3d == P_3d:
        same_as_P.append('R')
    if S_3d == P_3d:
        same_as_P.append('S')

    print(f"\nPoints same as P: {same_as_P}")

    assert same_as_P == ['R'], f"Expected ['R'], got {same_as_P}"

    # Verify Q and S are at same vertex (but different from P)
    assert Q_3d == S_3d, "Q and S should be at same vertex"
    assert Q_3d != P_3d, "Q should not be at same vertex as P"

    # Verify choices
    choices = {
        1: "Qのみ",
        2: "Sのみ",
        3: "Rのみ",  # CORRECT
        4: "QとR",
        5: "RとS",
    }

    print(f"\n問2 検証結果: OK")
    print(f"正解: (3) Rのみ")

    # Additional verification: which faces meet at each marked vertex
    vertices_3d_faces = {
        (0, 0, 0): {'エ', 'ウ', 'カ'},  # using wrong labels...
        # Actually let me define properly
    }

    # 8 cube vertices and their 3 faces:
    # エ=front, ア=back, イ=top, オ=bottom, ア=left... wait
    # エ=front, カ=back, イ=top, オ=bottom, ア=left, ウ=right
    cube_vertices = {
        (0, 0, 0): {'エ', 'ア', 'オ'},  # front-left-bottom
        (1, 0, 0): {'エ', 'ウ', 'オ'},  # front-right-bottom
        (0, 0, 1): {'エ', 'ア', 'イ'},  # front-left-top
        (1, 0, 1): {'エ', 'ウ', 'イ'},  # front-right-top
        (0, 1, 0): {'カ', 'ア', 'オ'},  # back-left-bottom
        (1, 1, 0): {'カ', 'ウ', 'オ'},  # back-right-bottom
        (0, 1, 1): {'カ', 'ア', 'イ'},  # back-left-top
        (1, 1, 1): {'カ', 'ウ', 'イ'},  # back-right-top
    }

    print(f"\nP at {P_3d}: faces = {cube_vertices[P_3d]}")
    print(f"Q at {Q_3d}: faces = {cube_vertices[Q_3d]}")
    print(f"R at {R_3d}: faces = {cube_vertices[R_3d]}")
    print(f"S at {S_3d}: faces = {cube_vertices[S_3d]}")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("セット103 問題検証")
    print("=" * 60)

    print("\n--- 問1 検証 ---")
    verify_q1()

    print("\n--- 問2 検証 ---")
    verify_q2()

    print("\n" + "=" * 60)
    print("全検証完了")
    print("=" * 60)
