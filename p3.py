import networkx as nx
import matplotlib.pyplot as plt
import math
from random import sample
from random import randrange
from collections import deque

def bellman_ford(G, start):
    # Set cost associated with each node to either 0 or infinity
    for node in G.nodes:
        if node == start:
            G.nodes[node]['cost'] = 0
        else:
            G.nodes[node]['cost'] = math.inf
    
    for i in range(len(G) - 1):
        for (u, v, data) in G.edges.data():
            edge_weight = data["weight"]
            cost_u = G.nodes[u]["cost"]
            cost_v = G.nodes[v]["cost"]
            if cost_u + edge_weight < cost_v:
                G.nodes[v]['cost'] = cost_u + edge_weight
    
    for (u, v, data) in G.edges.data():
            if G.nodes[u]["cost"] + data["weight"] < G.nodes[v]["cost"]:
                return 0
    
    return(G.nodes.data())

def generate_graph(num_nodes):
    nodes = range(num_nodes)
    
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    
    for node in G:
        adj_nodes = sample(nodes, randrange(num_nodes))
        for adj in adj_nodes:
            G.add_edge(node, adj, weight=randrange(-5,15))
    
    return G

def do_test():
    num_nodes = 6
    G = nx.random_k_out_graph(num_nodes, 3, 1, self_loops=False)

    weights = {}
    for e in G.edges:
       weights[e] = randrange(-10, 30)
    nx.set_edge_attributes(G, values = weights, name = 'weight')

    start = randrange(num_nodes)

    try:
        # nx_output = nx.single_source_bellman_ford(G, start)[0]
        our_output = bellman_ford(G, start)
        # nx.draw(our_output)

        pos = nx.spring_layout(G)
        node_labels = nx.get_node_attributes(G, "cost")
        nx.draw_networkx(G, pos, labels=node_labels, connectionstyle='arc3, rad = 0.1')

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        print(G.edges(data=True))

        plt.show()
        # for n in nx_output:
        #     if nx_output[n] != our_output[n]["cost"]:
        #         return 0
        #     else:
        #         return 1
    except nx.exception.NetworkXUnbounded:
        # print("Negative Cycle.")
        return -1
    
# num_passed = 0
# num_tested = 0

# for n in range (1000):
#     ret = do_test()

#     if ret != -1:
#         num_passed += ret
#         num_tested += 1

do_test()

# print("Proportion Passed: {}/{}".format(num_passed, num_tested))