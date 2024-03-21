class Node():
    def __init__(self):
        self.left = 0
        self.right = 0
        self.deg_minus = 0
        self.deg_plus = 0
        self.dir_from = []
        self.dir_to = []


def find_achievable_nodes(start_node, graph, D):
    visited = set()
    queue = [start_node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            for node_out_dir in graph[node].dir_to:
                if node_out_dir in D:
                    graph[node_out_dir].left=1
                    queue.append(node_out_dir)
            visited.add(node)

    return graph


def find_led_nodes(end_node, graph, D):
    visited = set()
    queue = [end_node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            for node_in_dir in graph[node].dir_from:
                if node_in_dir in D:
                    graph[node_in_dir].right = 1
                    queue.append(node_in_dir)
            visited.add(node)
    return graph


def add_graph(filepath):
    file = open(filepath, 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    graph = {}
    if len(lines) > 0:
        for row, info in enumerate(lines):
            if row+1 not in graph.keys():
                graph[row+1] = Node()

            info = info.replace('\n', '').split()
            for col, edge in enumerate(info):
                if edge != '-':
                    graph[row+1].deg_plus += 1
                    graph[row+1].dir_to.append(col + 1)

                    if col+1 not in graph.keys():
                        graph[col + 1] = Node()
                    graph[col + 1].deg_minus +=1
                    graph[col + 1].dir_from.append(row + 1)
    return graph


def leifman_algorithm(filepath):
    graph = add_graph(filepath)
    C = []
    L = [list(graph.keys())]

    while L:
        D = L.pop(0)
        nodes_to_delete_from_D = []
        for node in D:
            if graph[node].deg_plus==0 or graph[node].deg_minus==0:
                C.append(node)
                nodes_to_delete_from_D.append(node)
        D = list(set(D) - set(nodes_to_delete_from_D))
        print("\n\nExploring: " + str(D))

        if len(D)>0:
            v = D[0]
            V00 = []
            V11 = []
            V10 = []
            V01 = []

            graph = find_achievable_nodes(v, graph, D)
            graph = find_led_nodes(v, graph, D)

            for i in range(1, len(graph)+1):
                if i in D:
                    if graph[i].left == 0 and graph[i].right == 0:
                        V00.append(i)
                    elif graph[i].left == 1 and graph[i].right == 1:
                        V11.append(i)
                    elif graph[i].left == 1 and graph[i].right == 0:
                        V10.append(i)
                    elif graph[i].left == 0 and graph[i].right == 1:
                        V01.append(i)
                graph[i].left = 0
                graph[i].right = 0
            print("V11 - " + str(V11))
            print("V10 - " + str(V10))
            print("V01 - " + str(V01))
            print("V00 - " + str(V00))

            if V11:
                C.append(V11)
                if V10:
                    L.append(V10)
                if V01:
                    L.append(V01)
                if V00:
                    L.append(V00)
            else:
                C.append(v)
                if v in V00:
                    V00.remove(v)
                if V10:
                    L.append(V10)
                if V01:
                    L.append(V01)
                if V00:
                    L.append(V00)

            print("C = " + str(C))
            print("L = " + str(L))


leifman_algorithm("leifman.txt")