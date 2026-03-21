"""
航大思考75 一筆書き問題の検証スクリプト

問1: 5つの図形のうち一筆書きできるものを判定
問2: 立方体グラフに辺を追加して一筆書き可能にする最小本数
"""

from itertools import combinations


def count_odd_vertices(edges, vertices):
    """各頂点の次数を計算し、奇数次の頂点数を返す"""
    degree = {v: 0 for v in vertices}
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    odd_count = sum(1 for v in vertices if degree[v] % 2 == 1)
    return odd_count, degree


def can_euler_path(edges, vertices):
    """一筆書き可能かどうか判定 (0個または2個の奇数次頂点)"""
    odd_count, _ = count_odd_vertices(edges, vertices)
    return odd_count == 0 or odd_count == 2


def verify_problem1():
    """問1: 5つの図形の一筆書き可否を検証"""
    print("=" * 60)
    print("問1: 一筆書き可能な図形の判定")
    print("=" * 60)

    # ア: 正五角形 (5頂点, 5辺, 全頂点degree=2)
    fig_a_v = [1, 2, 3, 4, 5]
    fig_a_e = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
    odd_a, deg_a = count_odd_vertices(fig_a_e, fig_a_v)
    can_a = can_euler_path(fig_a_e, fig_a_v)
    print(f"\nア (正五角形): 次数={dict(deg_a)}, 奇数次頂点={odd_a}, 一筆書き={can_a}")

    # イ: 五角形 + 対角線1本 (1-3)
    fig_b_v = [1, 2, 3, 4, 5]
    fig_b_e = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)]
    odd_b, deg_b = count_odd_vertices(fig_b_e, fig_b_v)
    can_b = can_euler_path(fig_b_e, fig_b_v)
    print(f"イ (五角形+対角線1本): 次数={dict(deg_b)}, 奇数次頂点={odd_b}, 一筆書き={can_b}")

    # ウ: K5 (五角形+星形=完全グラフ, 全頂点degree=4)
    fig_c_v = [1, 2, 3, 4, 5]
    fig_c_e = [(i, j) for i in fig_c_v for j in fig_c_v if i < j]
    odd_c, deg_c = count_odd_vertices(fig_c_e, fig_c_v)
    can_c = can_euler_path(fig_c_e, fig_c_v)
    print(f"ウ (K5/星形): 次数={dict(deg_c)}, 奇数次頂点={odd_c}, 一筆書き={can_c}")

    # エ: 正方形 + 両対角線 (4頂点, 6辺, 全頂点degree=3)
    fig_d_v = [1, 2, 3, 4]
    fig_d_e = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3), (2, 4)]
    odd_d, deg_d = count_odd_vertices(fig_d_e, fig_d_v)
    can_d = can_euler_path(fig_d_e, fig_d_v)
    print(f"エ (正方形+両対角線): 次数={dict(deg_d)}, 奇数次頂点={odd_d}, 一筆書き={can_d}")

    # オ: 家形 (四角形+三角屋根, 5頂点, 6辺)
    # 頂点: 1=左下, 2=右下, 3=右上, 4=屋根頂点, 5=左上
    # 辺: 1-2, 2-3, 3-4, 4-5, 5-1, 3-5
    fig_e_v = [1, 2, 3, 4, 5]
    fig_e_e = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (3, 5)]
    odd_e, deg_e = count_odd_vertices(fig_e_e, fig_e_v)
    can_e = can_euler_path(fig_e_e, fig_e_v)
    print(f"オ (家形): 次数={dict(deg_e)}, 奇数次頂点={odd_e}, 一筆書き={can_e}")

    # 結果まとめ
    results = {
        "ア": can_a,
        "イ": can_b,
        "ウ": can_c,
        "エ": can_d,
        "オ": can_e
    }
    drawable = [k for k, v in results.items() if v]
    not_drawable = [k for k, v in results.items() if not v]

    print(f"\n一筆書き可能: {', '.join(drawable)}")
    print(f"一筆書き不可: {', '.join(not_drawable)}")
    print(f"\n正解: ア、イ、ウ、オ の4つ → 選択肢(4)")

    assert drawable == ["ア", "イ", "ウ", "オ"], f"期待: ア,イ,ウ,オ, 実際: {drawable}"
    assert not_drawable == ["エ"], f"期待: エ, 実際: {not_drawable}"
    print("問1 検証OK!")
    return True


