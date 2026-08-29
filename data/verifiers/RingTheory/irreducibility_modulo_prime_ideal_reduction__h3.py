import sympy
from sympy import Poly, isprime
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: a_n not in P",
    "H_4: The reduction of f(x) modulo P is irreducible over R/P",
    "not Q: f(x) is reducible over R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        f_expr, p = witness
        if isinstance(f_expr, str):
            f_expr = sympy.sympify(f_expr)
        
        symbols = getattr(f_expr, "free_symbols", set())
        if len(symbols) == 1:
            gen = list(symbols)[0]
        else:
            gen = x
            
        f = Poly(f_expr, gen, domain='ZZ')
    except Exception:
        return [False] * 5

    try:
        h1 = (f.domain == sympy.ZZ)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        LC = f.LC()
        h3 = bool((LC % p) != 0)
    except Exception:
        h3 = False

    try:
        f_mod = Poly(f, domain=sympy.GF(p))
        h4 = (f_mod.is_irreducible == True)
    except Exception:
        h4 = False

    try:
        neg_q = (f.is_irreducible == False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]