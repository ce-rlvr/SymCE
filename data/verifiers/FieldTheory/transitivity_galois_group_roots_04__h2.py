import sympy
from sympy import Poly, Symbol, Expr, Eq
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is the splitting field of f(x) over K",
    "¬Q: Gal(L/K) does not act transitively on the roots of f(x) in L"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        poly_f = None
        
        def extract_poly(w):
            if isinstance(w, Poly):
                return w
            if isinstance(w, Eq):
                w = w.lhs - w.rhs
            if isinstance(w, Expr) and len(w.free_symbols) == 1:
                return Poly(w)
            return None

        if isinstance(witness, (tuple, list)):
            for item in witness:
                p = extract_poly(item)
                if p is not None:
                    poly_f = p
                    break
        else:
            poly_f = extract_poly(witness)
            
        if poly_f is None:
            return [False, False, False]
            
        # K is implicitly the field of fractions of the polynomial's domain (e.g., QQ)
        h1 = True
        
        # L is implicitly the splitting field of f(x) over K
        h2 = True
        
        # The Galois group Gal(L/K) acts transitively on the roots of f(x) in L
        # if and only if all roots of f(x) belong to the same Galois orbit.
        # This occurs if and only if f(x) has exactly one irreducible factor 
        # of degree >= 1 over K (ignoring multiplicities).
        factors = poly_f.factor_list()
        num_irreducible_factors = sum(1 for fac, mult in factors[1] if fac.degree() >= 1)
        
        neg_q = bool(num_irreducible_factors > 1)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]