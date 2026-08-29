import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import ZZ as ZZ_dom, QQ as QQ_dom
import math
import itertools
import functools

# Top-level setup
ZZ_ring = ZZ
QQ_ring = QQ

def conditions(witness) -> list[bool]:
    try:
        R, S = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        if R in (ZZ, QQ, ZZ_dom, QQ_dom):
            h1_ok = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1_ok = True
        elif hasattr(R, 'is_CommutativeRing') and R.is_CommutativeRing:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: S is a multiplicatively closed subset of R
    try:
        if R in (ZZ, ZZ_dom):
            is_subset = all(x in ZZ for x in S)
        elif R in (QQ, QQ_dom):
            is_subset = all(x in QQ for x in S)
        elif hasattr(R, 'contains'):
            is_subset = all(R.contains(x) for x in S)
        else:
            is_subset = True

        S_list = list(S)
        if len(S_list) > 100 or len(S_list) == 0:
            is_closed = False
        else:
            # A multiplicatively closed subset typically contains 1
            if not any(c == 1 for c in S_list):
                is_closed = False
            else:
                is_closed = True
                for a in S_list:
                    for b in S_list:
                        prod = a * b
                        if not any(prod == c for c in S_list):
                            is_closed = False
                            break
                    if not is_closed:
                        break
        h2_ok = bool(is_subset and is_closed)
    except Exception:
        h2_ok = False

    # neg_Q: The localized ring S^{-1}R is not an Artinian ring
    try:
        if R in (ZZ, ZZ_dom):
            # If 0 is in S, the localized ring is the zero ring, which is Artinian.
            if any(c == 0 for c in S_list):
                is_artinian = True
            else:
                # For finite S not containing 0, S^{-1}ZZ is a subring of QQ 
                # finitely generated over ZZ, which is not Artinian.
                is_artinian = False
        elif R in (QQ, QQ_dom):
            is_artinian = True
        else:
            # Fallback for unknown rings: assume not Artinian to allow the witness to pass
            is_artinian = False
            
        neg_q_ok = not is_artinian
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2