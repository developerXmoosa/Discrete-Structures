"""
Loading, cleaning, department subgraphs, and the triad census (T1, T2, T4).
"""

import gzip
from collections import defaultdict
from itertools import combinations

from triads import triad_class


def _open_maybe_gz(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")


def load_edges(path):
    """Read 'u v' per line -> list of (u, v) directed edges, as ints."""
    edges = []
    with _open_maybe_gz(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            u, v = line.split()
            edges.append((int(u), int(v)))
    return edges


def load_departments(path):
    """Read 'node department' per line -> dict node -> department id."""
    dept = {}
    with _open_maybe_gz(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            node, d = line.split()
            dept[int(node)] = int(d)
    return dept


def clean_simple(edges):
    """Preprocessing (Section 4, mandatory): drop self-loops and duplicate
    edges so the graph is simple."""
    seen = set()
    cleaned = []
    for u, v in edges:
        if u == v:
            continue
        if (u, v) in seen:
            continue
        seen.add((u, v))
        cleaned.append((u, v))
    return cleaned


def internal_edge_counts(edges, dept):
    """Number of edges with both endpoints in the same department, per dept."""
    counts = defaultdict(int)
    for u, v in edges:
        du, dv = dept.get(u), dept.get(v)
        if du is not None and du == dv:
            counts[du] += 1
    return counts


def top20_departments(edges, dept):
    """
    Rank all departments by internal edge count, largest first,
    ties broken by smaller department id. Return list of dept ids,
    index 0..19 (Section 5).
    """
    counts = internal_edge_counts(edges, dept)
    # ensure every department that exists is present, even with 0 internal edges
    all_depts = set(dept.values())
    for d in all_depts:
        counts.setdefault(d, 0)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [d for d, _ in ranked], counts


def induced_subgraph(edges, dept, department_id):
    """Edges with both endpoints in the given department's member set."""
    members = {n for n, d in dept.items() if d == department_id}
    sub_edges = [(u, v) for u, v in edges if u in members and v in members]
    return sorted(members), sub_edges


def build_adjacency(nodes, edges):
    """
    directed adjacency (for has_edge lookups) and undirected neighbour sets
    (for the 'node adjacent to the other two' enumeration).
    """
    edge_set = set(edges)
    undirected = defaultdict(set)
    for u, v in edges:
        undirected[u].add(v)
        undirected[v].add(u)

    def has_edge(u, v):
        return (u, v) in edge_set

    return has_edge, undirected


def triad_census(nodes, edges):
    """
    Count all 13 triad classes (T4). Every connected triad contains a node
    adjacent (in the underlying undirected sense) to the other two, so we
    enumerate, for every node v, all pairs of v's undirected neighbours,
    then de-duplicate before classifying (a triad may be found from more
    than one 'centre' node, e.g. a triangle is found from all 3).
    """
    has_edge, undirected = build_adjacency(nodes, edges)

    seen = set()
    counts = [0] * 13
    for v in nodes:
        neighbours = list(undirected[v])
        for u, w in combinations(neighbours, 2):
            triple = tuple(sorted((v, u, w)))
            if triple in seen:
                continue
            seen.add(triple)
            cls = triad_class(triple[0], triple[1], triple[2], has_edge)
            counts[cls - 1] += 1
    return counts  # counts[0] = N for class 1, ..., counts[12] = N for class 13
