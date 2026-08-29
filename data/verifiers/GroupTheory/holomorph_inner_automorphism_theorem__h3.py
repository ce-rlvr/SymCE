import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import math
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
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, alpha = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2 is a definitional statement about Hol(G)
    h2 = True
    
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(G.elements)
            is_aut = True
            mapping = {}
            
            if isinstance(alpha, dict):
                mapping = alpha
            elif callable(alpha):
                try:
                    mapping = {g: alpha(g) for g in elements}
                except Exception:
                    is_aut = False
            else:
                is_aut = False

            if is_aut:
                for g in elements:
                    if g not in mapping or mapping[g] not in elements:
                        is_aut = False
                        break
            
            if is_aut:
                for g1 in elements:
                    for g2 in elements:
                        if mapping[g1 * g2] != mapping[g1] * mapping[g2]:
                            is_aut = False
                            break
                    if not is_aut:
                        break
                        
            if is_aut:
                if len(set(mapping.values())) != len(elements):
                    is_aut = False
                    
            # The conclusion holds iff alpha is an automorphism of G.
            # Therefore, the negated conclusion holds iff alpha is NOT an automorphism.
            neg_q = not is_aut
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Hol(G) = G ⋊ Aut(G) is the holomorph of G",
    "¬Q: There is no element in Hol(G) whose inner automorphism restricts exactly to alpha on G"
]

N_HYP = 2
NEG_Q_INDEX = 2