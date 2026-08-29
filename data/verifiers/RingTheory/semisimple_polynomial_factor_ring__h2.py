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

from sympy import QQ, ZZ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let F be a field. The factor ring F[x]/<f(x)> is a semisimple ring if and only if f(x) is square-free."
    
    The missing hypothesis is that f(x) is a non-constant polynomial.
    If f(x) is a non-zero constant (e.g., f(x) = 1), then f(x) is square-free, 
    but F[x]/<f(x)> is the zero ring, which is not a semisimple ring.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F_domain, f = witness
        else:
            F_domain = QQ
            f = witness
            
        if hasattr(F_domain, 'is_Field'):
            h1 = bool(F_domain.is_Field)
        elif F_domain in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        f_expr = sympy.sympify(f)
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = sympy.Symbol('x')
        else:
            neg_q = False
            return [h1, neg_q]

        f_poly = sympy.Poly(f_expr, var, domain=F_domain)
        
        if f_poly.is_zero:
            is_sqf = False
            is_semi = False
        else:
            deg = f_poly.degree()
            if deg <= 0:
                is_sqf = True
                is_semi = False
            else:
                sqf = f_poly.sqf_list()
                has_repeated = any(mult > 1 for factor, mult in sqf[1])
                is_sqf = not has_repeated
                is_semi = not has_repeated
                
        iff_holds = (is_semi == is_sqf)
        neg_q = not iff_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "¬Q: The equivalence fails"]

N_HYP = 1
NEG_Q_INDEX = 1