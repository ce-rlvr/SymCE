import sympy
from sympy import Symbol, Poly, oo, isprime, S

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be an integral domain. Let the degree of f(x) be n. 
    Then f(x) has at most n distinct roots in R."
    
    The dropped hypothesis from the true theorem is that f(x) must be non-zero.
    A valid counterexample is the zero polynomial, which has degree -oo but 
    infinitely many (or |R|) roots.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Parse witness. Expected formats:
        # 1. (ring_modulus, f_expr) where ring_modulus is 0 for Z, or p for Z_p
        # 2. f_expr (assumes ring is Z)
        if isinstance(witness, tuple):
            if len(witness) == 2:
                ring, f_expr = witness
            else:
                return [False, False, False]
                
            if ring in ("Z", S.Integers, 0):
                p = 0
                h1 = True
            elif isinstance(ring, int) and ring > 1:
                p = ring
                h1 = isprime(p)
            else:
                p = -1
        else:
            f_expr = witness
            p = 0
            h1 = True
            
        if p != -1:
            # Check H2: f(x) has a well-defined degree n
            f_poly_zz = Poly(f_expr, x, domain='ZZ')
            
            if p > 0:
                # Reduce coefficients modulo p for the field Z_p
                coeffs_mod = [c % p for c in f_poly_zz.all_coeffs()]
                f_poly = Poly.from_list(coeffs_mod, gens=x, domain='ZZ')
            else:
                f_poly = f_poly_zz
                
            n = f_poly.degree()
            if n == -oo or (n.is_Integer and n >= 0):
                h2 = True
            
            # Check ¬Q: f(x) has more than n distinct roots in R
            if p == 0:
                if f_poly.is_zero:
                    roots_count = oo
                else:
                    roots_dict = sympy.roots(f_poly)
                    roots_count = sum(1 for r in roots_dict if r.is_Integer)
            else:
                roots_count = 0
                for i in range(p):
                    val = f_poly.eval(i)
                    if val % p == 0:
                        roots_count += 1
                        
            if roots_count > n:
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f(x) has a well-defined degree n",
    "¬Q: f(x) has more than n distinct roots in R"
]

N_HYP = 2
NEG_Q_INDEX = 2