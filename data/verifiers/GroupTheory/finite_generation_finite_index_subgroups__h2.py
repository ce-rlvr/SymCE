import sympy
from sympy.combinatorics import FreeGroup, FpGroup, FpSubgroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        if isinstance(witness, tuple) and len(witness) == 2:
            F, H = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1 = False
    try:
        if isinstance(F, FreeGroup):
            h1 = len(F.generators) < float('inf')
        elif isinstance(F, FpGroup) and len(F.relators) == 0:
            h1 = len(F.generators) < float('inf')
    except Exception:
        pass

    h2 = False
    try:
        if hasattr(F, 'index'):
            idx = F.index(H)
            if callable(idx): 
                idx = idx()
            h2 = (idx < float('inf'))
        elif hasattr(H, 'index'):
            idx = H.index(F)
            if callable(idx): 
                idx = idx()
            h2 = (idx < float('inf'))
        elif isinstance(F, FpGroup):
            gens = H.generators if hasattr(H, 'generators') else H
            table = F.coset_enumeration(gens)
            h2 = len(table) < float('inf')
    except Exception:
        pass

    neg_q = False
    try:
        if hasattr(H, 'is_finitely_generated'):
            is_fg = H.is_finitely_generated
            if callable(is_fg): 
                is_fg = is_fg()
            neg_q = not is_fg
        elif hasattr(H, 'generators'):
            neg_q = len(H.generators) == float('inf')
        elif isinstance(H, (list, tuple, set)):
            neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "H_2: The index of H in F is finite",
    "not Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2