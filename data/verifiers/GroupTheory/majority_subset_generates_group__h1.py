import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros, Matrix
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if hasattr(witness, 'G') and hasattr(witness, 'S'):
            G = witness.G
            S = witness.S
        else:
            G, S = witness
    except Exception:
        return [False, False, False]
        
    def get_unique(lst):
        try:
            return list(set(lst))
        except TypeError:
            unique = []
            for item in lst:
                if not any(item == u for u in unique):
                    unique.append(item)
            return unique

    try:
        G_list = list(G)
        S_list = list(S)
        G_unique = get_unique(G_list)
        S_unique = get_unique(S_list)
    except Exception:
        return [False, False, False]

    try:
        h1 = all(any(s == g for g in G_unique) for s in S_unique)
    except Exception:
        h1 = False
        
    try:
        h2 = len(S_unique) > len(G_unique) / 2
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        for g in G_unique:
            can_form = False
            for x in S_unique:
                for y in S_unique:
                    try:
                        if x * y == g:
                            can_form = True
                            break
                    except Exception:
                        pass
                if can_form:
                    break
            if not can_form:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a subset of G",
    "H_2: The cardinality of S is strictly greater than |G| / 2",
    "¬Q: There exists g in G such that g != xy for all x, y in S"
]

N_HYP = 2
NEG_Q_INDEX = 2