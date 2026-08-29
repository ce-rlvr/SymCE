import sympy
from sympy import Poly, Symbol, Rational, I, sqrt, cbrt
from sympy.abc import x, y, z
from sympy import QQ, ZZ

# Top-level setup
# The witness should be a tuple: (f, K, L)
# where:
#   - f is a SymPy polynomial or expression (e.g., x**3 - 2)
#   - K is the base field domain (e.g., QQ)
#   - L is the extension field domain (e.g., QQ.algebraic_field(cbrt(2))), 
#     or a list of algebraic generators (e.g., [cbrt(2)]), 
#     or a single algebraic generator (e.g., cbrt(2)).

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        f, K, L = witness
        
        # Extract the variable and expression
        if hasattr(f, 'gen'):
            x_sym = f.gen
            f_expr = f.as_expr()
        else:
            syms = list(f.free_symbols)
            if len(syms) != 1:
                return [False, False, False]
            x_sym = syms[0]
            f_expr = f
            
        # Check H_1: f(x) is irreducible over K
        try:
            poly_K = Poly(f_expr, x_sym, domain=K)
            h1 = bool(poly_K.is_irreducible)
        except Exception:
            h1 = False
            
        # Construct the extension field L
        try:
            if isinstance(L, (list, tuple)):
                L_domain = K.algebraic_field(*L)
            elif isinstance(L, sympy.Expr):
                L_domain = K.algebraic_field(L)
            else:
                L_domain = L
                
            poly_L = Poly(f_expr, x_sym, domain=L_domain)
            factors = poly_L.factor_list()[1]
            
            # Check H_2: f(x) has at least one root in L (at least one linear factor)
            h2 = any(fac.degree() == 1 for fac, mult in factors)
        except Exception:
            h2 = False
            
        # Check ¬Q: f(x) does NOT split completely into linear factors over L
        try:
            q = all(fac.degree() == 1 for fac, mult in factors)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) over K is an irreducible polynomial",
    "H_2: f(x) has at least one root in L",
    "¬Q: f(x) does not split completely into linear factors over L"
]

N_HYP = 2
NEG_Q_INDEX = 2