import sympy
from sympy import Poly, gcd, Tuple

# Top-level setup
x = sympy.Symbol('x')

def is_in_Zx(witness):
    try:
        if isinstance(witness, (list, tuple, set, Tuple)):
            witness = list(witness)
            if len(witness) == 0:
                return False
            for w in witness:
                w_expr = sympy.sympify(w)
                p = Poly(w_expr, x)
                if not p.domain.is_ZZ:
                    return False
                if not w_expr.free_symbols.issubset({x}):
                    return False
            return True
        else:
            w_expr = sympy.sympify(witness)
            p = Poly(w_expr, x)
            if not p.domain.is_ZZ:
                return False
            if not w_expr.free_symbols.issubset({x}):
                return False
            return True
    except Exception:
        return False

def conclusion_holds(witness):
    try:
        if isinstance(witness, (list, tuple, set, Tuple)):
            witness = list(witness)
            if len(witness) == 0:
                return False
            g = sympy.sympify(witness[0])
            for w in witness[1:]:
                g = gcd(g, sympy.sympify(w))
            p = g
        else:
            p = sympy.sympify(witness)
            
        poly = Poly(p, x)
        if not poly.domain.is_ZZ:
            return False
        if poly.degree() != 2:
            return False
        
        coeffs = poly.all_coeffs()
        if abs(coeffs[0]) != 1:
            return False
        
        if coeffs[0] == -1:
            coeffs = [-c for c in coeffs]
            
        B = coeffs[1]
        C = coeffs[2]
        
        if B**2 - 4*C == 4:
            return True
        return False
    except Exception:
        return False

def conditions(witness):
    H1 = is_in_Zx(witness)
    neg_Q = not conclusion_holds(witness)
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: I is an ideal in the polynomial ring over Z",
    "not Q: The factor ring is NOT isomorphic to the subring of Z x Z where a = b mod 2"
]

N_HYP = 1
NEG_Q_INDEX = 1