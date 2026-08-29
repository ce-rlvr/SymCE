import sympy
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
CC = sympy.CC
QQ = sympy.QQ
RR = sympy.RR
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (K, f) or just an expression f (in which case K defaults to CC).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        K, f = witness
    else:
        K = 'CC'
        f = witness

    # H_1: K is an algebraically closed field
    try:
        if isinstance(K, str):
            h1 = K in ['CC', 'C', 'Complexes', 'ComplexField', 'AlgebraicField']
        else:
            h1 = K == sympy.CC or str(K) == 'CC'
    except Exception:
        h1 = False

    # H_2: The degree of f(x) is a positive integer n
    try:
        # Determine the generator (variable)
        if hasattr(f, 'free_symbols'):
            symbols = f.free_symbols
            if x in symbols:
                gen = x
            elif len(symbols) > 0:
                gen = list(symbols)[0]
            else:
                gen = x
        else:
            gen = x
            
        n = sympy.degree(f, gen)
        h2 = bool(n.is_integer and n >= 1)
    except Exception:
        h2 = False

    # ¬Q: f(x) CANNOT be factored into the form c(x-a_1)(x-a_2)...(x-a_n) over K
    # If f(x) can be factored into n linear factors, it must be equivalent to a polynomial of degree n.
    # Since K is algebraically closed, ANY polynomial of degree n >= 1 factors into n linear factors.
    # Thus, the conclusion fails iff f(x) is NOT equivalent to a polynomial of degree n.
    try:
        if not h2:
            neg_q = True
        else:
            f_simp = sympy.cancel(f)
            p = sympy.Poly(f_simp, gen)
            actual_degree = p.degree()
            if actual_degree != n:
                neg_q = True
            else:
                neg_q = False
    except sympy.polys.polyerrors.PolynomialError:
        # If it cannot be converted to a polynomial (e.g., contains 1/x, sin(x), sqrt(x)), it cannot be factored as such.
        neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: The degree of f(x) is a positive integer n",
    "¬Q: f(x) cannot be factored into n linear factors over K"
]

N_HYP = 2
NEG_Q_INDEX = 2