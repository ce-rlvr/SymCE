import sympy
import sympy.combinatorics
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        G, K, L = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
    except Exception:
        G_elems = []

    try:
        K_list = list(K)
        if not K_list or not G_elems:
            h2 = False
        else:
            k_elem = K_list[0]
            if k_elem not in G_elems:
                h2 = False
            else:
                conj_class = set()
                for g in G_elems:
                    try:
                        inv_g = ~g
                    except Exception:
                        inv_g = g**-1
                    conj_class.add(g * k_elem * inv_g)
                h2 = (set(K) == conj_class)
    except Exception:
        h2 = False

    try:
        L_list = list(L)
        if not L_list or not G_elems:
            h3 = False
        else:
            l_elem = L_list[0]
            if l_elem not in G_elems:
                h3 = False
            else:
                conj_class = set()
                for g in G_elems:
                    try:
                        inv_g = ~g
                    except Exception:
                        inv_g = g**-1
                    conj_class.add(g * l_elem * inv_g)
                h3 = (set(L) == conj_class)
    except Exception:
        h3 = False

    try:
        if not G_elems:
            neg_q = False
        else:
            KL = set()
            for k in K:
                for l in L:
                    KL.add(k * l)
            
            is_union = True
            for x in KL:
                for g in G_elems:
                    try:
                        inv_g = ~g
                    except Exception:
                        inv_g = g**-1
                    if (g * x * inv_g) not in KL:
                        is_union = False
                        break
                if not is_union:
                    break
            neg_q = not is_union
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a conjugacy class of G",
    "H_3: L is a conjugacy class of G",
    "¬Q: KL is not a union of conjugacy classes of G"
]

N_HYP = 3
NEG_Q_INDEX = 3