import sympy
from sympy import Symbol, Poly

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial",
    "H_2: R is the factor ring",
    "¬Q: Der_F(R, R) is zero iff f(x) has no repeated roots fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            f_poly = witness
            if len(f_poly.gens) != 1:
                return [False, False, False]
        elif hasattr(witness, 'free_symbols'):
            free = witness.free_symbols
            if len(free) == 1:
                f_poly = Poly(witness, list(free)[0])
            elif len(free) == 0:
                f_poly = Poly(witness, x)
            else:
                return [False, False, False]
        else:
            f_poly = Poly(witness, x)
            
        h1 = bool(f_poly.degree() >= 1)
    except Exception:
        h1 = False

    h2 = h1

    try:
        if not h1:
            neg_q = False
        else:
            f_diff = f_poly.diff()
            gcd_poly = f_poly.gcd(f_diff)
            
            der_zero = bool(gcd_poly.is_one)
            no_repeated_roots = bool(gcd_poly.degree() == 0)
            
            neg_q = bool(der_zero != no_repeated_roots)
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]