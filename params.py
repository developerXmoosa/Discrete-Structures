"""
CS1005 - Discrete Structures - Fall 2026 Course Project
Group: Moosa Hussain (25I-0547), Abdul Rehman (25I-0543) - Section A

Group parameters (Section 5 of the project statement).
R = sum of the last 4 digits of every member's roll number.
"""

ROLL_LAST4 = {
    "Moosa Hussain (25I-0547)": 547,
    "Abdul Rehman (25I-0543)": 543,
}

R = sum(ROLL_LAST4.values())                 # 1090

PAIR_INDEX = R % 190                          # 140
NUM_RANDOM_NETWORKS = 20 + (R % 31)           # 25
SWAP_MULTIPLIER = 5 + (R % 6)                 # 9   -> attempts = SWAP_MULTIPLIER * |E|
SEED = R                                      # 1090


def pair_ij(pair_index: int = PAIR_INDEX, n: int = 20):
    """Return (i, j), 0 <= i < j < n, for the given lexicographic pair index."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return pairs[pair_index]


if __name__ == "__main__":
    i, j = pair_ij()
    print(f"R = {R}")
    print(f"Pair index (R mod 190) = {PAIR_INDEX}  ->  (i, j) = ({i}, {j})")
    print(f"Number of random networks (20 + R mod 31) = {NUM_RANDOM_NETWORKS}")
    print(f"Swap-attempt multiplier (5 + R mod 6) = {SWAP_MULTIPLIER}  (attempts = {SWAP_MULTIPLIER} x |E_subgraph|)")
    print(f"Random seed = {SEED}")
