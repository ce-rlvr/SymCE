import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import a, b, c, d, x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        u, v = witness
    except Exception:
        return [False, False]
    
    # H_1: x and y are elements of R
    try:
        # Check if they support basic ring operations
        _ = u + v
        _ = u - v
        _ = u * v
        _ = (u - v)**2
        h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: (x - y)^2 != x + y
    try:
        lhs = (u - v)**2
        rhs = u + v
        
        if isinstance(lhs, sympy.MatrixBase) and isinstance(rhs, sympy.MatrixBase):
            is_eq = (lhs == rhs)
        else:
            try:
                diff = sympy.simplify(lhs - rhs)
                if hasattr(diff, 'is_zero') and diff.is_zero is not None:
                    is_eq = bool(diff.is_zero)
                else:
                    is_eq = (lhs == rhs)
            except Exception:
                is_eq = (lhs == rhs)
        neg_q = not is_eq
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "¬Q: (x - y)^2 != x + y"
]

N_HYP = 1
NEG_Q_INDEX = 1