import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: x and y are elements of F",
    "H_2: n is a non-zero integer",
    "H_3: x^n = y^n",
    "¬Q: x != y"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    F, x, y, n = None, None, None, None
    
    if isinstance(witness, dict):
        F = witness.get('F', None)
        x = witness.get('x', None)
        y = witness.get('y', None)
        n = witness.get('n', None)
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            ints = [i for i in witness if isinstance(i, int)]
            groups = [g for g in witness if hasattr(g, 'contains') or hasattr(g, 'elements') or hasattr(g, 'is_group')]
            if len(ints) == 1 and len(groups) == 1:
                n = ints[0]
                F = groups[0]
                rem = [item for item in witness if item is not n and item is not F]
                if len(rem) == 2:
                    x, y = rem[0], rem[1]
                elif len(rem) == 1:
                    x, y = rem[0], rem[0]
                else:
                    F, x, y, n = witness
            else:
                F, x, y, n = witness
        elif len(witness) == 3:
            ints = [i for i in witness if isinstance(i, int)]
            if len(ints) == 1:
                n = ints[0]
                rem = [item for item in witness if item is not n]
                if len(rem) == 2:
                    x, y = rem[0], rem[1]
                elif len(rem) == 1:
                    x, y = rem[0], rem[0]
                else:
                    x, y, n = witness
            else:
                x, y, n = witness

    h1 = False
    try:
        if F is not None:
            if hasattr(F, '__contains__'):
                h1 = bool(x in F and y in F)
            elif hasattr(F, 'contains'):
                h1 = bool(F.contains(x) and F.contains(y))
            else:
                h1 = True
        else:
            h1 = x is not None and y is not None
    except Exception:
        h1 = False

    h2 = False
    try:
        h2 = isinstance(n, int) and n != 0
    except Exception:
        h2 = False

    h3 = False
    try:
        h3 = bool(x**n == y**n)
    except Exception:
        h3 = False

    neg_q = False
    try:
        neg_q = bool(x != y)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]