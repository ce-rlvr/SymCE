import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def _get_order(group):
    order_attr = group.order
    if callable(order_attr):
        return order_attr()
    return order_attr

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            A = witness['A']
            x = witness['x']
        else:
            G, A, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if hasattr(G, "order") and hasattr(G, "elements"):
            order_G = _get_order(G)
            if order_G <= 10000:
                if x in G:
                    h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            is_ab = A.is_abelian
            if callable(is_ab):
                is_ab = is_ab()
            if is_ab and A.is_subgroup(G):
                h2 = True
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2:
            ccl = set()
            for g in G.elements:
                ccl.add(~g * x * g)
            ccl_size = len(ccl)
            
            order_G = _get_order(G)
            order_A = _get_order(A)
            index = order_G / order_A
            
            neg_q = bool(ccl_size > index)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a finite group and x is an element of G", "H_2: A is an abelian subgroup of G", "¬Q: The size of the conjugacy class of x in G is strictly greater than the index of A in G"]
N_HYP = 2
NEG_Q_INDEX = 2