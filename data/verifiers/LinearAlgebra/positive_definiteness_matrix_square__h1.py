import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not bool(getattr(witness, 'is_square', False)):
            h1 = False
        else:
            h1 = bool(witness.det() != 0)
    except Exception:
        h1 = False

    try:
        if not bool(getattr(witness, 'is_square', False)):
            neg_q = False
        else:
            A2 = witness**2
            
            def is_pd(M):
                # A matrix is positive definite if its symmetric part has all positive leading principal minors.
                Sym = (M + M.T) / 2
                for i in range(1, Sym.rows + 1):
                    d = Sym[:i, :i].det()
                    if bool(d <= 0):
                        return False
                return True
                
            neg_q = not is_pd(A2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is non-singular",
    "¬Q: A^2 is not positive definite"
]

N_HYP = 1
NEG_Q_INDEX = 1