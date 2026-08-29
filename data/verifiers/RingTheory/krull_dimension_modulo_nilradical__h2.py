import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring
    try:
        h1 = False
        if hasattr(witness, 'is_commutative'):
            h1 = bool(witness.is_commutative)
        elif hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring())
    except Exception:
        h1 = False

    # ¬Q: The Krull dimension of R is not equal to the Krull dimension of R/N
    try:
        neg_q = False
        if hasattr(witness, 'krull_dimension') and hasattr(witness, 'nilradical'):
            dim_R = witness.krull_dimension()
            N = witness.nilradical()
            if hasattr(witness, 'quo'):
                dim_R_mod_N = witness.quo(N).krull_dimension()
                neg_q = bool(dim_R != dim_R_mod_N)
            elif hasattr(witness, 'quotient'):
                dim_R_mod_N = witness.quotient(N).krull_dimension()
                neg_q = bool(dim_R != dim_R_mod_N)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The Krull dimension of R is not equal to the Krull dimension of R/N"
]

N_HYP = 1
NEG_Q_INDEX = 1