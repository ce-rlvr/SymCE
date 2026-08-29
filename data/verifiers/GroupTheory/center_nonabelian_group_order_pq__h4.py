import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # The witness might be a tuple (p, q, G) or just the group G.
    # If p and q are not provided, we supply dummy distinct primes 
    # so that H_1 is satisfied, as p and q are universally quantified.
    p, q, G = 2, 3, None
    if isinstance(witness, tuple):
        if len(witness) == 3:
            p, q, G = witness
        elif len(witness) == 2:
            p, q = 2, 3
            G = witness[1]
        elif len(witness) == 1:
            p, q = 2, 3
            G = witness[0]
        else:
            G = witness
    else:
        G = witness

    # H_1: Let p and q be distinct prime numbers
    try:
        h1 = bool(sympy.isprime(p) and sympy.isprime(q) and p != q)
    except Exception:
        h1 = False

    # H_2: Let G be a group
    try:
        if isinstance(G, PermutationGroup):
            h2 = True
        else:
            h2 = hasattr(G, 'is_abelian') and hasattr(G, 'center')
    except Exception:
        h2 = False

    # H_3: Assume that G is non-abelian
    try:
        h3 = bool(not G.is_abelian)
    except Exception:
        h3 = False

    # ¬Q: The center Z(G) is NOT the trivial subgroup
    try:
        neg_q = bool(G.center().order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: G is a group",
    "H_3: G is non-abelian",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3