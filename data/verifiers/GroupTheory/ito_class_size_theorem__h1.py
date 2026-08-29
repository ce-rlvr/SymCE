import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(group):
    order = group.order
    if callable(order):
        return order()
    return order

def get_generators(group):
    gens = group.generators
    if callable(gens):
        return gens()
    return gens

def is_abelian(group):
    prop = group.is_abelian
    if callable(prop):
        return prop()
    return prop

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False] * 5
        G, A, x = witness
    except Exception:
        return [False] * 5

    # H1: A is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(A, PermutationGroup)
        if h1:
            A_gens = get_generators(A)
            h1 = all(gen in G for gen in A_gens)
    except Exception:
        h1 = False

    # H2: A is abelian
    try:
        h2 = h1 and bool(is_abelian(A))
    except Exception:
        h2 = False

    # H3: A is a normal subgroup of G
    try:
        h3 = h1
        if h3:
            G_gens = get_generators(G)
            A_gens = get_generators(A)
            for g in G_gens:
                for a in A_gens:
                    if (g * a * ~g) not in A:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # H4: x is an element of G
    try:
        h4 = isinstance(G, PermutationGroup) and isinstance(x, Permutation) and (x in G)
    except Exception:
        h4 = False

    # neg_Q: The size of the conjugacy class of x in G does NOT divide the index of A in G
    try:
        if h1 and h4:
            index = get_order(G) // get_order(A)
            
            # Compute the size of the conjugacy class of x in G using BFS
            orbit = {x}
            queue = [x]
            G_gens = get_generators(G)
            while queue:
                curr = queue.pop(0)
                for g in G_gens:
                    nxt = g * curr * ~g
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            cc_size = len(orbit)
            
            neg_q = (index % cc_size != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a subgroup of G",
    "H_2: A is abelian",
    "H_3: A is a normal subgroup of G",
    "H_4: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G does not divide the index of A in G"
]

N_HYP = 4
NEG_Q_INDEX = 4