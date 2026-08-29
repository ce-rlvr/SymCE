import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_normal_subgroup(H, K):
    if not H.is_subgroup(K):
        return False
    for h in H.generators:
        for k in K.generators:
            if (k * h * ~k) not in H:
                return False
            if (~k * h * k) not in H:
                return False
    return True

def conditions(witness):
    """
    witness is expected to be a tuple (G, series) where:
      - G is a PermutationGroup
      - series is a list of PermutationGroup objects representing the subnormal series
        [G_0, G_1, ..., G_n] with G_0 = G.
    """
    try:
        G, series = witness
        if not isinstance(G, PermutationGroup):
            return [False, False, False]
        if not isinstance(series, list):
            return [False, False, False]
        if len(series) < 2:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    n = len(series) - 1
    
    # H_1: G possesses a subnormal series of length n
    try:
        h1 = True
        # Check if series[0] is essentially G
        if not (series[0].is_subgroup(G) and G.is_subgroup(series[0])):
            h1 = False
        else:
            # Check if each G_{i+1} is a normal subgroup of G_i
            for i in range(n):
                H = series[i+1]
                K = series[i]
                if not is_normal_subgroup(H, K):
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H_2: All factor groups of this subnormal series are abelian
    try:
        h2 = True
        for i in range(n):
            H = series[i+1]
            K = series[i]
            # K/H is abelian iff the derived subgroup of K is a subgroup of H
            K_prime = K.derived_subgroup()
            if not K_prime.is_subgroup(H):
                h2 = False
                break
    except Exception:
        h2 = False
        
    # ¬Q: The n-th term of the derived series, G^(n), is NOT the trivial subgroup
    try:
        curr = G
        for _ in range(n):
            curr = curr.derived_subgroup()
        neg_q = curr.order() != 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G possesses a subnormal series of length n",
    "H_2: All factor groups of this subnormal series are abelian",
    "¬Q: The n-th term of the derived series, G^(n), is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2