import sympy
from sympy.combinatorics import free_group
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        H, F, n = witness
    except Exception:
        return [False, False]
        
    rank_H = None
    
    # H_1: H is a free factor of F
    try:
        if type(F).__name__ != 'FreeGroup':
            h1 = False
        else:
            if type(H).__name__ == 'FreeGroup':
                h_gen_strs = {str(g) for g in H.generators}
                f_gen_strs = {str(g) for g in F.generators}
                h1 = h_gen_strs.issubset(f_gen_strs)
                rank_H = len(H.generators)
            elif isinstance(H, (list, tuple, set)):
                h1 = set(H).issubset(set(F.generators))
                rank_H = len(set(H))
            else:
                h1 = False
    except Exception:
        h1 = False
        
    # ¬Q: The rank of H is infinite or greater than n
    try:
        if rank_H is None:
            neg_q = False
        elif not isinstance(n, (int, sympy.Integer)):
            neg_q = False
        else:
            neg_q = rank_H > n
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a free factor of F",
    "¬Q: The rank of H is infinite or greater than n"
]

N_HYP = 1
NEG_Q_INDEX = 1