import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
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

def _eval_prop(obj, prop_name, default=False):
    if not hasattr(obj, prop_name):
        return default
    val = getattr(obj, prop_name)
    if callable(val):
        return val()
    return val

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_group'):
            h1 = bool(_eval_prop(witness, 'is_group'))
        else:
            h1 = hasattr(witness, 'generators') or isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_nilpotent'):
            h2 = bool(_eval_prop(witness, 'is_nilpotent'))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if hasattr(witness, 'is_supersolvable'):
            is_super = bool(_eval_prop(witness, 'is_supersolvable'))
        else:
            is_super = True
        neg_q = not is_super
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is nilpotent",
    "¬Q: G is not supersolvable"
]

N_HYP = 2
NEG_Q_INDEX = 2