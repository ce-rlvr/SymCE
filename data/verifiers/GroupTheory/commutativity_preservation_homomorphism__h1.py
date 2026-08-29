import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def evaluate_f(f, a):
    if isinstance(f, dict):
        return f[a]
    return f(a)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            x = witness['x']
            y = witness['y']
        else:
            G, H, f, x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: f is a group homomorphism from G to H
    h1 = False
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        h1 = True
        for a in elements:
            fa = evaluate_f(f, a)
            if fa not in H:
                h1 = False
                break
            for b in elements:
                fb = evaluate_f(f, b)
                fab = evaluate_f(f, a * b)
                if fab != fa * fb:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: x and y are elements of G such that xy = yx
    h2 = False
    try:
        if x in G and y in G:
            if x * y == y * x:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: f(x)f(y) != f(y)f(x) in H
    neg_q = False
    try:
        fx = evaluate_f(f, x)
        fy = evaluate_f(f, y)
        if fx * fy != fy * fx:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: x and y are elements of G such that xy = yx",
    "¬Q: f(x)f(y) != f(y)f(x) in H"
]

N_HYP = 2
NEG_Q_INDEX = 2