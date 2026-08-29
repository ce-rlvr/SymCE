import sympy
from sympy import *
import itertools
import math

# Top-level setup
# No named bindings needed for number theory; use integers directly.
# The verifier interprets an integer `n` as the ring Z_n with the identity map.
# It also accepts a tuple `(n, m, f)` where `f` is a dict, list, or callable.

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = int(witness)
            m = int(witness)
            f_obj = lambda x: x
        elif isinstance(witness, dict):
            f_obj = witness
            n = len(f_obj)
            m = n
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                n, f_obj = witness
                m = n
            elif len(witness) == 3:
                n, m, f_obj = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if not (isinstance(n, int) and n >= 2):
            return [False, False, False]
        if not (isinstance(m, int) and m >= 2):
            return [False, False, False]
            
        # Evaluate f on 0..n-1
        if isinstance(f_obj, dict):
            f = lambda x: f_obj.get(x, x)
        elif isinstance(f_obj, (list, tuple)):
            f = lambda x: f_obj[x]
        elif callable(f_obj):
            f = f_obj
        else:
            return [False, False, False]
            
        f_vals = []
        for i in range(n):
            val = f(i)
            if not isinstance(val, int) and not (hasattr(val, 'is_Integer') and val.is_Integer):
                return [False, False, False]
            f_vals.append(int(val) % m)
            
    except Exception:
        return [False, False, False]

    # H1: R and S are commutative rings
    # Z_n and Z_m are commutative rings for any n, m >= 2
    h1 = True

    # H2: f: R -> S is a ring homomorphism
    h2 = True
    try:
        # f(1) == 1
        if f_vals[1] != 1:
            h2 = False
        
        # f(a+b) == f(a) + f(b)
        for a in range(n):
            for b in range(n):
                if f_vals[(a + b) % n] != (f_vals[a] + f_vals[b]) % m:
                    h2 = False
                    break
            if not h2:
                break
                
        # f(a*b) == f(a) * f(b)
        if h2:
            for a in range(n):
                for b in range(n):
                    if f_vals[(a * b) % n] != (f_vals[a] * f_vals[b]) % m:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The nilradical of R is NOT contained in the kernel of f
    neg_q = False
    try:
        # Find nilradical of Z_n
        nilradical = []
        for x in range(n):
            p = x
            is_nil = False
            for k in range(1, n + 1):
                if p % n == 0:
                    is_nil = True
                    break
                p = (p * x) % n
            if is_nil:
                nilradical.append(x)
                
        # Check if nilradical is contained in kernel
        # Kernel is {x | f(x) == 0 mod m}
        for x in nilradical:
            if f_vals[x] != 0:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: The nilradical of R is not contained in the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2