import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math

# Top-level setup for standard rings
Z_ring = sympy.ZZ
Q_ring = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Q is a P-primary ideal in R",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The intersection S \\cap Q is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, Q, S), checks if it satisfies the hypotheses and falsifies the conclusion.
    R: The ring (e.g., 'ZZ' or sympy.ZZ)
    Q: The ideal, represented by a generator or list of generators
    S: The multiplicatively closed subset, represented as an iterable or sympy Set
    """
    try:
        R, Q, S = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = (R in ('ZZ', sympy.ZZ, sympy.S.Integers, QQ, sympy.QQ, 'QQ'))
    except Exception:
        h1 = False

    # H_2: Q is a P-primary ideal in R
    try:
        if R in ('ZZ', sympy.ZZ, sympy.S.Integers):
            if isinstance(Q, (list, tuple, set)):
                q = 0
                for gen in Q:
                    q = math.gcd(q, abs(int(gen)))
            else:
                q = abs(int(Q))
            
            if q == 0:
                h2 = True
            elif q == 1:
                h2 = False
            else:
                factors = sympy.factorint(q)
                h2 = (len(factors) == 1)
        elif R in (QQ, sympy.QQ, 'QQ'):
            if isinstance(Q, (list, tuple, set)):
                q = 0
                for gen in Q:
                    if gen != 0:
                        q = 1
                        break
            else:
                q = 1 if Q != 0 else 0
            h2 = (q == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: S is a multiplicatively closed subset of R
    try:
        if S in (sympy.S.Naturals, sympy.S.Naturals0, sympy.S.Integers):
            h3 = True
        else:
            S_list = []
            for idx, item in enumerate(S):
                if idx > 100:
                    raise ValueError("Set too large or infinite")
                S_list.append(item)
            
            if len(S_list) == 0:
                h3 = False
            else:
                h3 = True
                for item in S_list:
                    try:
                        if R in ('ZZ', sympy.ZZ, sympy.S.Integers):
                            if int(item) != item:
                                h3 = False
                                break
                        elif R in (QQ, sympy.QQ, 'QQ'):
                            sympy.Rational(item)
                    except Exception:
                        h3 = False
                        break
                
                if h3:
                    for a in S_list:
                        for b in S_list:
                            if (a * b) not in S_list:
                                h3 = False
                                break
                        if not h3:
                            break
    except Exception:
        h3 = False

    # ¬Q: The intersection S \cap Q is empty
    try:
        neg_q = True
        if R in ('ZZ', sympy.ZZ, sympy.S.Integers):
            if isinstance(Q, (list, tuple, set)):
                q = 0
                for gen in Q:
                    q = math.gcd(q, abs(int(gen)))
            else:
                q = abs(int(Q))
            
            if S == sympy.S.Naturals:
                if q == 0:
                    neg_q = True
                else:
                    neg_q = False
            elif S == sympy.S.Naturals0:
                neg_q = False
            elif S == sympy.S.Integers:
                neg_q = False
            else:
                S_list = []
                for idx, item in enumerate(S):
                    if idx > 100:
                        raise ValueError("Set too large or infinite")
                    S_list.append(item)
                for s in S_list:
                    if q == 0:
                        if s == 0:
                            neg_q = False
                            break
                    else:
                        if s % q == 0:
                            neg_q = False
                            break
        elif R in (QQ, sympy.QQ, 'QQ'):
            if isinstance(Q, (list, tuple, set)):
                q = 0
                for gen in Q:
                    if gen != 0:
                        q = 1
                        break
            else:
                q = 1 if Q != 0 else 0
            
            S_list = []
            for idx, item in enumerate(S):
                if idx > 100:
                    raise ValueError("Set too large or infinite")
                S_list.append(item)
            for s in S_list:
                if q == 0:
                    if s == 0:
                        neg_q = False
                        break
                else:
                    neg_q = False
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]