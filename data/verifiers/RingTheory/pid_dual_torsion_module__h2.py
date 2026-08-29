import sympy
from sympy import ZZ, QQ, Matrix
from sympy.abc import x

# Top-level setup
Z2 = sympy.S(2)
Z = ZZ
Q = QQ

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        R = None
        M_info = None
        
        if isinstance(witness, tuple):
            R = witness[0]
            if len(witness) > 1:
                M_info = witness[1]
        else:
            if hasattr(witness, 'rows'):
                R = ZZ
                M_info = witness
            else:
                R = witness
                M_info = 1
                
        # Check H1: R is a PID
        if hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID)
        elif R in [ZZ, QQ]:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
            
        # Check neg_Q: Hom_R(M, R) != 0
        if hasattr(M_info, 'rows'):
            A = M_info
            # Assume M = Coker(A), so M = R^m / Im(A) where A is m x n
            # Free rank is m - rank(A)
            neg_q = A.rank() < A.rows
        elif hasattr(M_info, 'rank') and not callable(M_info.rank):
            neg_q = M_info.rank > 0
        elif hasattr(M_info, 'rank') and callable(M_info.rank):
            neg_q = M_info.rank() > 0
        elif isinstance(M_info, (list, tuple)):
            free_rank = sum(1 for factor in M_info if factor == 0)
            neg_q = free_rank > 0
        elif hasattr(M_info, 'is_Ring') and M_info.is_Ring:
            neg_q = True
        elif isinstance(M_info, int):
            neg_q = M_info > 0
        elif M_info is None:
            neg_q = True
        else:
            neg_q = int(M_info) > 0
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The dual module Hom_R(M, R) is not isomorphic to the zero module"
]

N_HYP = 1
NEG_Q_INDEX = 1