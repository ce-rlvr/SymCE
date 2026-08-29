import sympy
from sympy import eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: x is an element of R such that x^n = 0 for some positive integer n",
    "¬Q: x is not an element of P"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Witness can be either:
      (R, P, x)
      (R, add_func, mul_func, P, x)
    where R is a finite list of elements representing the ring,
    P is a list of elements representing the ideal,
    and x is the nilpotent element.
    """
    try:
        if len(witness) == 5:
            R_in, add, mul, P_in, x = witness
        elif len(witness) == 3:
            R_in, P_in, x = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        # Safely convert R to a list, limiting size to prevent hangs
        if not isinstance(R_in, (list, tuple)):
            R_iter = iter(R_in)
            R = []
            for _ in range(101):
                try:
                    R.append(next(R_iter))
                except StopIteration:
                    break
        else:
            R = list(R_in)
            
        if len(R) > 100:
            return [False, False, False]
            
        # Safely convert P to a list
        if not isinstance(P_in, (list, tuple)):
            P_iter = iter(P_in)
            P = []
            for _ in range(101):
                try:
                    P.append(next(P_iter))
                except StopIteration:
                    break
        else:
            P = list(P_in)
            
        if len(P) > 100:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def contains(lst, item):
        for elem in lst:
            try:
                if elem == item:
                    return True
            except Exception:
                pass
        return False

    def get_zero(R):
        for r in R:
            try:
                is_zero = True
                for a in R:
                    if add(a, r) != a or add(r, a) != a:
                        is_zero = False
                        break
                if is_zero:
                    return r
            except Exception:
                pass
        return None

    def check_h1():
        if not R or not P: 
            return False
        
        zero = get_zero(R)
        if zero is None: 
            return False
        
        # Check for multiplicative identity (unital ring)
        has_identity = False
        for e in R:
            is_id = True
            for r in R:
                try:
                    if mul(e, r) != r or mul(r, e) != r:
                        is_id = False
                        break
                except Exception:
                    is_id = False
                    break
            if is_id:
                has_identity = True
                break
        if not has_identity:
            return False
            
        # Check R is a valid ring
        for a in R:
            # Additive inverse
            has_inv = False
            for b in R:
                try:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv: 
                return False
            
            for b in R:
                try:
                    if not contains(R, add(a, b)): return False
                    if not contains(R, mul(a, b)): return False
                    if add(a, b) != add(b, a): return False
                except Exception:
                    return False
                    
                for c in R:
                    try:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                    except Exception:
                        return False
                        
        # Check P is subset of R
        for p in P:
            if not contains(R, p): 
                return False
            
        # Check P is closed under +
        for p1 in P:
            for p2 in P:
                try:
                    if not contains(P, add(p1, p2)): 
                        return False
                except Exception:
                    return False
                
        # Check P is an ideal (absorbs multiplication)
        for r in R:
            for p in P:
                try:
                    if not contains(P, mul(r, p)): return False
                    if not contains(P, mul(p, r)): return False
                except Exception:
                    return False
                
        # Check P != R
        if all(contains(P, r) for r in R):
            return False
            
        # Check prime condition: a R b \subseteq P => a \in P or b \in P
        for a in R:
            for b in R:
                aRb_in_P = True
                for r in R:
                    try:
                        term = mul(a, mul(r, b))
                        if not contains(P, term):
                            aRb_in_P = False
                            break
                    except Exception:
                        return False
                if aRb_in_P:
                    if not contains(P, a) and not contains(P, b):
                        return False
        return True

    def check_h2():
        if not contains(R, x): 
            return False
        zero = get_zero(R)
        if zero is None: 
            return False
        
        curr = x
        for _ in range(len(R) + 1):
            if curr == zero:
                return True
            try:
                curr = mul(curr, x)
            except Exception:
                return False
        return False

    def check_neg_q():
        return not contains(P, x)

    try:
        h1 = check_h1()
    except Exception:
        h1 = False

    try:
        h2 = check_h2()
    except Exception:
        h2 = False

    try:
        neg_q = check_neg_q()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]