import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
    # Extract R, e, x
    R, e, x = None, None, None
    if isinstance(witness, tuple) and len(witness) == 3:
        R, e, x = witness
    elif isinstance(witness, dict):
        R = witness.get('R')
        e = witness.get('e')
        x = witness.get('x')
    else:
        try:
            R = witness.R
            e = witness.e
            x = witness.x
        except Exception:
            pass

    if R is None or e is None or x is None:
        return [False, False, False, False]

    try:
        elements = R.elements if hasattr(R, 'elements') else list(R)
        elements = list(elements)
    except Exception:
        return [False, False, False, False]

    # H1: R is a reduced ring (contains no non-zero nilpotent elements)
    h1 = False
    try:
        if hasattr(R, 'zero'):
            zero = R.zero
        else:
            zero = None
            for z in elements:
                is_zero = True
                for a in elements:
                    if not (z + a == a):
                        is_zero = False
                        break
                if is_zero:
                    zero = z
                    break
            if zero is None:
                zero = e - e
                
        h1 = True
        # Check closure under addition and multiplication
        for a in elements:
            for b in elements:
                sum_ab = a + b
                prod_ab = a * b
                if not any(sum_ab == c for c in elements):
                    h1 = False
                    break
                if not any(prod_ab == c for c in elements):
                    h1 = False
                    break
            if not h1:
                break

        # Check for nilpotents
        if h1:
            for a in elements:
                if a == zero:
                    continue
                # Right powers
                curr = a
                for _ in range(len(elements)):
                    curr = curr * a
                    if curr == zero:
                        h1 = False
                        break
                if not h1:
                    break
                # Left powers
                curr = a
                for _ in range(len(elements)):
                    curr = a * curr
                    if curr == zero:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: e is an idempotent element of R
    h2 = False
    try:
        e_in_R = False
        for a in elements:
            if e == a:
                e_in_R = True
                break
        if e_in_R and e * e == e:
            h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of R
    h3 = False
    try:
        x_in_R = False
        for a in elements:
            if x == a:
                x_in_R = True
                break
        if x_in_R:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: ex != xe (e is not in the center of R)
    neg_q = False
    try:
        if e * x != x * e:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "H_2: e is an idempotent element of R",
    "H_3: x is an element of R",
    "¬Q: ex != xe"
]

N_HYP = 3
NEG_Q_INDEX = 3