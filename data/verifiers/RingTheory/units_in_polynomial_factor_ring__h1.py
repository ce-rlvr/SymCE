import sympy as sp
from sympy import Poly, groebner

# Top-level setup
# No special groups or matrices are needed for this ring theory theorem.
# The witness is expected to be a tuple of two sympy expressions: (p(x), f(x)).

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            p_expr, f_expr = witness
        else:
            return [False, False, False]
            
        p_expr = sp.sympify(p_expr)
        f_expr = sp.sympify(f_expr)
        
        symbols = p_expr.free_symbols | f_expr.free_symbols
        if len(symbols) == 1:
            var = list(symbols)[0]
        elif len(symbols) == 0:
            var = sp.Symbol('x')
        else:
            if sp.Symbol('x') in symbols:
                var = sp.Symbol('x')
            else:
                var = list(symbols)[0]
                
        p_poly = Poly(p_expr, var)
        f_poly = Poly(f_expr, var)
        
        domain = p_poly.domain.unify(f_poly.domain)
        
        # H_1: p(x) is a non-constant polynomial
        h1 = p_poly.degree() > 0
        
        # H_2: f(x) is a polynomial
        h2 = True
        
        # Check if f(x) and p(x) are relatively prime
        gcd_poly = p_poly.gcd(f_poly)
        is_rel_prime = False
        if gcd_poly.is_ground:
            c = gcd_poly.LC()
            if domain.is_Field:
                if c != 0:
                    is_rel_prime = True
            else:
                if c == 1 or c == -1:
                    is_rel_prime = True
                    
        # Check if f(x) + (p(x)) is a unit in F[x]/(p(x))
        gb = groebner([p_poly, f_poly], var, domain=domain)
        is_unit = False
        for g in gb.polys:
            if g.is_ground:
                c = g.LC()
                if domain.is_Field:
                    if c != 0:
                        is_unit = True
                        break
                else:
                    if c == 1 or c == -1:
                        is_unit = True
                        break
                        
        conclusion = (is_unit == is_rel_prime)
        neg_q = not conclusion
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: p is a non-constant polynomial",
    "H_2: f is a polynomial",
    "¬Q: The equivalence fails"
]

N_HYP = 2
NEG_Q_INDEX = 2