import sympy
from sympy import S
import math
from functools import reduce

# Top-level setup for potential witness expressions
ZZ = S.Integers
QQ = S.Rationals

def get_gens(X):
    """Helper to extract integer generators from various ideal representations."""
    if X is S.Integers or X == 'ZZ':
        return [1]
    if X is S.Rationals or X == 'QQ':
        return [1]
    if isinstance(X, sympy.Expr) and X.has(S.Integers):
        coeff = X.subs(S.Integers, 1)
        try:
            return [int(coeff)]
        except Exception:
            pass
    if hasattr(X, 'gens'):
        res = []
        for g in X.gens:
            try:
                res.append(int(g))
            except Exception:
                pass
        if res:
            return res
    if isinstance(X, (int, sympy.Integer)):
        return [int(X)]
    if isinstance(X, (set, list, tuple)):
        res = []
        for x in X:
            try:
                res.append(int(x))
            except Exception:
                pass
        if not res:
            raise ValueError
        return res
    try:
        return [int(X)]
    except Exception:
        raise ValueError

def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is an integral domain
    try:
        if R in (S.Integers, 'ZZ', S.Rationals, 'QQ'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: I is a non-zero ideal of R
    try:
        I_gens = get_gens(I)
        h2 = any(x != 0 for x in I_gens)
    except Exception:
        h2 = False

    # neg_Q: I \cap J is NOT a non-zero ideal of R
    try:
        I_gens = get_gens(I)
        J_gens = get_gens(J)
        
        gcd_I = abs(reduce(math.gcd, I_gens)) if I_gens else 0
        gcd_J = abs(reduce(math.gcd, J_gens)) if J_gens else 0
        
        if gcd_I == 0 or gcd_J == 0:
            intersection_gen = 0
        else:
            intersection_gen = abs(gcd_I * gcd_J) // math.gcd(gcd_I, gcd_J)
            
        neg_q = (intersection_gen == 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: I is a non-zero ideal of R",
    "¬Q: The intersection I \\cap J is not a non-zero ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2