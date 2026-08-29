import math
import itertools
import functools
import sympy
from sympy import Rational, Integer, Symbol

def is_real_num(x):
    try:
        return math.isfinite(float(x))
    except Exception:
        return False

def is_bounded_real_seq(seq):
    if is_real_num(seq):
        return True
    if isinstance(seq, (list, tuple)):
        if len(seq) == 0: 
            return False
        return all(is_real_num(x) for x in seq)
    if callable(seq):
        try:
            vals = [seq(n) for n in range(100)]
            return all(is_real_num(x) for x in vals)
        except Exception:
            return False
    return False

def is_subseq_limit(seq, L):
    try:
        L_val = float(L)
    except Exception:
        return False
        
    if is_real_num(seq):
        return abs(float(seq) - L_val) < 1e-7
        
    if isinstance(seq, (list, tuple)):
        for x in seq:
            if abs(float(x) - L_val) < 1e-7:
                return True
        return False
        
    if callable(seq):
        try:
            for n in range(10000):
                if abs(float(seq(n)) - L_val) < 1e-5:
                    return True
            return False
        except Exception:
            return False
            
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        X, Y, L = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_bounded_real_seq(X)
    except Exception:
        h1 = False
        
    try:
        h2 = is_bounded_real_seq(Y)
    except Exception:
        h2 = False
        
    try:
        if not is_real_num(L):
            neg_q = False
        else:
            q = is_subseq_limit(X, L) or is_subseq_limit(Y, L)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is a bounded sequence of real numbers",
    "H_2: (y_n) is a bounded sequence of real numbers",
    "¬Q: L is neither a subsequential limit of (x_n) nor of (y_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2