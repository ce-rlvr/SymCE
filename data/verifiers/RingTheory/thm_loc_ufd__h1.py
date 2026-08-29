import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
class MockRing:
    def __init__(self, name, is_ufd, zero=0, one=1):
        self.name = name
        self.is_ufd = is_ufd
        self.zero = zero
        self.one = one
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name

# Standard counterexamples for UFD-related conjectures
Z_sqrt_minus_5 = MockRing("Z[sqrt(-5)]", is_ufd=False, zero=0, one=1)
Z_x_y_z_w_mod_xy_zw = MockRing("Z[x,y,z,w]/(xy-zw)", is_ufd=False, zero=0, one=1)
Z = MockRing("Z", is_ufd=True, zero=0, one=1)
Q = MockRing("Q", is_ufd=True, zero=0, one=1)

def conditions(witness):
    try:
        R, S = witness
        
        # Handle string representations of R
        if isinstance(R, str):
            if "sqrt(-5)" in R:
                R = Z_sqrt_minus_5
            elif "xy-zw" in R:
                R = Z_x_y_z_w_mod_xy_zw
            elif R == "Z":
                R = Z
            elif R == "Q":
                R = Q
                
        # Handle various representations of S
        if isinstance(S, str):
            S_str = S.replace(" ", "")
            if S_str in ("{1}", "[1]", "(1,)", "1"):
                S = [1]
            elif S_str in ("{0}", "[0]", "(0,)", "0"):
                S = [0]
            elif S_str in ("{1,-1}", "[-1,1]", "{-1,1}", "[1,-1]"):
                S = [1, -1]
            else:
                S = [S]
        elif hasattr(S, '__iter__'):
            S = list(S)
        else:
            S = [S]
            
    except Exception:
        return [False, False, False]

    # H1: S is a multiplicatively closed subset of R
    try:
        if hasattr(R, 'one'):
            one = R.one
        else:
            one = 1
            
        is_closed = True
        if not S:
            is_closed = False
        else:
            for a in S:
                for b in S:
                    if (a * b) not in S:
                        is_closed = False
                        break
                if not is_closed:
                    break
        h1 = is_closed
    except Exception:
        h1 = False

    # H2: The zero element is not in S
    try:
        if hasattr(R, 'zero'):
            zero = R.zero
        else:
            zero = 0
        h2 = zero not in S
    except Exception:
        h2 = False

    # neg_Q: The localized ring S^{-1}R is NOT a Unique Factorization Domain
    try:
        if hasattr(R, 'one'):
            one = R.one
        else:
            one = 1
            
        # If S is {1} or {1, -1}, S^{-1}R is isomorphic to R
        if set(S) == {one} or set(S) == {one, -1}:
            if hasattr(R, 'is_ufd'):
                is_ufd = R.is_ufd
            elif hasattr(R, 'is_UFD'):
                is_ufd = R.is_UFD
            else:
                is_ufd = True
            neg_q = not is_ufd
        else:
            # For other S, we don't have a general way to check UFD in this mock.
            # But we can check if R is a known non-UFD and S is a subset of units.
            if getattr(R, 'name', '') in ("Z[sqrt(-5)]", "Z[x,y,z,w]/(xy-zw)") and set(S).issubset({1, -1}):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: The zero element is not in S",
    "¬Q: The localized ring S^{-1}R is not a Unique Factorization Domain"
]

N_HYP = 2
NEG_Q_INDEX = 2