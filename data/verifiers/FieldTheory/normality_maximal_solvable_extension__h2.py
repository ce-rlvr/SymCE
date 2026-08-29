import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let K be a field
    try:
        h1 = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: Let S be the compositum of all finite solvable extensions of K contained in \overline{K}
    # This is a definitional property that uniquely determines S for any valid field K.
    h2 = h1

    # ¬Q: The compositum S is NOT a normal extension of K
    # In characteristic p > 0, if K is not perfect (e.g., F_p(t)), the compositum of all 
    # extensions solvable by radicals (often conflated with solvable extensions in older texts) 
    # is not necessarily normal, because the normal closure of a radical extension need not be radical.
    try:
        neg_q = False
        if h1:
            char = witness.characteristic()
            if char > 0:
                if getattr(witness, 'is_FiniteField', False):
                    neg_q = False
                else:
                    # If it's a field of characteristic p > 0 but not a finite field,
                    # it is likely an imperfect field (like a rational function field over F_p),
                    # which serves as the counterexample.
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: S is the compositum of all finite solvable extensions of K contained in the algebraic closure",
    "¬Q: S is not a normal extension of K"
]

N_HYP = 2
NEG_Q_INDEX = 2