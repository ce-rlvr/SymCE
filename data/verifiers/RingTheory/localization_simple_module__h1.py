import sympy
from sympy import Matrix, eye, zeros
import itertools

I2 = eye(2)
O2 = zeros(2, 2)

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        M = witness['M']
        zero_M = witness['zero_M']
        action_R_M = witness['action_R_M']
        
        h1 = True
        if len(M) <= 1:
            h1 = False
        else:
            for m in M:
                if m != zero_M:
                    Rm = {action_R_M(r, m) for r in R}
                    if set(Rm) != set(M):
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        S = witness['S']
        mul_R = witness['mul_R']
        
        h2 = True
        if not S:
            h2 = False
        else:
            for s1 in S:
                for s2 in S:
                    if mul_R(s1, s2) not in S:
                        h2 = False
                        break
    except Exception:
        h2 = False

    try:
        S_inv_R = witness['S_inv_R']
        S_inv_M = witness['S_inv_M']
        zero_S_inv_M = witness['zero_S_inv_M']
        action_S_inv = witness['action_S_inv_R_S_inv_M']
        
        is_zero = (len(S_inv_M) <= 1)
        
        is_simple = True
        if not is_zero:
            for x in S_inv_M:
                if x != zero_S_inv_M:
                    Rx = {action_S_inv(r, x) for r in S_inv_R}
                    if set(Rx) != set(S_inv_M):
                        is_simple = False
                        break
        else:
            is_simple = False
            
        neg_q = (not is_zero) and (not is_simple)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a simple R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M is neither the zero module nor a simple S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2