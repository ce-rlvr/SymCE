import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_cyclic(grp):
    try:
        if not getattr(grp, 'is_abelian', False):
            return False
        order = grp.order()
        for g in grp.generate():
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_cyclic(H)
    except Exception:
        h1 = False
        
    try:
        is_iso = G.is_isomorphic(H)
        same_order = (G.order() == H.order())
        neg_q = bool(is_iso != same_order)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a cyclic group",
    "¬Q: G and H are not isomorphic but have the same order (or vice versa)"
]

N_HYP = 1
NEG_Q_INDEX = 1