import random
import networkx as nx
import matplotlib.pyplot as plt
import scipy

def Ramsey(G, sG):
    # O(1)
    if len(sG) == 0:
        return (nx.Graph(), nx.Graph())
    
    # O(1)
    v = sG.pop()
    adj = G.adj[v]

    # Neighbors
    # O(n)
    N = sG.copy()
    # Non-Neighbors
    # O(n)
    NC = sG.copy()

    # Iterate through the nodes in the subgraph, if they are adjacent to v remove them from
    # the non-neighbor set, and vice versa for the neighbor set.
    for u in sG:
        if u in adj:
            NC.remove(u)
        else:
            N.remove(u)
            
    # Recursive calls
    C1, I1 = Ramsey(G, N)
    C2, I2 = Ramsey(G, NC)

    # All O(1)
    if len(C1.nodes) + 1 > len(C2.nodes):
        C = C1
        C.add_node(v)
    else:
        C = C2

    if I2.number_of_nodes() + 1 > I1.number_of_nodes():
        I = I2
        I.add_node(v)
    else:
        I = I1

    return C, I








# SEND A COPY OF G AS THE ARGUMENT
def clique_removal(G):
    Cs, Is = [], []
    C, I = Ramsey(G,set(G))
    Cs.append(C)
    Is.append(I)
    while G.number_of_nodes() != 0:
        G.remove_nodes_from(C.nodes)
        C, I = Ramsey(G,set(G))
        Cs.append(C)
        Is.append(I)
    return max(Is, key=lambda x: x.number_of_nodes())

def max_clique(G):
    G = nx.complement(G)
    max_clique = clique_removal(G)
    return set(max_clique.nodes)

# Both test1 and test2 have a call to plt.show() at the end, uncomment this to see a visualization
# of the algorithms output.

# Test function for Ramsey algorithm without clique removal
def test(G):
    G1 = G.copy()
    C, I = Ramsey(G1, set(G1))

    fig, axes = plt.subplots(1, 2)
    pos = nx.spring_layout(G1, k=0.05)


    axes[0].set_title("C")
    axes[1].set_title("I")

    nx.draw(G1, pos, ax=axes[0], node_color=["#FF6961" if node in C.nodes else "#87CEEB" for node in G.nodes], with_labels=True)
    nx.draw(G1, pos, ax=axes[1], node_color=["#FF6961" if node in I.nodes else "#87CEEB" for node in G.nodes], with_labels=True)
    # nx.draw(G1, pos, with_labels=True)

    nx.draw_networkx_labels(G1, pos, ax=axes[0])
    nx.draw_networkx_labels(G1, pos, ax=axes[1])

    print(f"Clique found: {len(C)} nodes")
    print(f"Independent set found: {len(I)} nodes")
    plt.show()

# Test function for Ramsey with clique removal
def test2(G):
    G1 = G.copy()
    C = max_clique(G)

    pos = nx.spring_layout(G1)


    nx.draw(G1, pos, node_color=["#FF6961" if node in C else "#87CEEB" for node in G.nodes], with_labels=True)

    nx.draw_networkx_labels(G1, pos)

    print(f"Clique found: {len(C)} nodes")
    plt.show()

# Generate random graph, then run test1 and test2
n = 10
c = 0.5
G1 = nx.fast_gnp_random_graph(n, c)

print(f"For graph with {n} nodes and {c} chance of nodes being connected,\n")
print("Without clique removal")
test(G1)
print("\nWith clique removal")
test2(G1)