import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math

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

def _lcm(a, b):
    a, b = int(a), int(b)
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1:
            order_G = int(witness.order())
            if order_G > 10000:
                h2 = False
            else:
                exp = 1
                for g in witness.elements:
                    exp = _lcm(exp, g.order())
                h2 = (exp == order_G)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            order_G = int(witness.order())
            if order_G > 10000:
                neg_q = False
            else:
                is_cyclic = False
                for g in witness.elements:
                    if int(g.order()) == order_G:
                        is_cyclic = True
                        break
                neg_q = not is_cyclic
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The exponent of G is equal to the order of G",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2