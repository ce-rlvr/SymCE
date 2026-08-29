import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H), check the hypotheses and the negated conclusion.
    G should be a PermutationGroup and H an iterable of elements in G.
    """
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: For all a, b in G, (aH)(bH) == (ab)H
    try:
        h2 = False
        if h1:
            H_set = set(H)
            elements = list(G.elements)
            # H must be a subset of G for the cosets to be well-defined subsets of G
            if all(h in elements for h in H_set):
                h2_ok = True
                for a in elements:
                    aH = {a * h for h in H_set}
                    for b in elements:
                        bH = {b * h for h in H_set}
                        ab = a * b
                        abH = {ab * h for h in H_set}
                        
                        # Set product (aH)(bH)
                        aHbH = {x * y for x in aH for y in bH}
                        
                        if aHbH != abH:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
                h2 = h2_ok
    except Exception:
        h2 = False
        
    # neg_Q: H is not a normal subgroup of G
    try:
        neg_q = False
        if h1:
            H_set = set(H)
            elements = list(G.elements)
            
            # Check if H is a subgroup
            is_subgroup = True
            if not H_set:
                is_subgroup = False
            elif G.identity not in H_set:
                is_subgroup = False
            else:
                for h1_el in H_set:
                    if h1_el**-1 not in H_set:
                        is_subgroup = False
                        break
                    for h2_el in H_set:
                        if h1_el * h2_el not in H_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            
            # Check if H is normal
            is_normal = False
            if is_subgroup:
                is_normal = True
                for g in elements:
                    for h in H_set:
                        if g * h * (g**-1) not in H_set:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: For all a, b in G, (aH)(bH) = (ab)H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2