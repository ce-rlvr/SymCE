import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools
import math
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
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: G is a finite group
    try:
        if isinstance(witness, PermutationGroup):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The Frattini subgroup of G is NOT the trivial subgroup
    try:
        if not h1:
            neg_q = False
        else:
            # Limit the order to prevent timeouts on excessively large groups
            if witness.order() > 100:
                neg_q = False
            else:
                elements = list(witness.generate())
                n = len(elements)
                if n == 1:
                    # Trivial group has trivial Frattini subgroup
                    neg_q = False
                else:
                    # Generate all subgroups
                    subgroups = set()
                    for g in elements:
                        H = PermutationGroup([g])
                        subgroups.add(frozenset(H.generate()))
                        
                    queue = list(subgroups)
                    max_iters = 5000
                    iters = 0
                    
                    # Close under join to find all subgroups
                    while queue and iters < max_iters:
                        iters += 1
                        H1 = queue.pop(0)
                        for H2 in list(subgroups):
                            if not H1.issubset(H2) and not H2.issubset(H1):
                                H_new = PermutationGroup(list(H1) + list(H2))
                                fs = frozenset(H_new.generate())
                                if fs not in subgroups:
                                    subgroups.add(fs)
                                    queue.append(fs)
                                    
                    proper_subgroups = [H for H in subgroups if len(H) < n]
                    
                    # Identify maximal subgroups
                    maximal_subgroups = []
                    for H in proper_subgroups:
                        is_maximal = True
                        for K in proper_subgroups:
                            if H != K and H.issubset(K):
                                is_maximal = False
                                break
                        if is_maximal:
                            maximal_subgroups.append(H)
                            
                    # Frattini subgroup is the intersection of all maximal subgroups
                    if not maximal_subgroups:
                        frattini_size = 1
                    else:
                        frattini = set(maximal_subgroups[0])
                        for M in maximal_subgroups[1:]:
                            frattini = frattini.intersection(M)
                        frattini_size = len(frattini)
                        
                    # The conclusion fails if the Frattini subgroup is non-trivial
                    neg_q = (frattini_size > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The Frattini subgroup of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1