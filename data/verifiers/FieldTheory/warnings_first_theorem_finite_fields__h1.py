import sympy
from sympy import Poly
from sympy.ntheory import isprime
import itertools

from sympy.abc import x, y, z, t, u, v, w

def get_val(witness, key):
    if isinstance(witness, dict):
        return witness[key]
    return getattr(witness, key)

def conditions(witness):
    # H1: f_1, ..., f_k are polynomials in F_q
    try:
        q = get_val(witness, 'q')
        vars = get_val(witness, 'vars')
        polys = get_val(witness, 'polys')
        
        h1 = isinstance(q, int) and q > 1 and len(polys) >= 1
        if h1:
            for f in polys:
                p_obj = Poly(f, *vars)
                if not all(c.is_integer for c in p_obj.coeffs()):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: sum of total degrees is strictly less than n
    try:
        vars = get_val(witness, 'vars')
        polys = get_val(witness, 'polys')
        n = len(vars)
        
        total_deg = 0
        for f in polys:
            p_obj = Poly(f, *vars)
            deg = p_obj.total_degree()
            total_deg += deg
            
        h2 = bool(total_deg < n)
    except Exception:
        h2 = False

    # H3: N is the number of common zeros of f_1, ..., f_k in F_q^n
    try:
        q = get_val(witness, 'q')
        vars = get_val(witness, 'vars')
        polys = get_val(witness, 'polys')
        expected_N = get_val(witness, 'N')
        
        n = len(vars)
        actual_N = 0
        
        for vals in itertools.product(range(q), repeat=n):
            is_zero = True
            for f in polys:
                val = f.subs(dict(zip(vars, vals)))
                if int(val) % q != 0:
                    is_zero = False
                    break
            if is_zero:
                actual_N += 1
                
        h3 = (actual_N == expected_N)
    except Exception:
        h3 = False

    # neg_Q: N is not divisible by p
    try:
        N = get_val(witness, 'N')
        p = get_val(witness, 'p')
        neg_q = (N % p) != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f_1 to f_k are polynomials in F_q",
    "H_2: sum of total degrees is strictly less than n",
    "H_3: N is the number of common zeros of f_1 to f_k in F_q^n",
    "not Q: N is not divisible by p"
]

N_HYP = 3
NEG_Q_INDEX = 3