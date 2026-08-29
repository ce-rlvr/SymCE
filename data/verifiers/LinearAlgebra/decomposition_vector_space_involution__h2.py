import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: V is a vector space over a field F whose characteristic is not equal to 2.
        # We interpret the witness as a linear operator T on V = F^n.
        # We require T to be a square sympy Matrix of dimension > 0.
        # (Standard sympy matrices over Q or C have characteristic 0 != 2).
        h1 = isinstance(witness, Matrix) and witness.is_square and witness.shape[0] > 0
    except Exception:
        h1 = False

    try:
        # ¬Q: V is NOT the direct sum of the kernel of T - I and the kernel of T + I.
        # Since char F != 2, ker(T - I) intersection ker(T + I) is always {0}.
        # Thus, the sum is direct, and it equals V if and only if the sum of their dimensions is n.
        # We check if dim(ker(T - I)) + dim(ker(T + I)) != n.
        n = witness.shape[0]
        I = eye(n)
        rank_minus = (witness - I).rank()
        rank_plus = (witness + I).rank()
        
        dim_ker_minus = n - rank_minus
        dim_ker_plus = n - rank_plus
        
        neg_q = (dim_ker_minus + dim_ker_plus) != n
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F whose characteristic is not equal to 2",
    "¬Q: V is not the direct sum of the kernel of T - I and the kernel of T + I"
]

N_HYP = 1
NEG_Q_INDEX = 1