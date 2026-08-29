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

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.get('E_is_algebraic_extension_of_F', False))
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.get('Omega_is_algebraically_closed_containing_E', False))
    except Exception:
        h2 = False

    try:
        h3 = bool(witness.get('A_F_is_algebraic_closure_of_F_in_Omega', False))
    except Exception:
        h3 = False

    try:
        q = bool(witness.get('A_F_equals_A_E', True))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E is an algebraic field extension of F",
    "H_2: \Omega is an algebraically closed field containing E",
    "H_3: A_F is the algebraic closure of F in \Omega",
    "¬Q: A_F != A_E"
]

N_HYP = 3
NEG_Q_INDEX = 3