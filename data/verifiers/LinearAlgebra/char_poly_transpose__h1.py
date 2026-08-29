import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, "charpoly") or not hasattr(witness, "T"):
            return [False]
            
        try:
            cp_A = witness.charpoly()
            cp_AT = witness.T.charpoly()
            eq = (cp_A == cp_AT)
        except Exception:
            eq = False
            
        neg_q = not eq
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The characteristic polynomial of A is not equal to the characteristic polynomial of A^T (or is undefined)"
]

N_HYP = 0
NEG_Q_INDEX = 0