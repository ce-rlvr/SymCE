import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
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
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be a tuple: (G, N, H, K) where all are PermutationGroup objects.
    """
    # H_1: K is a normal subgroup of H
    h1_ok = False
    try:
        G, N, H, K = witness
        
        def is_sub(sub, sup):
            return all(g in sup for g in sub.generators)
            
        if (hasattr(G, 'generators') and hasattr(N, 'generators') and 
            hasattr(H, 'generators') and hasattr(K, 'generators') and
            is_sub(N, G) and is_sub(H, G) and is_sub(K, H)):
            
            is_normal = True
            for h in H.generators:
                for k in K.generators:
                    if (h * k * ~h) not in K:
                        is_normal = False
                        break
                if not is_normal:
                    break
            h1_ok = is_normal
    except Exception:
        h1_ok = False

    # neg_Q: The product NK = {nk | n ∈ N, k ∈ K} forms a normal subgroup of G (must FAIL)
    neg_q_ok = False
    try:
        G, N, H, K = witness
        
        NK_set = set()
        for n in N.generate():
            for k in K.generate():
                NK_set.add(n * k)
                
        is_normal_subgroup = True
        
        # 1. Check if it contains the identity
        has_id = any(x.is_Identity for x in NK_set)
        if not has_id:
            is_normal_subgroup = False
        else:
            # 2. Check closure under multiplication
            for a in NK_set:
                for b in NK_set:
                    if (a * b) not in NK_set:
                        is_normal_subgroup = False
                        break
                if not is_normal_subgroup:
                    break
            
            # 3. Check normality in G
            if is_normal_subgroup:
                for g in G.generators:
                    for x in NK_set:
                        if (g * x * ~g) not in NK_set:
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
                        
        neg_q_ok = not is_normal_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a normal subgroup of H",
    "¬Q: The product NK = {nk | n ∈ N, k ∈ K} does not form a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1