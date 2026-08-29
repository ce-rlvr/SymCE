import sympy
import sympy.ntheory
from sympy.abc import x

# Top-level setup
# (No specific named groups needed for FieldTheory, but we define x for polynomials)

def to_int(val):
    if isinstance(val, int):
        return val
    if hasattr(val, 'is_integer') and val.is_integer:
        return int(val)
    try:
        return int(val)
    except Exception:
        pass
    try:
        return int(val.rep)
    except Exception:
        pass
    return None

def extract_p_a_alpha(witness):
    p, a, alpha, alpha_minpoly = None, None, None, None
    if isinstance(witness, dict):
        p = witness.get('p')
        a = witness.get('a')
        alpha = witness.get('alpha')
        alpha_minpoly = witness.get('alpha_minpoly')
    elif isinstance(witness, (tuple, list)):
        ints = []
        others = []
        for item in witness:
            val = to_int(item)
            if val is not None:
                ints.append(val)
            else:
                others.append(item)
        if len(ints) >= 2:
            p = ints[0]
            a = ints[1]
            if len(ints) >= 3:
                alpha = ints[2]
            elif len(others) >= 1:
                alpha = others[0]
        elif len(ints) == 1 and len(others) >= 1:
            p = ints[0]
            a = others[0]
            if len(others) >= 2:
                alpha = others[1]
    return p, a, alpha, alpha_minpoly

def conditions(witness) -> list[bool]:
    p, a, alpha, alpha_minpoly = extract_p_a_alpha(witness)
    
    # H1: F is a field of prime characteristic p
    try:
        p_val = to_int(p)
        if p_val is not None:
            H1 = sympy.ntheory.isprime(p_val)
        else:
            H1 = False
    except Exception:
        H1 = False

    # H2: a in F, x^p - x - a has no roots in F
    try:
        p_val = to_int(p)
        a_val = to_int(a)
        if p_val is not None and a_val is not None and sympy.ntheory.isprime(p_val):
            # By Fermat's Little Theorem, x^p - x - a = -a mod p.
            # So it has no roots in F_p iff a != 0 mod p.
            H2 = (a_val % p_val != 0)
        else:
            H2 = False
    except Exception:
        H2 = False

    # neg_Q: x^p - x - a is NOT the minimal polynomial of alpha over F
    try:
        p_val = to_int(p)
        a_val = to_int(a)
        if p_val is not None and a_val is not None and sympy.ntheory.isprime(p_val):
            expected_list = [0] * (p_val + 1)
            expected_list[0] = 1
            expected_list[p_val - 1] = (-1) % p_val
            expected_list[p_val] = (-a_val) % p_val
            
            if alpha_minpoly is not None:
                if isinstance(alpha_minpoly, sympy.Poly):
                    alpha_coeffs = alpha_minpoly.all_coeffs()
                else:
                    alpha_coeffs = list(alpha_minpoly)
                alpha_coeffs = [to_int(c) % p_val for c in alpha_coeffs]
                while len(alpha_coeffs) > 1 and alpha_coeffs[0] == 0:
                    alpha_coeffs.pop(0)
                neg_Q = (alpha_coeffs != expected_list)
            else:
                if alpha is not None:
                    if isinstance(alpha, sympy.Symbol):
                        neg_Q = True
                    else:
                        alpha_val = to_int(alpha)
                        if alpha_val is not None:
                            alpha_coeffs = [1, (-alpha_val) % p_val]
                            neg_Q = (alpha_coeffs != expected_list)
                        else:
                            from sympy import minpoly
                            mp = minpoly(alpha, x)
                            mp_coeffs = sympy.Poly(mp, x).all_coeffs()
                            mp_coeffs = [to_int(c) % p_val for c in mp_coeffs]
                            while len(mp_coeffs) > 1 and mp_coeffs[0] == 0:
                                mp_coeffs.pop(0)
                            neg_Q = (mp_coeffs != expected_list)
                else:
                    # alpha not provided, so conclusion fails for alpha = 0
                    neg_Q = True
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p",
    "H_2: a in F and x^p - x - a has no roots in F",
    "¬Q: x^p - x - a is not the minimal polynomial of alpha over F"
]

N_HYP = 2
NEG_Q_INDEX = 2