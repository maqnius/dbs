import numpy as np
from graph_tool.all import *


def create_graph(nodes, transactions):
    g = Graph()
    node_map = {}  # mapping wallet ids to node ids

    # Add vertices with weights
    vertex_weight = g.new_vertex_property('int64_t', val=-1)
    vertex_size = g.new_vertex_property('double', val=0)

    size_func = calc_sizes([_[0] for _ in nodes])

    g.vp.vweight = vertex_weight  # Make property internal
    g.vp.vsize = vertex_size

    g.add_vertex(len(nodes))

    # Add weights and sizes to vertices
    for v in g.vertices():
        index = g.vertex_index[v]
        try:
            vertex_weight[v] = nodes[index][0]
            vertex_size[v] = size_func(vertex_weight[index])
            node_map[nodes[index][1]] = index
        except KeyError:
            pass

    # Add edges with weights
    edge_weight = g.new_edge_property('int64_t', val=-1)
    g.ep.eweight = edge_weight  # Make property internal

    edges = []
    for row in transactions:
        try:
            edges.append((node_map[row[0]], node_map[row[1]], row[2]))
        except KeyError as e:
            # Node der Transaktion nicht im Graphen gefunden
            pass

    g.add_edge_list(edges, eprops=(edge_weight,))

    return g


def add_lower_transaction_limit(g, limit):
    limit_filter = g.new_edge_property('bool')
    vertex_filter = g.new_vertex_property('bool')

    for edge in g.edges():
        limit_filter[edge] = g.ep.eweight[edge] > limit

    g.set_edge_filter(limit_filter)

    for v in g.vertices():
        vertex_filter[v] = len(list(v.all_edges())) > 0

    g.set_vertex_filter(vertex_filter)


def add_lower_income_limit(g, limit):
    limit_filter = g.new_vertex_property('bool')

    for v in g.vertices():
        limit_filter[v] = g.vp.vweight[v] > limit

    g.set_vertex_filter(limit_filter)


def calc_sizes(weights, max=40, min=2):
    """
    linear verteilt zwischen max und min

    Parameters
    ----------
    weights
    max
    min

    Returns
    -------

    """
    sizes = np.array(weights, dtype=np.int64)
    smin = sizes.min()
    smax = sizes.max()

    def calc_size(x):
        return (x - smin) * (max - min) / (smax - smin) + min

    return calc_size
