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

class CommutativeRing:
    def __init__(self, name, every_nonzero_prime_is_maximal, is_PID):
        self.name = name
        self.every_nonzero_prime_is_maximal = every_nonzero_prime_is_maximal
        self.is_PID = is_PID

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Standard rings for witness evaluation
Z = CommutativeRing("Z", True, True)
Q = CommutativeRing("Q", True, True)
Z_x = CommutativeRing("Z[x]", False, False)
Q_x = CommutativeRing("Q[x]", True, True)
Q_x_y = CommutativeRing("Q[x,y]", False, False)

# Counterexamples to the false conjecture
Z_sqrt_m5 = CommutativeRing("Z[sqrt(-5)]", True, False)
Z4 = CommutativeRing("Z/4Z", True, False)
Z6 = CommutativeRing("Z/6Z", True, False)
Q_x_mod_x2 = CommutativeRing("Q[x]/(x^2)", True, False)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, "every_nonzero_prime_is_maximal"):
            h1 = bool(witness.every_nonzero_prime_is_maximal)
        elif witness in [sympy.ZZ, sympy.QQ]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, "is_PID"):
            neg_q = not bool(witness.is_PID)
        elif witness in [sympy.ZZ, sympy.QQ]:
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Every non-zero prime ideal of R is a maximal ideal",
    "¬Q: R is not a Principal Ideal Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1