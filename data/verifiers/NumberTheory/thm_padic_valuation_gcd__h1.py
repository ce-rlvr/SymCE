import sympy
from sympy import multiplicity, Rational, sympify, gcd, oo

# Top-level setup
# (No specific named objects needed for this domain)

def v_p(p, n):
    """
    Computes the p-adic valuation of a rational number n.
    Returns sympy.oo if n is 0.
    """
    if n == 0:
        return oo
    try:
        n = Rational(sympify(n))
        return multiplicity(p, n.p) - multiplicity(p, n.q)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        p, a, b = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: v_p(n) denotes the p-adic valuation of n
    # This is a definitional hypothesis, so it holds by definition.
    h2 = True
    
    # ¬Q: v_p(gcd(a, b)) != min(v_p(a), v_p(b))
    try:
        a_sym = sympify(a)
        b_sym = sympify(b)
        
        val_a = v_p(p, a_sym)
        val_b = v_p(p, b_sym)
        
        # Compute gcd using sympy's standard gcd function
        g = gcd(a_sym, b_sym)
        val_g = v_p(p, g)
        
        if val_a is None or val_b is None or val_g is None:
            neg_q = False
        else:
            neg_q = bool(val_g != min(val_a, val_b))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: v_p(n) denotes the p-adic valuation of n",
    "¬Q: v_p(gcd(a, b)) != min(v_p(a), v_p(b))"
]

N_HYP = 2
NEG_Q_INDEX = 2