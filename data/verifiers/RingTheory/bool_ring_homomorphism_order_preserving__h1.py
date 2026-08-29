import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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

def conditions(witness) -> list[bool]:
    # Extract witness components
    R = None
    S = None
    f = None
    x = None
    y = None
    
    if isinstance(witness, dict):
        R = witness.get('R')
        S = witness.get('S')
        f = witness.get('f')
        x = witness.get('x')
        y = witness.get('y')
    else:
        R = getattr(witness, 'R', None)
        S = getattr(witness, 'S', None)
        f = getattr(witness, 'f', None)
        x = getattr(witness, 'x', None)
        y = getattr(witness, 'y', None)
        if f is None and x is None:
            try:
                R, S, f, x, y = witness
            except Exception:
                pass

    # H_1: f is a ring homomorphism from R to S
    h1_ok = False
    try:
        if hasattr(witness, 'is_ring_homomorphism'):
            h1_ok = bool(witness.is_ring_homomorphism())
        elif hasattr(f, 'is_ring_homomorphism'):
            h1_ok = bool(f.is_ring_homomorphism())
        else:
            # Check homomorphism properties on the provided elements
            h1_ok = True
            if f(x + y) != f(x) + f(y): h1_ok = False
            if f(x * y) != f(x) * f(y): h1_ok = False
            if f(y * x) != f(y) * f(x): h1_ok = False
            if f(x + x) != f(x) + f(x): h1_ok = False
            if f(y + y) != f(y) + f(y): h1_ok = False
            
            # If R is iterable, check exhaustively
            if h1_ok and R is not None and hasattr(R, '__iter__'):
                for a in R:
                    for b in R:
                        if f(a + b) != f(a) + f(b): h1_ok = False
                        if f(a * b) != f(a) * f(b): h1_ok = False
                        if not h1_ok: break
                    if not h1_ok: break
    except Exception:
        h1_ok = False

    # H_2: <= is defined by a <= b if and only if ab = a
    # This is a definitional hypothesis. We evaluate it as True since it establishes 
    # the meaning of <= for the subsequent conditions.
    h2_ok = True

    # H_3: x and y are elements of R such that x <= y
    h3_ok = False
    try:
        # Using the definition from H_2: x <= y iff x * y == x
        h3_ok = (x * y == x)
        if R is not None and hasattr(R, '__contains__'):
            h3_ok = h3_ok and (x in R) and (y in R)
    except Exception:
        h3_ok = False

    # neg_Q: f(x) <= f(y) in S is FALSE
    neg_q_ok = False
    try:
        # Using the definition from H_2: f(x) <= f(y) iff f(x) * f(y) == f(x)
        # The conclusion fails if f(x) * f(y) != f(x)
        neg_q_ok = (f(x) * f(y) != f(x))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: <= is defined by a <= b if and only if ab = a",
    "H_3: x and y are elements of R such that x <= y",
    "¬Q: f(x) <= f(y) in S is false"
]

N_HYP = 3
NEG_Q_INDEX = 3