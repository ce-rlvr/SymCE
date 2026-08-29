import sympy
from sympy import S
from sympy.abc import x, y, z
from sympy.polys import Poly

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are elements of R",
    "H_3: The greatest common divisor of a and b is a unit in R",
    "¬Q: The greatest common divisor of a^n and b^m is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            n = witness.get('n')
            m = witness.get('m', n)
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                _, a, b, n, m = witness
            elif len(witness) == 4:
                a, b, n, m = witness
            elif len(witness) == 3:
                a, b, n = witness
                m = n
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if a is None or b is None or n is None:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    # Determine the implied ring R based on the types of a and b
    if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
        R_type = 'ZZ'
    else:
        R_type = 'QQ[x]'

    def is_in_R(val):
        if R_type == 'ZZ':
            return isinstance(val, (int, sympy.Integer))
        else:
            try:
                if isinstance(val, (int, sympy.Integer, sympy.Rational, float)):
                    return True
                if not isinstance(val, sympy.Expr):
                    return False
                syms = val.free_symbols
                if not syms:
                    return True
                # Check if it's a valid polynomial in its free symbols
                sympy.Poly(val, *syms)
                return True
            except Exception:
                return False

    def is_unit(val):
        if R_type == 'ZZ':
            return val in (1, -1)
        else:
            try:
                if isinstance(val, (int, sympy.Integer, sympy.Rational, float)):
                    return val != 0
                if hasattr(val, 'is_constant') and val.is_constant():
                    return val != 0
                if hasattr(val, 'is_number') and val.is_number:
                    return val != 0
                return False
            except Exception:
                return False

    # H_1: R is a unique factorization domain
    # We restrict our domains to ZZ or QQ[x], both of which are UFDs.
    h1 = True

    # H_2: a and b are elements of R
    try:
        h2 = bool(is_in_R(a) and is_in_R(b))
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of a and b is a unit in R
    try:
        g = sympy.gcd(a, b)
        h3 = bool(is_unit(g))
    except Exception:
        h3 = False

    # ¬Q: The greatest common divisor of a^n and b^m is NOT a unit in R
    try:
        an = a**n
        bm = b**m
        g_nm = sympy.gcd(an, bm)
        neg_q = not bool(is_unit(g_nm))
    except Exception:
        # If exponentiation or gcd fails (e.g., negative power of 0), 
        # it's not a valid counterexample evaluation.
        neg_q = False

    return [h1, h2, h3, neg_q]