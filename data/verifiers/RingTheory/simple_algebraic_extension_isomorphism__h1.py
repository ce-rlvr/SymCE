import sympy
from sympy.abc import x

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "If alpha is algebraic over F and m(x) in F[x] is its minimal polynomial, 
    then F[x]/(m(x)) is isomorphic to the simple extension field F(alpha)."
    
    The dropped hypothesis is that F must be a field.
    """
    try:
        if isinstance(witness, dict):
            F = witness['F']
            alpha = witness['alpha']
            m = witness['m']
        else:
            F, alpha, m = witness
    except Exception:
        return [False, False, False]

    # H_1: alpha in E is algebraic over F
    try:
        p = sympy.minpoly(alpha, x)
        h1 = bool(p is not None and p.degree() >= 1)
    except Exception:
        h1 = False

    # H_2: m(x) in F[x] is the minimal polynomial of alpha over F
    try:
        if not isinstance(m, sympy.Poly):
            m = sympy.Poly(m, x, domain=F)
        
        in_F = (m.domain == F)
        is_root = (m.eval(alpha).simplify() == 0)
        is_irred = m.is_irreducible
        
        # To ensure it's the minimal polynomial, its degree must match the degree 
        # of the algebraic number over the field of fractions of F.
        p = sympy.minpoly(alpha, m.gen)
        is_min_deg = (m.degree() == p.degree())
        
        # Minimal polynomials are monic over fields, and primitive with positive LC over domains like ZZ.
        if getattr(F, 'is_Field', False):
            is_normalized = (m.LC() == 1)
        else:
            is_normalized = (m.LC() > 0)
            
        h2 = bool(in_F and is_root and is_irred and is_min_deg and is_normalized)
    except Exception:
        h2 = False

    # ¬Q: The factor ring F[x]/(m(x)) is not isomorphic to the simple extension field F(alpha)
    try:
        # The conclusion holds if F is a field. If F is not a field (e.g. ZZ),
        # F[x]/(m(x)) is not a field, but F(alpha) is a field, so they cannot be isomorphic.
        neg_q = not bool(getattr(F, 'is_Field', False))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha in E is algebraic over F",
    "H_2: m(x) in the polynomial ring over F is the minimal polynomial of alpha over F",
    "¬Q: The factor ring modulo m(x) is not isomorphic to the simple extension field F(alpha)"
]

N_HYP = 2
NEG_Q_INDEX = 2