import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                m_provided = None
            elif len(witness) == 3:
                G, N, m_provided = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: N is a normal subgroup of G
    try:
        h1 = False
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            is_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * (~g)) not in N:
                        is_normal = False
                        break
                    if ((~g) * n * g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            h1 = is_normal
    except Exception:
        h1 = False

    # H2: The index of N in G is a finite integer m
    try:
        h2 = False
        m = None
        if hasattr(G, 'order') and hasattr(N, 'order'):
            oG = G.order()
            oN = N.order()
            if oG < float('inf') and oN < float('inf') and oN > 0:
                if oG % oN == 0:
                    m_calc = oG // oN
                    if m_provided is None or m_provided == m_calc:
                        m = m_calc
                        h2 = True
    except Exception:
        h2 = False

    # neg_Q: For every element g \in G, g^m \in N. 
    try:
        neg_q = False
        if h2 and m is not None:
            for g in G.elements:
                if (g ** m) not in N:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The index of N in G is a finite integer m",
    "¬Q: There exists an element g in G such that g^m is not in N"
]

N_HYP = 2
NEG_Q_INDEX = 2