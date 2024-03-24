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


def get_successors_scheme_DICT_OF_LISTs(filepath):
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


def get_weight_scheme_DICT_OF_DICTs(filepath):
    successors_dict_start_from_1 = get_successors_scheme_DICT_OF_LISTs(filepath)
    weight_scheme_list_start_from_0 = get_weight_scheme_LIST_OF_LISTs(filepath)
    successors_with_weight_scheme = {}
    if len(successors_dict_start_from_1)>0 and len(weight_scheme_list_start_from_0)>0:
        for node, successors in successors_dict_start_from_1.items():
            node_info_successors_with_weight = {}
            if len(successors)>0:
                for s in successors:
                    node_info_successors_with_weight[s] = weight_scheme_list_start_from_0[node-1][int(s)-1]
            successors_with_weight_scheme[node] = node_info_successors_with_weight
    return successors_with_weight_scheme


def get_edges_with_weights_DICT(filepath, directed=False):
    weight_scheme_list_start_from_0 = get_weight_scheme_LIST_OF_LISTs(filepath)
    edges_with_weights_scheme = {}
    if len(weight_scheme_list_start_from_0)>0:
        for node_index_row, node_weights_info in enumerate(weight_scheme_list_start_from_0):
            if len(node_weights_info)>0:
                for node_index_column, edge_weight in enumerate(node_weights_info):
                    edge = (node_index_row+1, node_index_column+1)
                    if (edge_weight != 0 and edge_weight != float('inf')) and \
                            (not directed and (edge[::-1] not in edges_with_weights_scheme.keys())):
                        edges_with_weights_scheme[edge] = int(edge_weight)
    return edges_with_weights_scheme


def get_successors_scheme_DICT_OF_LISTs_good_view(filepath):
    successors_scheme = get_successors_scheme_DICT_OF_LISTs(filepath)
    for node, node_info in successors_scheme.items():
        print(str(node) + ": " + " ".join(str(element) for element in node_info))


def graph_steps_sequence_DES_SORT(filepath):
    steps_sequence = list()
    successors_scheme = get_successors_scheme_DICT_OF_LISTs(filepath)
    if len(successors_scheme)>0:
        for node_index, successors in successors_scheme.items():
            steps_sequence.append(len(successors))
        steps_sequence.sort(reverse=True)
    return steps_sequence


def graph_number_of_edges(filepath):
    edges_count = len(get_edges_with_weights_DICT(filepath))
    return edges_count


def graph_edges_weights_sum(filepath):
    edges_weights_sum = 0
    edges_with_weights_scheme = get_edges_with_weights_DICT(filepath)
    if len(edges_with_weights_scheme)>0:
        for edge, weight in edges_with_weights_scheme.items():
            if weight!=float('inf'):
                edges_weights_sum += weight
    return edges_weights_sum


def task01():
    graph_files = ['graph.txt', 'graph0.txt']
    for filepath in graph_files:
        # TASK a
        print("\n" + CYELLOWBG + "\tWEIGHT SCHEME\t" + CEND)
        print(get_weight_scheme_LIST_OF_LISTs(filepath))

        # TASK b
        print("\n" + CYELLOWBG + "\tSUCCESSORS SCHEME\t" + CEND)
        print(get_successors_scheme_DICT_OF_LISTs(filepath))

        # TASK c
        print("\n" + CYELLOWBG + "\tSUCCESSORS WITH WEIGHTS SCHEME\t" + CEND)
        print(get_weight_scheme_DICT_OF_DICTs(filepath))

        # TASK d
        print("\n" + CYELLOWBG + "\tEDGES WITH WEIGHTS SCHEME\t" + CEND)
        print(get_edges_with_weights_DICT(filepath))

        # TASK e
        print("\n" + CYELLOWBG + "\tLIST OF SUCCESSORS, GOOD VIEW\t" + CEND)
        get_successors_scheme_DICT_OF_LISTs_good_view(filepath)

        # TASK f
        print("\n" + CYELLOWBG + "\tSTEPS SEQUENCES (desc sort)\t" + CEND)
        print(" ".join(str(step) for step in graph_steps_sequence_DES_SORT(filepath)))
        print("\n" + CYELLOWBG + "\tEDGES COUNT\t" + CEND)
        print(graph_number_of_edges(filepath))
        print("\n" + CYELLOWBG + "\tSUM OF EDGES WEIGHTS\t" + CEND)
        print(graph_edges_weights_sum(filepath))


task01()