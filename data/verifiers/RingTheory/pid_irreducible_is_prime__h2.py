import sympy
from sympy import Integer, Poly, Expr, isprime, Rational
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def is_pid(w):
    try:
        if isinstance(w, (int, Integer)):
            return True
        if isinstance(w, Poly):
            if len(w.gens) == 1 and w.domain.is_Field:
                return True
            return False
        if isinstance(w, Expr):
            if not w.is_polynomial():
                return False
            free = w.free_symbols
            if len(free) == 0:
                return w.is_Integer or w.is_Rational
            if len(free) == 1:
                return True
        return False
    except Exception:
        return False

def is_prime_element(w):
    try:
        if isinstance(w, (int, Integer)):
            w_val = abs(int(w))
            if w_val in (0, 1):
                return False
            return isprime(w_val)
        if isinstance(w, Poly):
            if w.degree() <= 0:
                return False
            return w.is_irreducible
        if isinstance(w, Expr):
            if not w.is_polynomial():
                return False
            free = w.free_symbols
            if len(free) == 0:
                if w.is_Integer:
                    w_val = abs(int(w))
                    if w_val in (0, 1):
                        return False
                    return isprime(w_val)
                return False
            if len(free) == 1:
                p = Poly(w, list(free)[0], domain='QQ')
                if p.degree() <= 0:
                    return False
                return p.is_irreducible
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # Witness can be just the element p, or a tuple (R, p)
    if isinstance(witness, tuple) and len(witness) == 2:
        p = witness[1]
    else:
        p = witness

    try:
        h1 = bool(is_pid(p))
    except Exception:
        h1 = False

    try:
        neg_q = not bool(is_prime_element(p))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1