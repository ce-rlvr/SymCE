import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H, K), checks if it is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, H_3_ok, H_4_ok, neg_Q_ok].
    """
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a normal subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G) and H.is_normal(G)
    except Exception:
        h2 = False
        
    # Extract elements for set operations
    try:
        if isinstance(K, PermutationGroup):
            K_elems = set(K.generate_dimino())
        else:
            K_elems = set(K)
    except Exception:
        K_elems = set()
        
    try:
        H_elems = set(H.generate_dimino()) if isinstance(H, PermutationGroup) else set()
        G_elems = set(G.generate_dimino()) if isinstance(G, PermutationGroup) else set()
    except Exception:
        H_elems = set()
        G_elems = set()

    # H_3: G is the set product HK
    try:
        if not K_elems or not H_elems or not G_elems:
            h3 = False
        else:
            HK_elems = set()
            for h in H_elems:
                for k in K_elems:
                    HK_elems.add(h * k)
            h3 = (HK_elems == G_elems)
    except Exception:
        h3 = False
        
    # H_4: The intersection of H and K contains only the identity element
    try:
        if not H_elems or not K_elems or not h1:
            h4 = False
        else:
            intersection = H_elems.intersection(K_elems)
            h4 = (intersection == {G.identity})
    except Exception:
        h4 = False
        
    # neg_Q: The quotient group G/H is NOT isomorphic to K
    try:
        if not h1 or not isinstance(H, PermutationGroup) or not H.is_subgroup(G):
            neg_q = False
        elif not H.is_normal(G):
            # If H is not normal, G/H is not a group, so it cannot be isomorphic to K
            neg_q = True
        else:
            # Check if K is a subgroup (since it's a finite subset, closure is sufficient)
            is_group = True
            if G.identity not in K_elems:
                is_group = False
            else:
                for a in K_elems:
                    for b in K_elems:
                        try:
                            if a * b not in K_elems:
                                is_group = False
                                break
                        except Exception:
                            is_group = False
                            break
                    if not is_group:
                        break
            
            if not is_group:
                # K is not a group, so it cannot be isomorphic to G/H
                neg_q = True
            else:
                # K is a subgroup. Check if it has the correct order to be isomorphic to G/H.
                if len(K_elems) * len(H_elems) != len(G_elems):
                    neg_q = True
                else:
                    # If K is a subgroup, |K| = |G/H|, and H intersect K = {1}, 
                    # then by the Second Isomorphism Theorem, G/H is isomorphic to K.
                    intersection = H_elems.intersection(K_elems)
                    if intersection == {G.identity}:
                        neg_q = False
                    else:
                        # Fallback for invalid witnesses where intersection != {1}
                        neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: G is the set product HK",
    "H_4: The intersection of H and K contains only the identity element",
    "¬Q: The quotient group G/H is not isomorphic to K"
]

N_HYP = 4
NEG_Q_INDEX = 4