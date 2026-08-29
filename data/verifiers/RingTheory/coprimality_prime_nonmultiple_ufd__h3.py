import sympy
from sympy import isprime, gcd, Integer, Expr, Symbol, factor_list
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
# Symbols x, y, z are available for polynomial witnesses.

def conditions(witness):
    try:
        p, a = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a unique factorization domain
    # We consider Z and Q[x, y, z] as our UFDs.
    try:
        valid_types = (int, Integer, Expr, Symbol)
        h1 = isinstance(p, valid_types) and isinstance(a, valid_types)
    except Exception:
        h1 = False
        
    # H_2: p is a prime element
    try:
        if isinstance(p, int) or (hasattr(p, 'is_Integer') and p.is_Integer):
            h2 = isprime(abs(int(p)))
        else:
            # For polynomials, we check if it is irreducible over the default domain (usually Q)
            factors = factor_list(p)
            h2 = len(factors[1]) == 1 and factors[1][0][1] == 1
    except Exception:
        h2 = False
        
    # neg_Q: gcd(p, a) != 1
    try:
        g = gcd(p, a)
        if isinstance(g, int) or (hasattr(g, 'is_Integer') and g.is_Integer):
            neg_q = abs(int(g)) != 1
        else:
            # For polynomials, gcd is defined up to a unit.
            neg_q = (g != 1) and (g != -1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: p is a prime element",
    "¬Q: The greatest common divisor of p and a is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2