import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not getattr(witness, 'is_square', False):
            return [False]
            
        det_exp = witness.exp().det()
        exp_tr = sympy.exp(witness.trace())
        
        diff = sympy.simplify(det_exp - exp_tr)
        if diff == 0:
            neg_q = False
        elif diff.is_number:
            neg_q = abs(complex(diff.evalf())) > 1e-9
        else:
            neg_q = bool(sympy.expand(diff) != 0)
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: det(exp(A)) != exp(trace(A))"
]

N_HYP = 0
NEG_Q_INDEX = 0