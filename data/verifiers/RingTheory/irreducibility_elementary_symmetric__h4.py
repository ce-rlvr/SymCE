import sympy
from sympy import QQ, ZZ, GF
from itertools import combinations

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        F, n, k = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False
        
    try:
        h3 = isinstance(k, int) and 1 <= k <= n
    except Exception:
        h3 = False
        
    try:
        x_vars = sympy.symbols(f'x1:{n+1}')
        e_k = sum(sympy.Mul(*comb) for comb in combinations(x_vars, k))
        p = sympy.Poly(e_k, *x_vars, domain=F)
        
        try:
            factors = p.factor_list()[1]
            total_factors = sum(mult for factor, mult in factors)
            neg_q = total_factors > 1
        except NotImplementedError:
            if k == n and n >= 2:
                neg_q = True
            else:
                p_ZZ = sympy.Poly(e_k, *x_vars)
                factors_ZZ = p_ZZ.factor_list()[1]
                total_factors_ZZ = sum(mult for factor, mult in factors_ZZ)
                neg_q = total_factors_ZZ > 1
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n >= 2 is an integer",
    "H_3: k is an integer such that 1 <= k <= n",
    "¬Q: e_k is reducible in the polynomial ring"
]

N_HYP = 3
NEG_Q_INDEX = 3