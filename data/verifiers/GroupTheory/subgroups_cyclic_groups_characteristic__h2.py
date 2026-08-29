import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a cyclic group
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            is_cyc = G.is_cyclic
            if callable(is_cyc):
                is_cyc = is_cyc()
            h1 = bool(is_cyc)
    except Exception:
        h1 = False
        
    # neg_Q: H is not a characteristic subgroup of G
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            is_char = False
        else:
            is_sub = H.is_subgroup(G)
            if not is_sub:
                is_char = False
            else:
                is_cyc = G.is_cyclic
                if callable(is_cyc):
                    is_cyc = is_cyc()
                if is_cyc:
                    # In a cyclic group, every subgroup is characteristic
                    is_char = True
                else:
                    # Fallback for non-cyclic groups: at least check normality
                    if not H.is_normal(G):
                        is_char = False
                    else:
                        is_char = True
    except Exception:
        # If is_subgroup raises an exception (e.g., degree mismatch), it's not a subgroup
        is_char = False
        
    neg_q = not is_char
    
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1