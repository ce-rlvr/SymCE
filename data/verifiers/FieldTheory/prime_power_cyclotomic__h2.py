import sympy
import sympy.polys
from sympy import isprime
from sympy.abc import x

# Top-level setup
# (No specific named objects needed for this domain)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        p, k = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2 is a definitional statement, so it trivially holds for any valid witness
    h2 = True
    
    try:
        k_sym = sympy.sympify(k)
        p_sym = sympy.sympify(p)
        
        if not k_sym.is_real:
            neg_q = False
        else:
            n1 = p_sym**k_sym
            n2 = p_sym**(k_sym - 1)
            
            try:
                is_n1_valid = (n1 == int(n1)) and (n1 >= 1)
            except Exception:
                is_n1_valid = False
                
            if is_n1_valid:
                poly1 = sympy.polys.cyclotomic_poly(int(n1), x)
            else:
                poly1 = None
                
            try:
                is_p_valid = (p_sym == int(p_sym)) and (p_sym >= 1)
            except Exception:
                is_p_valid = False
                
            if is_p_valid:
                poly_p = sympy.polys.cyclotomic_poly(int(p_sym), x)
                poly2 = poly_p.subs(x, x**n2)
            else:
                poly2 = None
                
            if poly1 is None or poly2 is None:
                # If the terms are undefined (e.g. fractional index for cyclotomic polynomial),
                # the equality fails to hold.
                neg_q = True
            else:
                diff = sympy.simplify(poly1 - poly2)
                neg_q = not bool(diff.is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \\Phi_n(x) denotes the n-th cyclotomic polynomial",
    "¬Q: \\Phi_{p^k}(x) != \\Phi_p(x^{p^{k-1}})"
]

N_HYP = 2
NEG_Q_INDEX = 2