import sympy
from sympy import Matrix, eye, zeros, Symbol, expand

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = False
        if isinstance(witness, sympy.MatrixBase) and witness.is_square and witness.shape[0] >= 1:
            h1 = True
            for item in witness:
                if item.is_real is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        neg_q = False
        if h1:
            n = witness.shape[0]
            x = Symbol('x')
            char_poly = witness.charpoly(x).as_expr()
            expected_poly = ((x - 1)**(n - 1) * (x + 1))
            neg_q = expand(char_poly - expected_poly) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional Euclidean space (T is a real square matrix)",
    "¬Q: The characteristic polynomial of T is not (x-1)^{n-1}(x+1)"
]

N_HYP = 1
NEG_Q_INDEX = 1