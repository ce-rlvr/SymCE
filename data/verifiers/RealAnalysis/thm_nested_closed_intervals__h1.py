import sympy
from sympy import Interval, Symbol, oo, EmptySet, Union, Intersection, FiniteSet
import math
import itertools
import functools

# Top-level setup
S3 = None
Z4 = None
I2 = None

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    
    def check_nested(w):
        try:
            for i in range(1, 101):
                I_curr = w(i)
                I_next = w(i+1)
                
                if getattr(I_next, 'is_EmptySet', False):
                    continue
                    
                if getattr(I_curr, 'is_EmptySet', False):
                    if not getattr(I_next, 'is_EmptySet', False):
                        return False
                    continue
                    
                res = I_next.is_subset(I_curr)
                if res is not None:
                    if not res:
                        return False
                else:
                    if I_next.inf < I_curr.inf or I_next.sup > I_curr.sup:
                        return False
                    if I_next.inf == I_curr.inf and not getattr(I_next, 'left_open', False) and getattr(I_curr, 'left_open', False):
                        return False
                    if I_next.sup == I_curr.sup and not getattr(I_next, 'right_open', False) and getattr(I_curr, 'right_open', False):
                        return False
            return True
        except Exception:
            return False

    def is_intersection_empty(w):
        n = sympy.Symbol('n', integer=True, positive=True)
        try:
            I_n = w(n)
            if getattr(I_n, 'is_EmptySet', False):
                return True
            
            if isinstance(I_n, sympy.Interval):
                L_a = sympy.limit(I_n.inf, n, oo)
                L_b = sympy.limit(I_n.sup, n, oo)
                
                if L_a == oo or L_b == -oo:
                    return True
                if L_a > L_b:
                    return True
                if L_a < L_b:
                    return False
                if L_a == L_b:
                    L = L_a
                    if I_n.contains(L) == False:
                        return True
                    for i in range(1, 101):
                        try:
                            if w(i).contains(L) == False:
                                return True
                        except Exception:
                            pass
                    return False
        except Exception:
            pass

        # Fallback for non-symbolic or complex functions
        try:
            for i in range(1, 101):
                if getattr(w(i), 'is_EmptySet', False):
                    return True
                    
            I_large = w(100000)
            I_larger = w(200000)
            
            if getattr(I_large, 'is_EmptySet', False):
                return True
                
            a1, b1 = float(I_large.inf), float(I_large.sup)
            a2, b2 = float(I_larger.inf), float(I_larger.sup)
            
            if a2 > a1 and a2 > 500:
                return True
            if b2 < b1 and b2 < -500:
                return True
                
            if abs(a2 - b2) < 1e-5:
                L = a2
                for i in range(1, 101):
                    if w(i).contains(L) == False:
                        return True
                return False
                
        except Exception:
            pass

        return False

    h1_ok = check_nested(witness)
    neg_q_ok = is_intersection_empty(witness)
    
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I_{n+1} \\subseteq I_n for all n \\in \\mathbb{N}",
    "¬Q: The intersection \\bigcap_{n=1}^\\infty I_n is empty"
]

N_HYP = 1
NEG_Q_INDEX = 1