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

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        is_inf = (witness == sympy.oo) or (isinstance(witness, str) and witness.lower() in ['oo', 'infinity', 'inf'])
        if is_inf:
            h1_ok = True
        elif isinstance(witness, (int, sympy.Integer)):
            h1_ok = (witness >= 1)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        is_inf = (witness == sympy.oo) or (isinstance(witness, str) and witness.lower() in ['oo', 'infinity', 'inf'])
        neg_q_ok = is_inf
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U(n) is the set of all n x n complex unitary matrices",
    "¬Q: U(n) is not a compact topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1