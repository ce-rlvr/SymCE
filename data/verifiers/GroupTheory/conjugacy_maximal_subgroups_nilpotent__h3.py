import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory as ntheory

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        G, M1, M2 = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite nilpotent group
    try:
        h1 = bool(G.is_nilpotent())
    except Exception:
        h1 = False
        
    # H_2: M1 is a maximal subgroup of G
    try:
        h2 = False
        if M1.is_subgroup(G) and M1.order() < G.order():
            h2 = True
            for g in G.generate_dimino():
                if g not in M1:
                    H = PermutationGroup(*(M1.generators + [g]))
                    if H.order() != G.order():
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H_3: M2 is a maximal subgroup of G
    try:
        h3 = False
        if M2.is_subgroup(G) and M2.order() < G.order():
            h3 = True
            for g in G.generate_dimino():
                if g not in M2:
                    H = PermutationGroup(*(M2.generators + [g]))
                    if H.order() != G.order():
                        h3 = False
                        break
    except Exception:
        h3 = False

    # ¬Q: M1 != M2
    try:
        # Two subgroups are equal if they have the same order and one is a subgroup of the other
        neg_q = not (M1.order() == M2.order() and M1.is_subgroup(M2))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite nilpotent group",
    "H_2: M1 is a maximal subgroup of G",
    "H_3: M2 is a maximal subgroup of G",
    "¬Q: M1 != M2"
]

N_HYP = 3
NEG_Q_INDEX = 3