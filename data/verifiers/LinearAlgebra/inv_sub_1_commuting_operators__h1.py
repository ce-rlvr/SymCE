import sympy
from sympy import zeros, eye

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        S, T = witness
        if not (hasattr(S, 'is_Matrix') and S.is_Matrix and hasattr(T, 'is_Matrix') and T.is_Matrix):
            return [False, False, False]
        if S.shape != T.shape or S.rows != S.cols:
            return [False, False, False]
        h1 = True
    except Exception:
        return [False, False, False]
        
    try:
        diff = S * T - T * S
        h2 = all(val.expand() == 0 for val in diff)
    except Exception:
        h2 = False
        
    try:
        ker_invariant = True
        for v in S.nullspace():
            Tv = T * v
            STv = S * Tv
            if not all(val.expand() == 0 for val in STv):
                ker_invariant = False
                break
                
        im_invariant = True
        rank_S = S.rank()
        for v in S.columnspace():
            Tv = T * v
            if S.row_join(Tv).rank() > rank_S:
                im_invariant = False
                break
                
        neg_q = not (ker_invariant and im_invariant)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S and T are linear operators on V",
    "H_2: S and T commute (ST = TS)",
    "¬Q: The kernel of S or the image of S is not T-invariant"
]

N_HYP = 2
NEG_Q_INDEX = 2