import sympy
import math

# Top-level setup
Z = sympy.S.Integers
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            I = witness.get("I")
            J = witness.get("J")
        else:
            R, I, J = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring
    try:
        is_Z = R in ("Z", "ZZ", Z)
        is_poly = False
        if not is_Z:
            if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
                is_poly = True
            elif hasattr(R, 'gens') and hasattr(R, 'domain'):
                is_poly = True
        
        h1 = bool(is_Z or is_poly)
    except Exception:
        h1 = False

    # H2: I and J are ideals of R
    try:
        h2 = False
        if is_Z:
            def extract_gen(ideal):
                if hasattr(ideal, 'gen'):
                    return int(ideal.gen)
                if isinstance(ideal, (tuple, list, set)) and len(ideal) == 1:
                    return int(list(ideal)[0])
                return int(ideal)
            I_val = extract_gen(I)
            J_val = extract_gen(J)
            h2 = True
        elif is_poly:
            def extract_poly_gen(ideal):
                if hasattr(ideal, 'gen'):
                    return sympy.poly(ideal.gen, *R.gens)
                if isinstance(ideal, (tuple, list, set)) and len(ideal) == 1:
                    return sympy.poly(list(ideal)[0], *R.gens)
                return sympy.poly(ideal, *R.gens)
            I_val = extract_poly_gen(I)
            J_val = extract_poly_gen(J)
            h2 = True
    except Exception:
        h2 = False

    # H3: R/I is Artinian
    try:
        h3 = False
        if h1 and h2:
            if is_Z:
                h3 = bool(I_val != 0)
            elif is_poly:
                if hasattr(R, 'domain') and R.domain.is_Field:
                    h3 = bool(not I_val.is_zero)
    except Exception:
        h3 = False

    # neg_Q: R/(I \cap J) is NOT Artinian
    try:
        neg_q = False
        if h1 and h2:
            if is_Z:
                if I_val == 0 and J_val == 0:
                    lcm_val = 0
                else:
                    lcm_val = abs(I_val * J_val) // math.gcd(abs(I_val), abs(J_val))
                neg_q = bool(lcm_val == 0)
            elif is_poly:
                if I_val.is_zero or J_val.is_zero:
                    lcm_val = 0
                else:
                    lcm_val = 1
                neg_q = bool(lcm_val == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are ideals of R",
    "H_3: R/I is Artinian",
    "¬Q: R/(I \\cap J) is not Artinian"
]

N_HYP = 3
NEG_Q_INDEX = 3