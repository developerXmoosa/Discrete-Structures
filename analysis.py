"""
Main driver: T1 (parameters), T2 (subgraphs), T4 (census), T6 (Z-scores),
T7 (chart). Run as:

    python3 analysis.py <edges_file> <department_labels_file>

Accepts either the raw .gz files from SNAP or already-decompressed .txt files.
"""

import sys
import csv
import statistics

import params
from graph_utils import (
    load_edges, load_departments, clean_simple,
    top20_departments, induced_subgraph, triad_census,
)
from randomize import randomize, degree_sequences


def compute_z_scores(real_counts, random_counts_list):
    """real_counts: list[13]; random_counts_list: list of list[13]."""
    z_scores = []
    for k in range(13):
        sample = [rc[k] for rc in random_counts_list]
        mu = statistics.mean(sample)
        sigma = statistics.pstdev(sample)  # population std dev
        if sigma == 0:
            z_scores.append(0.0)
        else:
            z_scores.append((real_counts[k] - mu) / sigma)
    return z_scores


def run_department(nodes, edges, label, num_random, seed):
    print(f"\n--- Department {label}: {len(nodes)} nodes, {len(edges)} edges ---")

    real_counts = triad_census(nodes, edges)
    print("Triad census (class 1..13):", real_counts)

    attempts = params.SWAP_MULTIPLIER * len(edges)
    out0, in0 = degree_sequences(edges)

    random_counts_list = []
    for r in range(num_random):
        rnd_edges = randomize(edges, attempts=attempts, seed=seed + r)
        # degree-preservation check (T5), re-verified for every sample
        out1, in1 = degree_sequences(rnd_edges)
        assert out0 == out1 and in0 == in1, "degree sequence changed during randomization!"
        random_counts_list.append(triad_census(nodes, rnd_edges))

    z_scores = compute_z_scores(real_counts, random_counts_list)
    return real_counts, z_scores


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    edges_path, dept_path = sys.argv[1], sys.argv[2]

    print("Loading data...")
    raw_edges = load_edges(edges_path)
    dept = load_departments(dept_path)
    edges = clean_simple(raw_edges)
    print(f"Raw edges: {len(raw_edges)}  |  Simple edges after cleaning: {len(edges)}")

    top20, internal_counts = top20_departments(edges, dept)
    print("\nTop-20 departments by internal edge count (idx: dept_id (internal edges)):")
    for idx, d in enumerate(top20):
        print(f"  {idx:2d}: dept {d:3d}  ({internal_counts[d]} internal edges)")

    i, j = params.pair_ij()
    dept_A, dept_B = top20[i], top20[j]

    print("\n=== Group parameters (R) ===")
    print(f"R = {params.R}")
    print(f"Pair index (R mod 190) = {params.PAIR_INDEX} -> (i, j) = ({i}, {j})")
    print(f"Department A = top20[{i}] = dept {dept_A}")
    print(f"Department B = top20[{j}] = dept {dept_B}")
    print(f"Number of random networks = {params.NUM_RANDOM_NETWORKS}")
    print(f"Swap multiplier = {params.SWAP_MULTIPLIER} (attempts = multiplier x |E_subgraph|)")
    print(f"Seed = {params.SEED}")

    nodes_A, edges_A = induced_subgraph(edges, dept, dept_A)
    nodes_B, edges_B = induced_subgraph(edges, dept, dept_B)

    counts_A, z_A = run_department(nodes_A, edges_A, f"A (dept {dept_A})",
                                    params.NUM_RANDOM_NETWORKS, params.SEED)
    counts_B, z_B = run_department(nodes_B, edges_B, f"B (dept {dept_B})",
                                    params.NUM_RANDOM_NETWORKS, params.SEED + 1000)

    # --- write results table (T4 + T6 deliverable) ---
    with open("../results/results_table.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["class", f"N_A(dept{dept_A})", f"Z_A", f"N_B(dept{dept_B})", f"Z_B"])
        for k in range(13):
            w.writerow([k + 1, counts_A[k], round(z_A[k], 3), counts_B[k], round(z_B[k], 3)])
    print("\nWrote ../results/results_table.csv")

    # --- chart (T7) ---
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    classes = list(range(1, 14))
    fig, ax = plt.subplots(figsize=(11, 6))
    width = 0.35
    ax.bar([c - width / 2 for c in classes], z_A, width, label=f"Dept A ({dept_A})")
    ax.bar([c + width / 2 for c in classes], z_B, width, label=f"Dept B ({dept_B})")
    ax.axhline(2, linestyle="--", color="gray", linewidth=1)
    ax.axhline(-2, linestyle="--", color="gray", linewidth=1)
    ax.set_xticks(classes)
    ax.set_xlabel("Triad class (1-13)")
    ax.set_ylabel("Z-score")
    ax.set_title(f"Triad motif Z-scores: Dept {dept_A} vs Dept {dept_B}  (R = {params.R})")
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/motif_zscores.png", dpi=150)
    print("Wrote ../results/motif_zscores.png")

    with open("../results/parameters.txt", "w") as f:
        f.write(f"R = {params.R}\n")
        f.write(f"Pair index = {params.PAIR_INDEX} -> (i,j) = ({i},{j})\n")
        f.write(f"Department A = {dept_A} (top20[{i}])\n")
        f.write(f"Department B = {dept_B} (top20[{j}])\n")
        f.write(f"Num random networks = {params.NUM_RANDOM_NETWORKS}\n")
        f.write(f"Swap multiplier = {params.SWAP_MULTIPLIER}\n")
        f.write(f"Seed = {params.SEED}\n")
        f.write(f"|V_A|={len(nodes_A)} |E_A|={len(edges_A)}\n")
        f.write(f"|V_B|={len(nodes_B)} |E_B|={len(edges_B)}\n")


if __name__ == "__main__":
    main()
