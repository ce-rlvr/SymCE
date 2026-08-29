import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

CONDITION_LABELS = [
    "¬Q: (x^2 ≡ -1 mod p has a solution) XOR (p ≡ 1 mod 4)"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if isinstance(witness, bool):
            return [False]
        p = int(witness)
        if p != witness:
            return [False]
    except Exception:
        return [False]
        
    try:
        if p == 0:
            A = False
        else:
            abs_p = abs(p)
            A = False
            if abs_p <= 10000000:
                for x in range(abs_p):
                    if (x*x + 1) % abs_p == 0:
                        A = True
                        break
            else:
                try:
                    from sympy.ntheory import nthroot_mod
                    A = (nthroot_mod(-1, 2, abs_p) is not None)
                except Exception:
                    return [False]
    except Exception:
        A = False

    try:
        B = (p % 4 == 1)
    except Exception:
        B = False

    try:
        neg_q = (A != B)
    except Exception:
        neg_q = False

    return [neg_q]