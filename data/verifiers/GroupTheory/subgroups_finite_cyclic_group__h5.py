import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, n, d = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a cyclic group
    try:
        h2 = False
        if h1:
            order_G = G.order()
            for g in G.elements:
                if g.order() == order_G:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # H_3: the order of G is n
    try:
        h3 = False
        if h1:
            h3 = (G.order() == n)
    except Exception:
        h3 = False

    # H_4: d is a positive integer
    try:
        h4 = isinstance(d, (int, sympy.Integer)) and d > 0
    except Exception:
        h4 = False

    # ¬Q: G does not contain exactly one subgroup of order d
    try:
        neg_q = False
        if h1 and h4:
            if G.order() % d != 0:
                count = 0
            else:
                subgroups = set()
                id_elem = G.identity
                for g in G.elements:
                    o = g.order()
                    if o % d == 0:
                        gen = g ** (o // d)
                        elems = set()
                        curr = gen
                        elems.add(id_elem)
                        # Generate the cyclic subgroup
                        for _ in range(d + 2):
                            if curr == id_elem:
                                break
                            elems.add(curr)
                            curr = curr * gen
                        if len(elems) == d:
                            subgroups.add(frozenset(elems))
                count = len(subgroups)
            neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a cyclic group",
    "H_3: the order of G is n",
    "H_4: d is a positive integer",
    "¬Q: G does not contain exactly one subgroup of order d"
]

N_HYP = 4
NEG_Q_INDEX = 4