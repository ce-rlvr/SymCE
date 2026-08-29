import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, M1, M2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite nilpotent group
    try:
        if hasattr(G, 'is_nilpotent'):
            nilp = G.is_nilpotent() if callable(G.is_nilpotent) else G.is_nilpotent
            h1 = bool(nilp)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: M_1 and M_2 are conjugate in G
    try:
        h2 = False
        # Check if M1 and M2 are subgroups of G
        if all(G.contains(g) for g in M1.generators) and all(G.contains(g) for g in M2.generators):
            # Conjugate subgroups must have the same order
            if M1.order() == M2.order():
                for g in G.generate():
                    conj_gens = [g * m * (~g) for m in M1.generators]
                    if all(M2.contains(gen) for gen in conj_gens):
                        h2 = True
                        break
    except Exception:
        h2 = False

    # ¬Q: M_1 != M_2
    try:
        if M1.order() != M2.order():
            neg_q = True
        else:
            # Since they have the same order, they are equal iff M1 is a subgroup of M2
            if all(M2.contains(g) for g in M1.generators):
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite nilpotent group",
    "H_2: M_1 and M_2 are conjugate in G",
    "¬Q: M_1 != M_2"
]

N_HYP = 2
NEG_Q_INDEX = 2