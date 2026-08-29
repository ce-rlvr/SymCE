import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import primefactors

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

def conditions(witness):
    try:
        G = witness
        if not hasattr(G, 'center') or not hasattr(G, 'order') or not hasattr(G, 'elements'):
            h1_ok = False
        else:
            Z = G.center()
            n = G.order() // Z.order()
            
            if n == 1:
                h1_ok = True
            else:
                p_factors = primefactors(n)
                h1_ok = False
                for g in G.elements:
                    is_gen = True
                    for p in p_factors:
                        if (g**(n // p)) in Z:
                            is_gen = False
                            break
                    if is_gen:
                        h1_ok = True
                        break
    except Exception:
        h1_ok = False

    try:
        G = witness
        if hasattr(G, 'is_abelian'):
            neg_q = not G.is_abelian
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: the quotient group G / Z(G) is a cyclic group",
    "¬Q: G is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1