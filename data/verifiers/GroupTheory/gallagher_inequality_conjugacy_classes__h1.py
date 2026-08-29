import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    try:
        return list(G.generate())
    except Exception:
        return list(G.elements)

def k_group(G):
    if hasattr(G, 'conjugacy_classes'):
        cc = G.conjugacy_classes
        if callable(cc):
            return len(cc())
        else:
            return len(cc)
            
    elements = get_elements(G)
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        orbit = set()
        for g in elements:
            cx = g * x * ~g
            orbit.add(cx)
        unseen -= orbit
        classes.append(orbit)
    return len(classes)

def k_quotient(G, N):
    elements = get_elements(G)
    
    rep_of = {}
    reps = []
    for x in elements:
        found = False
        for r in reps:
            if (x * ~r) in N:
                rep_of[x] = r
                found = True
                break
        if not found:
            reps.append(x)
            rep_of[x] = x
            
    classes = []
    unseen = set(reps)
    while unseen:
        x = unseen.pop()
        orbit = set()
        for g in elements:
            cx = g * x * ~g
            r = rep_of[cx]
            orbit.add(r)
        unseen -= orbit
        classes.append(orbit)
    return len(classes)

def is_normal_subgroup(G, N):
    if not all(g in G for g in N.generators):
        return False
    for g in G.generators:
        for n in N.generators:
            if (g * n * ~g) not in N:
                return False
    return True

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = is_normal_subgroup(G, N)
    except Exception:
        h1 = False
        
    # ¬Q: k(G) > k(N) * k(G/N)
    try:
        if h1:
            kg = k_group(G)
            kn = k_group(N)
            kgn = k_quotient(G, N)
            neg_q = kg > kn * kgn
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: k(G) > k(N) k(G/N)"
]

N_HYP = 1
NEG_Q_INDEX = 1