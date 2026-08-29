import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
        if len(witness) != 2:
            return [False, False]
        G, alpha = witness
    except Exception:
        return [False, False]

    try:
        elements = list(G.generate())
        elements_set = set(elements)
        derived = G.derived_subgroup()
        derived_elements = list(derived.generate())
        
        if len(derived_elements) != len(elements):
            h1 = False
        else:
            if isinstance(alpha, dict):
                mapping = alpha
            else:
                mapping = {g: alpha(g) for g in elements}
                
            h1 = True
            for g in elements:
                if g not in mapping or mapping[g] not in elements_set:
                    h1 = False
                    break
            if h1:
                if len(set(mapping.values())) != len(elements):
                    h1 = False
                else:
                    for g in elements:
                        for h in elements:
                            if mapping[g * h] != mapping[g] * mapping[h]:
                                h1 = False
                                break
                        if not h1:
                            break
    except Exception:
        h1 = False

    try:
        elements = list(G.generate())
        if isinstance(alpha, dict):
            mapping = alpha
        else:
            mapping = {g: alpha(g) for g in elements}
            
        neg_q = False
        for g in elements:
            if g in mapping and mapping[g] != g:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a perfect group and alpha is an automorphism of G",
    "¬Q: alpha is not the identity automorphism on G"
]

N_HYP = 1
NEG_Q_INDEX = 1