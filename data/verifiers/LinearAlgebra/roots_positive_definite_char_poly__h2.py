import sympy
from sympy import Matrix, eye, zeros, Symbol

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, lam = witness
        lam = sympy.sympify(lam)
    except Exception:
        return [False, False, False]
        
    # H1: A is an n x n symmetric matrix over the real numbers
    try:
        if not isinstance(A, sympy.MatrixBase):
            h1 = False
        elif not A.is_square or A.shape[0] < 1:
            h1 = False
        elif A != A.T:
            h1 = False
        else:
            h1 = all(sympy.sympify(e).is_real for e in A)
    except Exception:
        h1 = False
        
    # H2: \lambda is a root of the characteristic polynomial of A
    try:
        x = Symbol('x')
        poly_expr = A.charpoly(x).as_expr()
        val = poly_expr.subs(x, lam)
        h2 = bool(sympy.simplify(val) == 0)
    except Exception:
        h2 = False
        
    # neg_Q: \lambda is not a strictly positive real number
    try:
        if lam.is_real:
            neg_q = not bool(lam > 0)
        else:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n symmetric matrix over the real numbers",
    "H_2: \\lambda is a root of the characteristic polynomial of A",
    "¬Q: \\lambda is not a strictly positive real number"
]

N_HYP = 2
NEG_Q_INDEX = 2