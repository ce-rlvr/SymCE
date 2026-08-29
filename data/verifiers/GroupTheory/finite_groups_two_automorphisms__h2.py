import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            try:
                order = witness.order()
            except TypeError:
                order = witness.order
                
            try:
                is_cyclic = witness.is_cyclic
                if callable(is_cyclic):
                    is_cyclic = is_cyclic()
            except Exception:
                is_cyclic = False
                for g in witness.elements:
                    try:
                        g_order = g.order()
                    except TypeError:
                        g_order = g.order
                    if g_order == order:
                        is_cyclic = True
                        break
                        
            is_Z3 = (is_cyclic == True) and (order == 3)
            is_Z4 = (is_cyclic == True) and (order == 4)
            is_Z6 = (is_cyclic == True) and (order == 6)
            
            neg_q = not (is_Z3 or is_Z4 or is_Z6)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not isomorphic to Z3, Z4, or Z6"
]

N_HYP = 1
NEG_Q_INDEX = 1