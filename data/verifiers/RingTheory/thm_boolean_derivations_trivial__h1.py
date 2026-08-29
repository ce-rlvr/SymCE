import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R_raw, add, mul, d = witness
            elif len(witness) == 2:
                R_raw, d = witness
                add = lambda x, y: x + y
                mul = lambda x, y: x * y
            else:
                return [False, False]
        else:
            R_raw = witness.R
            add = witness.add
            mul = witness.mul
            d = witness.d
            
        # Safely convert R to a list and limit size to prevent infinite loops
        R = []
        for i, x in enumerate(R_raw):
            if i > 1000:
                return [False, False]
            R.append(x)
    except Exception:
        return [False, False]

    def eq(a, b):
        try:
            return bool(a == b)
        except Exception:
            return False

    def contains(lst, item):
        return any(eq(x, item) for x in lst)

    # H_1: d is a derivation on R
    try:
        h1 = True
        for x in R:
            if not h1: break
            if not contains(R, d(x)):
                h1 = False
                break
            for y in R:
                if not contains(R, add(x, y)):
                    h1 = False
                    break
                if not contains(R, mul(x, y)):
                    h1 = False
                    break
                if not eq(d(add(x, y)), add(d(x), d(y))):
                    h1 = False
                    break
                if not eq(d(mul(x, y)), add(mul(d(x), y), mul(x, d(y)))):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: d is not identically zero
    try:
        zeros_list = [z for z in R if all(eq(add(z, x), x) for x in R)]
        if not zeros_list:
            neg_q = False
        else:
            zero = zeros_list[0]
            neg_q = any(not eq(d(x), zero) for x in R)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is a derivation on R",
    "¬Q: d is not identically zero"
]

N_HYP = 1
NEG_Q_INDEX = 1