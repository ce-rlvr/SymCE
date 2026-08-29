import sympy
from itertools import combinations

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    F, n, k = None, None, None
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n, k = witness
                F = QQ
            elif len(witness) == 3:
                F, n, k = witness
    except Exception:
        pass

    try:
        h1 = hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False

    try:
        h3 = isinstance(k, int)
    except Exception:
        h3 = False

    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            if k < 0 or k > n:
                ek = sympy.Integer(0)
            elif k == 0:
                ek = sympy.Integer(1)
            else:
                X = sympy.symbols(f'x1:{n+1}')
                ek = sum((sympy.Mul(*comb) for comb in combinations(X, k)), sympy.Integer(0))
            
            if ek == 0:
                is_irred = False
            else:
                coeff, factors = sympy.factor_list(ek, domain=F)
                total_factors = sum(power for base, power in factors)
                is_irred = (total_factors == 1)
            
            neg_q = not is_irred
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n >= 2 is an integer",
    "H_3: k is an integer",
    "¬Q: e_k is not irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3