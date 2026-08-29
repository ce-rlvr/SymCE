import sympy
from sympy import Integer, Poly, Symbol

# Top-level setup
x = Symbol('x')

def extract_pbc(witness):
    """
    Attempt to extract the characteristic p, and coefficients b, c 
    from various possible witness formats.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            if all(isinstance(val, (int, Integer)) for val in witness):
                return int(witness[0]), int(witness[1]), int(witness[2])
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            return int(witness['p']), int(witness['b']), int(witness['c'])
    except Exception:
        pass

    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            f = witness[1]
            if hasattr(f, 'all_coeffs'):
                coeffs = f.all_coeffs()
                if len(coeffs) == 3 and coeffs[0] == 1:
                    if hasattr(f, 'domain') and hasattr(f.domain, 'mod'):
                        p = f.domain.mod
                    else:
                        p_obj = witness[0]
                        if hasattr(p_obj, 'mod'):
                            p = p_obj.mod
                        else:
                            p = p_obj
                    return int(p), int(coeffs[1]), int(coeffs[2])
    except Exception:
        pass

    try:
        if hasattr(witness, 'all_coeffs'):
            coeffs = witness.all_coeffs()
            if len(coeffs) == 3 and coeffs[0] == 1:
                if hasattr(witness, 'domain') and hasattr(witness.domain, 'mod'):
                    p = witness.domain.mod
                    return int(p), int(coeffs[1]), int(coeffs[2])
    except Exception:
        pass

    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            p_obj = witness[0]
            if hasattr(p_obj, 'mod'):
                p = int(p_obj.mod)
            else:
                p = int(p_obj)
            expr = witness[1]
            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 3 and coeffs[0] == 1:
                return p, int(coeffs[1]), int(coeffs[2])
    except Exception:
        pass
    
    return None, None, None

def conditions(witness) -> list[bool]:
    try:
        p, b, c = extract_pbc(witness)
    except Exception:
        p, b, c = None, None, None

    try:
        h1 = p is not None and sympy.isprime(p)
    except Exception:
        h1 = False

    try:
        h2 = b is not None and c is not None and isinstance(b, int) and isinstance(c, int)
    except Exception:
        h2 = False

    h3 = True if (h1 and h2) else False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            def is_sq(D, p):
                D = D % p
                if D == 0:
                    return True
                if p == 2:
                    return True
                return pow(D, (p - 1) // 2, p) == 1

            if p == 2:
                root_E = (c % 2 == 0) or ((1 + b + c) % 2 == 0)
            else:
                D = (b**2 - 4*c) % p
                root_E = is_sq(D, p)
            
            deg_E = 1 if root_E else 2
            
            D = (b**2 - 4*c) % p
            root_D = is_sq(D, p)
            deg_F_sqrt = 1 if root_D else 2
            
            neg_q = (deg_E != deg_F_sqrt)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) = x^2 + bx + c is a polynomial over F",
    "H_3: E is a splitting field of f(x) over F",
    "¬Q: E is not isomorphic to F(sqrt(b^2 - 4c)) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3