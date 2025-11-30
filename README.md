# Exact-Cover

Exact Cover is a problem where we need to select subsets from a given set of subsets in such a way that every element appears exactly once. 
More formally: Given a collection $S$ of subsets of set $X$, an exact cover is the subset $S^*$ of $S$ such that each element of $X$ is contained is exactly one subset of $S^*$.
It should satisfy the following properties:
- Intersection of any two subsets in $S^*$ is empty
- Union of all subsets in $S^*$ is equal to $X$

Example of a valid exact cover:

```
$S = \{A, B, C, D, E, F\}$
$X = \{1, 2, 3, 4, 5, 6, 7\}$

$A = \{1, 4, 7\}$
$B = \{1, 4\}$
$C = \{4, 5, 7\}$
$D = \{3, 5, 6\}$
$E = \{2, 3, 6, 7\}$
$F = \{2, 7\}$

Where $S^* = \{B, D, F\}$
```

How to use:

```bash
python exact_cover.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

-h, --help            show this help message and exit
-i, --input           The instance file.
-o, --output          Output file for the DIMACS format (i.e. the CNF formula).
-s, --solver          The SAT solver to be used.
-v, --verb            Verbosity of the SAT solver used.

Example:
```bash
python exact_cover.py -i examples/test1_satisfiable.txt -o formula.cnf -s glucose-syrup -v 1
```


