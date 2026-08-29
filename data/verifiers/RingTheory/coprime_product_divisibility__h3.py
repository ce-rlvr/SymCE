import sympy
from sympy.abc import x, y, z

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
    
    def is_ufd_element(val):
        if isinstance(val, bool):
            return False
        if isinstance(val, (int, sympy.Integer)):
            return True
        if isinstance(val, sympy.Expr) and not getattr(val, 'is_Matrix', False):
            return True
        return False

    try:
        h1 = is_ufd_element(a) and is_ufd_element(b) and is_ufd_element(c)
        if h1:
            if isinstance(a, sympy.Expr):
                h1 = h1 and (sympy.simplify(a) != 0)
            else:
                h1 = h1 and (a != 0)
            if isinstance(b, sympy.Expr):
                h1 = h1 and (sympy.simplify(b) != 0)
            else:
                h1 = h1 and (b != 0)
            if isinstance(c, sympy.Expr):
                h1 = h1 and (sympy.simplify(c) != 0)
            else:
                h1 = h1 and (c != 0)
    except Exception:
        h1 = False

    def divides(divisor, dividend):
        try:
            if isinstance(divisor, (int, sympy.Integer)) and isinstance(dividend, (int, sympy.Integer)):
                if divisor == 0:
                    return False
                return dividend % divisor == 0
            
            div_sym = sympy.sympify(divisor)
            dividend_sym = sympy.sympify(dividend)
            if div_sym == 0:
                return False
            
            try:
                res = sympy.div(dividend_sym, div_sym)
            except Exception:
                res = None
                
            if res is not None:
                q, r = res
                return sympy.simplify(r) == 0
            else:
                ratio = sympy.simplify(dividend_sym / div_sym)
                return ratio.is_polynomial() == True
        except Exception:
            return False

    try:
        h2 = divides(a, c)
    except Exception:
        h2 = False

    try:
        h3 = divides(b, c)
    except Exception:
        h3 = False

    try:
        neg_q = not divides(a * b, c)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements in a UFD",
    "H_2: a divides c",
    "H_3: b divides c",
    "¬Q: ab does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3