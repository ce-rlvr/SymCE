import sympy
from sympy.matrices import MatrixBase

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            tr = witness.trace()
            tr_abs = sympy.Abs(tr)
            
            try:
                svs = witness.singular_values()
            except Exception:
                M = witness.H * witness
                evs = M.eigenvals(multiple=True)
                svs = [sympy.sqrt(ev) for ev in evs]
                
            sv_sum = sum(svs)
            
            diff = (tr_abs - sv_sum).evalf()
            if diff.is_number:
                # Using a small tolerance to avoid floating-point inaccuracies
                neg_q = bool(diff > 1e-10)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: |Tr(A)| > sum(sigma_i(A))"
]

N_HYP = 1
NEG_Q_INDEX = 1