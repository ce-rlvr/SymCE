import sympy
import sympy.abc

def divides(a, b):
    if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
        return b % a == 0
    try:
        q, r = sympy.div(b, a)
        return r == 0
    except Exception:
        pass
    try:
        return sympy.rem(b, a) == 0
    except Exception:
        pass
    try:
        return sympy.simplify(b % a) == 0
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        witness_tuple = tuple(witness)
        if len(witness_tuple) == 3:
            a, b, c = witness_tuple
        elif len(witness_tuple) == 4:
            _, a, b, c = witness_tuple
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain
    try:
        def is_ufd_element(elem):
            if isinstance(elem, (int, sympy.Integer, sympy.Rational)):
                return True
            if hasattr(elem, 'is_Matrix') and elem.is_Matrix:
                return False
            if isinstance(elem, (sympy.Expr, sympy.Poly)):
                return True
            return False
        
        h1 = is_ufd_element(a) and is_ufd_element(b) and is_ufd_element(c)
    except Exception:
        h1 = False

    # H_2: a, b, and c are non-zero elements of R
    try:
        h2 = bool(a != 0) and bool(b != 0) and bool(c != 0)
    except Exception:
        h2 = False

    # H_3: a divides the product bc
    try:
        h3 = bool(divides(a, b * c))
    except Exception:
        h3 = False

    # ¬Q: a does not divide c
    try:
        neg_q = not bool(divides(a, c))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: a divides the product bc",
    "¬Q: a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3