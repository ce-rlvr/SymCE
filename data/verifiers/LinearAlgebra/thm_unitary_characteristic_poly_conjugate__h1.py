import sympy as sp
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not getattr(witness, 'is_Matrix', False):
            U = sp.Matrix(witness)
        else:
            U = witness
            
        if not U.is_square:
            h1 = False
        else:
            h1 = True
    except Exception:
        return [False, False]
        
    if not h1:
        return [False, False]
        
    try:
        n = U.shape[0]
        lam = sp.Symbol('lam')
        p = U.charpoly(lam)
        c = p.all_coeffs()
        detU = U.det()
        
        conclusion_holds = True
        for k in range(n + 1):
            diff = c[k] - ((-1)**n * detU * sp.conjugate(c[n-k]))
            diff = sp.simplify(sp.expand(diff))
            if diff != 0:
                conclusion_holds = False
                break
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a square matrix",
    "¬Q: The characteristic polynomial does not satisfy the conjugate reciprocal property"
]

N_HYP = 1
NEG_Q_INDEX = 1