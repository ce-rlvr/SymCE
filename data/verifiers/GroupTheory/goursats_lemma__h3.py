import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H, S) where G and H are groups, 
    and S is a subset of G x H.
    """
    try:
        G, H, S = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails.
    # By Goursat's Lemma, the conclusion holds IF AND ONLY IF S is a subgroup of G x H.
    # Therefore, the conclusion fails iff S is NOT a subgroup of G x H.
    try:
        if not h1 or not h2:
            neg_q = True
        else:
            is_subgroup = True
            if not S:
                is_subgroup = False
            else:
                S_list = list(S)
                try:
                    S_set = set(S_list)
                except Exception:
                    S_set = S_list
                    
                id_G = G.identity
                id_H = H.identity
                
                if (id_G, id_H) not in S_set:
                    is_subgroup = False
                else:
                    # Check if S is a subset of G x H
                    for x in S_set:
                        if not isinstance(x, tuple) or len(x) != 2:
                            is_subgroup = False
                            break
                        g, h = x
                        if g not in G or h not in H:
                            is_subgroup = False
                            break
                    
                    # Check closure under group operation
                    if is_subgroup:
                        for (g1, h1_el) in S_set:
                            for (g2, h2_el) in S_set:
                                if (g1 * g2, h1_el * h2_el) not in S_set:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                                
                    # Check closure under inverses
                    if is_subgroup:
                        for (g, h_el) in S_set:
                            if (g**-1, h_el**-1) not in S_set:
                                is_subgroup = False
                                break
                                
            neg_q = not is_subgroup
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "¬Q: S is not a subgroup of G x H (so it cannot be represented as a fiber product of subgroups)"
]

N_HYP = 2
NEG_Q_INDEX = 2