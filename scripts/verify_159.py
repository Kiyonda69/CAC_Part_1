"""
航大思考159 検証スクリプト
立方体の展開図問題（5択）

立方体の面: T(top), B(bottom), F(front), K(back), L(left), R(right)
12辺: T-F, T-K, T-L, T-R, B-F, B-K, B-L, B-R, F-L, F-R, K-L, K-R
"""

def verify_net_from_cuts(kept_edges, faces=('T','B','F','K','L','R')):
    """5辺をkeepした時、面の連結性をチェック（spanning tree判定）"""
    from collections import defaultdict
    adj = defaultdict(set)
    for e in kept_edges:
        a, b = e
        adj[a].add(b)
        adj[b].add(a)
    visited = set()
    stack = ['F']
    while stack:
        f = stack.pop()
        if f in visited: continue
        visited.add(f)
        stack.extend(adj[f] - visited)
    return len(visited) == 6 and len(kept_edges) == 5

def unfold(kept_edges):
    """keptエッジから2D座標に展開する。F=(0,0)を中心とする。"""
    EDGES_OF_FACE = {
        'F': {'T':'top', 'B':'bottom', 'L':'left', 'R':'right'},
        'T': {'K':'top', 'F':'bottom', 'L':'left', 'R':'right'},
        'B': {'F':'top', 'K':'bottom', 'L':'left', 'R':'right'},
        'L': {'T':'top', 'B':'bottom', 'K':'left', 'F':'right'},
        'R': {'T':'top', 'B':'bottom', 'F':'left', 'K':'right'},
        'K': {'T':'top', 'B':'bottom', 'R':'left', 'L':'right'},
    }
    DIR = {'top':(0,-1), 'bottom':(0,1), 'left':(-1,0), 'right':(1,0)}
    OPP = {'top':'bottom','bottom':'top','left':'right','right':'left'}

    from collections import defaultdict
    adj = defaultdict(set)
    for a, b in kept_edges:
        adj[a].add(b)
        adj[b].add(a)

    pos = {'F': (0,0)}
    orient = {'F': {'top':'T', 'bottom':'B', 'left':'L', 'right':'R'}}
    visited = {'F'}
    stack = [('F', None)]
    queue = [('F', f) for f in adj['F']]
    while queue:
        parent, child = queue.pop(0)
        if child in visited: continue
        cube_edge = (min(parent,child), max(parent,child))
        # find direction in 2D where child is placed relative to parent
        parent_orient = orient[parent]
        direction_2d = None
        for d, n in parent_orient.items():
            if n == child:
                direction_2d = d
                break
        if direction_2d is None:
            return None
        dx, dy = DIR[direction_2d]
        px, py = pos[parent]
        pos[child] = (px+dx, py+dy)
        # determine child's orientation
        # child's edge facing parent (opposite of direction_2d) corresponds to (parent face) in cube
        # Use the cube-edge correspondence
        child_orient = {}
        opp_dir = OPP[direction_2d]
        child_orient[opp_dir] = parent
        # Other 3 edges: need to determine based on cube geometry
        # The remaining 3 cube faces adjacent to child are EDGES_OF_FACE[child] minus parent
        # But we need to know which 2D direction each maps to.
        # Use canonical orientation: when child face unfolds, it rotates around the kept edge.
        # Strategy: use parent's orientation to determine child's
        #
        # Specifically: when child unfolds to direction_2d from parent, the child's
        # opp_dir edge faces parent. Then child's other edges are determined by the
        # rotation that places child flat on the 2D plane.
        #
        # We use the following rule: rotation about the shared edge maps cube-axes to 2D axes.
        # 
        # Use a stable convention based on EDGES_OF_FACE.
        # Find: child's "up direction" (in 2D when placed): this is opposite of opp_dir
        # but also needs to know cube orientation.
        # 
        # Simpler approach: for each pair (parent, child), precompute rotation.
        # But for correctness we use a known convention via face normals.
        #
        # Actually, I'll use a different strategy: each face has a fixed local frame
        # in 3D, and unfolding is a rotation. Track the local frame as we unfold.
        visited.add(child)
        # populate child_orient using rotation rules
        # Define cube vertex/face frame. Skip rigorous, use lookup table:
        child_orient = compute_child_orientation(child, parent, direction_2d)
        orient[child] = child_orient
        for n in adj[child] - visited:
            queue.append((child, n))
    return pos, orient

