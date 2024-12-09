import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from random import random
from itertools import combinations

"""
Greedy Influence Maximization Algorithm

Input:
    - A networkX Graph object called G
    - A float activation probability between 0 and 1 that represents the chance a node has of activating each of its neighbors
    - An integer greater than or equal to 1 that represents the number of trials to perform to determine the average number of activated nodes per node

Output:
    - A dict object keyed on node names of G with values representing the average influence of each node over trials trials

This function will perform a breadth-first search on the graph G trials times for every node, but will only visit nodes that are activated by adjacent nodes.
Each node has activation_probability chance of being activated by any activated adjacent node.
The average number of visited nodes given a starting node is that starting node's calculated influence.
"""
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

"""
High Degree Influence Maximization Algorithm

Input:
    - A networkX Graph object called G

Output:
    - A dict object keyed on node names of G with values representing the influence of each node

This function will calculate the influence of each node by retrieving its degree, or the number of adjacent nodes.
"""
def high_degree_heuristic_influence_maximization(G):
    nodes = G.nodes
    influence = {n: G.degree(n) for n in nodes}
    return influence

"""
Test -- A testing function for the previously defined influence maximization algorithms

Input:
    - A networkX Graph object called G

No Output is given for this function.

This function runs the previous two influence calculation functions on the given graph.
The graph is plotted using pyplot twice, side by side.
The right sub-plot shows each node labeled with its High Degree Influence value.
The left sub-plot shows each node labeled with its Greedy Influence value.

"""
def test(G):
    G1 = G.copy()
    greedy = greedy_influence_maximization(G)
    greedy_max = max(greedy.values())

    high_degree = high_degree_heuristic_influence_maximization(G)
    high_degree_max = max(high_degree.values())

    nx.set_node_attributes(G1, greedy, "greedy_influence")
    nx.set_node_attributes(G1, high_degree, "high_degree_influence")

    fig, axes = plt.subplots(1, 2)
    pos = nx.spring_layout(G1, k=0.05)


    axes[0].set_title("Greedy Influence")
    axes[1].set_title("High Degree Heuristic Influence")

    nx.draw(G1, pos, ax=axes[0], node_color=["red" if greedy[node] == greedy_max else "blue" for node in G.nodes])
    nx.draw(G1, pos, ax=axes[1], node_color=["red" if high_degree[node] == high_degree_max else "blue" for node in G.nodes])
    # nx.draw(G1, pos, with_labels=True)

    nx.draw_networkx_labels(G1, pos, ax=axes[0], labels = greedy, font_size=8)
    nx.draw_networkx_labels(G1, pos, ax=axes[1], labels = high_degree)

    plt.show()


########################################################################################################
#  To Run a Test case, uncomment it and leave the others commented.
########################################################################################################

# Intuition for differences between algorithms
# G1 = nx.Graph([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (10, 11), (10, 13), (16, 17), (15, 17), (13, 11), (10, 14), (10, 21), (14, 15), (14, 16), (14, 17), (14, 18), (18, 17), (19, 18), (20, 19), (20, 21), (11, 21), (12, 21), (22, 12), (21, 22), (15, 13), (10, 19), (12, 14), (22, 18), (16, 12), (20, 13)])

# Test 1
G1 = nx.connected_watts_strogatz_graph(100, 5, 0.2)

# Test 2
# G1 = nx.fast_gnp_random_graph(20, 0.2)
# isolated_nodes = list(nx.isolates(G1))
# G1.remove_nodes_from(isolated_nodes)

# Test 3
# G1 = nx.generators.community.stochastic_block_model([10, 25, 13], [[0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8]])

# Test 4
# G1 = nx.generators.community.stochastic_block_model([15, 10, 15], [[0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8]])

# Test 5
# G1 = nx.gaussian_random_partition_graph(70, 15, 5, 0.4, 0.05)

# Test 6
# G1 = nx.Graph()
# G1.add_nodes_from([*range(1,11)])

# Test 7
# G1 = nx.Graph([*combinations(range(1,11), 2)])

# Test 8
# G1 = nx.Graph([*combinations(range(1,6), 2)] + [*combinations(range(6,11), 2)] + [*combinations(range(11,16), 2)])

# Runs the test case
test(G1)
