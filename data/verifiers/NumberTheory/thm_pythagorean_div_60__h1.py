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

# Top-level setup
Rational = sympy.Rational
Integer = sympy.Integer

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(x**2 + y**2 == z**2)
    except Exception:
        h1 = False

    try:
        xyz = x * y * z
        neg_q = bool(xyz % 60 != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^2 + y^2 = z^2",
    "¬Q: xyz is not equivalent to 0 mod 60"
]

N_HYP = 1
NEG_Q_INDEX = 1