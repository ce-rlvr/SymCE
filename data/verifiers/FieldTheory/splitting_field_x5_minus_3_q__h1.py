import math
import sympy
from sympy import Poly, roots, minpoly
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

# Top-level setup
# The witness is expected to be a polynomial expression in x over Q.

def conditions(witness):
    try:
        p = Poly(witness, x)
        h1_ok = bool((p.domain.is_QQ or p.domain.is_ZZ) and p.degree() >= 1)
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            p = Poly(witness, x, domain='QQ')
            factors = p.factor_list()[1]
            max_order = 1
            for fac, mult in factors:
                max_order *= math.factorial(fac.degree())
            
            # The degree of the splitting field must divide the product of the factorials 
            # of the degrees of its irreducible factors.
            if max_order % 20 != 0:
                neg_q_ok = True
            # Fast-path for polynomials of the form c_5 * x^5 + c_0
            elif p.degree() == 5 and p.is_irreducible and p.all_coeffs()[1:5] == [0, 0, 0, 0]:
                neg_q_ok = False
            else:
                # Fallback to computing the exact degree of the splitting field
                rts = roots(p, multiple=True)
                if len(rts) < p.degree():
                    # If we cannot find all roots, we cannot easily verify the counterexample
                    neg_q_ok = False
                else:
                    exts = []
                    for r in rts:
                        if not r.is_rational and r not in exts:
                            exts.append(r)
                    
                    if not exts:
                        deg = 1
                    elif len(exts) == 1:
                        deg = minpoly(exts[0], x).degree()
                    else:
                        g = primitive_element(exts, x)
                        deg = Poly(g, x).degree()
                        
                    neg_q_ok = bool(deg != 20)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q of degree >= 1",
    "¬Q: The degree of the splitting field of f(x) over Q is not 20"
]

N_HYP = 1
NEG_Q_INDEX = 1