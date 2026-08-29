import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = hasattr(witness, "is_square") and witness.is_square
    except Exception:
        h1 = False

    try:
        h2 = hasattr(witness, "is_symmetric") and witness.is_symmetric()
    except Exception:
        h2 = False

    try:
        h3 = all(getattr(e, "is_real", False) for e in witness)
    except Exception:
        h3 = False

    try:
        if not h1 or not h2 or not h3:
            neg_q = False
        elif witness.shape[0] == 0:
            neg_q = True
        else:
            is_pd = witness.is_positive_definite
            is_nd = witness.is_negative_definite
            
            if is_pd or is_nd:
                neg_q = True
            elif is_pd is False and is_nd is False:
                neg_q = False
            else:
                evals = list(witness.eigenvals().keys())
                all_pos = all(e > 0 for e in evals)
                all_neg = all(e < 0 for e in evals)
                neg_q = bool(all_pos or all_neg)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: q is represented by a square matrix (finite-dimensional vector space)",
    "H_2: q is symmetric (quadratic form)",
    "H_3: q has real entries (real vector space)",
    "¬Q: q has no non-zero isotropic vectors (q(x) != 0 for all x != 0)"
]

N_HYP = 3
NEG_Q_INDEX = 3