import sympy
from sympy import QQ, ZZ, RR, CC, GF, sqrt, I
from sympy.abc import x, y, z
import math
from sympy.polys.domains import AlgebraicField, FractionField

CONDITION_LABELS = [
    "H_1: L is a field extension of K",
    "¬Q: L is not a regular extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        K, L = witness
    except Exception:
        return [False, False]
        
    # H_1: L is a field extension of K
    h1_ok = False
    try:
        if getattr(K, 'is_Field', False) and getattr(L, 'is_Field', False):
            if K == L:
                h1_ok = True
            else:
                try:
                    if K.unify(L) == L:
                        h1_ok = True
                except Exception:
                    pass
                
                if not h1_ok:
                    curr = L
                    while hasattr(curr, 'domain') and curr.domain != curr:
                        curr = curr.domain
                        if curr == K:
                            h1_ok = True
                            break
                
                if not h1_ok:
                    if getattr(K, 'is_FiniteField', False) and getattr(L, 'is_FiniteField', False):
                        if K.characteristic == L.characteristic:
                            k = round(math.log(L.order, K.order))
                            if K.order ** k == L.order:
                                h1_ok = True
                                
                if not h1_ok:
                    if K == QQ and L in (RR, CC):
                        h1_ok = True
                    elif K == RR and L == CC:
                        h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: L is not a regular extension of K
    # A regular extension means K is algebraically closed in L and L is separable over K.
    # We return True if L is NOT regular.
    neg_q_ok = False
    try:
        if h1_ok:
            is_regular = True
            if K == L:
                is_regular = True
            else:
                base_L = L
                # Strip transcendental parts to find the algebraic base field
                while True:
                    if isinstance(base_L, FractionField):
                        base_L = base_L.domain
                    elif getattr(base_L, 'is_PolynomialRing', False):
                        base_L = base_L.domain
                    else:
                        break
                
                if base_L != K:
                    if isinstance(base_L, AlgebraicField):
                        curr = base_L
                        while isinstance(curr, AlgebraicField):
                            if curr.domain == K:
                                is_regular = False
                                break
                            curr = curr.domain
                    elif getattr(K, 'is_FiniteField', False) and getattr(base_L, 'is_FiniteField', False):
                        if base_L.order > K.order:
                            is_regular = False
                    elif base_L == CC and K in (QQ, RR):
                        is_regular = False
                    elif base_L == RR and K == QQ:
                        is_regular = False
            
            neg_q_ok = not is_regular
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]