class Node:
    def __init__(self, index):
        self.index = index
        self.predecessors = []
        self.successors = []
        self.parent = None
        self.b = None
        self.e = None


class Graph:
    def __init__(self, h_scheme, f_scheme, s, t):
        self.h_scheme = h_scheme
        self.f_scheme = f_scheme
        self.s = s
        self.t = t


def get_h_scheme_and_nodes_info_from_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    h_scheme = {}
    f_scheme = {}

    for line in lines:
        striped_line = line.strip()
        if len(striped_line) == 0:
            lines.remove(line)

    nodes_list = [0] * (len(lines) + 1)

    for node_row, row in enumerate(lines):
        row = "".join(row.split())
        if nodes_list[node_row + 1] == 0:
            nodes_list[node_row + 1] = Node(node_row + 1)
        for node_column, h in enumerate(row):
            if nodes_list[node_column + 1] == 0:
                nodes_list[node_column + 1] = Node(node_column + 1)
            if h != "-":
                nodes_list[node_row + 1].successors.append(node_column + 1)
                nodes_list[node_column + 1].predecessors.append(node_row + 1)
                h_scheme[str(node_row + 1) + str(node_column + 1)] = int(h)
                f_scheme[str(node_row + 1) + str(node_column + 1)] = 0

    return h_scheme, f_scheme, nodes_list


def main(filepath=""):
    if not filepath:
        filepath = "graph13.txt"

    h_scheme, f_scheme, nodes_list = get_h_scheme_and_nodes_info_from_file(filepath)

    for node in nodes_list:
        if node != 0:
            node.predecessors.sort()
            node.successors.sort()

    graph = Graph(h_scheme, f_scheme, 1, len(nodes_list) - 1)
    nodes_list[graph.s].b = True
    nodes_list[graph.s].e = float('inf')

    found_max_flow = False
    S = []
    W = []

    while not found_max_flow:
        W.append(graph.s)

        while set(W) != set(S) and graph.t not in W:
            for x in W:
                if x not in S:
                    S.append(x)
                    for s in nodes_list[x].successors:
                        if s not in W and graph.f_scheme[str(x) + str(s)] < graph.h_scheme[str(x) + str(s)]:
                            nodes_list[s].parent = x
                            nodes_list[s].b = True
                            nodes_list[s].e = min(nodes_list[x].e,
                                                  graph.h_scheme[str(x) + str(s)] - graph.f_scheme[str(x) + str(s)])
                            W.append(s)
                    for pr in nodes_list[x].predecessors:
                        if pr not in W and graph.f_scheme[str(pr) + str(x)] > 0:
                            nodes_list[pr].parent = x
                            nodes_list[pr].b = False
                            nodes_list[pr].e = min(nodes_list[x].e, graph.f_scheme[str(pr) + str(x)])
                            W.append(pr)

        if graph.t in W:
            node = nodes_list[graph.t]
            e = node.e
            path = []

            while node.index != graph.s:
                path.append(node.index)
                if node.b:
                    graph.f_scheme[str(node.parent) + str(node.index)] += e
                else:
                    graph.f_scheme[str(node.index) + str(node.parent)] -= e
                node = nodes_list[node.parent]

            path.append(graph.s)
            print(f"\nMax path: {path[::-1]}")
            print(f"\tAdded value: {e}")
            S.clear()
            W.clear()
        else:
            found_max_flow = True
            print(f"\nMin cut: {S}")
            print(f"The value of the flow in the maximum flow on subsequent edges:")
            for edge in graph.f_scheme:
                print(f"\t{edge} : {graph.f_scheme[edge]}")

            max_flow_value = 0
            for s in nodes_list[graph.s].successors:
                max_flow_value += graph.f_scheme[str(graph.s) + str(s)]
            for pr in nodes_list[graph.s].predecessors:
                max_flow_value -= graph.f_scheme[str(pr) + str(graph.s)]

            print(f"Max flow value: {max_flow_value}")


if __name__ == "__main__":
    main()
