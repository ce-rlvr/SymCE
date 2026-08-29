import sympy
from sympy import QQ, ZZ, I, sqrt, Rational, degree, minpoly
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: E is an extension field of F",
    "H_2: α is algebraic over F",
    "¬Q: The degree of the minimal polynomial of α over E is greater than the degree of the minimal polynomial of α over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        F_in, E_in, alpha = witness
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(F_in, (list, tuple, set)):
            F = QQ.algebraic_field(*F_in) if F_in else QQ
        else:
            F = F_in
            
        if isinstance(E_in, (list, tuple, set)):
            E = QQ.algebraic_field(*E_in) if E_in else QQ
        else:
            E = E_in
    except Exception:
        return [False, False, False]

    # H_1: E is an extension field of F
    try:
        h1 = False
        if getattr(F, 'is_Field', False) and getattr(E, 'is_Field', False):
            if F == E:
                h1 = True
            elif F == QQ:
                h1 = True
            elif isinstance(F_in, (list, tuple, set)):
                all_in_E = True
                for g in F_in:
                    try:
                        E.from_sympy(g)
                    except Exception:
                        all_in_E = False
                        break
                h1 = all_in_E
            else:
                h1 = (F.unify(E) == E)
    except Exception:
        h1 = False

    # H_2: α is algebraic over F
    try:
        poly_F = minpoly(alpha, x, domain=F)
        h2 = degree(poly_F, x) >= 1
    except Exception:
        h2 = False

    # neg_Q: deg(minpoly(α, E)) > deg(minpoly(α, F))
    try:
        poly_E = minpoly(alpha, x, domain=E)
        poly_F = minpoly(alpha, x, domain=F)
        deg_E = degree(poly_E, x)
        deg_F = degree(poly_F, x)
        neg_q = deg_E > deg_F
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]