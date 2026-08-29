import sympy as sp
from sympy.abc import x, y, z
import math
import itertools
import functools

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for Ore's Prime Value Irreducibility Criterion (false conjecture).
    The witness can be:
      - f (a sympy expression)
      - (f, c_list)
      - (f, p_val)
      - (f, p_val, c_list)
    """
    p_val = None
    c_list = None
    
    if isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            f, p_val, c_list = witness
        elif len(witness) == 2:
            if isinstance(witness[1], (list, tuple, set)):
                f, c_list = witness
            else:
                f, p_val = witness
        elif len(witness) > 0:
            f = witness[0]
        else:
            return [False, False, False, False]
    else:
        f = witness

    try:
        if isinstance(f, str):
            f = sp.sympify(f)
    except Exception:
        pass

    # H1: f(x) is a polynomial over integers
    h1 = False
    var = sp.Symbol('x')
    poly_f = None
    try:
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = sp.Symbol('x')
        else:
            var = sp.Symbol('x')
            
        poly_f = sp.Poly(f, var)
        if poly_f.domain.is_ZZ:
            h1 = True
    except Exception:
        pass

    # H2: The degree n of f(x) satisfies n >= 5
    h2 = False
    n = -1
    try:
        if h1 and poly_f is not None:
            n = poly_f.degree()
            if n >= 5:
                h2 = True
    except Exception:
        pass

    # H3: There exist n distinct integers c_i such that |f(c_i)| = p for all 1 <= i <= n
    h3 = False
    try:
        if h1 and h2 and poly_f is not None:
            coeffs = [int(coeff) for coeff in poly_f.all_coeffs()]
            
            def eval_poly(c_val):
                res = 0
                for coeff in coeffs:
                    res = res * c_val + coeff
                return abs(res)

            def check_p_match(val, p_val):
                if not sp.isprime(val):
                    return False
                if p_val is not None:
                    try:
                        target_p = int(sp.sympify(p_val))
                        return val == target_p
                    except Exception:
                        return False
                return True

            if c_list is not None:
                valid_c = []
                for c in c_list:
                    try:
                        c_val = sp.sympify(c)
                        if c_val.is_integer:
                            valid_c.append(int(c_val))
                    except Exception:
                        pass
                valid_c = list(set(valid_c))
                if len(valid_c) >= n:
                    vals = [eval_poly(c) for c in valid_c]
                    counts = {}
                    for val in vals:
                        counts[val] = counts.get(val, 0) + 1
                    for val, count in counts.items():
                        if count >= n:
                            if check_p_match(val, p_val):
                                h3 = True
                                break
            
            if not h3:
                val_counts = {}
                # Search a reasonable range of integers
                for c in range(-2000, 2001):
                    val = eval_poly(c)
                    if val not in val_counts:
                        val_counts[val] = set()
                    val_counts[val].add(c)
                    if len(val_counts[val]) >= n:
                        if check_p_match(val, p_val):
                            h3 = True
                            break
    except Exception:
        pass

    # neg_Q: f(x) is NOT irreducible over Q (i.e., it is reducible)
    neg_q = False
    try:
        if h1:
            factors = sp.factor_list(f, domain='QQ')
            num_factors = sum(mult for fac, mult in factors[1] if fac.as_poly(var).degree() > 0)
            if num_factors > 1:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over integers",
    "H_2: degree n is at least 5",
    "H_3: n distinct integers give absolute value p",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3