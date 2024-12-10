import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from collections import deque

# Inputs: A graph to run Bellman-Ford on and a start node
# Outputs: The graph with the lowest cost to reach each node
#          stored at it's nodes
def bellman_ford(G, start):
    # Set cost associated with start node to 0, others to infinity
    for node in G.nodes:
        if node == start:
            G.nodes[node]['cost'] = 0
        else:
            G.nodes[node]['cost'] = math.inf
    
    # Iterate |V| - 1 times
    for i in range(len(G) - 1):
        # Each time, relax each edge
        for (u, v, data) in G.edges.data():
            edge_weight = data["weight"]
            cost_u = G.nodes[u]["cost"]
            cost_v = G.nodes[v]["cost"]
            # If relaxing an edge yields a better cost update that cost
            if cost_u + edge_weight < cost_v:
                G.nodes[v]['cost'] = cost_u + edge_weight

    # If another relaxation yields better results there is a negative cycle    
    for (u, v, data) in G.edges.data():
            if G.nodes[u]["cost"] + data["weight"] < G.nodes[v]["cost"]:
                return -1
    
    return G


# Function that generates input for our algorithm.
# Inputs: Takes the num_nodse and a float between 0 and 1 specifying how sparse the graph should be.
# Outputs: Produces a random graph with num_nodes nodes and random edge weights
def make_input(num_nodes, p):
    # G = undirected_to_directed(G)
    G = nx.fast_gnp_random_graph(num_nodes, p, directed=True)

    weights = {}
    for e in G.edges:
       weights[e] = random.randrange(-5, 5)
    nx.set_edge_attributes(G, values = weights, name = 'weight')

    start = random.randrange(num_nodes)

    return G, start


# Function for visualizing the output of our code relative to the nx code.
# Takes as input the number of nodes in the graph to be generated and the sparsity of the graph
def draw_example(num_nodes, p):
    # Initialize graph
    G, start = make_input(num_nodes, p)

    # Set up for graphing
    pos = nx.spring_layout(G, k=10)

    #See if nx detects a negative cycle, compare it to our output
    try:
        nx_output = nx.single_source_bellman_ford(G, start)[0]
        nx_fig_text = "No negative cycle"
    except nx.exception.NetworkXUnbounded:
        nx_output = {}
        nx_fig_text = "Negative Cycle Detected"
    
    if bellman_ford(G, start) == -1:
        for n in G.nodes():
            del G.nodes(data=True)[n]["cost"]
        our_fig_text = "Negative Cycle Detected"
    else:
        for (n,a) in G.nodes(data=True):
            if a["cost"] == math.inf:
                del G.nodes(data=True)[n]["cost"]
        our_fig_text = "No negative cycle"

    # Assign color map to each node, specify connection style
    line_style='arc3, rad = 0.3'
    
    cmap = []
    for n in range(num_nodes):
        if n == start:
            cmap.append("Red")
        else:
            cmap.append("LightGreen")

    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("NetworkX Output")
    axes[1].set_title("Our Output")
    axes[0].text(-0.5, -1.2, nx_fig_text)
    axes[1].text(-0.5, -1.2, our_fig_text)

    # Draw nx graph
    node_labels = nx_output
    nx.draw(G, pos, ax=axes[0], labels=node_labels, node_color=cmap
            , connectionstyle=line_style, node_size=500)

    # Draw our graph
    node_labels = nx.get_node_attributes(G, "cost")
    nx.draw(G, pos, ax=axes[1], labels=node_labels, node_color=cmap
            , connectionstyle=line_style, node_size=500)

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, ax=axes[0]
                                , edge_labels=edge_labels, connectionstyle=line_style)
    nx.draw_networkx_edge_labels(G, pos, ax=axes[1]
                                , edge_labels=edge_labels, connectionstyle=line_style)

    plt.show()
    

# Runs a single test
# Inputs: num_nodes, number of nodes for input graph
#         p, float between 0 and 1 influencing how sparse the graph will be
# Outputs: Boolean value indicating whether or not our output matches networkx
def do_test(num_nodes, p):
    G, start = make_input(num_nodes, p)

    try:
        nx_output = nx.single_source_bellman_ford(G, start)
        G = bellman_ford(G, start)    
        our_output = G.nodes(data=True)

        for n in nx_output[0]:
            if nx_output[0][n] != our_output[n]["cost"]:
                return False
        return True
    except nx.exception.NetworkXUnbounded:
        return bellman_ford(G, start) == -1

# Takes as input the size of graph to test on, a list of sparsity values,
# and the number of tests to run for each sparsity value, and prints the
# result of running those tests
def test_helper(node_count, ps, num_tests):
    passed = 0

    for p in ps:
        for _ in range (num_tests):
            passed += do_test(node_count, p)

    print(f"{passed} / {num_tests*len(ps)} tests pass for graphs with {node_count} nodes.")

# Function to run a variety of tests on nodes of varying sparsity and size
def tests():
    test_helper(10, [0.05, 0.3, 0.8], 100)
    test_helper(100, [0.05, 0.3, 0.8], 50)
    test_helper(1000, [0.02, 0.1], 5)
    test_helper(10000, [0.0001], 1)


draw_example(10,0.1)

# tests()