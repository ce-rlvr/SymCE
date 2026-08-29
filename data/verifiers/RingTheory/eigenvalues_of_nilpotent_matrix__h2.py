import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = hasattr(witness, 'rows') and hasattr(witness, 'cols')
    except Exception:
        h1 = False

    try:
        if not getattr(witness, 'is_square', False):
            is_nilp = False
            all_zero = False
        else:
            n = witness.rows
            if n == 0:
                is_nilp = True
                all_zero = True
            else:
                is_nilp = (witness**n == zeros(n, n))
                all_zero = all(v == 0 for v in witness.eigenvals().keys())
        neg_q = (is_nilp != all_zero)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: A is nilpotent is not equivalent to all eigenvalues of A being zero"
]

N_HYP = 1
NEG_Q_INDEX = 1