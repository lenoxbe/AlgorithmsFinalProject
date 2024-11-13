import random
import networkx as nx
import matplotlib.pyplot as plt

def Ramsey(G):
    adjacency = G.adj
    if len(G.nodes) == 0:
        return (nx.Graph(), nx.Graph())
    v = random.choice(list(G.nodes))
    v_neighborhood = G.copy()
    for n1 in G.nodes:
        if n1 not in adjacency[v]:
            v_neighborhood.remove_node(n1)
    v_antineighborhood = G.copy()
    v_antineighborhood.remove_node(v)
    for n1 in G.nodes:
        if n1 in adjacency[v]:
            v_antineighborhood.remove_node(n1)
    C1, I1 = Ramsey(v_neighborhood)
    C2, I2 = Ramsey(v_antineighborhood)
    if C1.number_of_nodes() + 1 > C2.number_of_nodes():
        c_set = set(C1.nodes).union({v})
    else:
        c_set = set(C2.nodes)
    if I2.number_of_nodes() + 1 > I1.number_of_nodes():
        i_set = set(I2.nodes).union({v})
    else:
        i_set = set(I1.nodes)
    C = G.copy()
    for n1 in G.nodes:
        if n1 not in c_set:
            C.remove_node(n1)
    I = G.copy()
    for n1 in G.nodes:
        if n1 not in i_set:
            I.remove_node(n1)
    return C, I

# SEND A COPY OF G AS THE ARGUMENT
def clique_removal(G):
    Cs, Is = [], []
    C, I = Ramsey(G)
    Cs.append(C)
    Is.append(I)
    while G.number_of_nodes() != 0:
        G.remove_nodes_from(C.nodes)
        C, I = Ramsey(G)
        Cs.append(C)
        Is.append(I)
    return max(Is, key=lambda x: x.number_of_nodes())

def max_clique(G):
    G = nx.complement(G)
    max_clique = clique_removal(G)
    return set(max_clique.nodes)


def test(G):
    G1 = G.copy()
    C, I = Ramsey(G1)

    fig, axes = plt.subplots(1, 2)
    pos = nx.spring_layout(G1, k=0.05)


    axes[0].set_title("C")
    axes[1].set_title("I")

    nx.draw(G1, pos, ax=axes[0], node_color=["red" if node in C.nodes else "blue" for node in G.nodes], with_labels=True)
    nx.draw(G1, pos, ax=axes[1], node_color=["red" if node in I.nodes else "blue" for node in G.nodes], with_labels=True)
    # nx.draw(G1, pos, with_labels=True)

    nx.draw_networkx_labels(G1, pos, ax=axes[0])
    nx.draw_networkx_labels(G1, pos, ax=axes[1])

    plt.show()

def test2(G):
    G1 = G.copy()
    C = max_clique(G)

    pos = nx.spring_layout(G1)


    nx.draw(G1, pos, node_color=["red" if node in C else "blue" for node in G.nodes], with_labels=True)

    nx.draw_networkx_labels(G1, pos)

    plt.show()

# G1 = nx.complete_graph(5)
# G1.add_node(5)
# G1.add_node(6)
G1 = nx.fast_gnp_random_graph(50, 0.3)
G2 = nx.complete_graph(8)
G3 = nx.union(G1, G2, rename=("G", "H"))
G3.add_edges_from([("G" + str(random.randint(0,49)), "H" + str(random.randint(0,7))) for _ in range(50)])

test2(G3)
test(G3)
