import numpy as np
from graph_tool.all import *

g = Graph()
v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)
graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="two-nodes.png")


def create_graph(nodes, transactions):
    g = Graph()

    # Add vertices with weights
    vertex_weight = g.new_vertex_property('int64_t', val=-1)
    vertex_size = g.new_vertex_property('double', val=0)

    size_func = calc_sizes(list(nodes.values()))

    g.vp.vweight = vertex_weight  # Make property internal
    g.vp.vsize = vertex_size

    max_id = max([int(row) for row in nodes.keys()])

    g.add_vertex(max_id + 1)

    for v in g.vertices():
        try:
            vertex_weight[v] = nodes[int(v)]
            vertex_size[v] = size_func(nodes[int(v)])
        except KeyError:
            pass

    # Add edges with weights
    edge_weight = g.new_edge_property('int64_t', val=-1)
    g.ep.eweight = edge_weight  # Make property internal

    edges = [row[:3] for row in transactions]
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


def calc_sizes(weights, max=20, min=2):
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
