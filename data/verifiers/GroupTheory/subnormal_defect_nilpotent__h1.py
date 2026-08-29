import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_trivial_group(G):
    try:
        if hasattr(G, 'is_trivial'):
            val = G.is_trivial
            if callable(val):
                return val()
            return val
    except Exception:
        pass
    return len(list(G.generate())) == 1

def get_nilpotency_class(G):
    try:
        if hasattr(G, 'nilpotency_class'):
            val = G.nilpotency_class
            if callable(val):
                return val()
            if val is not None:
                return val
    except Exception:
        pass
        
    if is_trivial_group(G):
        return 0
    L = G
    c = 0
    while True:
        gens = []
        for h in list(L.generate()):
            for k in list(G.generate()):
                comm = (h**-1)*(k**-1)*h*k
                if comm != G.identity:
                    gens.append(comm)
        if not gens:
            return c
        next_L = PermutationGroup(gens)
        if next_L.is_subgroup(L) and L.is_subgroup(next_L):
            return float('inf')
        L = next_L
        c += 1

def check_nilpotent(G):
    try:
        if hasattr(G, 'is_nilpotent'):
            val = G.is_nilpotent
            if callable(val):
                return val()
            if val is not None:
                return val
    except Exception:
        pass
    return get_nilpotency_class(G) != float('inf')

def subnormal_defect(H, G):
    if H.is_subgroup(G) and G.is_subgroup(H):
        return 0
    N = G
    d = 0
    while True:
        gens = []
        for h in list(H.generate()):
            for n in list(N.generate()):
                gens.append((n**-1)*h*n)
        next_N = PermutationGroup(gens) if gens else PermutationGroup([G.identity])
        d += 1
        if next_N.is_subgroup(H) and H.is_subgroup(next_N):
            return d
        if next_N.is_subgroup(N) and N.is_subgroup(next_N):
            return float('inf')
        N = next_N

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, c = witness
                h1 = check_nilpotent(G) and get_nilpotency_class(G) == c
            elif len(witness) == 2:
                G, H = witness
                h1 = check_nilpotent(G)
                c = get_nilpotency_class(G)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        h2 = H.is_subgroup(G)
        
        if not (h1 and h2):
            return [bool(h1), bool(h2), False]
            
        defect = subnormal_defect(H, G)
        neg_q = defect > c
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is nilpotent of class c",
    "H_2: H is a subgroup of G",
    "¬Q: H is not subnormal in G or its subnormal defect is greater than c"
]

N_HYP = 2
NEG_Q_INDEX = 2