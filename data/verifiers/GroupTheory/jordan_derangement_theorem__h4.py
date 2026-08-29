import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "H_3: |X| >= 2",
    "¬Q: Every element in G has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G = None
        deg = None
        if isinstance(witness, PermutationGroup):
            G = witness
            deg = witness.degree
            h1 = True
            h2 = True
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], PermutationGroup):
            G = witness[0]
            if isinstance(witness[1], int):
                deg = witness[1]
                h1 = True
                h2 = True
            elif hasattr(witness[1], '__len__'):
                deg = len(witness[1])
                h1 = True
                h2 = True
            else:
                h1 = False
                h2 = False
        else:
            h1 = False
            h2 = False
    except Exception:
        h1 = False
        h2 = False

    try:
        h3 = bool(h1 and deg >= 2 and deg >= G.degree)
    except Exception:
        h3 = False

    try:
        if not (h1 and h3):
            neg_q = False
        else:
            neg_q = True
            count = 0
            for g in G.generate():
                if len(g.support()) >= deg:
                    neg_q = False
                    break
                count += 1
                if count > 100000:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]