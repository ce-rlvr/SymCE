import sympy
from sympy import S, Symbol, solveset, Eq
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        x, n = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: x >= 0
    try:
        x_sym = sympy.sympify(x)
        h1 = bool(x_sym >= 0)
    except Exception:
        h1 = False

    # H2: n is an integer
    try:
        n_sym = sympy.sympify(n)
        h2 = n_sym.is_integer
        if h2 is None:
            h2 = isinstance(n, int)
        h2 = bool(h2)
    except Exception:
        h2 = False

    # H3: n >= 1
    try:
        h3 = bool(n_sym >= 1)
    except Exception:
        h3 = False

    # neg_Q: not (exists unique real y >= 0 st y^n = x)
    try:
        if x_sym == S.Infinity:
            # Infinity is not a real number, so y^n = oo has no real solution y.
            neg_q = True
        elif x_sym.is_real and x_sym.is_finite:
            # For any finite real x >= 0 and integer n >= 1, there is exactly one real root y >= 0.
            neg_q = False
        else:
            # Fallback for other potential objects
            y = Symbol('y', real=True)
            roots = solveset(Eq(y**n_sym, x_sym), y, domain=S.Reals)
            if roots.is_FiniteSet:
                valid_roots = []
                for r in roots:
                    try:
                        if bool(r >= 0):
                            valid_roots.append(r)
                    except Exception:
                        pass
                neg_q = len(valid_roots) != 1
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x >= 0",
    "H_2: n is an integer",
    "H_3: n >= 1",
    "¬Q: There does not exist a unique real number y >= 0 such that y^n = x"
]

N_HYP = 3
NEG_Q_INDEX = 3