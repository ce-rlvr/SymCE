import sympy
from sympy.abc import x, y, z
import math
import itertools
import functools

def conditions(witness):
    try:
        I_gens, J_gens, m, n = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a commutative ring with identity
    # We implicitly define R by the generators provided. 
    # We check that the generators are valid mathematical expressions.
    try:
        h1 = isinstance(I_gens, list) and isinstance(J_gens, list)
        if h1:
            for e in I_gens + J_gens:
                sympy.sympify(e)
    except Exception:
        h1 = False

    # H_2: I and J are ideals of R
    # Any non-empty list of elements generates an ideal in R.
    try:
        h2 = isinstance(I_gens, list) and isinstance(J_gens, list) and len(I_gens) > 0 and len(J_gens) > 0
    except Exception:
        h2 = False

    # H_3: m and n are positive integers
    try:
        h3 = isinstance(m, int) and m > 0 and isinstance(n, int) and n > 0
    except Exception:
        h3 = False

    # neg_Q: I^m + J^n != R
    try:
        I_gens_sym = [sympy.sympify(e) for e in I_gens]
        J_gens_sym = [sympy.sympify(e) for e in J_gens]
        
        # Generators for I^m are all products of m elements from I_gens
        I_m_gens = [math.prod(p) for p in itertools.product(I_gens_sym, repeat=m)]
        # Generators for J^n are all products of n elements from J_gens
        J_n_gens = [math.prod(p) for p in itertools.product(J_gens_sym, repeat=n)]
        
        # Generators for the sum ideal I^m + J^n
        sum_gens = I_m_gens + J_n_gens
        
        # The ideal is the whole ring iff the gcd of its generators is a unit.
        # In ZZ or K[x], the units are 1 and -1 (sympy.gcd normalizes to monic for polynomials).
        ideal_gcd = functools.reduce(sympy.gcd, sum_gens)
        is_unit = (ideal_gcd == 1 or ideal_gcd == -1)
        
        neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "H_3: m and n are positive integers",
    "¬Q: I^m + J^n != R"
]

N_HYP = 3
NEG_Q_INDEX = 3