import sympy
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_automorphism(G, alpha):
    try:
        if not isinstance(G, PermutationGroup):
            return False
        
        elements = list(G.elements)
        
        if isinstance(alpha, dict):
            mapped = [alpha.get(g, None) for g in elements]
            if any(m is None for m in mapped):
                return False
        else:
            mapped = [alpha(g) for g in elements]
            
        if set(mapped) != set(elements):
            return False
            
        gens = G.generators
        for g in gens:
            for h in elements:
                gh = g * h
                val1 = alpha[gh] if isinstance(alpha, dict) else alpha(gh)
                ag = alpha[g] if isinstance(alpha, dict) else alpha(g)
                ah = alpha[h] if isinstance(alpha, dict) else alpha(h)
                if val1 != ag * ah:
                    return False
        return True
    except Exception:
        return False

def is_subgroup(G, S):
    try:
        if isinstance(S, PermutationGroup):
            return S.is_subgroup(G)
        
        if not S:
            return False
        S_set = set(S)
        elements = set(G.elements)
        if not S_set.issubset(elements):
            return False
        
        if G.identity not in S_set:
            return False
            
        for x in S_set:
            if x**-1 not in S_set:
                return False
            for y in S_set:
                if x * y not in S_set:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            alpha = witness.get('alpha')
            S = witness.get('S', None)
        else:
            if len(witness) == 2:
                G, alpha = witness
                S = None
            elif len(witness) == 3:
                G, alpha, S = witness
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = is_automorphism(G, alpha)
    except Exception:
        h2 = False

    # If S is not explicitly provided, assume the theorem was about the set of elements inverted by alpha
    if S is None and h1 and h2:
        try:
            elements = list(G.elements)
            if isinstance(alpha, dict):
                S = [g for g in elements if alpha.get(g) == g**-1]
            else:
                S = [g for g in elements if alpha(g) == g**-1]
        except Exception:
            S = []

    try:
        neg_q = not is_subgroup(G, S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: \\alpha is an automorphism of G",
    "¬Q: S is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2