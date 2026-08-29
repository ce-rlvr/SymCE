import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if len(witness) == 3:
            G, K, L = witness
            KL_given = None
        elif len(witness) == 4:
            G, K, L, KL_given = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        H1 = isinstance(G, PermutationGroup)
        if H1:
            try:
                G_elements = set(G.elements)
            except AttributeError:
                G_elements = set(G.generate())
        else:
            G_elements = set()
    except Exception:
        H1 = False
        G_elements = set()

    try:
        K_set = set(K)
        if not K_set or not K_set.issubset(G_elements):
            H2 = False
        else:
            k0 = next(iter(K_set))
            conj_class = {g * k0 * ~g for g in G_elements}
            H2 = (K_set == conj_class)
    except Exception:
        H2 = False

    try:
        L_set = set(L)
        H3 = L_set.issubset(G_elements)
        if KL_given is not None:
            KL_set = set(KL_given)
            H3 = H3 and (KL_set == {k * l for k in K_set for l in L_set})
    except Exception:
        H3 = False

    try:
        KL = {k * l for k in K_set for l in L_set}
        is_union = True
        for x in KL:
            for g in G_elements:
                if g * x * ~g not in KL:
                    is_union = False
                    break
            if not is_union:
                break
        neg_Q = not is_union
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a conjugacy class of G",
    "H_3: KL = {kl | k in K, l in L}",
    "¬Q: KL is not a union of conjugacy classes of G"
]

N_HYP = 3
NEG_Q_INDEX = 3