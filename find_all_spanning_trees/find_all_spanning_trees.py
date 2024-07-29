import itertools


def get_adjacency_matrix(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    adjacency_matrix = []
    for line in lines:
        row = [(int(x) if x!="-" else float('inf')) for x in line.strip()]
        adjacency_matrix.append(row)
    return adjacency_matrix


def get_edges(scheme):
    edges = []
    for i in range(len(scheme)):
        for j in range(i + 1, len(scheme)):
            if scheme[i][j] == 1:
                edges.append((i+1, j+1))
    return edges


def find_spanning_trees(edges, num_vertices):
    all_edges = set(edges)
    spanning_trees = []
    for combination in itertools.combinations(all_edges, num_vertices - 1):
        if is_spanning_tree(combination, num_vertices):
            spanning_trees.append(combination)
    return spanning_trees


def is_spanning_tree(edges, num_vertices):
    adjacency_list = {}
    for u, v in edges:
        if u not in adjacency_list:
            adjacency_list[u] = []
        if v not in adjacency_list:
            adjacency_list[v] = []
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)

    visited = set()

    def dfs(vertex):
        if vertex in visited:
            return
        visited.add(vertex)
        for neighbor in adjacency_list.get(vertex, []):
            dfs(neighbor)

    start_vertex = list(adjacency_list.keys())[0]
    dfs(start_vertex)

    return len(visited) == num_vertices and len(edges) == num_vertices - 1


def find_all_spanning_trees(filepath):
    scheme = get_adjacency_matrix(filepath)
    vertices_count = len(scheme)
    edges_list = get_edges(scheme)

    spanning_trees = find_spanning_trees(edges_list, vertices_count)

    for i, tree in enumerate(spanning_trees):
        print(f"Spanning tree {i + 1}: {sorted(list(tree), key=lambda x: (x[0], x[1]))}")


find_all_spanning_trees("Trees.txt")
