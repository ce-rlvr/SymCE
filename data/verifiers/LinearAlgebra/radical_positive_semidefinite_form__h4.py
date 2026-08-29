import sympy
from sympy import Matrix, eye, zeros
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (B, x) where B is a sympy Matrix representing
    the symmetric bilinear form, and x is a sympy Matrix representing a column vector.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        B, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: V is a vector space over the real numbers
    try:
        if not isinstance(B, Matrix) or not isinstance(x, Matrix):
            h1_ok = False
        elif B.shape[0] != B.shape[1]:
            h1_ok = False
        elif x.shape[0] != B.shape[0] or x.shape[1] != 1:
            h1_ok = False
        else:
            # Ensure all entries are real numbers (evaluable as floats, no complex/symbols)
            for e in B:
                float(e)
            for e in x:
                float(e)
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: B is a symmetric bilinear form on V
    try:
        h2_ok = bool(h1_ok and B == B.T)
    except Exception:
        h2_ok = False

    # H_3: B is positive semi-definite
    # Using Sylvester's criterion for positive semi-definiteness:
    # A symmetric matrix is PSD iff ALL of its principal minors are non-negative.
    try:
        if not h1_ok or not h2_ok:
            h3_ok = False
        else:
            n = B.shape[0]
            h3_ok = True
            for k in range(1, n + 1):
                for indices in itertools.combinations(range(n), k):
                    sub_B = B.extract(indices, indices)
                    if sub_B.det() < 0:
                        h3_ok = False
                        break
                if not h3_ok:
                    break
    except Exception:
        h3_ok = False

    # ¬Q: There exists y \in V such that B(x,y) != 0
    # This is equivalent to saying the vector B*x is not the zero vector.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            Bx = B * x
            neg_q_ok = not all(e == 0 for e in Bx)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space over the real numbers",
    "H_2: B is a symmetric bilinear form on V",
    "H_3: B is positive semi-definite",
    "¬Q: There exists y in V such that B(x,y) != 0"
]

N_HYP = 3
NEG_Q_INDEX = 3