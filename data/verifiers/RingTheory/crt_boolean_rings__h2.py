import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = list(witness['R'])
            x = witness['x']
            y = witness['y']
            one = witness.get('one', None)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                R, x, y = witness
                R = list(R)
                one = None
            elif len(witness) == 4:
                R, x, y, one = witness
                R = list(R)
            else:
                return [False, False, False]
        else:
            R = list(witness.R)
            x = witness.x
            y = witness.y
            one = getattr(witness, 'one', None)
            
        if one is None:
            ones = [e for e in R if all(e * a == a for a in R) and all(a * e == a for a in R)]
            if ones:
                one = ones[0]
            else:
                one = 1
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring
    try:
        is_bool_ring = True
        zero = x - x
        for a in R:
            if a * a != a:
                is_bool_ring = False
                break
            if a + a != zero:
                is_bool_ring = False
                break
            for b in R:
                if a + b != b + a:
                    is_bool_ring = False
                    break
                if a * b != b * a:
                    is_bool_ring = False
                    break
                if (a + b) not in R:
                    is_bool_ring = False
                    break
                if (a * b) not in R:
                    is_bool_ring = False
                    break
    except Exception:
        is_bool_ring = False

    # H_2: x + y + xy = 1
    try:
        h2 = bool(x + y + x * y == one)
    except Exception:
        h2 = False

    # ¬Q: The principal ideals (x) and (y) are not comaximal in R
    try:
        ideal_x = []
        for r in R:
            for elem in (x * r, x * r + x, x * r - x):
                if elem not in ideal_x:
                    ideal_x.append(elem)
                    
        ideal_y = []
        for r in R:
            for elem in (y * r, y * r + y, y * r - y):
                if elem not in ideal_y:
                    ideal_y.append(elem)
                    
        ideal_sum = []
        for a in ideal_x:
            for b in ideal_y:
                elem = a + b
                if elem not in ideal_sum:
                    ideal_sum.append(elem)
                    
        q = True
        for r in R:
            if r not in ideal_sum:
                q = False
                break
    except Exception:
        q = True

    return [is_bool_ring, h2, not q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x + y + xy = 1",
    "¬Q: The principal ideals (x) and (y) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2