def compute_child_orientation(child, parent, direction_2d):
    """Given parent has orient[parent], and child unfolds in direction_2d from parent,
    compute child's 2D-edge to cube-face mapping."""
    # The shared edge: parent's direction_2d edge = child's opp(direction_2d) edge.
    # In cube: parent face shares edge with child face. The edge's direction in 3D
    # determines how child rotates.
    #
    # Use a hardcoded rotation lookup based on cube geometry.
    # For each (parent_face, child_face, direction_2d), compute child's full orientation.
    
    OPP = {'top':'bottom','bottom':'top','left':'right','right':'left'}
    
    # Cube face adjacency in 3D (a face's "natural" view):
    # When viewing the cube with F=front, T=top, B=bottom, L=left, R=right, K=back:
    # F's natural orientation: top=T, bottom=B, left=L, right=R
    # When you unfold T around the F-T edge (T was attached to F's top), 
    #   T rotates 180° about F-T edge to lie flat. T's natural orientation in cube:
    #   T's bottom (toward F) was facing F. After unfold to (1,0), T's bottom edge (2D)
    #   is the F-T edge. T's left/right in 2D: when unfolded "up", T's left in 2D = T's
    #   left in cube (looking down at cube), but we view from the same side as F.
    # 
    # Convention: the unfolded net is "right side up" - we view all faces from the
    # OUTSIDE of the cube. So F is viewed normally, T is viewed from above (after
    # unfolding, we see T's outer face). Mirroring may apply.
    
    # I'll define orientations in canonical form:
    # Cube coordinate system: x=right, y=up, z=toward viewer
    # F is at z=+1 plane (front face), normal +z, "up" direction=+y, "right"=+x → maps top=T, bottom=B, left=L, right=R
    # T at y=+1, normal +y, "up"=−z (looking down at top, "up" points away), "right"=+x
    #   When unfold to F's top: rotate T about the F-T edge (the line x∈[0,1], y=1, z=1) by -90° (around x-axis)
    #   After unfolding, T lies flat. From the viewer's perspective (looking at front of cube), T is now above F, with:
    #     T's bottom (2D) = T-F edge (which was T's "front" in cube)
    #     T's top (2D) = T-K edge (T's "back" in cube)
    #     T's left (2D) = T-L (T's left in cube)
    #     T's right (2D) = T-R (T's right in cube)
    #   So T's 2D orientation: top=K, bottom=F, left=L, right=R
    
    # Similarly for unfolding B (down from F): B's 2D orient: top=F, bottom=K, left=L, right=R
    # L unfold to F's left: L's 2D orient: top=T, bottom=B, left=K, right=F
    # R unfold to F's right: R's 2D orient: top=T, bottom=B, left=F, right=K
    
    # Now for 2nd-level unfoldings, e.g., from R unfold K to right:
    # R's 2D orient is top=T, bottom=B, left=F, right=K. K is to right of R.
    # K's 2D orient: When K unfolds from R (to the right), K's left edge (2D) = R-K edge.
    # K in cube: top=T, bottom=B, left=R, right=L. After unfolding by rotating 180° about R-K edge:
    # The edge R-K in cube is the right-back vertical edge. When we view from front and unfold R right,
    # then K right of R. K's orientation:
    #   K's left (2D) = K-R edge (= K's "left" in cube)
    #   K's top (2D) = K-T (= K's "top" in cube)
    #   K's bottom (2D) = K-B
    #   K's right (2D) = K-L
    # So K's 2D orient when unfolded from R-right: top=T, bottom=B, left=R, right=L
    
    # General rule: each face has a "natural cube orientation" (which face is to its top,bottom,left,right
    # when viewed from outside). When unfolded, the face's 2D orient is the natural orient,
    # but possibly rotated/mirrored depending on the unfolding.
    
    # Natural cube orientations (face viewed from OUTSIDE):
    NATURAL = {
        'F': {'top':'T', 'bottom':'B', 'left':'L', 'right':'R'},
        'K': {'top':'T', 'bottom':'B', 'left':'R', 'right':'L'},  # viewed from back, L/R swap
        'T': {'top':'K', 'bottom':'F', 'left':'L', 'right':'R'},  # viewed from above
        'B': {'top':'F', 'bottom':'K', 'left':'L', 'right':'R'},  # viewed from below
        'L': {'top':'T', 'bottom':'B', 'left':'K', 'right':'F'},  # viewed from left
        'R': {'top':'T', 'bottom':'B', 'left':'F', 'right':'K'},  # viewed from right
    }
    
    OPP = {'top':'bottom','bottom':'top','left':'right','right':'left'}
    
    # When unfolded into 2D, a face's orientation depends on its rotation about the shared edge.
    # The natural orientation is preserved for the level-1 unfoldings (T,B,L,R from F).
    # For deeper unfoldings, we rotate the natural orientation.
    
    # Algorithm: child's natural orient says: child's "X-direction" face is N.
    # We need to find the rotation R such that when applied to child's natural, the edge
    # (child, parent) maps to the 2D direction opp(direction_2d).
    
    # Find which natural direction of child has parent as its neighbor.
    nat = NATURAL[child]
    parent_nat_dir = None
    for d, n in nat.items():
        if n == parent:
            parent_nat_dir = d
            break
    
    # We need to rotate child's natural so that parent_nat_dir → opp(direction_2d)
    target_dir = OPP[direction_2d]
    
    # Number of 90° clockwise rotations needed
    DIR_ORDER = ['top', 'right', 'bottom', 'left']
    rot = (DIR_ORDER.index(target_dir) - DIR_ORDER.index(parent_nat_dir)) % 4
    
    rotated = {}
    for d, n in nat.items():
        new_d = DIR_ORDER[(DIR_ORDER.index(d) + rot) % 4]
        rotated[new_d] = n
    return rotated


# 設計: 問1の正解
# kept edges (5本): T-F, B-F, L-F, R-F, R-K
kept_edges_q1 = [('T','F'),('B','F'),('L','F'),('R','F'),('R','K')]
print("問1 spanning tree?", verify_net_from_cuts(kept_edges_q1))
result_q1 = unfold(kept_edges_q1)
if result_q1:
    pos, orient = result_q1
    print("問1 展開図 座標:")
    for f, p in sorted(pos.items()):
        print(f"  {f}: {p}")

# 問2: より高難度の展開
# 文字付き面の展開図問題：6面に異なるマークを描き、その配置を考える。
# kept edges: T-F, F-R, R-B, B-L, L-K  (連続的なジグザグ)
# 検証
kept_edges_q2 = [('T','F'),('F','R'),('R','B'),('B','L'),('L','K')]
print("\n問2 spanning tree?", verify_net_from_cuts(kept_edges_q2))
result_q2 = unfold(kept_edges_q2)
if result_q2:
    pos, orient = result_q2
    print("問2 展開図 座標:")
    for f, p in sorted(pos.items()):
        print(f"  {f}: {p}")
