import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        A, B = witness
        
        if not hasattr(A, 'charpoly'):
            A = sympy.Matrix(A)
        if not hasattr(B, 'charpoly'):
            B = sympy.Matrix(B)
    except Exception:
        return [False, False]

    try:
        h1 = bool(A.is_square and B.is_square and A.shape == B.shape)
    except Exception:
        h1 = False

    try:
        x = sympy.Symbol('x')
        poly_A = A.charpoly(x)
        poly_B = B.charpoly(x)
        diff = sympy.expand(poly_A.as_expr() - poly_B.as_expr())
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n complex matrices",
    "¬Q: The characteristic polynomial of A is not identical to the characteristic polynomial of B"
]

N_HYP = 1
NEG_Q_INDEX = 1