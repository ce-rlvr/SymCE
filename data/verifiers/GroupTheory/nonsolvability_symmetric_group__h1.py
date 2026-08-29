import math
import itertools
import functools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # H_1: Let S_n be the symmetric group on n letters
    try:
        if isinstance(witness, int) and not isinstance(witness, bool):
            n = witness
            h1_ok = (n >= 1)
        else:
            G = witness
            n = G.degree
            # A permutation group of degree n and order n! must be S_n
            h1_ok = (G.order() == math.factorial(n))
    except Exception:
        h1_ok = False

    # ¬Q: The symmetric group S_n IS a solvable group
    try:
        if isinstance(witness, int) and not isinstance(witness, bool):
            if witness < 1:
                neg_q_ok = False
            else:
                G = SymmetricGroup(witness)
                neg_q_ok = bool(G.is_solvable)
        else:
            G = witness
            neg_q_ok = bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "¬Q: S_n is a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1