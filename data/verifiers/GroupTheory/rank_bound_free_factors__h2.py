import sympy
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "¬Q: The rank of H is infinite or strictly greater than n"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # Extract F and H from the witness
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
        else:
            F, H = witness
    except Exception:
        return [False, False]
        
    # H_1: F is a free group of finite rank n
    try:
        h1_ok = isinstance(F, FreeGroup)
    except Exception:
        h1_ok = False
        
    # ¬Q: The rank of H is infinite or strictly greater than n
    try:
        # Determine the rank of H
        if isinstance(H, (int, float)):
            rank_H = H
        elif hasattr(H, 'is_Integer') and H.is_Integer:
            rank_H = int(H)
        elif hasattr(H, 'rank'):
            rank_H = H.rank
        elif hasattr(H, 'generators'):
            rank_H = len(H.generators)
        elif isinstance(H, (list, tuple, set)):
            rank_H = len(H)
        else:
            rank_H = None
            
        if rank_H is None:
            neg_q_ok = False
        else:
            from sympy import oo
            # Determine the rank of F
            if hasattr(F, 'rank'):
                n = F.rank
            elif hasattr(F, 'generators'):
                n = len(F.generators)
            else:
                n = None
                
            if n is None:
                neg_q_ok = False
            else:
                neg_q_ok = bool((rank_H == oo) or (rank_H > n))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]