import networkx as nx
import matplotlib.pyplot as plt


def get_data_from_file(filepath):
    person_hobbies_dir = {}
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        person, hobbies = line.strip().split(":")
        print(line)
        person_hobbies_dir[str(person.strip())] = set(hobbies.strip().split())
    return person_hobbies_dir


def find_and_draw_max_weight_matching(filepath):
    person_hobbies_dir = get_data_from_file(filepath)
    G = nx.Graph()

    for person1 in person_hobbies_dir:
        for person2 in person_hobbies_dir:
            if person1 != person2 and person_hobbies_dir[person1].intersection(person_hobbies_dir[person2]):
                G.add_edge(person1, person2)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='yellow', font_size=10, font_weight='bold', edge_color='blue', width=3)

    max_matching = nx.max_weight_matching(G, maxcardinality=True)

    max_matching_edges = list(max_matching)
    nx.draw_networkx_edges(G, pos, edgelist=max_matching_edges, edge_color='red', width=8)

    if len(max_matching) * 2 == len(G.nodes):
        desc = "There is a pairing"
    else:
        desc = "There is no a pairing"
    plt.title(desc)
    print(f"\t{desc}")
    plt.show()


def main():
    files_to_check = ["N8a.txt", "N8b.txt"]
    for filepath in files_to_check:
        find_and_draw_max_weight_matching(filepath)


main()