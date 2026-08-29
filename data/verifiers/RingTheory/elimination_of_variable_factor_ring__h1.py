import sympy

x, y = sympy.symbols('x y')
A, B, C = sympy.symbols('A B C', commutative=False)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f = witness[-1]
        else:
            f = witness

        if isinstance(f, list):
            f = sympy.Matrix(f)
        elif not isinstance(f, sympy.MatrixBase):
            f = sympy.sympify(f)
    except Exception:
        return [False, False, False]

    h1 = True

    try:
        if isinstance(f, sympy.MatrixBase):
            h2 = True
            for entry in f:
                if entry.has(y):
                    h2 = False
                if entry.has(x) and not entry.is_polynomial(x):
                    h2 = False
        else:
            h2 = True
            if f.has(y):
                h2 = False
            if f.has(x) and not f.is_polynomial(x):
                h2 = False
    except Exception:
        h2 = False

    try:
        if isinstance(f, sympy.MatrixBase):
            if f.rows != f.cols:
                neg_q = True
            else:
                is_scalar = True
                for i in range(f.rows):
                    for j in range(f.cols):
                        if i == j:
                            diff = sympy.expand(f[i, j] - f[0, 0])
                        else:
                            diff = sympy.expand(f[i, j])
                        if diff != 0:
                            is_scalar = False
                
                if is_scalar and getattr(f[0, 0], 'is_commutative', True) is False:
                    is_scalar = False
                    
                neg_q = not is_scalar
        else:
            neg_q = (getattr(f, 'is_commutative', True) is False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The ring is the polynomial ring in two variables over R",
    "H_2: f is a polynomial in one variable",
    "¬Q: The factor ring is not isomorphic to the polynomial ring in one variable"
]

N_HYP = 2
NEG_Q_INDEX = 2