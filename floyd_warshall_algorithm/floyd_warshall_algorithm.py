from copy import deepcopy
import sys
from collections import deque

CYELLOWBG = '\33[43m'
CEND = '\33[0m'
CRED2 = '\33[91m'


def open_and_read_file(filepath):
    file = open(filepath, 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    if len(lines) > 0:
        return lines
    else:
        return list()


def get_weight_scheme_LIST_OF_LISTs(filepath):
    graph_info = open_and_read_file(filepath)
    weight_scheme = list()
    if len(graph_info) > 0:
        for line in graph_info:
            if len(line) > 0:
                weights_line_info = line.replace('\n', '').split()
                for i, weight in enumerate(weights_line_info):
                    if weight == '-':
                        weights_line_info[i] = float('inf')
                    else:
                        weights_line_info[i] = int(weight)
                weight_scheme.append(weights_line_info)
            else: weight_scheme.append(list())
    return weight_scheme


def initial_zeros_parents_matrix(draft):
    for parent_node_index, node_info in enumerate(draft):
        for node_index, node in enumerate(node_info):
            if node != float('inf'):
                draft[parent_node_index][node_index] = parent_node_index + 1
            else:
                draft[parent_node_index][node_index] = None
    return draft


def find_shortest_path(parents, node_from, node_to):
    shortest_path = deque()
    shortest_path.append(node_to + 1)
    x = node_to
    if node_from==node_to and parents[node_to][node_from]:
        shortest_path.appendleft(node_from + 1)
        return list(shortest_path)
    while x != node_from:
        p_index = parents[node_from][x]
        if p_index is None:
            return "no path"
        shortest_path.appendleft(p_index)
        x = p_index - 1
    return list(shortest_path)


def floyd_warshall_algorithm(filepath):
    draft_for_weights = get_weight_scheme_LIST_OF_LISTs(filepath)
    for i in range(len(draft_for_weights)):
        draft_for_weights[i][i] = 0
    weights_scheme = {0: draft_for_weights}
    parents_scheme = {0: initial_zeros_parents_matrix(deepcopy(weights_scheme[0]))}
    print("W0:")
    for key, value in weights_scheme.items():
        for row in value:
            print(f"\t{row}")
    print("P0:")
    for key, value in parents_scheme.items():
        for row in value:
            print(f"\t{row}")

    n = len(weights_scheme[0])
    last_iter = 0
    negative_cycle = False
    for t in range(1, n + 1):
        if not negative_cycle:
            weights_scheme[t] = weights_scheme.get(t - 1)
            parents_scheme[t] = parents_scheme.get(t - 1)
            for i in range(n):
                if i != t - 1:
                    for j in range(n):
                        if j != t - 1:
                            weights_t_minus_1 = weights_scheme.get(t - 1)
                            if weights_t_minus_1[i][j] > weights_t_minus_1[i][t - 1] + weights_t_minus_1[t - 1][j]:
                                weights_scheme.get(t)[i][j] = weights_t_minus_1[i][t - 1] + weights_t_minus_1[t - 1][j]
                                parents_scheme[t][i][j] = parents_scheme[t - 1][t - 1][j]
            print(f"W{t}:")
            for row in weights_scheme[t]:
                print(f"\t{row}")
            print(f"P{t}:")
            for row in parents_scheme[t]:
                print(f"\t{row}")
                last_iter = t
            for i in range(n):
                if weights_scheme[t][i][i] < 0:
                    print(f"\t\t{CRED2}!!! NEGATIVE CYCLE !!!{CEND}")
                    print(f"\t\t{CRED2}!!! there is no solution !!!{CEND}")
                    negative_cycle = True

    print("final weights (W) and parents (P) matrix:")
    print(f"W{last_iter}:")
    for row in weights_scheme[last_iter]:
        print(f"\t{row}")
    print(f"P{last_iter}:")
    for row in parents_scheme[last_iter]:
        print(f"\t{row}")

    if not negative_cycle:
        print("\nshortest paths:")
        for i in range(n):
            for j in range(n):
                print(f"\tfrom {i + 1} to {j + 1}: {find_shortest_path(parents_scheme[last_iter], i, j)}")


for file in ["graphNegCycle.txt", "graph.txt"]:
    print(f"\n\n{CYELLOWBG} FILE: {file} {CEND}")
    floyd_warshall_algorithm(file)
