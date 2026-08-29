import sympy
from sympy import Poly, Rational
from sympy.abc import x
from sympy.polys.domains import ZZ, QQ

CONDITION_LABELS = [
    "H_1: E is an extension field of F",
    "H_2: alpha is an element of E that is algebraic over F",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "¬Q: The field extension F(alpha) is not isomorphic to the quotient ring modulo m(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        F, E, alpha, m = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: E is an extension field of F
    try:
        E_is_field = getattr(E, 'is_Field', False) or getattr(E, 'is_field', False)
        F_is_ring = getattr(F, 'is_Ring', False) or getattr(F, 'is_ring', False)
        is_subring = (F.unify(E) == E)
        h1 = bool(E_is_field and F_is_ring and is_subring)
    except Exception:
        h1 = False
        
    # H2: alpha is an element of E that is algebraic over F
    try:
        in_E = False
        try:
            if hasattr(E, 'from_sympy'):
                E.from_sympy(sympy.sympify(alpha))
                in_E = True
            elif alpha in E:
                in_E = True
        except Exception:
            pass
                
        val = m.eval(alpha)
        is_root = (val == 0 or getattr(val, 'is_zero', False))
        h2 = bool(in_E and is_root)
    except Exception:
        h2 = False
        
    # H3: m(x) is the minimal polynomial of alpha over F
    try:
        m_in_F = (m.domain == F)
        is_irred = m.is_irreducible
        val = m.eval(alpha)
        is_root = (val == 0 or getattr(val, 'is_zero', False))
        h3 = bool(m_in_F and is_irred and is_root)
    except Exception:
        h3 = False
        
    # ¬Q: F(alpha) is NOT isomorphic to the quotient ring modulo m(x)
    try:
        # F(alpha) is a field. The quotient ring F[x]/(m(x)) is a field iff m(x) is maximal.
        # If F is an integral domain but not a field (e.g., ZZ), 
        # an irreducible polynomial (e.g., 2x-1) may not generate a maximal ideal,
        # so the quotient ring is not a field (e.g., ZZ[1/2]), thus not isomorphic to F(alpha).
        neg_q = not getattr(F, 'is_Field', False)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]