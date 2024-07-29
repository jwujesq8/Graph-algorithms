import networkx as nx
import matplotlib.pyplot as plt


def create_graph_with_common_letter(words):
    G = nx.Graph()
    for word in words:
        G.add_node(word)
    for i, word1 in enumerate(words):
        for j, word2 in enumerate(words):
            if i < j:
                if any(word1[k] == word2[k] for k in range(3)):
                    G.add_edge(word1, word2)
    return G


def draw_graph(G, matching=None, title=""):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='yellow', font_size=10, font_weight='bold',
            edge_color='blue', width=3)

    if matching:
        matching_edges = list(matching)
        nx.draw_networkx_edges(G, pos, edgelist=matching_edges, edge_color='red', width=10)

    plt.title(title)
    plt.show()


def find_and_draw_max_matching(words):
    G = create_graph_with_common_letter(words)
    max_matching = nx.max_weight_matching(G, maxcardinality=True)
    draw_graph(G, max_matching, "Maximum Matching in the Graph")


def main():
    files_to_check = ["N1a.txt","N1b.txt"]
    for filepath in files_to_check:
        with open(filepath, 'r') as file:
            words = file.read().strip().split()
        find_and_draw_max_matching(words)


main()
