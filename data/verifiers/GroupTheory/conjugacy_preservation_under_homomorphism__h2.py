import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            x = witness.get('x')
            y = witness.get('y')
        else:
            G, H, f, x, y = witness
    except Exception:
        return [False, False, False, False]

    try:
        G_elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        H_elements = list(H.elements) if hasattr(H, 'elements') else list(H)
    except Exception:
        return [False, False, False, False]

    try:
        if callable(f):
            f_map = {g: f(g) for g in G_elements}
        elif isinstance(f, dict):
            f_map = f
        else:
            f_map = dict(f)
    except Exception:
        f_map = {}

    try:
        h1 = True
        for a in G_elements:
            if a not in f_map:
                h1 = False
                break
            if f_map[a] not in H_elements:
                h1 = False
                break
            for b in G_elements:
                ab = a * b
                if ab not in f_map:
                    h1 = False
                    break
                if f_map[ab] != f_map[a] * f_map[b]:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    try:
        h2 = x in G_elements
    except Exception:
        h2 = False

    try:
        h3 = y in G_elements
    except Exception:
        h3 = False

    try:
        if x not in f_map or y not in f_map:
            neg_q = False
        else:
            fx = f_map[x]
            fy = f_map[y]
            are_conjugate = False
            for h in H_elements:
                try:
                    h_inv = ~h
                except Exception:
                    h_inv = h**-1
                if h * fx * h_inv == fy:
                    are_conjugate = True
                    break
            neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "¬Q: f(x) and f(y) are not conjugate in H"
]

N_HYP = 3
NEG_Q_INDEX = 3