# CS1005 Discrete Structures - Fall 2026 Project
## Finding Network Motifs in an Email Network

Group members:
- Moosa Hussain, 25I-0547, Section A
- Abdul Rehman, 25I-0543, Section A

## Our parameters (R)

R is the sum of the last 4 digits of both our roll numbers.
R = 547 + 543 = 1090

From this:
- Pair index = R mod 190 = 140, which gives (i, j) = (9, 15)
- Department A = top20[9] = department 11 (339 internal edges)
- Department B = top20[15] = department 9 (146 internal edges)
- Number of random networks = 20 + (R mod 31) = 20 + 5 = 25
- Swap attempts per random network = (5 + R mod 6) x number of edges = 9 x edges
- Seed = R = 1090

After cleaning the dataset (removing self loops and duplicate edges), the full
graph has 24,929 edges instead of the original 25,571.

Department A (dept 11) subgraph: 29 nodes, 339 edges
Department B (dept 9) subgraph: 32 nodes, 146 edges

## How to run the code

Go into the src folder and run:

```
python3 params.py
python3 triads.py
python3 randomize.py
python3 analysis.py <edges_file> <department_labels_file>
python3 validate_with_networkx.py <edges_file> <department_labels_file>
```

The edges file and department labels file are the two SNAP dataset files
(email-Eu-core.txt.gz and email-Eu-core-department-labels.txt.gz).

analysis.py does the main work: it computes our parameters, builds both
department subgraphs, counts all 13 triad classes, generates 25 random graphs
for each department, computes Z-scores and saves the chart.

Results get saved in the results folder: results_table.csv (counts and
Z-scores), motif_zscores.png (the chart), and parameters.txt.

We also wrote validate_with_networkx.py which checks our triad counts against
networkx's built in triadic_census function, just to confirm our counting
code is correct. This is only used to check our answer, not to compute the
actual results, which the rules allow.

## What's in each file

- triads.py: the triad_class function. For a triple of nodes it checks all 6
  orderings, builds a 6 bit number for each one based on which edges exist,
  and takes the minimum. That minimum number tells us which of the 13 classes
  the triad belongs to.
- graph_utils.py: loads the edge list and department labels, removes self
  loops and duplicate edges, builds the subgraph for a department, and counts
  all triads by checking neighbours of each node instead of checking every
  possible group of 3 nodes.
- randomize.py: generates a random graph with the same in and out degree for
  every node, by repeatedly picking two edges and swapping their endpoints if
  it does not create a duplicate edge or a self loop.
- analysis.py: runs everything together and produces the final numbers and
  chart.
- validate_with_networkx.py: extra check against networkx.
- params.py: just has our R value and the numbers calculated from it.

## Results

Looking at the 13 triad classes, both departments show the same basic
pattern: the classes that come out above the +2 line are class 8 (two
reciprocal relationships sharing one person in the middle, but the other two
people don't talk to each other) and class 13 (three people who all email
each other back and forth). Everything else is at or below zero, and a lot of
classes are below -2.

This means people in these departments don't just email in one direction and
move on. If two people email each other, they usually reply, and groups of 3
people tend to form closed loops where everyone talks to everyone, rather
than one-way chains where A emails B who emails C.

Department 9 shows this much more strongly than department 11. Its Z-scores
for the reciprocal classes are bigger (class 8 is 10.7 vs 2.5, class 13 is 8.8
vs 6.2) and its Z-scores for the one-way classes are more negative (class 1 is
-7.3 vs -1.7, class 4 is -6.7 vs -2.1). So department 9's communication is
almost entirely reciprocal pairs and small closed groups, while department 11
still has a bit more one-way/hierarchical communication mixed in.

## Contributions

- Moosa Hussain: triad classification code, graph loading and census code
- Abdul Rehman: randomization code, Z-score and chart code

## Notes

- Self loops and duplicate edges were removed before anything else, as the
  project statement says to do.
- The actual classification, counting, randomization and Z-score logic is
  all written from scratch, no networkx functions used for that. networkx is
  only used in the separate validation script to double check our counts.
