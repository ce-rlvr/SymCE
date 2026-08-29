import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, DihedralGroup, CyclicGroup, AlternatingGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
            h1 = False
            if isinstance(G, PermutationGroup) and G.order() == 120 and G.degree <= 5:
                if isinstance(P, PermutationGroup):
                    h1 = P.degree <= 5
        else:
            P = witness
            h1 = isinstance(P, PermutationGroup) and P.degree <= 5
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P = witness[1]
        else:
            P = witness
            
        if not isinstance(P, PermutationGroup):
            neg_q = False
        else:
            is_D4 = False
            if P.order() == 8 and not P.is_abelian:
                try:
                    elements = list(P.generate())
                except Exception:
                    elements = list(P.elements)
                order_4 = sum(1 for g in elements if g.order() == 4)
                if order_4 == 2:
                    is_D4 = True
            neg_q = not is_D4
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group on 5 letters, S_5",
    "¬Q: P is not isomorphic to the dihedral group of order 8"
]

N_HYP = 1
NEG_Q_INDEX = 1