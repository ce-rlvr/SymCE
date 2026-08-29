import sympy
import math

x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        a, b = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        poly_a = sympy.minpoly(a)
        poly_b = sympy.minpoly(b)
        deg_K = sympy.degree(poly_a)
        deg_L = sympy.degree(poly_b)
        h1 = (deg_K >= 1) and (deg_L >= 1)
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        max_deg = 0
        for c in range(1, 5):
            try:
                p = sympy.minpoly(a + c * b)
                d = sympy.degree(p)
                if d > max_deg:
                    max_deg = d
            except Exception:
                pass
        deg_KL = max_deg
        
        h3 = False
        if h1:
            if math.gcd(deg_K, deg_L) == 1:
                h3 = True
            elif sympy.isprime(deg_K) and deg_KL > deg_L:
                h3 = True
            elif sympy.isprime(deg_L) and deg_KL > deg_K:
                h3 = True
    except Exception:
        h3 = False

    try:
        if h1 and max_deg > 0:
            neg_q = (deg_KL != deg_K * deg_L)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K/F and L/F are field extensions contained in a common overfield",
    "H_2: K/F is a separable extension",
    "H_3: The intersection of K and L is exactly the base field F",
    "¬Q: K and L are not linearly disjoint over F"
]

N_HYP = 3
NEG_Q_INDEX = 3