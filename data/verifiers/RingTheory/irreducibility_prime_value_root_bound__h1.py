import sympy as sp
from sympy import Poly
from sympy.abc import x, y, z
import math

CONDITION_LABELS = [
    "H_1: There exists an integer c such that |f(c)| is a prime number",
    "H_2: c > 1 + max{|alpha| : f(alpha) = 0}",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    if isinstance(witness, (tuple, list)):
        if len(witness) != 2:
            return [False, False, False]
        f, c = witness
    else:
        f = witness
        c = None

    try:
        f = sp.sympify(f)
        f = sp.nsimplify(f, rational=True)
        free_vars = f.free_symbols
        if len(free_vars) != 1:
            return [False, False, False]
        var = list(free_vars)[0]
        poly_f = Poly(f, var)
        if poly_f.degree() < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        roots = poly_f.nroots()
        max_root = max(abs(complex(r)) for r in roots) if roots else 0
    except Exception:
        max_root = float('inf')

    h1 = False
    h2 = False

    if c is not None:
        try:
            c_val = int(c)
            val_eval = sp.sympify(poly_f.eval(c_val))
            if val_eval.is_integer and sp.isprime(abs(int(val_eval))):
                h1 = True
            if c_val > 1 + max_root:
                h2 = True
        except Exception:
            pass
    else:
        try:
            # Check H1 independently
            for test_c in range(-1000, 1000):
                try:
                    val_eval = sp.sympify(poly_f.eval(test_c))
                    if val_eval.is_integer and sp.isprime(abs(int(val_eval))):
                        h1 = True
                        break
                except Exception:
                    pass
            
            # Check H2 (which implies H1 if we find such c)
            if max_root != float('inf'):
                start_c = int(math.floor(max_root + 1)) + 1
                for test_c in range(start_c, start_c + 1000):
                    try:
                        val_eval = sp.sympify(poly_f.eval(test_c))
                        if val_eval.is_integer and sp.isprime(abs(int(val_eval))):
                            h2 = True
                            h1 = True
                            break
                    except Exception:
                        pass
        except Exception:
            pass

    try:
        factors = sp.factor_list(f, domain='QQ')
        num_factors = sum(mult for fac, mult in factors[1] if Poly(fac, var).degree() >= 1)
        neg_q = (num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]