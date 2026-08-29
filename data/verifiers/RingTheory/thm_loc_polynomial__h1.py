import sympy
from sympy import eye, zeros, Rational, Integer, Symbol, Matrix
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        R, S, X = witness
    except Exception:
        return [False, False, False]
        
    # H1: S is a multiplicatively closed subset of R
    h1 = True
    try:
        for s in S:
            if s not in R:
                h1 = False
                break
        if h1:
            for s1 in S:
                for s2 in S:
                    if (s1 * s2) not in S:
                        h1 = False
                        break
    except Exception:
        h1 = False
                    
    # H2: X is an indeterminate over R
    try:
        h2 = isinstance(X, sympy.Symbol) or getattr(X, 'is_Symbol', False)
    except Exception:
        h2 = False
        
    # neg_Q: S^{-1}(R[X]) is NOT isomorphic to (S^{-1}R)[X]
    try:
        is_commutative = True
        if hasattr(R, 'is_commutative') and R.is_commutative is not None:
            is_commutative = bool(R.is_commutative)
        else:
            for r1 in R:
                for r2 in R:
                    if r1 * r2 != r2 * r1:
                        is_commutative = False
                        break
                if not is_commutative:
                    break
                    
        if is_commutative:
            neg_q = False
        else:
            right_ore = True
            for r in R:
                for s in S:
                    found = False
                    for r_prime in R:
                        for s_prime in S:
                            if r * s_prime == s * r_prime:
                                found = True
                                break
                        if found: break
                    if not found:
                        right_ore = False
                        break
                if not right_ore:
                    break
                    
            left_ore = True
            for r in R:
                for s in S:
                    found = False
                    for r_prime in R:
                        for s_prime in S:
                            if s_prime * r == r_prime * s:
                                found = True
                                break
                        if found: break
                    if not found:
                        left_ore = False
                        break
                if not left_ore:
                    break
                    
            neg_q = not (right_ore and left_ore)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: X is an indeterminate over R",
    "¬Q: Localization of polynomial ring is not isomorphic to polynomial ring over localized ring"
]

N_HYP = 2
NEG_Q_INDEX = 2