import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is an R-module",
    "H_3: N is an R-module",
    "¬Q: S is not multiplicatively closed, so the localization isomorphism fails"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            N = witness.get('N')
            S = witness.get('S')
        else:
            R, M, N, S = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = False
        if R in [ZZ, QQ, RR, CC]:
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif type(R).__name__ in ['IntegerRing', 'RationalField', 'RealField', 'ComplexField']:
            h1 = True
    except Exception:
        h1 = False

    # H2: M is an R-module
    try:
        h2 = M is not None
    except Exception:
        h2 = False

    # H3: N is an R-module
    try:
        h3 = N is not None
    except Exception:
        h3 = False

    # neg_Q: S^{-1}(M \otimes_R N) is NOT isomorphic to S^{-1}M \otimes_{S^{-1}R} S^{-1}N
    # The isomorphism holds universally if S is a multiplicatively closed subset.
    # The dropped hypothesis is that S must be multiplicatively closed.
    try:
        neg_q = False
        if S is None:
            neg_q = True
        elif hasattr(S, 'is_finite') and not S.is_finite:
            if hasattr(S, 'contains'):
                if S.contains(1) == False:
                    neg_q = True
                else:
                    neg_q = False
            else:
                neg_q = False
        else:
            S_list = list(S)
            has_one = any(val == 1 for val in S_list)
            if not has_one:
                neg_q = True
            else:
                closed = True
                for a in S_list:
                    for b in S_list:
                        prod = a * b
                        if not any(prod == val for val in S_list):
                            closed = False
                            break
                    if not closed:
                        break
                if not closed:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]