import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_bool_prop(obj, *names, default=False):
    if isinstance(obj, dict):
        for name in names:
            if name in obj:
                return bool(obj[name])
    else:
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    return bool(val())
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            h1 = get_bool_prop(R, "is_left_noetherian", "is_left_noetherian_ring", "left_noetherian", default=False)
            is_two_sided = get_bool_prop(I, "is_two_sided_ideal", "is_ideal", "is_two_sided", default=True)
            if not is_two_sided:
                q = False
            else:
                q = get_bool_prop(R, "is_quotient_left_noetherian", "quotient_is_left_noetherian", default=True)
            return [h1, not q]
        
        h1 = get_bool_prop(witness, "is_left_noetherian", "is_left_noetherian_ring", "left_noetherian", default=False)
        q = get_bool_prop(witness, "is_quotient_left_noetherian", "quotient_is_left_noetherian", "is_quotient_ring_left_noetherian", default=True)
        return [h1, not q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a left Noetherian ring",
    "¬Q: The quotient ring R/I is not a left Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1