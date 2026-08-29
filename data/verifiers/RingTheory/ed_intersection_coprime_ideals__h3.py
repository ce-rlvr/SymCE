import sympy
from sympy import abc

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False]
        
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        syms = a_sym.free_symbols | b_sym.free_symbols
    except Exception:
        return [False, False, False]
        
    try:
        # H1: R is a Euclidean domain. We restrict to Z or Q polynomials for simplicity.
        if a_sym.has(sympy.Float) or b_sym.has(sympy.Float):
            h1 = False
        elif len(syms) > 1:
            h1 = False
        elif len(syms) == 1:
            gen = list(syms)[0]
            h1 = bool(a_sym.is_polynomial(gen) and b_sym.is_polynomial(gen))
        else:
            h1 = bool(a_sym.is_integer and b_sym.is_integer)
    except Exception:
        h1 = False
        
    try:
        # H2: a and b are non-zero elements of R
        h2 = bool(a_sym != 0 and b_sym != 0)
    except Exception:
        h2 = False
        
    try:
        # ¬Q: The intersection of (a) and (b) is not (ab).
        # In a Euclidean domain, (a) intersection (b) = (lcm(a, b)).
        # (lcm(a, b)) == (ab) if and only if gcd(a, b) is a unit.
        # Thus, the conclusion fails iff gcd(a, b) is NOT a unit.
        if a_sym == 0 or b_sym == 0:
            neg_q = False
        else:
            g = sympy.gcd(a_sym, b_sym)
            syms_g = g.free_symbols
            if len(syms_g) == 0:
                if len(syms) == 0:
                    # Domain is Z, units are 1 and -1
                    is_unit = bool(abs(g) == 1)
                else:
                    # Domain is Q polynomials, any non-zero constant is a unit
                    is_unit = bool(g != 0)
            else:
                # g is a polynomial of degree >= 1, so it is not a unit
                is_unit = False
            neg_q = not is_unit
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: a and b are non-zero elements of R",
    "¬Q: The intersection of a and b is not ab"
]

N_HYP = 2
NEG_Q_INDEX = 2