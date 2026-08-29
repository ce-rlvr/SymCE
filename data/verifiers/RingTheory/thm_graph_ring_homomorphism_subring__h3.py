import sympy
from sympy import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness references
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, f_input = witness
        else:
            # Fallback: assume witness is just the mapping f for Z2 -> Z2
            R, S = 2, 2
            f_input = witness
            
        # Setup rings R and S
        if isinstance(R, int) and isinstance(S, int):
            n, m = R, S
            if n < 2 or m < 2:
                return [False, False, False]
            elements_R = list(range(n))
            elements_S = list(range(m))
            add_R = lambda x, y: (x + y) % n
            mul_R = lambda x, y: (x * y) % n
            add_S = lambda x, y: (x + y) % m
            mul_S = lambda x, y: (x * y) % m
            zero_R = 0
            one_R = 1
            zero_S = 0
            one_S = 1
        elif isinstance(R, (list, tuple, set)) and isinstance(S, (list, tuple, set)):
            elements_R = list(R)
            elements_S = list(S)
            add_R = lambda x, y: x + y
            mul_R = lambda x, y: x * y
            add_S = lambda x, y: x + y
            mul_S = lambda x, y: x * y
            
            zero_R = None
            for z in elements_R:
                if all(add_R(z, x) == x for x in elements_R):
                    zero_R = z
                    break
            one_R = None
            for u in elements_R:
                if all(mul_R(u, x) == x and mul_R(x, u) == x for x in elements_R):
                    one_R = u
                    break
                    
            zero_S = None
            for z in elements_S:
                if all(add_S(z, x) == x for x in elements_S):
                    zero_S = z
                    break
            one_S = None
            for u in elements_S:
                if all(mul_S(u, x) == x and mul_S(x, u) == x for x in elements_S):
                    one_S = u
                    break
                    
            if zero_R is None or one_R is None or zero_S is None or one_S is None:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # Setup homomorphism f
        if callable(f_input):
            f = f_input
        elif isinstance(f_input, (list, tuple)):
            f = lambda x: f_input[x]
        elif isinstance(f_input, dict):
            def dict_f(x):
                if x in f_input:
                    return f_input[x]
                for k, v in f_input.items():
                    if k == x:
                        return v
                raise KeyError(x)
            f = dict_f
        else:
            return [False, False, False]
            
        # H_1: R and S are rings (check closure)
        h1 = True
        for x in elements_R:
            for y in elements_R:
                if not contains(elements_R, add_R(x, y)): h1 = False
                if not contains(elements_R, mul_R(x, y)): h1 = False
        for x in elements_S:
            for y in elements_S:
                if not contains(elements_S, add_S(x, y)): h1 = False
                if not contains(elements_S, mul_S(x, y)): h1 = False
                
        # H_2: f: R -> S is a ring homomorphism
        h2 = True
        for x in elements_R:
            try:
                fx = f(x)
            except Exception:
                h2 = False
                break
            if not contains(elements_S, fx):
                h2 = False
            for y in elements_R:
                try:
                    if f(add_R(x, y)) != add_S(f(x), f(y)):
                        h2 = False
                    if f(mul_R(x, y)) != mul_S(f(x), f(y)):
                        h2 = False
                except Exception:
                    h2 = False
                    
        # ¬Q: G is not a subring of R x S
        # G is a subring iff it contains the multiplicative identity of R x S, which is (one_R, one_S).
        # Since G = {(x, f(x)) | x in R}, G contains (one_R, one_S) iff f(one_R) == one_S.
        try:
            neg_q = (f(one_R) != one_S)
        except Exception:
            neg_q = False
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: G is not a subring of R x S"
]

N_HYP = 2
NEG_Q_INDEX = 2