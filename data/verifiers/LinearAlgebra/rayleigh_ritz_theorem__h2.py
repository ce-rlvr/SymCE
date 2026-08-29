import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, x = witness
        else:
            A = witness
            x = None
    except Exception:
        return [False, False]

    try:
        H_1 = bool(A.is_square and A.is_hermitian)
    except Exception:
        H_1 = False

    neg_Q = False
    try:
        if x is not None:
            if hasattr(x, 'shape') and x.shape[0] == A.shape[0] and x.shape[1] == 1 and not x.is_zero_matrix:
                x_star = x.H
                num = (x_star * A * x)[0, 0]
                den = (x_star * x)[0, 0]
                if den != 0:
                    rq = sp.simplify(num / den)
                    evals = A.eigenvals()
                    if evals:
                        real_evals = [sp.re(e) for e in evals.keys()]
                        l_min = min(real_evals)
                        l_max = max(real_evals)
                        
                        if rq.is_real is False:
                            neg_Q = True
                        else:
                            if sp.simplify(rq < l_min) == True or sp.simplify(rq > l_max) == True:
                                neg_Q = True
    except Exception:
        pass

    return [H_1, neg_Q]

CONDITION_LABELS = ["H_1: A is an n x n Hermitian matrix", "¬Q: Rayleigh quotient is out of bounds"]
N_HYP = 1
NEG_Q_INDEX = 1