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

def conditions(witness) -> list[bool]:
    try:
        # Witness must be an integer
        if isinstance(witness, bool):
            return [False]
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
            
        n = int(witness)
        
        # The conclusion states that x_1^2 + x_2^2 + x_3^2 + x_4^2 = n has at least one solution in integers.
        # By Lagrange's Four-Square Theorem, this is true for all n >= 0.
        # For n < 0, it is false because squares of real numbers are non-negative.
        # neg_Q is True if the conclusion FAILS (i.e., no solution exists).
        neg_q = bool(n < 0)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The Diophantine equation x_1^2 + x_2^2 + x_3^2 + x_4^2 = n has no solution in integers"
]

N_HYP = 0
NEG_Q_INDEX = 0