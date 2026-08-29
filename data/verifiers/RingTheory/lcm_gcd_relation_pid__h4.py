import sympy
import math

def is_divides(x, y):
    try:
        if x == 0:
            return y == 0
        if isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)):
            return int(y) % int(x) == 0
        
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        
        if x_sym.is_Integer and y_sym.is_Integer:
            return int(y_sym) % int(x_sym) == 0
            
        q, r = sympy.div(y_sym, x_sym)
        return r == 0
    except Exception:
        return False

def is_associate(x, y):
    return is_divides(x, y) and is_divides(y, x)

def is_gcd(d, a, b):
    if not (is_divides(d, a) and is_divides(d, b)):
        return False
    try:
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            actual_gcd = math.gcd(int(a), int(b))
            return is_associate(d, actual_gcd)
        else:
            a_sym = sympy.sympify(a)
            b_sym = sympy.sympify(b)
            actual_gcd = sympy.gcd(a_sym, b_sym)
            return is_associate(d, actual_gcd)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 5:
                R, a, b, d, m = witness
            elif len(witness) == 4:
                a, b, d, m = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if not all(isinstance(x, (int, sympy.Integer)) for x in (a, b, d, m)):
            a = sympy.sympify(a)
            b = sympy.sympify(b)
            d = sympy.sympify(d)
            m = sympy.sympify(m)
    except Exception:
        return [False, False, False, False]

    # H_1: R is a principal ideal domain
    try:
        symbols = set()
        for x in (a, b, d, m):
            if hasattr(x, 'free_symbols'):
                symbols.update(x.free_symbols)
        if len(symbols) > 1:
            h1 = False
        elif any(isinstance(x, sympy.MatrixBase) for x in (a, b, d, m)):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: a and b are non-zero elements of R
    try:
        h2 = bool((a != 0) and (b != 0))
    except Exception:
        h2 = False

    # H_3: d is a greatest common divisor of a and b
    try:
        h3 = bool(is_gcd(d, a, b))
    except Exception:
        h3 = False

    # ¬Q: The product ab is not associate to the product dm in R
    try:
        neg_q = not is_associate(a * b, d * m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a and b are non-zero elements of R",
    "H_3: d is a greatest common divisor of a and b",
    "¬Q: The product ab is not associate to the product dm in R"
]

N_HYP = 3
NEG_Q_INDEX = 3