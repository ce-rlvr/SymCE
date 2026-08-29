import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: P acts on X",
    "H_3: X^P is the set of elements in X fixed by all elements of P",
    "¬Q: |X| is not congruent to |X^P| mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    P = None
    p = None
    try:
        if isinstance(witness, dict):
            P_in = witness.get('P', witness.get('G'))
            if isinstance(P_in, PermutationGroup):
                P = P_in
            elif isinstance(P_in, list):
                P = PermutationGroup(P_in)
            p = int(witness.get('p', 0))
        elif isinstance(witness, tuple) and len(witness) == 2:
            P_in, p_in = witness
            if isinstance(P_in, PermutationGroup):
                P = P_in
            elif isinstance(P_in, list):
                P = PermutationGroup(P_in)
            p = int(p_in)
        else:
            for item in witness:
                if isinstance(item, PermutationGroup):
                    P = item
                elif isinstance(item, int) and not isinstance(item, bool):
                    p = item
    except Exception:
        pass

    try:
        h1 = isinstance(P, PermutationGroup) and P.degree >= 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(P, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(p, int) and p >= 2
    except Exception:
        h3 = False

    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            X_size = P.degree
            fixed_points = 0
            for i in range(X_size):
                if all(g(i) == i for g in P.generators):
                    fixed_points += 1
            neg_q = (X_size % p) != (fixed_points % p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]