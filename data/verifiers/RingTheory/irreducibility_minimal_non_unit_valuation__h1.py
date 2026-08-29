import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    witness can be a tuple (n, d_dict, x) representing the ring Z/nZ,
    where d_dict is a dictionary or list mapping non-zero elements to their Euclidean valuation,
    and x is the element in question.
    Alternatively, witness can be an object with attributes:
    elements, add, mul, zero, one, d, x.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
            n, d_dict, x = witness
            elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            zero = 0
            one = 1
            if isinstance(d_dict, (dict, list)):
                d = lambda a, d_dict=d_dict: d_dict[a]
            else:
                d = d_dict
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            d = witness.d
            x = witness.x
    except Exception:
        return [False, False, False, False]

    def is_unit(a):
        for b in elements:
            if mul(a, b) == one:
                return True
        return False

    # H1: d is a submultiplicative Euclidean function on R
    h1 = False
    try:
        h1_ok = True
        # Check if d maps non-zero elements to non-negative integers
        for a in elements:
            if a != zero:
                val = d(a)
                if not isinstance(val, int) or val < 0:
                    h1_ok = False
                    break
        
        # Check Euclidean property: for all a, b != 0, exists q, r such that a = bq + r and (r == 0 or d(r) < d(b))
        if h1_ok:
            for a in elements:
                for b in elements:
                    if b != zero:
                        found = False
                        for q in elements:
                            for r in elements:
                                if a == add(mul(b, q), r):
                                    if r == zero or d(r) < d(b):
                                        found = True
                                        break
                            if found:
                                break
                        if not found:
                            h1_ok = False
                            break
                if not h1_ok:
                    break
                    
        # Check submultiplicative property: d(ab) <= d(a)d(b) for all a, b such that ab != 0
        if h1_ok:
            for a in elements:
                for b in elements:
                    if a != zero and b != zero:
                        ab = mul(a, b)
                        if ab != zero:
                            if d(ab) > d(a) * d(b):
                                h1_ok = False
                                break
                if not h1_ok:
                    break
        h1 = h1_ok
    except Exception:
        h1 = False

    # H2: x is a non-zero non-unit in R
    h2 = False
    try:
        if x != zero and not is_unit(x):
            h2 = True
    except Exception:
        h2 = False

    # H3: d(x) is minimal among all non-zero non-units in R
    h3 = False
    try:
        dx = d(x)
        h3_ok = True
        for a in elements:
            if a != zero and not is_unit(a):
                if d(a) < dx:
                    h3_ok = False
                    break
        h3 = h3_ok
    except Exception:
        h3 = False

    # neg_Q: x is NOT an irreducible element in R
    # An element x is irreducible if it is non-zero, non-unit, and x = ab implies a is a unit or b is a unit.
    neg_q = False
    try:
        if x == zero or is_unit(x):
            neg_q = True
        else:
            is_irred = True
            for a in elements:
                for b in elements:
                    if mul(a, b) == x:
                        if not is_unit(a) and not is_unit(b):
                            is_irred = False
                            break
                if not is_irred:
                    break
            neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: d is a submultiplicative Euclidean function on R",
    "H_2: x is a non-zero non-unit in R",
    "H_3: d(x) is minimal among all non-zero non-units in R",
    "¬Q: x is not an irreducible element in R"
]

N_HYP = 3
NEG_Q_INDEX = 3