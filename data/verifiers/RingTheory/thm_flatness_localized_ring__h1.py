import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup for potential witness elements
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (R, S) where R is a finite ring (iterable of elements)
    and S is a subset of R.
    """
    try:
        if len(witness) != 2:
            return [False, False]
        R, S = witness
        R = list(R)
        S = list(S)
    except Exception:
        return [False, False]
    
    # H_1: S is a multiplicative subset of R
    try:
        h1 = True
        if not S:
            h1 = False
        else:
            # Check if S is a subset of R
            for s in S:
                if not any(s == r for r in R):
                    h1 = False
                    break
            # Check closure under multiplication
            if h1:
                for a in S:
                    for b in S:
                        ab = a * b
                        if not any(ab == s for s in S):
                            h1 = False
                            break
    except Exception:
        h1 = False

    # ¬Q: The localized ring S^{-1}R is NOT a flat R-module
    # For a non-commutative ring R, the localized ring S^{-1}R is a flat R-module 
    # (on both sides) if and only if S is both a left and right Ore set.
    # If it fails either Ore condition, the localization is either non-existent 
    # or not flat, meaning the conclusion fails.
    try:
        is_right_ore = True
        for r in R:
            for s in S:
                found = False
                for r_prime in R:
                    for s_prime in S:
                        if r * s_prime == s * r_prime:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    is_right_ore = False
                    break
            if not is_right_ore:
                break
                
        is_left_ore = True
        for r in R:
            for s in S:
                found = False
                for r_prime in R:
                    for s_prime in S:
                        if s_prime * r == r_prime * s:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    is_left_ore = False
                    break
            if not is_left_ore:
                break
                
        neg_q = not (is_right_ore and is_left_ore)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a multiplicative subset of R",
    "¬Q: The localized ring S^{-1}R is not a flat R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1