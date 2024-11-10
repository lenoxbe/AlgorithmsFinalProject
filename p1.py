import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from random import random

def greedy_influence_maximization(G, activation_probability=0.2, trials=1000):
    nodes = G.nodes
    adj = G.adj
    influence_avg = {n: 0 for n in nodes}
    for n in nodes:
        for _ in range(trials):
            q = deque()
            q.append(n)
            visited = set()
            while q:
                curr = q.popleft()
                visited.add(curr)
                for n1 in adj[curr]:
                    if random() < activation_probability and n1 not in q and n1 not in visited:
                        q.append(n1)
            influence_avg[n] += len(visited)
        influence_avg[n] /= trials
    return influence_avg

def high_degree_heuristic_influence_maximization(G):
    nodes = G.nodes
    influence = {n: G.degree(n) for n in nodes}
    return influence

def test(G):
    G1 = G.copy()
    greedy = greedy_influence_maximization(G)
    greedy_max = max(greedy, key=greedy.get)

    high_degree = high_degree_heuristic_influence_maximization(G)
    high_degree_max = max(high_degree.values())

    nx.set_node_attributes(G1, greedy, "greedy_influence")
    nx.set_node_attributes(G1, high_degree, "high_degree_influence")

    fig, axes = plt.subplots(1, 2)
    pos = nx.spring_layout(G1)


    axes[0].set_title("Greedy Influence")
    axes[1].set_title("High Degree Heuristic Influence")

    nx.draw(G1, pos, ax=axes[0], node_color=["red" if node == greedy_max else "blue" for node in G.nodes])
    nx.draw(G1, pos, ax=axes[1], node_color=["red" if high_degree[node] == high_degree_max else "blue" for node in G.nodes])
    # nx.draw(G1, pos, with_labels=True)

    nx.draw_networkx_labels(G1, pos, ax=axes[0], labels = greedy, font_size=8)
    nx.draw_networkx_labels(G1, pos, ax=axes[1], labels = high_degree)

    plt.show()

# Test 1
# G1 = nx.connected_watts_strogatz_graph(100, 5, 0.2)
# Test 2
# G1 = nx.fast_gnp_random_graph(20, 0.2)
# isolated_nodes = list(nx.isolates(G1))
# G1.remove_nodes_from(isolated_nodes)
test(G1)
