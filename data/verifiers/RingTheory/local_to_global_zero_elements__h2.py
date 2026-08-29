import itertools
import math
import functools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        n, add, mul, x = witness
        elements = list(range(n))
    except Exception:
        return [False, False, False]

    h1 = True
    zero = None
    one = None
    try:
        for i in elements:
            for j in elements:
                if add[i][j] != add[j][i]: h1 = False
                if mul[i][j] != mul[j][i]: h1 = False
        for i in elements:
            for j in elements:
                for k in elements:
                    if add[add[i][j]][k] != add[i][add[j][k]]: h1 = False
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: h1 = False
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: h1 = False
        for i in elements:
            if all(add[i][j] == j for j in elements):
                zero = i
                break
        if zero is None: h1 = False
        if h1:
            for i in elements:
                if not any(add[i][j] == zero for j in elements): h1 = False
        for i in elements:
            if all(mul[i][j] == j for j in elements):
                one = i
                break
        if one is None or one == zero: h1 = False
    except Exception:
        h1 = False

    h2 = False
    try:
        if h1:
            ideals = []
            for r in range(1, n + 1):
                for subset in itertools.combinations(elements, r):
                    subset = set(subset)
                    if zero not in subset: continue
                    if not all(add[i][j] in subset for i in subset for j in subset): continue
                    if not all(mul[i][r_elem] in subset for i in subset for r_elem in elements): continue
                    ideals.append(subset)
            
            proper_ideals = [I for I in ideals if len(I) < n]
            maximal_ideals = []
            for I in proper_ideals:
                is_max = True
                for J in proper_ideals:
                    if I != J and I.issubset(J):
                        is_max = False
                        break
                if is_max:
                    maximal_ideals.append(I)
            
            h2_ok = True
            for M in maximal_ideals:
                found_s = False
                for s in elements:
                    if s not in M and mul[s][x] == zero:
                        found_s = True
                        break
                if not found_s:
                    h2_ok = False
                    break
            h2 = h2_ok
    except Exception:
        h2 = False

    neg_q = False
    try:
        if h1:
            neg_q = (x != zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: For every maximal ideal M of R, the image of x in the localization R_M is zero",
    "¬Q: x != 0 in R"
]

N_HYP = 2
NEG_Q_INDEX = 2