import sympy
from sympy import Symbol

# Top-level setup for potential witness expressions
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        R, a, b, n, m = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a unique factorization domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H2: a and b are elements of R
    try:
        h2 = bool(a in R and b in R)
    except Exception:
        h2 = False

    # H3: n and m are positive integers
    try:
        h3 = bool(isinstance(n, int) and isinstance(m, int) and n > 0 and m > 0)
    except Exception:
        h3 = False

    # neg_Q: The greatest common divisor of a^n and b^m is NOT a unit in R
    try:
        # Convert to domain elements if possible for robust gcd computation
        try:
            a_dom = R.from_sympy(sympy.sympify(a)) if hasattr(R, 'from_sympy') else a
            b_dom = R.from_sympy(sympy.sympify(b)) if hasattr(R, 'from_sympy') else b
        except Exception:
            a_dom = a
            b_dom = b
            
        an = a_dom**n
        bm = b_dom**m
        g = R.gcd(an, bm)
        
        # In a domain, an element g is a unit iff it exactly divides 1
        try:
            R.exquo(R.one, g)
            is_unit = True
        except Exception:
            is_unit = False
            
        neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are elements of R",
    "H_3: n and m are positive integers",
    "¬Q: The greatest common divisor of a^n and b^m is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3