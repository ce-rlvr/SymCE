import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
        A = sympy.Matrix(A)
        B = sympy.Matrix(B)
        if A.shape[0] != A.shape[1] or B.shape[0] != B.shape[1]:
            h1 = False
        elif A.shape != B.shape:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        A, B = witness
        A = sympy.Matrix(A)
        h2 = bool(A.det() != 0)
    except Exception:
        h2 = False

    try:
        A, B = witness
        B = sympy.Matrix(B)
        n = B.shape[0]
        h3 = bool((B**n) == sympy.zeros(n, n))
    except Exception:
        h3 = False

    try:
        A, B = witness
        A = sympy.Matrix(A)
        B = sympy.Matrix(B)
        neg_q = bool((A + B).det() == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space (A and B are square matrices of same dimension)",
    "H_2: A is an invertible linear operator",
    "H_3: B is a nilpotent linear operator",
    "¬Q: A + B is not invertible"
]

N_HYP = 3
NEG_Q_INDEX = 3