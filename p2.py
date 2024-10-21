import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def sort_edge(tpl):
    return tuple(sorted(tpl))

def BFS(g, start):
    q = deque()
    q.append(start)
    result = {start: 0}
    visited = set()
    adj_list = dict(g.adjacency())
    while q:
        current = q.popleft()
        visited.add(current)
        for n in adj_list.get(current):
            if n not in visited and n not in q:
                result[n] = result[current] + 1
                q.append(n)
    return result

def num_shortest_path(g, dist_dict, start):
    result = dict((n, 0) for n in g.nodes())
    result[start] = 1
    visited = set()
    adj_list = dict(g.adjacency())
    dists = sorted(dist_dict.items(), key=lambda x: x[1])
    for n, d in dists:
        for pred in adj_list[n]:
            if dist_dict[pred] == d - 1:
                result[n] += max(1, result[pred])
    return result

def calculate_edge_weights(g, dist_dict, sp_dict):
    dists = sorted(dist_dict.items(), key=lambda x: x[1], reverse=True)
    edge_weights = {e : 0 for e in g.edges()}
    adj_list = dict(g.adjacency())
    for n, d in dists:
        sum_incoming = 0
        for succ in adj_list[n]:
            if dist_dict[succ] == d + 1:
                sum_incoming += edge_weights[sort_edge((n, succ))]
        for pred in adj_list[n]:
            if dist_dict[pred] == d - 1:
                edge_weights[sort_edge((n, pred))] = (1 + sum_incoming) * (sp_dict[pred] / sp_dict[n])
    return edge_weights

def calculate_edge_betweenness_centrality(g):
    for e in g.edges():
        g.edges[e]['betweenness'] = 0
    for n in g.nodes():
        dist_dict = BFS(g, n)
        sp_dict = num_shortest_path(g, dist_dict, n)
        edge_weights = calculate_edge_weights(g, dist_dict, sp_dict)
        for e in edge_weights:
            g.edges[e]['betweenness'] += edge_weights[e]
    for e in g.edges():
        g.edges[e]['betweenness'] /= 2

def path_exists(g, a, b):
    adj_list = dict(g.adj)
    stack = [a]
    visited = set()
    while stack:
        current = stack.pop()
        visited.add(current)
        if current == b:
            return True
        for n in adj_list[current]:
            if n not in stack and n not in visited:
                stack.append(n)
    return False

def same_component(components, n1, n2):
    n1_comp = set()
    for n_set in components:
        if n1 in n_set:
            n1_comp = n_set
            break
    return n2 in n1_comp

def modularity(g, components):
    sum_stuff = 0
    m = g.number_of_edges()
    for n1 in g.nodes:
        for n2 in g.nodes:
            if same_component(components, n1, n2):
                A = g.has_edge(n1, n2)
                d1 = g.degree(n1)
                d2 = g.degree(n2)
                sum_stuff += A - (d1*d2 / (2 * m))
    return sum_stuff / (2 * m)

def detect_connected_components(g, all_nodes = {}):
    components = []
    if not all_nodes: all_nodes = set(g.nodes)
    else: all_nodes = all_nodes.copy()
    adj_list = dict(g.adj)
    while all_nodes:
        visited = set()
        stack = [all_nodes.pop()]
        all_nodes.add(stack[0])
        while stack:
            current = stack.pop()
            visited.add(current)
            all_nodes.remove(current)
            for n in adj_list[current]:
                if n not in stack and n not in visited:
                    stack.append(n)
        components.append(visited)
    return components


def girvan_newman(g, mod_bound = 0.5):
    g2 = g.copy()
    connected_components = detect_connected_components(g2)
    while modularity(g, connected_components) < mod_bound:
        calculate_edge_betweenness_centrality(g2)
        try:
            max_edge = max(g2.edges(data=True), key=lambda e: e[2]['betweenness'])
        except:
            # print(e2.edges(data=True))
            break
        n1, n2 = max_edge[0:2]
        g2.remove_edge(n1, n2)
        curr_component = set()
        for node_set in connected_components:
            if n1 in node_set:
                curr_component = node_set
                break
        new_components = detect_connected_components(g2, curr_component)
        if len(new_components) == 2:
            connected_components.remove(curr_component)
            connected_components.extend(new_components)
    print(connected_components)
    return g2

# G = nx.Graph()
#
# G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
#
# G.add_edges_from([("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("E", "G"), ("E", "H"), ("F", "G"), ("G", "H")])
#
# ebc = nx.edge_betweenness_centrality(G)
# print({k: v*28 for k, v in ebc.items()})
# nx.set_edge_attributes(G, ebc, "betweenness")
#
# calculate_edge_betweenness_centrality(G)
# edge_labels = nx.get_edge_attributes(G,'betweenness')
# print(edge_labels)
# nx.set_edge_attributes(G, edge_labels, "betweenness")
#
# pos = nx.spring_layout(G)

# nx.draw(G, pos, with_labels=True)
# edge_labels = nx.get_edge_attributes(G,'betweenness')
# nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
# plt.show()








def round_dict(d):
    return {k: round(v, 2) for k, v in d.items()}

G1 = nx.random_partition_graph([20, 30, 40], 0.5, 0.1)
# G1 = nx.Graph()
# G1.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 8), (1, 2), (1, 4), (1, 17), (2, 3), (2, 9), (2, 11), (3, 14), (5, 7), (5, 8), (5, 11), (5, 12), (5, 16), (6, 7), (6, 9), (6, 12), (7, 8), (7, 9), (7, 11), (7, 12), (7, 17), (8, 9), (8, 10), (8, 11), (8, 12), (9, 11), (9, 12), (10, 11), (10, 12), (11, 12), (11, 15), (12, 13), (13, 15), (13, 16), (16, 17)])

G2 = girvan_newman(G1, mod_bound = 0.3)
# G2 = G1.copy()


# Create a figure with two subplots
fig, axes = plt.subplots(1, 2)

# Draw the first graph on the first subplot
nx.draw(G1, ax=axes[0], with_labels=True)

# calculate_edge_betweenness_centrality(G2)
# ebc2 = nx.get_edge_attributes(G2, 'betweenness')
# nx.set_edge_attributes(G2, ebc2, "betweenness")
# print(ebc2)
# pos2 = nx.spring_layout(G2)
# nx.draw_networkx_edge_labels(G1, pos1, ax=axes[0], edge_labels = round_dict(ebc))

# Draw the second graph on the second subplot
nx.draw(G2, ax=axes[1], with_labels=True)

# ebc = nx.edge_betweenness_centrality(G1)
# print({k: v*153 for k, v in ebc.items()})
# nx.set_edge_attributes(G1, ebc, "betweenness")
# pos1 = nx.spring_layout(G1)
# nx.draw_networkx_edge_labels(G2, pos2, ax=axes[1], edge_labels = round_dict(ebc2))

# Show the plot
plt.show()
