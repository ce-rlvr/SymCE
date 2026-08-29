import sympy
from sympy import Poly, QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If L/K is a field extension and f in K[x] is the minimal polynomial of alpha over K,
    then in any splitting field of f over K, alpha is the unique root of f."
    
    A valid witness is a tuple (f, alpha) where:
      - f is a sympy Poly (or an expression convertible to one) representing the minimal polynomial.
      - alpha is a sympy expression representing the algebraic element.
    """
    try:
        f, alpha = witness
        if not isinstance(f, Poly):
            f = Poly(f)
        if not f.is_univariate:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: L/K is a field extension
    # We verify this by checking that the base domain of f (K) is a field.
    # (If f is given over ZZ, we implicitly take its fraction field QQ).
    try:
        K = f.domain.get_field()
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    # H_2: f is the minimal polynomial of alpha over K
    # This requires f to be monic, irreducible over K, and f(alpha) == 0.
    try:
        is_monic = (f.LC() == 1)
        is_irred = f.is_irreducible
        val = f.as_expr().subs(f.gen, alpha)
        if hasattr(val, 'simplify'):
            val = val.simplify()
        is_root = (val == 0)
        h2 = bool(is_monic and is_irred and is_root)
    except Exception:
        h2 = False
        
    # ¬Q: alpha is NOT the unique root of f in its splitting field.
    # An irreducible polynomial f has a unique root in its splitting field 
    # if and only if it is purely inseparable (i.e., f(x) = x^(p^e) - a).
    # If it is not purely inseparable, it has more than one distinct root.
    try:
        def is_purely_inseparable(poly):
            if poly.degree() == 1:
                return True
            char = getattr(poly.domain, 'char', 0)
            if char == 0:
                return False
            
            terms = poly.terms()
            if len(terms) > 2:
                return False
            if len(terms) == 1:
                q = terms[0][0][0]
            else:
                deg1, _ = terms[0]
                deg2, _ = terms[1]
                if deg2[0] != 0:
                    return False
                q = deg1[0]
            
            p = char
            while q % p == 0 and q > 1:
                q //= p
            return q == 1

        neg_q = not is_purely_inseparable(f)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: f is the minimal polynomial of alpha over K",
    "¬Q: alpha is not the unique root of f in its splitting field"
]

N_HYP = 2
NEG_Q_INDEX = 2