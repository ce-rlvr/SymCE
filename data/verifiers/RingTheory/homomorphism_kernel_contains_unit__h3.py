import sympy
from sympy import ZZ
import math
import itertools
import functools

# Top-level setup: named object bindings for the witness namespace
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
zero_ring = 1

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, S, f = witness
            elif len(witness) == 2:
                R, S = witness
                f = None
            else:
                R, S, f = None, None, None
        else:
            R, S, f = None, None, None
    except Exception:
        R, S, f = None, None, None

    def parse_ring(ring):
        if ring is ZZ: 
            return 0
        if str(ring) == 'ZZ': 
            return 0
        return int(ring)

    # H_1: R and S are rings with identity
    try:
        n = parse_ring(R)
        m = parse_ring(S)
        h1 = (n >= 0) and (m >= 0)
    except Exception:
        h1 = False

    # H_2: f: R -> S is a ring homomorphism such that f(1_R) = 1_S
    try:
        n = parse_ring(R)
        m = parse_ring(S)
        
        # Check if the natural projection is well-defined
        if m == 0:
            h2 = (n == 0)
        else:
            h2 = (n % m == 0)
            
        # If an explicit mapping is provided, verify its properties
        if h2 and f is not None:
            if isinstance(f, (dict, list, tuple)):
                def f_call(x):
                    key = x if n == 0 else x % n
                    return f[key]
                func = f_call
            else:
                func = f

            # Check f(1_R) = 1_S
            val = func(1)
            if m == 0:
                if val != 1: 
                    h2 = False
            else:
                if val % m != 1 % m: 
                    h2 = False
            
            # Check homomorphism properties on a sample of elements
            elements = [0, 1, 2, 3, 4, 5]
            for a in elements:
                for b in elements:
                    sum_ab = a + b
                    prod_ab = a * b
                    if m == 0:
                        if func(sum_ab) != func(a) + func(b): 
                            h2 = False
                        if func(prod_ab) != func(a) * func(b): 
                            h2 = False
                    else:
                        if func(sum_ab) % m != (func(a) + func(b)) % m: 
                            h2 = False
                        if func(prod_ab) % m != (func(a) * func(b)) % m: 
                            h2 = False
    except Exception:
        h2 = False

    # ¬Q: S is not the zero ring
    try:
        m = parse_ring(S)
        # The ring Z/mZ is the zero ring if and only if m == 1
        neg_q = (m != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f: R -> S is a ring homomorphism such that f(1_R) = 1_S",
    "¬Q: S is not the zero ring"
]

N_HYP = 2
NEG_Q_INDEX = 2