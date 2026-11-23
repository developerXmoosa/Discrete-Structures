"""
Triad classification (Section 2 of the project statement).

Fixed encoding: for an ordering (x0, x1, x2) of three nodes, bit k of a
6-bit integer is 1 iff the corresponding directed edge is present.

Bit   0       1       2       3       4       5
Edge  0->1    0->2    1->0    1->2    2->0    2->1

The canonical code of a triad T is the minimum of this integer over all
6 orderings (permutations) of T. Two triads are isomorphic iff they have
the same canonical code. The 13 connected canonical codes, in ascending
order, are numbered Class 1 .. Class 13.
"""

from itertools import permutations

# The 13 connected canonical codes, ascending -> class 1..13
CONNECTED_CODES = [3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63]
CODE_TO_CLASS = {code: idx + 1 for idx, code in enumerate(CONNECTED_CODES)}


def _encode(order, has_edge):
    """6-bit configuration integer for one fixed ordering (x0, x1, x2)."""
    x0, x1, x2 = order
    bits = 0
    if has_edge(x0, x1):
        bits |= 1 << 0
    if has_edge(x0, x2):
        bits |= 1 << 1
    if has_edge(x1, x0):
        bits |= 1 << 2
    if has_edge(x1, x2):
        bits |= 1 << 3
    if has_edge(x2, x0):
        bits |= 1 << 4
    if has_edge(x2, x1):
        bits |= 1 << 5
    return bits


def canonical_code(a, b, c, has_edge):
    """Minimum 6-bit configuration over all 6 orderings of {a, b, c}."""
    return min(_encode(p, has_edge) for p in permutations((a, b, c)))


def triad_class(a, b, c, has_edge):
    """
    Return the class (1..13) of the connected triad {a, b, c}.

    has_edge(u, v) -> bool : True iff there is a directed edge u -> v.

    Caller must guarantee {a, b, c} is connected in the underlying
    undirected sense; a disconnected triple has no class (raises ValueError).
    """
    code = canonical_code(a, b, c, has_edge)
    if code not in CODE_TO_CLASS:
        raise ValueError(
            f"triple ({a},{b},{c}) with canonical code {code} is not connected "
            "(not one of the 13 connected classes)"
        )
    return CODE_TO_CLASS[code]


# ---------------------------------------------------------------------------
# Hand-worked example (T3 deliverable)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Example: a -> b, b -> c, a -> c  (a "transitive chain": two senders of
    # a share a path, c receives from both a and b)
    edges = {("a", "b"), ("b", "c"), ("a", "c")}

    def has_edge(u, v):
        return (u, v) in edges

    print("Worked example: edges = a->b, b->c, a->c")
    print("Orderings and their 6-bit codes:")
    for p in permutations(("a", "b", "c")):
        print(f"  order {p}: code = {_encode(p, has_edge)}")

    code = canonical_code("a", "b", "c", has_edge)
    cls = triad_class("a", "b", "c", has_edge)
    print(f"Canonical code (minimum over orderings) = {code}")
    print(f"=> Class {cls}")

    # By hand: with order (a,b,c): bit0(a->b)=1, bit1(a->c)=1, bit3(b->c)=1
    # others 0 => bits = 1+2+8 = 11. Check other 5 orderings all give >= 11.
    # Order (a,c,b): bit0(a->c)=1,bit1(a->b)=1,bit5(c->b)=0,bit4(c->a)=0,
    # bit2(c... ) -> recompute: x0=a,x1=c,x2=b
    #   bit0: a->c =1 ; bit1: a->b=1 ; bit2: c->a=0 ; bit3: c->b=0
    #   bit4: b->a=0 ; bit5: b->c=1  => bits = 1+2+32 = 35 (bigger)
    # So minimum stays 11 -> Class 5 (since CONNECTED_CODES[4] == 11).
    assert code == 11
    assert cls == 5
    print("Hand check OK: minimum code is 11 -> Class 5.")
