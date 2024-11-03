import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from random import randrange

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


def girvan_newman(g, mod_bound = 0.3):
    g2 = g.copy()
    connected_components = detect_connected_components(g2)
    while modularity(g, connected_components) < mod_bound and not nx.is_empty(g2):
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

# G1 = nx.Graph()
#
# G1.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
#
# G1.add_edges_from([("A", "B"), ("A", "C"), ("A", "D"), ("B", "I"), ("C", "I"), ("F", "J"), ("E", "J"), ("J", "K"), ("F", "K"), ("D", "I"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("E", "G"), ("E", "H"), ("F", "G"), ("G", "H")])
#
# ebc = nx.edge_betweenness_centrality(G)
# print({k: v*28 for k, v in ebc.items()})
# nx.set_edge_attributes(G, ebc, "betweenness")
#





def round_dict(d):
    return {k: round(v, 2) for k, v in d.items()}

def test(G, mb=0.3, show_ebc=False):
    G1 = G
    G2 = girvan_newman(G1, mb)

    if show_ebc:
        calculate_edge_betweenness_centrality(G1)
        edge_labels = round_dict(nx.get_edge_attributes(G1,'betweenness'))
        nx.set_edge_attributes(G1, edge_labels, "betweenness")

    fig, axes = plt.subplots(1, 2)
    pos = nx.spring_layout(G1)
    pos2 = nx.spring_layout(G2, k=0.75)

    nx.draw(G1, pos, ax=axes[0], with_labels=True)
    nx.draw(G2, pos, ax=axes[1], with_labels=True)
    # nx.draw(G1, pos, with_labels=True)

    if show_ebc:
        nx.draw_networkx_edge_labels(G1, pos, ax=axes[0], edge_labels = edge_labels)

    plt.show()

def random_community_structure(num_communities, community_sizes, intra_community_connections=0.65, inter_community_connections=0.05, mod_bound=0.4):
    if type(community_sizes) is tuple:
        arg1 = [randrange(community_sizes[0], community_sizes[1]) for _ in range(num_communities)]
    else:
        arg1 = [community_sizes] * num_communities

    arg2 = [[intra_community_connections if i == j else inter_community_connections for i in range(num_communities)] for j in range(num_communities)]

    return nx.generators.community.stochastic_block_model(arg1, arg2)

# Test 1
# G1 = random_community_structure(5, (4, 10))
# Test 2
# G1 = random_community_structure(7, (3, 8), intra_community_connections=0.8)
# Test 3
# G1 = random_community_structure(10, 10, intra_community_connections=0.8, inter_community_connections=0.02)
# Test 4
# G1 = random_community_structure(3, 50, inter_community_connections=0.02)
# Test 5
# G1 = random_community_structure(5, (5, 15))
# test(G1, 0.5)

# Test 6
# G1 = nx.fast_gnp_random_graph(100, 0.02)
# isolated_nodes = list(nx.isolates(G1))
# G1.remove_nodes_from(isolated_nodes)
# Test 7
G1 = nx.fast_gnp_random_graph(20, 0.1)
isolated_nodes = list(nx.isolates(G1))
G1.remove_nodes_from(isolated_nodes)
test(G1, 0.4)
