import sympy
from sympy import Poly, Symbol, Integer, Rational, RootOf, factor_list
from sympy.abc import x

# Top-level setup
# No special named bindings required for this domain, but we provide x.
# The witness is expected to be an irreducible polynomial over QQ defining the extension L/K.

def conditions(witness):
    try:
        # Extract the minimal polynomial defining the extension L/K
        if isinstance(witness, tuple):
            expr = witness[0]
        else:
            expr = witness
            
        if hasattr(expr, 'free_symbols') and len(expr.free_symbols) == 1:
            gen = list(expr.free_symbols)[0]
        else:
            gen = x
            
        L_minpoly = Poly(expr, gen, domain='QQ')
    except Exception:
        return [False, False, False]
        
    # H_1: L/K is a finite field extension
    # This holds if the defining polynomial is irreducible over QQ.
    try:
        h1 = bool(L_minpoly.is_irreducible)
    except Exception:
        h1 = False
        
    # H_2: alpha is an element of L
    # Any valid extension L has elements, and we can trivially pick alpha to be the generator.
    h2 = h1
    
    # ¬Q: The splitting field of c(x) over K is not a normal extension of K
    # Note: The splitting field of ANY polynomial is unconditionally normal. 
    # The false conjecture arises from dropping the "IsSplittingField" hypothesis from a formal theorem 
    # (like Lean's `Normal.of_isSplittingField`), leaving the formal conclusion `Normal K L`.
    # The prompt generator translated `Normal K L` using the theorem's docstring.
    # Thus, the actual mathematical conclusion being tested is "L is a normal extension of K".
    # We check if L/K is NOT normal.
    try:
        deg = L_minpoly.degree()
        if deg <= 2:
            is_normal = True
        elif deg == 3:
            # A cubic extension is normal iff its discriminant is a perfect square in QQ
            disc = L_minpoly.discriminant()
            disc_rat = Rational(disc)
            is_normal = bool(Integer(disc_rat.p).is_square and Integer(disc_rat.q).is_square)
        elif deg <= 6:
            # For degree 4 to 6, we check if the polynomial splits completely in L
            theta = RootOf(L_minpoly, 0)
            factors = factor_list(L_minpoly.as_expr(), extension=theta)[1]
            is_normal = (len(factors) == deg)
        else:
            # Fallback for high degrees to avoid timeout; assume normal to prevent false positives
            is_normal = True 
            
        neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite field extension",
    "H_2: alpha is an element of L",
    "¬Q: The splitting field of c(x) over K is not a normal extension of K (interpreted as L/K is not normal)"
]

N_HYP = 2
NEG_Q_INDEX = 2