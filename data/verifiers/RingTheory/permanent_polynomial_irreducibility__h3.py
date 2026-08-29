import sympy
from sympy import symbols, Poly, Rational, Integer
from sympy.polys.polytools import factor_list
from sympy.polys.domains import QQ, ZZ, GF
from sympy.abc import x, y, z
import itertools

def conditions(witness) -> list[bool]:
    try:
        n, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(K.is_Field)
    except Exception:
        h1_ok = False

    try:
        h2_ok = int(n) == n and n >= 2
    except Exception:
        h2_ok = False

    try:
        if not (h1_ok and h2_ok):
            neg_q = False
        else:
            n_int = int(n)
            var_names = [f"x_{i}_{j}" for i in range(n_int) for j in range(n_int)]
            syms = symbols(var_names)
            
            perm_poly = 0
            for sigma in itertools.permutations(range(n_int)):
                term = 1
                for i in range(n_int):
                    term *= syms[i * n_int + sigma[i]]
                perm_poly += term
            
            factors = factor_list(perm_poly, domain=K)
            num_factors = sum(power for f, power in factors[1])
            neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 2 is an integer",
    "¬Q: The permanent polynomial perm(X) is reducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2