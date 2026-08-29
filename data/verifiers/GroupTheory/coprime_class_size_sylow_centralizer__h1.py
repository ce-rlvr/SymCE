import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    """
    witness is a tuple (G, p, x)
    """
    try:
        G, p, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h2 = G.contains(x)
        elif hasattr(G, '__contains__'):
            h2 = x in G
        elif hasattr(G, 'elements'):
            h2 = x in G.elements
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: the size of the conjugacy class of x is coprime to p
    try:
        if hasattr(G, 'conjugacy_class_size'):
            size = G.conjugacy_class_size(x)
        elif hasattr(G, 'centralizer') and hasattr(G, 'order'):
            C = G.centralizer(x)
            size = G.order() // C.order()
        else:
            size = sum(1 for _ in G.conjugacy_class(x))
        h3 = (math.gcd(int(size), int(p)) == 1)
    except Exception:
        h3 = False

    # neg_Q: The centralizer C_G(x) does NOT contain a Sylow p-subgroup of G
    try:
        if hasattr(G, 'centralizer_contains_sylow'):
            contains = G.centralizer_contains_sylow(x, p)
        else:
            C = G.centralizer(x)
            if hasattr(G, 'sylow_subgroups'):
                sylows = G.sylow_subgroups(p)
                contains = any(S.is_subgroup(C) for S in sylows)
            else:
                s_G = G.sylow_subgroup(p)
                s_C = C.sylow_subgroup(p)
                contains = (s_G.order() == s_C.order())
        neg_q = not contains
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: x is an element of G",
    "H_3: the size of the conjugacy class of x is coprime to p",
    "¬Q: The centralizer C_G(x) does NOT contain a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3