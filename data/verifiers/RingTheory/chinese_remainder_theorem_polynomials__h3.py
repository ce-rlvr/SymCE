import sympy
from sympy import Poly, QQ, ZZ
from sympy.abc import x

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness should be a tuple: (F, p1, p2)
    where F is a SymPy domain (e.g., QQ) and p1, p2 are expressions or Poly objects.
    """
    try:
        F, p1, p2 = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: p_1 and p_2 are polynomials over F
    try:
        syms = set()
        for p in (p1, p2):
            if hasattr(p, 'free_symbols'):
                syms.update(p.free_symbols)
                
        if len(syms) == 1:
            gen = list(syms)[0]
        elif len(syms) == 0:
            gen = x
        else:
            gen = None
            
        if gen is not None:
            poly1 = Poly(p1, gen, domain=F)
            poly2 = Poly(p2, gen, domain=F)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The factor ring is NOT isomorphic to the direct product
    # By the Chinese Remainder Theorem, they are isomorphic if and only if p_1 and p_2 are coprime.
    # Thus, they are NOT isomorphic iff gcd(p_1, p_2) has degree > 0 (or if both are 0).
    try:
        if not h2:
            neg_q = False
        else:
            g = poly1.gcd(poly2)
            neg_q = g.degree() > 0 or g.is_zero
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p_1 and p_2 are polynomials over F",
    "¬Q: The factor ring is not isomorphic to the direct product"
]

N_HYP = 2
NEG_Q_INDEX = 2