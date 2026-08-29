import sympy as sp

x = sp.Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to provide (alpha, a, b, c, d, n) where F is implicitly Q.
    """
    try:
        if isinstance(witness, dict):
            alpha = witness['alpha']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
            n = int(witness['n'])
        else:
            # Unpack from the end to allow optional F at the beginning
            n = int(witness[-1])
            d = witness[-2]
            c = witness[-3]
            b = witness[-4]
            a = witness[-5]
            alpha = witness[-6]
    except Exception:
        return [False, False, False, False]
        
    # H1: alpha is algebraic over F (we use F = Q)
    try:
        poly_alpha = sp.minpoly(alpha)
        h1 = True
    except Exception:
        h1 = False
        
    # H2: a, b, c, d in F and ad - bc != 0
    try:
        a_rat = sp.Rational(a)
        b_rat = sp.Rational(b)
        c_rat = sp.Rational(c)
        d_rat = sp.Rational(d)
        h2 = bool((a_rat * d_rat - b_rat * c_rat) != 0)
    except Exception:
        h2 = False
        
    # H3: c*alpha + d != 0
    try:
        h3 = bool(sp.simplify(c * alpha + d) != 0)
    except Exception:
        h3 = False
        
    # neg_Q: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F does NOT have degree n
    try:
        beta = sp.simplify((a * alpha + b) / (c * alpha + d))
        poly_beta = sp.minpoly(beta)
        deg_beta = sp.degree(poly_beta)
        neg_q = bool(deg_beta != n)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F",
    "H_2: a, b, c, d in F and ad - bc != 0",
    "H_3: c*alpha + d != 0",
    "¬Q: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F does not have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3