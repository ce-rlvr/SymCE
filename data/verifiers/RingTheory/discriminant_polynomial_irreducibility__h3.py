import sympy
from sympy.polys.domains import GF, QQ, ZZ, RR, CC

GF2 = GF(2)
GF3 = GF(3)
GF5 = GF(5)
GF7 = GF(7)

def conditions(witness) -> list[bool]:
    try:
        K, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(getattr(K, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False

    try:
        x = sympy.Symbol('x')
        A = sympy.symbols(f'a0:{n+1}')
        f = sum(A[i] * x**i for i in range(n+1))
        D = sympy.discriminant(f, x)
        
        P = sympy.Poly(D, *A, domain=K)
        try:
            is_irred = P.is_irreducible
        except Exception:
            facs = sympy.factor_list(D, *A, domain=K)
            is_irred = (len(facs[1]) == 1 and facs[1][0][1] == 1)
            
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 2 is an integer",
    "¬Q: The discriminant polynomial is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2