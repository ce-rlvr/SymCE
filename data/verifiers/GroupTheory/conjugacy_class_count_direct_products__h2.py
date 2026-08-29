import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.matrices import eye, zeros
from sympy import oo
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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a finite group
    try:
        if isinstance(G, PermutationGroup):
            h1_ok = True
        else:
            if hasattr(G, 'order'):
                order = G.order() if callable(G.order) else G.order
                h1_ok = (order != oo) and (order < float('inf'))
            elif hasattr(G, 'is_finite'):
                h1_ok = bool(G.is_finite)
            else:
                h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: The number of conjugacy classes of G x H is NOT equal to the product
    try:
        def get_direct_product(g, h):
            try:
                from sympy.combinatorics.group_constructs import DirectProduct
                return DirectProduct(g, h)
            except Exception:
                pass
            try:
                return g * h
            except Exception:
                pass
            if hasattr(g, 'direct_product'):
                return g.direct_product(h)
            raise ValueError("Cannot compute direct product")

        def get_num_classes(obj):
            if hasattr(obj, 'conjugacy_classes'):
                c = obj.conjugacy_classes
                res = c() if callable(c) else c
                try:
                    return len(res)
                except TypeError:
                    return sum(1 for _ in res)
            elif hasattr(obj, 'classes'):
                c = obj.classes
                res = c() if callable(c) else c
                try:
                    return len(res)
                except TypeError:
                    return sum(1 for _ in res)
            elif hasattr(obj, 'n_conjugacy_classes'):
                c = obj.n_conjugacy_classes
                return c() if callable(c) else c
            else:
                raise ValueError("Cannot determine number of conjugacy classes")

        GxH = get_direct_product(G, H)
        num_G = get_num_classes(G)
        num_H = get_num_classes(H)
        num_GxH = get_num_classes(GxH)

        neg_q_ok = (num_GxH != num_G * num_H)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The number of conjugacy classes of G x H is not equal to the product of the number of conjugacy classes of G and H"
]

N_HYP = 1
NEG_Q_INDEX = 1