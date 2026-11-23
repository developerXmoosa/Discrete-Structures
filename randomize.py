"""
Null-model sampling by double-edge swaps (Section 3, step 11 / T5).
"""

import random
from collections import Counter


def degree_sequences(edges):
    out_deg = Counter()
    in_deg = Counter()
    for u, v in edges:
        out_deg[u] += 1
        in_deg[v] += 1
    return out_deg, in_deg


def randomize(edges, attempts, seed):
    """
    One swap attempt: pick two edges (a,b) and (c,d) uniformly at random
    from the CURRENT edge list; replace them with (a,d) and (c,b).
    Reject (leave graph unchanged) if a==d, c==b, (a,d) in E, or (c,b) in E.
    Rejected attempts still count toward `attempts`.
    """
    rng = random.Random(seed)
    edge_list = list(edges)
    edge_set = set(edge_list)
    n = len(edge_list)

    for _ in range(attempts):
        i, j = rng.sample(range(n), 2)
        a, b = edge_list[i]
        c, d = edge_list[j]

        if a == d or c == b:
            continue
        if (a, d) in edge_set or (c, b) in edge_set:
            continue

        # perform the swap
        edge_set.discard((a, b))
        edge_set.discard((c, d))
        edge_set.add((a, d))
        edge_set.add((c, b))
        edge_list[i] = (a, d)
        edge_list[j] = (c, b)

    return edge_list


if __name__ == "__main__":
    # Passing check (T5 deliverable): in/out-degree sequence is unchanged.
    sample_edges = [(0, 1), (1, 2), (2, 0), (0, 2), (3, 1), (1, 3), (2, 3), (3, 0)]
    out0, in0 = degree_sequences(sample_edges)

    randomized = randomize(sample_edges, attempts=50, seed=1090)
    out1, in1 = degree_sequences(randomized)

    assert out0 == out1, "out-degree sequence changed!"
    assert in0 == in1, "in-degree sequence changed!"
    assert len(set(randomized)) == len(randomized), "duplicate edge introduced!"
    assert all(u != v for u, v in randomized), "self-loop introduced!"

    print("Original edges :", sample_edges)
    print("Randomized     :", randomized)
    print("Out-degrees unchanged:", out0 == out1)
    print("In-degrees unchanged :", in0 == in1)
    print("PASS")
