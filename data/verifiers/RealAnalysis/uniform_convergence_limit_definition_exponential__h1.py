import sympy
from sympy import Symbol, oo
import math
import itertools
import functools

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def get_M(witness):
    if witness == sympy.Reals:
        return sympy.oo
    try:
        if hasattr(witness, 'is_Interval') and witness.is_Interval:
            return witness.end
    except Exception:
        pass
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            return witness[1]
    except Exception:
        pass
    return witness

def conditions(witness):
    M = get_M(witness)
    
    try:
        if M == sympy.oo or M == float('inf') or str(M) == 'oo':
            h1 = True
        else:
            h1 = float(M) >= 0
    except Exception:
        h1 = False
        
    try:
        if M == sympy.oo or M == float('inf') or str(M) == 'oo':
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f_n is defined on the interval from -M to M",
    "not Q: f_n does not converge uniformly to e^x"
]

N_HYP = 1
NEG_Q_INDEX = 1