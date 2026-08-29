import sympy
from sympy.abc import x
import math
import itertools
import functools

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            K = witness['K']
            f = witness['f']
        else:
            K, f = witness
    except Exception:
        return [False, False]
    
    # H_1: K is a compact subset of R^n
    h1 = False
    try:
        if isinstance(K, sympy.Interval):
            h1 = (not K.left_open) and (not K.right_open) and K.is_bounded
        else:
            K_list = list(K)
            if len(K_list) > 0:
                first = K_list[0]
                if isinstance(first, (int, float, sympy.Basic)):
                    h1 = all(isinstance(val, (int, float, sympy.Basic)) for val in K_list)
                elif isinstance(first, (tuple, list)):
                    n = len(first)
                    h1 = all(isinstance(val, (tuple, list)) and len(val) == n for val in K_list)
            else:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The function f is not surjective on K
    neg_q = False
    try:
        if isinstance(K, sympy.Interval):
            from sympy.calculus.util import function_range
            from sympy.abc import x
            rng = function_range(f, x, K)
            # f must map K to K to be a valid function on K
            if not rng.is_subset(K):
                neg_q = False
            else:
                # Not surjective means K is not a subset of the image
                neg_q = not K.is_subset(rng)
        else:
            K_list = list(K)
            image = []
            for val in K_list:
                if isinstance(f, dict):
                    y = f[val]
                elif isinstance(f, sympy.Expr):
                    y = f.subs(sympy.abc.x, val)
                else:
                    y = f(val)
                image.append(y)
            
            # f must map K to K to be a valid function on K
            maps_to_K = True
            for y in image:
                if y not in K_list:
                    maps_to_K = False
                    break
            
            if not maps_to_K:
                neg_q = False
            else:
                is_surjective = True
                for k in K_list:
                    if k not in image:
                        is_surjective = False
                        break
                neg_q = not is_surjective
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^n",
    "¬Q: The function f is not surjective on K"
]

N_HYP = 1
NEG_Q_INDEX = 1