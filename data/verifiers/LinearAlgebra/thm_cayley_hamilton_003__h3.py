import sympy
from sympy import Matrix, zeros, eye, Symbol, Poly, Expr

x = Symbol('x')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            p = witness.get('p')
        else:
            T, p = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = isinstance(T, Matrix) and T.shape[0] > 0
    except Exception:
        h1 = False

    # H_2: T: V -> V is a linear operator
    try:
        h2 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h2 = False

    # neg_Q: p(T) is NOT the zero operator on V
    try:
        if callable(p):
            result = p(T)
        elif isinstance(p, (list, tuple)):
            coeffs = p
            n = T.shape[0]
            result = zeros(n, n)
            for i, c in enumerate(coeffs):
                power = len(coeffs) - 1 - i
                result += c * (T ** power)
        else:
            if isinstance(p, Expr):
                syms = p.free_symbols
                if len(syms) == 1:
                    var = list(syms)[0]
                    poly = Poly(p, var)
                else:
                    poly = Poly(p, x)
            else:
                poly = Poly(p, x)
            
            coeffs = poly.all_coeffs()
            n = T.shape[0]
            result = zeros(n, n)
            for i, c in enumerate(coeffs):
                power = len(coeffs) - 1 - i
                result += c * (T ** power)
                
        if isinstance(result, Matrix):
            neg_q = not result.is_zero_matrix
        else:
            neg_q = bool(result != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T: V -> V is a linear operator",
    "¬Q: p(T) is not the zero operator on V"
]

N_HYP = 2
NEG_Q_INDEX = 2