import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
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
V4 = DihedralGroup(2)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a finite solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False
        
    # ¬Q: N is NOT an elementary abelian p-group for some prime p
    try:
        is_elem_ab = True
        if not N.is_abelian:
            is_elem_ab = False
        else:
            order = N.order()
            if order == 1:
                is_elem_ab = True
            else:
                factors = factorint(order)
                if len(factors) > 1:
                    is_elem_ab = False
                else:
                    p = list(factors.keys())[0]
                    for g in N.generators:
                        if not g.is_Identity and g.order() != p:
                            is_elem_ab = False
                            break
        neg_q = not is_elem_ab
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "¬Q: N is not an elementary abelian p-group for any prime p"
]

N_HYP = 1
NEG_Q_INDEX = 1