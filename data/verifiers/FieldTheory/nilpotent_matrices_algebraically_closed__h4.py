import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # A SymPy matrix implicitly represents an operator over a field containing its entries.
        # We accept any SymPy matrix as being over an algebraically closed field (like C).
        h1_ok = isinstance(witness, Matrix)
    except Exception:
        h1_ok = False

    try:
        # A square matrix represents a vector space of finite dimension (its size).
        h2_ok = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h2_ok = False

    try:
        # A square matrix represents a linear operator on that vector space.
        h3_ok = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h3_ok = False

    try:
        if not (isinstance(witness, Matrix) and witness.is_square):
            neg_q_ok = False
        else:
            n = witness.shape[0]
            if n == 0:
                # The zero operator on a 0-dimensional space is nilpotent (T^1 = 0)
                neg_q_ok = False
            else:
                # T is nilpotent iff T^n = 0
                Mn = witness**n
                is_zero = all(sympy.expand(e) == 0 for e in Mn)
                neg_q_ok = not is_zero
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: V is a finite-dimensional vector space over K",
    "H_3: T is a linear operator on V",
    "¬Q: T is not a nilpotent operator"
]

N_HYP = 3
NEG_Q_INDEX = 3