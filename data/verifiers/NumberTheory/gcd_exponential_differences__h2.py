import sympy

def conditions(witness):
    try:
        a, n, m = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool) and a > 1
    except Exception:
        h1 = False
        
    try:
        if not (isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and 
                isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool)):
            neg_q = False
        else:
            a_sym = sympy.Rational(a)
            left = sympy.gcd(a_sym**n - 1, a_sym**m - 1)
            right = a_sym**sympy.gcd(n, m) - 1
            neg_q = bool(left != right)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer strictly greater than 1",
    "¬Q: gcd(a^n - 1, a^m - 1) != a^{gcd(n, m)} - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1