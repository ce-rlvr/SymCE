import sympy
from sympy import Matrix, eye, zeros

# Standard linear algebra objects for potential witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
    except Exception:
        return [False, False, False]

    def is_nilpotent(m):
        try:
            # Check for square matrices
            if hasattr(m, 'shape') and len(m.shape) == 2 and m.shape[0] == m.shape[1]:
                n = m.shape[0]
                mn = m**n
                return bool(mn == zeros(n, n))
            else:
                # Check for scalars or elements of other rings (up to a reasonable power)
                curr = m
                for _ in range(16):
                    if curr == 0:
                        return True
                    curr = curr * m
                return False
        except Exception:
            return False

    # H_1: x and y are nilpotent elements in R
    try:
        h1_ok = is_nilpotent(x) and is_nilpotent(y)
    except Exception:
        h1_ok = False

    # H_2: x and y commute
    try:
        h2_ok = bool(x * y == y * x)
    except Exception:
        h2_ok = False

    # ¬Q: The product xy is NOT a nilpotent element
    try:
        neg_q_ok = not is_nilpotent(x * y)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x and y are nilpotent elements in R",
    "H_2: x and y commute",
    "¬Q: The product xy is not a nilpotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2