import sympy

X = sympy.Symbol('X')

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            f, g = witness[-2], witness[-1]
        else:
            return [False, False, False]
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        
        try:
            f_poly = sympy.Poly(f, X, domain='ZZ')
            g_poly = sympy.Poly(g, X, domain='ZZ')
            h1 = True
        except Exception:
            h1 = False

        h2 = h1

    except Exception:
        h1 = False
        h2 = False

    try:
        gcd_Z = sympy.gcd(f, g, domain='ZZ')
        rp_Z = (gcd_Z == 1 or gcd_Z == -1)
        
        gcd_Q = sympy.gcd(f, g, domain='QQ')
        rp_Q = (gcd_Q == 1 or gcd_Q == -1)
        
        neg_q = (rp_Z != rp_Q)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: K is the field of fractions of R",
    "not Q: f and g are relatively prime in R iff they are relatively prime in K FAILS"
]

N_HYP = 2
NEG_Q_INDEX = 2