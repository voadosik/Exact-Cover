# Exact-Cover

Exact Cover is a problem where we need to select subsets from a given set of subsets in such a way that every element appears exactly once. 
More formally: Given a collection S of subsets of set X, an exact cover is the subset S* of S such that each element of X is contained is exactly one subset of S*.
It should satisfy the following properties:
- Intersection of any two subsets in S* is empty
- Union of all subsets in S* is equal to X

Example of a valid exact cover:

```
S = {A, B, C, D, E, F}
X = {1, 2, 3, 4, 5, 6, 7}

A = {1, 4, 7}
B = {1, 4}
C = {4, 5, 7}
D = {3, 5, 6}
E = {2, 3, 6, 7}
F = {2, 7}

Where S* = {B, D, F}
```

### Encoding Constraints

**1. Universe Coverage**

To ensure that every element in the universe is covered, the encoder iterates through each element. At least one subset must cover each element.

For each element $e$, a clause is added consisting of all subsets $S_i, S_j...$ that contain $e$:
$$S_i \lor S_j \lor \dots$$

or in DIMACS CNF:
`i j ... 0`


**2. Disjoint Subsets**

To ensure that no element is covered more than once (intersection of any two subsets is empty), the encoder enforces pairwise exclusion for overlapping subsets. It ensures no two selected subsets share an element.

For each element $e$, if it appears in both subset $S_i$ and subset $S_j$, they cannot both be selected:
$$\neg S_i \lor \neg S_j$$

or in DIMACS CNF:
`-i -j 0`

---

## DIMACS CNF Format

The CNF formula is output in DIMACS format:
* The header specifies the number of variables and clauses: `p cnf <num_variables> <num_clauses>`.
* Each line represents a clause ending with 0.


## User Documentation

How to use:

```bash
python exact_cover.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

- -h, --help            show this help message and exit
- -i, --input           The instance file.
- -o, --output          Output file for the DIMACS format (i.e. the CNF formula).
- -s, --solver          The SAT solver to be used.
- -v, --verb            Verbosity of the SAT solver used.

Example:
```bash
python exact_cover.py -i examples/test1_satisfiable.txt -o formula.cnf -s glucose-syrup -v 1
```


