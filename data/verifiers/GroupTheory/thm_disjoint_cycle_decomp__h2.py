import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

SymmetricGroup = sympy.combinatorics.named_groups.SymmetricGroup
AlternatingGroup = sympy.combinatorics.named_groups.AlternatingGroup
DihedralGroup = sympy.combinatorics.named_groups.DihedralGroup
CyclicGroup = sympy.combinatorics.named_groups.CyclicGroup
Permutation = sympy.combinatorics.permutations.Permutation
eye = sympy.matrices.eye
zeros = sympy.matrices.zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: The context is a finite set X, and the witness pi is a mapping on X.
        # We accept lists, tuples, dicts representing functions X -> X, or SymPy Permutations.
        if isinstance(witness, (list, tuple)):
            h1 = len(witness) > 0 and all(isinstance(x, (int, sympy.Integer)) and 0 <= x < len(witness) for x in witness)
        elif isinstance(witness, dict):
            keys = list(witness.keys())
            values = list(witness.values())
            n = len(keys)
            h1 = n > 0 and set(keys) == set(range(n)) and all(isinstance(v, (int, sympy.Integer)) and 0 <= v < n for v in values)
        elif isinstance(witness, Permutation):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: pi CANNOT be expressed as a product of disjoint cycles.
        # This happens if and only if pi is not a bijection (i.e., not a permutation).
        if isinstance(witness, (list, tuple)):
            is_bijection = len(set(witness)) == len(witness)
            neg_q = not is_bijection
        elif isinstance(witness, dict):
            is_bijection = len(set(witness.values())) == len(witness)
            neg_q = not is_bijection
        elif isinstance(witness, Permutation):
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let S_n be the symmetric group on a finite set X (witness is a mapping on X)",
    "¬Q: pi cannot be expressed as a product of disjoint cycles (pi is not a bijection)"
]

N_HYP = 1
NEG_Q_INDEX = 1