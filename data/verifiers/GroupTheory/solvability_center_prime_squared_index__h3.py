import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime
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
A5 = AlternatingGroup(5)
S5 = SymmetricGroup(5)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'p'):
            G = witness.G
            p = witness.p
        else:
            G = witness
            p = None
    except Exception:
        G = witness
        p = None

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = bool(isprime(p))
    except Exception:
        h2_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: p is a prime number",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2