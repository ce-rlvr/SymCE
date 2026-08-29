import sympy
import sympy.polys
import math
import itertools
import functools

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        K, t_list, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(K, 'is_Field'):
            h1 = bool(K.is_Field)
        elif hasattr(K, 'is_field'):
            h1 = bool(K.is_field)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not isinstance(t_list, (list, tuple)):
            h2 = False
        elif len(t_list) != n:
            h2 = False
        elif n == 0:
            h2 = True
        else:
            h2 = all(isinstance(t, (sympy.Symbol, sympy.Dummy)) for t in t_list) and len(set(t_list)) == n
    except Exception:
        h2 = False

    try:
        if n == 0:
            neg_q = True
        elif n < 0:
            neg_q = True
        else:
            x = sympy.Symbol('x')
            poly = x**n + sum(t_list[i] * x**i for i in range(n))
            factored = sympy.factor(poly)
            neg_q = factored != poly
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: K is a field", "H_2: t_i are algebraically independent", "\u00acQ: polynomial is not irreducible"]

N_HYP = 2
NEG_Q_INDEX = 2