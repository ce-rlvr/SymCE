import sympy
from sympy import symbols, Rational, Integer, Matrix, eye, zeros
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The degree of L over K is an odd integer",
    "H_2: a in K is an element such that the polynomial x^2 - a has no root in K",
    "not Q: The polynomial x^2 - a HAS a root in L"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            L, K, a = witness
        else:
            L = getattr(witness, 'L', None)
            K = getattr(witness, 'K', None)
            a = getattr(witness, 'a', None)
    except Exception:
        return [False, False, False]

    try:
        deg = None
        if hasattr(witness, 'degree') and callable(getattr(witness, 'degree')):
            deg = witness.degree()
        elif hasattr(L, 'degree') and callable(getattr(L, 'degree')):
            try:
                deg = L.degree(K)
            except TypeError:
                deg = L.degree()
        elif hasattr(L, 'index') and callable(getattr(L, 'index')):
            deg = L.index(K)
        elif hasattr(L, '__len__') and hasattr(K, '__len__'):
            size_L = len(list(L))
            size_K = len(list(K))
            if size_K > 1:
                deg_float = math.log(size_L, size_K)
                deg = round(deg_float)
                if abs(deg_float - deg) > 1e-7:
                    deg = size_L // size_K
        
        if deg is not None:
            h1_ok = (int(deg) % 2 == 1)
    except Exception:
        h1_ok = False

    try:
        has_root_in_K = False
        if hasattr(witness, 'has_root_in_K') and callable(getattr(witness, 'has_root_in_K')):
            has_root_in_K = witness.has_root_in_K(a)
        elif hasattr(K, 'has_root') and callable(getattr(K, 'has_root')):
            has_root_in_K = K.has_root(a)
        elif hasattr(K, '__iter__'):
            for x in K:
                try:
                    if x * x == a or x**2 == a:
                        has_root_in_K = True
                        break
                except Exception:
                    pass
        h2_ok = not has_root_in_K
    except Exception:
        h2_ok = False

    try:
        has_root_in_L = False
        if hasattr(witness, 'has_root_in_L') and callable(getattr(witness, 'has_root_in_L')):
            has_root_in_L = witness.has_root_in_L(a)
        elif hasattr(L, 'has_root') and callable(getattr(L, 'has_root')):
            has_root_in_L = L.has_root(a)
        elif hasattr(L, '__iter__'):
            for x in L:
                try:
                    if x * x == a or x**2 == a:
                        has_root_in_L = True
                        break
                except Exception:
                    pass
        neg_q_ok = has_root_in_L
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]