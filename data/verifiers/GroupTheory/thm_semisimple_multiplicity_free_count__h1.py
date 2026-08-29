import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)
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
        k, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: k is a positive integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and k > 0
    except Exception:
        h1 = False
        
    # H_2: G is the direct product of exactly k pairwise non-isomorphic simple groups
    try:
        h2 = False
        if hasattr(G, 'normal_subgroups'):
            normals = G.normal_subgroups()
            non_trivial = [N for N in normals if N.order() > 1]
            min_normals = []
            
            # Find all minimal normal subgroups
            for N in non_trivial:
                is_minimal = True
                for M in non_trivial:
                    if M.order() < N.order():
                        # Check if M is a subgroup of N
                        if all(g in N for g in M.generators):
                            is_minimal = False
                            break
                if is_minimal:
                    min_normals.append(N)
            
            if len(min_normals) == k:
                all_simple = True
                for M in min_normals:
                    if len(M.normal_subgroups()) != 2:
                        all_simple = False
                        break
                
                if all_simple:
                    pairwise_non_iso = True
                    for i in range(len(min_normals)):
                        for j in range(i+1, len(min_normals)):
                            M1 = min_normals[i]
                            M2 = min_normals[j]
                            if M1.order() == M2.order():
                                if hasattr(M1, 'is_isomorphic'):
                                    if M1.is_isomorphic(M2):
                                        pairwise_non_iso = False
                                else:
                                    # Fallback for groups of the same order if is_isomorphic is missing
                                    pairwise_non_iso = False
                    
                    if pairwise_non_iso:
                        # Check if the minimal normal subgroups generate G
                        gens = []
                        for M in min_normals:
                            gens.extend(M.generators)
                        gen_group = PermutationGroup(gens)
                        if gen_group.order() == G.order():
                            h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: G does not have exactly 2^k distinct normal subgroups
    try:
        neg_q = len(G.normal_subgroups()) != (2 ** k)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "H_2: G is the direct product of exactly k pairwise non-isomorphic simple groups",
    "¬Q: G does not have exactly 2^k distinct normal subgroups"
]

N_HYP = 2
NEG_Q_INDEX = 2