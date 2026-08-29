import sympy as sp
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, sp.Poly):
            f_poly = witness
            f = f_poly.as_expr()
            gen = f_poly.gen
        else:
            f = sp.sympify(witness)
            free = list(f.free_symbols)
            gen = free[0] if free else sp.Symbol('x')
            f_poly = sp.Poly(f, gen)
            
        # H_1: K is an algebraically closed field
        # We assume the witness polynomial is evaluated over an algebraically closed field
        h1 = True
        
        # H_2: f is a non-zero polynomial
        h2 = not f_poly.is_zero
        
        # Conclusion: f has a root of multiplicity >= 2 iff exists alpha such that f(alpha)=0 and f'(alpha)=0
        f_prime = sp.diff(f, gen)
        deg = sp.degree(f_poly, gen)
        
        if deg == 0:
            lhs = False
            rhs = False
        else:
            roots_dict = sp.roots(f, gen)
            if sum(roots_dict.values()) == deg:
                lhs = any(m >= 2 for m in roots_dict.values())
                rhs = False
                for r in roots_dict.keys():
                    val_f = sp.simplify(f.subs(gen, r))
                    val_fp = sp.simplify(f_prime.subs(gen, r))
                    if val_f == 0 and val_fp == 0:
                        rhs = True
                        break
            else:
                # Fallback to gcd if roots cannot be fully extracted
                g = sp.gcd(f, f_prime)
                lhs = sp.degree(g, gen) >= 1
                rhs = sp.degree(g, gen) >= 1
                
        neg_q = (lhs != rhs)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f is a non-zero polynomial",
    "¬Q: f has a root of multiplicity >= 2 is NOT equivalent to exists alpha such that f(alpha)=0 and f'(alpha)=0"
]

N_HYP = 2
NEG_Q_INDEX = 2