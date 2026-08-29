import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

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

# Q8 (Quaternion group of order 8)
Q8 = PermutationGroup(
    Permutation(0, 2, 1, 3)(4, 7, 5, 6),
    Permutation(0, 4, 1, 5)(2, 6, 3, 7)
)

def has_complement(G, N):
    """
    Checks if there exists a subgroup H of G such that G = N \rtimes H.
    For finite groups, this is equivalent to finding a subgroup H of order |G|/|N|
    such that H \cap N = {1}.
    """
    target_order = G.order() // N.order()
    if target_order == 1:
        return True
        
    try:
        G_els = list(G.generate_dimino())
        N_els = set(N.generate_dimino())
    except AttributeError:
        G_els = list(G.elements)
        N_els = set(N.elements)
        
    id_el = None
    for g in G_els:
        if g * g == g:
            id_el = g
            break
            
    possible_elements = []
    for g in G_els:
        if g == id_el:
            continue
        if g in N_els:
            continue
        # In a subgroup of order target_order, the order of any element must divide target_order
        if target_order % g.order() == 0:
            possible_elements.append(g)
            
    if len(possible_elements) < target_order - 1:
        return False
        
    # Check all subsets of the right size to see if they form a subgroup
    for subset in itertools.combinations(possible_elements, target_order - 1):
        H_set = set(subset)
        H_set.add(id_el)
        
        is_subgroup = True
        for a in H_set:
            for b in H_set:
                if a * b not in H_set:
                    is_subgroup = False
                    break
            if not is_subgroup:
                break
                
        if is_subgroup:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # The conclusion is that the sequence splits (a complement exists).
            # The negated conclusion is that it does NOT split.
            neg_q = not has_complement(G, N)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The short exact sequence does not split (no complement to N in G exists)"
]

N_HYP = 2
NEG_Q_INDEX = 2