import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain

# Top-level setup: named object bindings
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: R is a commutative ring
    try:
        # In SymPy, domains represent commutative rings
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    # H_2: I is a finitely generated ideal of R
    try:
        if isinstance(I, (list, tuple, set)):
            h2 = all(e in R for e in I)
        elif I == R:
            h2 = True
        elif hasattr(I, 'ring'):
            h2 = I.ring == R
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: J is an ideal of R
    try:
        if isinstance(J, (list, tuple, set)):
            h3 = all(e in R for e in J)
        elif J == R:
            h3 = True
        elif hasattr(J, 'ring'):
            h3 = J.ring == R
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: J is contained in the Jacobson radical of R
    try:
        if isinstance(J, (list, tuple, set)):
            # For standard SymPy domains (ZZ, QQ, poly rings), the Jacobson radical is {0}
            h4 = all(e == 0 for e in J)
        elif J == R:
            h4 = (R.zero == R.one)
        elif hasattr(J, 'is_zero'):
            h4 = J.is_zero()
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: I != {0}
    try:
        if isinstance(I, (list, tuple, set)):
            neg_q = any(e != 0 for e in I)
        elif I == R:
            neg_q = (R.zero != R.one)
        elif hasattr(I, 'is_zero'):
            neg_q = not I.is_zero()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a finitely generated ideal of R",
    "H_3: J is an ideal of R",
    "H_4: J is contained in the Jacobson radical of R",
    "¬Q: I != {0}"
]

N_HYP = 4
NEG_Q_INDEX = 4