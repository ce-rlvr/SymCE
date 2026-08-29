import sympy
from sympy import Poly, QQ
from sympy.abc import x

def in_field(a, field):
    try:
        field.from_expr(a)
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 4:
            return [False, False, False, False]
        
        F_gens, f_expr, c, K_gens = witness
        
        if not isinstance(F_gens, (list, tuple)):
            F_gens = [F_gens]
        if not isinstance(K_gens, (list, tuple)):
            K_gens = [K_gens]
            
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        F_field = QQ.algebraic_field(*F_gens)
        H1 = True
    except Exception:
        H1 = False
        F_field = None

    # H2: f(x) is a polynomial over F
    try:
        if F_field is None:
            H2 = False
        else:
            f_poly = Poly(f_expr, x)
            coeffs = f_poly.coeffs()
            H2 = all(in_field(coeff, F_field) for coeff in coeffs)
    except Exception:
        H2 = False

    # H3: c is a non-zero element of F
    try:
        if F_field is None:
            H3 = False
        else:
            H3 = (c != 0) and in_field(c, F_field)
    except Exception:
        H3 = False

    # neg_Q: K is NOT the splitting field of c * f(x) over F
    try:
        if F_field is None:
            neg_Q = False
        else:
            P_poly = Poly(c * f_expr, x)
            if P_poly.is_zero:
                all_rts = []
            else:
                all_rts = P_poly.all_roots()
                
            SF_gens = list(F_gens) + list(all_rts)
            SF = QQ.algebraic_field(*SF_gens)
            
            K_field = QQ.algebraic_field(*K_gens)
            
            K_in_SF = all(in_field(g, SF) for g in K_gens)
            SF_in_K = all(in_field(g, K_field) for g in SF_gens)
            
            is_splitting_field = K_in_SF and SF_in_K
            neg_Q = not is_splitting_field
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "H_3: c is a non-zero element of F",
    "¬Q: K is not the splitting field of c * f(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3