def verify_problem2():
    """問2: 立方体グラフに辺を追加して一筆書き可能にする最小本数"""
    print("\n" + "=" * 60)
    print("問2: 立方体グラフの一筆書き化")
    print("=" * 60)

    # 立方体グラフ (8頂点, 12辺)
    vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
    edges = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),  # 前面
        ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),  # 背面
        ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H"),  # 接続
    ]

    odd_count, degree = count_odd_vertices(edges, vertices)
    print(f"\n立方体グラフ: {len(vertices)}頂点, {len(edges)}辺")
    print(f"各頂点の次数: {dict(degree)}")
    print(f"奇数次頂点数: {odd_count}")
    print(f"一筆書き可能: {can_euler_path(edges, vertices)}")

    # 全頂点がdegree 3 (奇数) であることを確認
    assert all(d == 3 for d in degree.values()), "全頂点の次数が3であるべき"
    assert odd_count == 8, "奇数次頂点は8個であるべき"

    # 最小追加辺数を総当たりで検証
    # 追加可能な辺 (まだ存在しない辺)
    existing = set(frozenset(e) for e in edges)
    possible_new_edges = []
    for i, u in enumerate(vertices):
        for j, v in enumerate(vertices):
            if i < j and frozenset((u, v)) not in existing:
                possible_new_edges.append((u, v))

    print(f"\n追加可能な辺: {len(possible_new_edges)}本")
    print(f"追加可能な辺一覧: {possible_new_edges}")

    # 1本追加で一筆書き可能か？
    found_1 = False
    for combo in combinations(possible_new_edges, 1):
        new_edges = edges + list(combo)
        if can_euler_path(new_edges, vertices):
            found_1 = True
            break

    print(f"\n1本追加で可能: {found_1}")

    # 2本追加で一筆書き可能か？
    found_2 = False
    for combo in combinations(possible_new_edges, 2):
        new_edges = edges + list(combo)
        if can_euler_path(new_edges, vertices):
            found_2 = True
            break

    print(f"2本追加で可能: {found_2}")

    # 3本追加で一筆書き可能か？
    found_3 = False
    count_3 = 0
    for combo in combinations(possible_new_edges, 3):
        new_edges = edges + list(combo)
        if can_euler_path(new_edges, vertices):
            count_3 += 1
            if not found_3:
                print(f"3本追加の例: {combo}")
                # 検証用に次数を表示
                _, new_degree = count_odd_vertices(new_edges, vertices)
                new_odd = sum(1 for v in vertices if new_degree[v] % 2 == 1)
                print(f"  追加後の次数: {dict(new_degree)}")
                print(f"  奇数次頂点数: {new_odd}")
            found_3 = True

    print(f"3本追加で可能: {found_3} ({count_3}通り)")

    # 理論的検証
    # 8個の奇数次頂点 → 2個にするには (8-2)/2 = 3本の辺追加が必要
    min_edges = (odd_count - 2) // 2
    print(f"\n理論値: (奇数次頂点数 - 2) / 2 = ({odd_count} - 2) / 2 = {min_edges}本")

    assert not found_1, "1本追加では不可能であるべき"
    assert not found_2, "2本追加では不可能であるべき"
    assert found_3, "3本追加で可能であるべき"
    assert min_edges == 3, f"最小追加数は3であるべき, 実際: {min_edges}"

    print(f"\n正解: 3本 → 選択肢(3)")
    print("問2 検証OK!")
    return True


if __name__ == "__main__":
    verify_problem1()
    verify_problem2()
    print("\n" + "=" * 60)
    print("全検証完了!")
    print("=" * 60)
