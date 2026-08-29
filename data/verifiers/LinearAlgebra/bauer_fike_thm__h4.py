import sympy
import math
import itertools
import functools
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, V, E, p, mu = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: A is an n by n complex matrix
    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H_2: A is diagonalizable such that A = V Lambda V^{-1} for some invertible matrix V and diagonal matrix Lambda
    try:
        if h1 and isinstance(V, sympy.MatrixBase) and V.shape == A.shape:
            if V.det() != 0:
                Lambda = V.inv() * A * V
                n = A.shape[0]
                is_diag = True
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            val = sympy.simplify(Lambda[i, j])
                            if val != 0:
                                try:
                                    if abs(complex(val.evalf())) > 1e-9:
                                        is_diag = False
                                        break
                                except Exception:
                                    is_diag = False
                                    break
                    if not is_diag:
                        break
                h2 = is_diag
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: E is an n by n complex matrix
    try:
        h3 = isinstance(E, sympy.MatrixBase) and E.shape == A.shape
    except Exception:
        h3 = False

    # H_4: ||.||_p denotes a matrix p-norm and kappa_p(V) is the condition number of V in that norm
    try:
        h4 = p in (1, 2, sympy.oo, math.inf, 'fro') and isinstance(mu, (int, float, complex, sympy.Expr))
    except Exception:
        h4 = False

    # ¬Q: For all eigenvalues lambda of A, |mu - lambda| > kappa_p(V) ||E||_p
    try:
        if not (h1 and h2 and h3 and h4):
            neg_q = False
        else:
            V_inv = V.inv()
            norm_V = V.norm(p)
            norm_V_inv = V_inv.norm(p)
            kappa = norm_V * norm_V_inv
            norm_E = E.norm(p)
            bound = kappa * norm_E

            Lambda = V_inv * A * V
            n = A.shape[0]
            eigenvalues = [Lambda[i, i] for i in range(n)]

            neg_q = True
            for lam in eigenvalues:
                diff_val = float(sympy.Abs(mu - lam).evalf())
                bound_val = float(sympy.Abs(bound).evalf())
                
                if diff_val <= bound_val + 1e-9:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n by n complex matrix",
    "H_2: A is diagonalizable such that A = V Lambda V^{-1} for some invertible matrix V and diagonal matrix Lambda",
    "H_3: E is an n by n complex matrix",
    "H_4: ||.||_p denotes a matrix p-norm and kappa_p(V) is the condition number of V in that norm",
    "¬Q: For all eigenvalues lambda of A, |mu - lambda| > kappa_p(V) ||E||_p"
]

N_HYP = 4
NEG_Q_INDEX = 4