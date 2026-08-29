import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            S = witness['S']
            f = witness['f']
        else:
            G, H, S, f = witness
    except Exception:
        return [False, False, False]

    def apply_f(func, x):
        if isinstance(func, dict):
            if x in func:
                return func[x]
            for k, v in func.items():
                if k == x:
                    return v
            raise KeyError(f"{x} not found in dictionary")
        return func(x)

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: S is a subset of G
    try:
        S_list = list(S)
        G_elems = list(G.elements)
        h2 = all(s in G_elems for s in S_list)
    except Exception:
        h2 = False

    # neg_Q: f(N_G(S)) is not a subset of N_H(f(S))
    try:
        S_set = set(S)
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        
        N_G_S = set()
        for g in G_elems:
            conj = {g * s * g**-1 for s in S_set}
            if conj == S_set:
                N_G_S.add(g)
                
        f_S = {apply_f(f, s) for s in S_set}
        
        N_H_f_S = set()
        for h in H_elems:
            try:
                conj = {h * x * h**-1 for x in f_S}
                if conj == f_S:
                    N_H_f_S.add(h)
            except Exception:
                pass
                
        f_N_G_S = {apply_f(f, g) for g in N_G_S}
        
        neg_q = not f_N_G_S.issubset(N_H_f_S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: S is a subset of G",
    "¬Q: f(N_G(S)) is not a subset of N_H(f(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2