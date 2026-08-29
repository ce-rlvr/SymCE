import sympy
from sympy.abc import x
import math
import itertools
import functools

def conditions(witness):
    try:
        if callable(witness):
            f = witness(x)
        else:
            f = witness
    except Exception:
        return [False]

    try:
        is_unif_cont = True
        
        # A function is uniformly continuous on (0, 1] iff it is continuous on (0, 1]
        # and the limits at the endpoints 0+ and 1- exist and are finite.
        
        # 1. Check limit at 0+
        L0 = sympy.limit(f, x, 0, dir='+')
        if not L0.is_number or not L0.is_finite:
            is_unif_cont = False
            
        # 2. Check limit at 1-
        if is_unif_cont:
            L1 = sympy.limit(f, x, 1, dir='-')
            if not L1.is_number or not L1.is_finite:
                is_unif_cont = False
                
        # 3. Check continuity on (0, 1]
        if is_unif_cont:
            try:
                from sympy.calculus.util import continuous_domain
                dom = continuous_domain(f, x, sympy.Interval.Lopen(0, 1))
                if not sympy.Interval.Lopen(0, 1).is_subset(dom):
                    is_unif_cont = False
            except Exception:
                # Fallback if continuous_domain fails
                sing = sympy.singularities(f, x)
                for s in sing:
                    if s.is_real and s > 0 and s <= 1:
                        is_unif_cont = False
                        break
                        
        neg_q = not is_unif_cont
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "not Q: The function f is not uniformly continuous on 0 < x <= 1"
]

N_HYP = 0
NEG_Q_INDEX = 0