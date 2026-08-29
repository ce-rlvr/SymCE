import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        if not isinstance(H, PermutationGroup):
            neg_q_ok = False
        else:
            normalizer_elements = []
            for g in G.elements:
                try:
                    gens = [g * h * ~g for h in H.generators]
                    gHg = PermutationGroup(gens)
                    if gHg == H:
                        normalizer_elements.append(g)
                except Exception:
                    pass
            
            if len(normalizer_elements) == 0:
                neg_q_ok = False
            else:
                index = G.order() // len(normalizer_elements)
                
                conjugates = []
                for g in G.elements:
                    try:
                        gens = [g * h * ~g for h in H.generators]
                        gHg = PermutationGroup(gens)
                        
                        is_subgroup = True
                        for gen in gHg.generators:
                            if gen not in G:
                                is_subgroup = False
                                break
                        
                        if is_subgroup:
                            if gHg not in conjugates:
                                conjugates.append(gHg)
                    except Exception:
                        pass
                            
                num_conjugate_subgroups = len(conjugates)
                neg_q_ok = (num_conjugate_subgroups != index)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "not Q: The number of distinct subgroups of G conjugate to H is not the index of N_G(H) in G"
]

N_HYP = 1
NEG_Q_INDEX = 1