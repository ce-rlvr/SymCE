import sympy
from sympy import Symbol, Poly, QQ, ZZ, I, sqrt, roots, GF
from sympy.matrices import eye, zeros

# Top-level setup
x = Symbol('x')

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) has no roots in F",
    "H_3: alpha is a root of f(x) in some extension field of F",
    "¬Q: f(x) is not the minimal polynomial of alpha over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        domain, f, alpha = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1 = bool(domain.is_Field)
    except Exception:
        h1 = False
        
    # H_2: f(x) has no roots in F
    try:
        p = Poly(f, x, domain=domain)
        if p.is_zero:
            h2 = False
        else:
            rts = sympy.roots(f, x, domain=domain)
            h2 = (len(rts) == 0)
    except Exception:
        h2 = False
        
    # H_3: alpha is a root of f(x) in some extension field of F
    try:
        val = f.subs(x, alpha)
        if hasattr(val, 'simplify'):
            val = val.simplify()
        h3 = bool(val == 0)
    except Exception:
        h3 = False
        
    # ¬Q: f(x) is not the minimal polynomial of alpha over F
    try:
        p = Poly(f, x, domain=domain)
        # The minimal polynomial of alpha over F must be monic and irreducible over F.
        is_minpoly = p.is_monic and p.is_irreducible
        neg_q = not is_minpoly
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]