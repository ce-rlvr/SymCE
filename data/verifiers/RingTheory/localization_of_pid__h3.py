import sympy
from sympy import ZZ, QQ
import math
import itertools
import functools

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If R is a principal ideal domain and S is a multiplicatively closed subset of R,
    then the localization S^{-1}R is a principal ideal domain."
    
    A valid counterexample must satisfy the hypotheses but fail the conclusion.
    (The conclusion fails if and only if 0 is in S, which makes S^{-1}R the zero ring,
    and the zero ring is not an integral domain, hence not a PID).
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a principal ideal domain
    try:
        h1 = False
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
            
        # A PID must be an integral domain
        if hasattr(R, 'is_IntegralDomain') and not R.is_IntegralDomain:
            h1 = False
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R
    try:
        h2 = True
        S_list = list(S)
        if not S_list:
            h2 = False # S should be non-empty to form a proper localization
            
        for a in S_list:
            # Check if a is in R
            in_R = False
            try:
                if a in R:
                    in_R = True
            except Exception:
                pass
            
            if not in_R:
                h2 = False
                break
            
            # Check multiplicative closure
            for b in S_list:
                prod = a * b
                if prod not in S_list:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The localization S^{-1}R is NOT a principal ideal domain
    # If R is a PID, S^{-1}R is a PID if and only if 0 is not in S.
    # If 0 is in S, S^{-1}R is the zero ring, which is not a PID.
    try:
        neg_q = False
        if 0 in S_list:
            neg_q = True
        else:
            try:
                if R.zero in S_list:
                    neg_q = True
            except Exception:
                pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localization S^{-1}R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2