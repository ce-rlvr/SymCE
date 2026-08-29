import sympy
from sympy import Symbol, Poly, sympify
from sympy.abc import x
import math

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "H_3: f is a polynomial over R",
    "H_4: f_bar is the image of f over R mod I",
    "¬Q: R_x mod J is not isomorphic to R_I_x mod f_bar"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            f = witness.get('f', x)
            J_gens = witness.get('J_gens', [0])
        else:
            n, f, J_gens = witness
    except Exception:
        return [False] * 5
        
    # H1: R is a commutative ring with identity
    # We assume R = Z, which is a commutative ring with identity.
    h1 = True
    
    # H2: I is a proper ideal of R
    try:
        n_val = int(sympify(n))
        h2 = abs(n_val) != 1
    except Exception:
        h2 = False
        
    # H3: f is a polynomial over R
    try:
        f_poly = Poly(f, x)
        h3 = all(c.is_integer for c in f_poly.coeffs())
    except Exception:
        h3 = False
        
    # H4: f_bar is the image of f over R mod I
    # This is true by definition for our setup.
    h4 = True
    
    # neg_Q: R_x mod J is NOT isomorphic to R_I_x mod f_bar
    try:
        if not isinstance(J_gens, (list, tuple)):
            J_gens = [J_gens]
            
        def get_size(gens):
            m = 0
            polys = []
            for gen in gens:
                gen_expr = sympify(gen)
                if gen_expr.is_Integer:
                    if m == 0:
                        m = int(gen_expr)
                    else:
                        m = math.gcd(m, int(gen_expr))
                else:
                    polys.append(Poly(gen_expr, x))
                    
            if m == 1 or m == -1:
                return 1
                
            min_deg = float('inf')
            for p in polys:
                lc = p.LC()
                if m == 0:
                    if lc == 1 or lc == -1:
                        min_deg = min(min_deg, p.degree())
                else:
                    if math.gcd(int(lc), m) == 1:
                        min_deg = min(min_deg, p.degree())
                        
            if min_deg == 0:
                return 1
            if m == 0:
                return float('inf')
            if min_deg == float('inf'):
                return float('inf')
            return abs(m) ** min_deg

        size_R_I_f = get_size([n_val, f])
        size_R_J = get_size(J_gens)
        
        neg_q = size_R_I_f != size_R_J
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]