import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup: named object bindings
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

def get_image(A, G, N, transversal):
    """
    Computes the image of subgroup A in the quotient group G/N.
    The quotient group is represented as a permutation group acting on the right cosets of N.
    """
    k = len(transversal)
    gens = []
    for g in A.generators:
        perm = []
        for i in range(k):
            target = transversal[i] * g
            found = False
            for j in range(k):
                # Check if target and transversal[j] are in the same right coset of N
                if (target * ~transversal[j]) in N:
                    perm.append(j)
                    found = True
                    break
            if not found:
                perm.append(i)
        gens.append(Permutation(perm))
    if not gens:
        return PermutationGroup([Permutation(list(range(k)))])
    return PermutationGroup(gens)

def check_conclusion(G, N):
    """
    Checks if the conclusion of the Fourth Isomorphism Theorem holds for (G, N).
    """
    subs_G = G.subgroups()
    # S1: set of subgroups of G containing N
    S1 = [A for A in subs_G if N.is_subgroup(A)]
    
    transversal = G.coset_transversal(N)
    # Q: quotient group G/N
    Q = get_image(G, G, N, transversal)
    # S2: set of subgroups of G/N
    S2 = Q.subgroups()
    
    if len(S1) != len(S2):
        return False
        
    images = []
    for A in S1:
        A_Q = get_image(A, G, N, transversal)
        images.append(A_Q)
        
        # Check normality condition: A is normal in G iff A/N is normal in G/N
        norm_A = A.is_normal(G)
        norm_AQ = A_Q.is_normal(Q)
        if norm_A != norm_AQ:
            return False
            
    def group_elements(grp):
        return frozenset(list(grp.generate()))
        
    S2_elements = set(group_elements(H) for H in S2)
    image_elements = [group_elements(H) for H in images]
    
    # Check if the natural map is well-defined into S2
    for img in image_elements:
        if img not in S2_elements:
            return False
            
    # Check if the natural map is a bijection
    if len(set(image_elements)) != len(S1):
        return False
        
    return True

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False
        
    # neg_Q: The conclusion fails
    try:
        if not h1:
            neg_q = False
        else:
            q = check_conclusion(G, N)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The conclusion fails"
]

N_HYP = 1
NEG_Q_INDEX = 1