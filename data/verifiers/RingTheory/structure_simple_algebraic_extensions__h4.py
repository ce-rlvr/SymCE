import sympy
from sympy import Poly, minpoly, degree
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            alpha = witness.get('alpha')
            m = witness.get('m')
        else:
            F, E, alpha, m = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    try:
        h2 = getattr(E, 'is_Field', False) and F.unify(E) == E
    except Exception:
        h2 = False
        
    try:
        E.from_sympy(alpha)
        p = minpoly(alpha, x)
        h3 = degree(p, x) >= 1
    except Exception:
        h3 = False
        
    try:
        m_poly = Poly(m, x, domain=F)
        if not m_poly.is_irreducible:
            neg_q = True
        else:
            p = minpoly(alpha, x)
            p_poly = Poly(p, x, domain=F)
            if m_poly.degree() != p_poly.degree():
                neg_q = True
            else:
                try:
                    F.from_sympy(alpha)
                    is_in_F = True
                except Exception:
                    is_in_F = False
                
                if is_in_F:
                    K = F
                else:
                    K = F.algebraic_field(alpha)
                    
                m_K = Poly(m, x, domain=K)
                factors = m_K.factor_list()[1]
                has_root = any(f.degree() == 1 for f, _ in factors)
                neg_q = not has_root
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: alpha is an element of E that is algebraic over F",
    "~Q: F(alpha) is not isomorphic to F(x) modulo m(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3