import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: i and j are positive integers such that i + j - 1 <= min(m, n)",
    "¬Q: sigma_{i+j-1}(A+B) > sigma_i(A) + sigma_j(B) or A+B is undefined"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        A, B, i, j = witness
    except Exception:
        return [False, False]
    
    # H_1: i and j are positive integers such that i + j - 1 <= min(m, n)
    try:
        if type(i) is not int or type(j) is not int:
            h1 = False
        elif i <= 0 or j <= 0:
            h1 = False
        elif not hasattr(A, 'shape'):
            h1 = False
        else:
            m, n = A.shape
            h1 = bool((i + j - 1) <= min(m, n))
    except Exception:
        h1 = False

    # neg_Q: The singular values satisfy the inequality \sigma_{i+j-1}(A+B) \le \sigma_i(A) + \sigma_j(B)
    try:
        if not (hasattr(A, 'shape') and hasattr(B, 'shape')):
            neg_q = False
        elif A.shape != B.shape:
            # If A and B have different dimensions, A+B is undefined.
            # The conclusion statement cannot hold, so its negation is True.
            neg_q = True
        else:
            sv_AB = (A + B).singular_values()
            sv_A = A.singular_values()
            sv_B = B.singular_values()
            
            val_AB = float(sp.re(sv_AB[i + j - 2].evalf()))
            val_A = float(sp.re(sv_A[i - 1].evalf()))
            val_B = float(sp.re(sv_B[j - 1].evalf()))
            
            # The conclusion is val_AB <= val_A + val_B
            # It fails if val_AB > val_A + val_B
            # We add a small epsilon to avoid floating point inaccuracies causing false positives
            neg_q = bool(val_AB > val_A + val_B + 1e-12)
    except Exception:
        neg_q = False

    return [h1, neg_q]