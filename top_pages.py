import heapq

import networkx as nx


def get_top_k_pages_for_domain(k: int, paths: dict, domain: str, graph: nx.Graph, kinds: dict):
    weights = {url: calc_page_weight(url, paths, kinds) for url in graph.neighbors(domain)}
    return heapq.nlargest(k, weights, key=weights.get)


# weight is the number of reachable emails
def calc_page_weight(url: str, paths: dict, kinds: dict) -> int:
    if url not in paths:
        raise ValueError('paths does not include url')
    return len(list(filter(lambda x: kinds[x] == 'email', paths[url].keys())))


def get_top_k_pages(k: int, graph: nx.Graph, depth: int = 20):
    paths = dict(nx.all_pairs_shortest_path(graph, cutoff=depth))
    kinds = nx.get_node_attributes(graph, "kind")

    top_k = {}

    for node, kind in dict(graph.nodes(data="kind")).items():
        if kind == 'domain':
            top_k[node] = get_top_k_pages_for_domain(k, paths, node, graph, kinds)

    return top_k
