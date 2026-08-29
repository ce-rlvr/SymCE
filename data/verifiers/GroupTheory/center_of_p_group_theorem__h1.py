import sympy
from sympy.combinatorics import PermutationGroup
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

CONDITION_LABELS = [
    "H_1: G is a finite p-group such that |G| = p^n for some integer n >= 1",
    "H_2: G acts on itself by conjugation",
    "¬Q: The center Z(G) has size <= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    G = None
    p = None
    n = None
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, p, n = witness
        elif len(witness) == 2:
            G, p = witness
        elif len(witness) >= 1:
            G = witness[0]
    else:
        G = witness

    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            order = int(G.order())
            if p is not None and n is not None:
                h1 = bool((order == p**n) and (n >= 1))
            elif p is not None:
                h1 = False
                for i in range(1, 100):
                    if p**i == order:
                        h1 = True
                        break
            else:
                h1 = bool(order >= 1)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    try:
        neg_q = int(G.center().order()) <= 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]