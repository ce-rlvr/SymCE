import sympy
from sympy import S, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a real closed field",
    "¬Q: The field extension R(i) is not an algebraically closed field"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, i = witness
        else:
            R = S.Reals
            i = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a real closed field
    try:
        h1 = (R == S.Reals) or (str(R) in ['RR', 'Reals', 'Real'])
    except Exception:
        h1 = False
        
    # ¬Q: R(i) is not algebraically closed
    try:
        is_alg_closed = False
        if hasattr(i, 'is_complex') and hasattr(i, 'is_real'):
            if i.is_complex and i.is_real is False:
                is_alg_closed = True
        elif isinstance(i, complex):
            if i.imag != 0:
                is_alg_closed = True
                
        neg_q = not is_alg_closed
    except Exception:
        neg_q = False
        
    return [h1, neg_q]