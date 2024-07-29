class Node:
    def __init__(self, node, parent, group):
        self.node = node
        self.parent = parent
        self.group = group


def get_successors_scheme_DICT_OF_LISTs(filepath):
    def open_and_read_file(filepath):
        file = open(filepath, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        if len(lines) > 0:
            return lines
        else:
            return list()

    graph_info = open_and_read_file(filepath)
    successors_dict = {}
    if len(graph_info) > 0:
        for i, line in enumerate(graph_info):
            if len(line)>0:
                line = line.replace('\n', '').split()
                node_info = list()
                for index, successor in enumerate(line):
                    if successor != '-' and successor != '0':
                        node_info.append(int(index)+1)
                successors_dict[i+1] = node_info
    return successors_dict


def get_graph_scheme_X_Y(filepath):
    schemeY_x = get_successors_scheme_DICT_OF_LISTs(filepath)
    schemeX_y = {}
    X = []
    Y = []
    for y in schemeY_x.keys():
        if y not in Y: Y.append(y)
        for x in schemeY_x[y]:
            if x not in schemeX_y.keys():
                schemeX_y[x] = []
            schemeX_y[x].append(y)
            if x not in X: X.append(x)
    schemeX_y = dict(sorted(schemeX_y.items()))
    X = sorted(X)
    Y = sorted(Y)
    return schemeX_y, X, Y


def get_new_M(tree, last_node, M):
    root = tree[0]
    group = ["Y", "X"]

    path = []
    if last_node.parent == root.node:
        path.append((root.node, last_node.node))
        M.append((root.node, last_node.node))
        return M, path

    # get new path
    node = last_node
    iter = 0
    visited = []
    while node.parent != 0:
        visited.append(node)
        if node.group=="Y":
            path.append((node.parent, node.node))
        else:
            path.append((node.node, node.parent))
        iter = iter + 1
        i = iter % 2  # to find proper group (Y or X)

        # find parent node
        for tuple in tree:
            if node.parent == tuple.node and tuple.group == group[i] and tuple not in visited:
                node = tuple
                break
    m_path = []
    for t in path:
        if t in M:
            M.remove(t)
        else:
            M.append(t)
            m_path.append(t)
    return M, m_path


def main(filepath):
    schemeX_y, X, Y = get_graph_scheme_X_Y(filepath)
    M = []
    while len(M) != len(X):
        for x in X:
            T = []
            visited = []
            S = [x]
            found_association = False
            tree = [Node(x, 0, "X")]
            for s in S:
                if s not in visited and not found_association:
                    visited.append(s)
                    for s_y in schemeX_y[s]:
                        if not found_association:
                            if s_y not in T:
                                T.append(s_y)
                                tree.append(Node(s_y, s, "Y"))


                                s_y_in_M = False
                                for m in M:
                                    if not s_y_in_M:
                                        if s_y == m[1]:  # jest nasycony
                                            s_y_in_M = True
                                            if m[0] not in S:
                                                S.append(m[0])
                                            tree.append(Node(m[0], s_y, "X"))


                                if not s_y_in_M:

                                    M, m_path = get_new_M(tree, Node(s_y, s, "Y"), M)
                                    print(f"\nM–powered path: {m_path}")
                                    print(f"Current association:{sorted(M, key=lambda x: x[0])}")
                                    found_association = True
                if s == S[len(S)-1] and not found_association:
                    print(f"\nThere is no association in the graph. For S = {sorted(S)}, cause |N(S)|<|S|")
                    # exit(0)
                    return
    print(f"\nWe found an association saturating the collection X\nCurrent association:{sorted(M, key=lambda x: x[0])}")


files = ["graph11.txt", "graph_without_association.txt"]
for file in files:
    print(f"\n\n\t{file}")
    main(file)
