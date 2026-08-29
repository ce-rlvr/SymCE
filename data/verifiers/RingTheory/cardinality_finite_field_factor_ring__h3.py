import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            q, n, f_expr = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if isinstance(q, (int, sympy.Integer)) and q >= 2:
            factors = sympy.ntheory.factorint(int(q))
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if h1:
            factors = sympy.ntheory.factorint(int(q))
            p_prime = list(factors.keys())[0]
            p = Poly(f_expr, x, domain=sympy.GF(p_prime))
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            if not isinstance(n, (int, sympy.Integer)):
                neg_q = True
            else:
                factors = sympy.ntheory.factorint(int(q))
                p_prime = list(factors.keys())[0]
                p = Poly(f_expr, x, domain=sympy.GF(p_prime))
                
                if p.is_zero:
                    neg_q = True
                else:
                    deg = p.degree()
                    neg_q = (int(q) ** int(deg)) != (int(q) ** int(n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ['H_1: F_q is a finite field', 'H_2: f is a polynomial', 'not Q: factor ring does not have q^n elements']

N_HYP = 2
NEG_Q_INDEX = 2