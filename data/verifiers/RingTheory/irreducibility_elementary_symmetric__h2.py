import sympy
from itertools import combinations

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (n, k) or (F, n, k).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, k = witness
                F_ok = True
            elif len(witness) == 3:
                F, n, k = witness
                F_ok = getattr(F, 'is_Field', False) or F in [sympy.QQ, sympy.RR, sympy.CC]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(F_ok)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and isinstance(k, int) and 1 <= k <= n
    except Exception:
        h2 = False

    try:
        h3 = h2
    except Exception:
        h3 = False

    try:
        if not h2:
            neg_q = False
        else:
            vars = sympy.symbols(f'x1:{n+1}')
            ek = sum(sympy.Mul(*c) for c in combinations(vars, k))
            
            if ek == 0:
                neg_q = False
            else:
                factors = sympy.factor_list(ek)
                num_factors = sum(mult for f, mult in factors[1])
                neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: k is an integer such that 1 <= k <= n",
    "H_3: e_k is the k-th elementary symmetric polynomial",
    "not Q: e_k is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3