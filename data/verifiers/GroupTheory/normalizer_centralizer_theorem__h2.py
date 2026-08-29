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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    witness should be a tuple (G, H) where G is a group and H is a subset of G.
    """
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # ¬Q: Conclusion fails
    # The Normalizer-Centralizer Theorem states that if H is a subgroup of G, 
    # then C_G(H) is a normal subgroup of N_G(H) and N_G(H)/C_G(H) is isomorphic to a subgroup of Aut(H).
    # This is unconditionally true for any subgroup H.
    # The dropped hypothesis is "H is a subgroup of G".
    # If H is not a subgroup, Aut(H) is undefined, and the conclusion fails.
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        elif isinstance(H, Permutation):
            # H is an element, not a subset/subgroup
            neg_q = True
        else:
            if isinstance(H, PermutationGroup):
                H_elems = list(H.generate_dimino())
            else:
                try:
                    H_elems = list(H)
                except TypeError:
                    H_elems = []
                    
            if not H_elems:
                is_sub = False
            else:
                is_sub = True
                for h in H_elems:
                    if not isinstance(h, Permutation) or h not in G:
                        is_sub = False
                        break
                
                if is_sub:
                    degree = G.degree
                    H_norm = set()
                    # Normalize permutations to the degree of G to ensure correct equality checks
                    for h in H_elems:
                        if h.size < degree:
                            arr = h.array_form + list(range(h.size, degree))
                            H_norm.add(Permutation(arr))
                        else:
                            H_norm.add(h)
                            
                    id_elem = Permutation(list(range(degree)))
                    if id_elem not in H_norm:
                        is_sub = False
                    else:
                        for a in H_norm:
                            inv_a = ~a
                            if inv_a.size < degree:
                                arr = inv_a.array_form + list(range(inv_a.size, degree))
                                inv_a = Permutation(arr)
                            if inv_a not in H_norm:
                                is_sub = False
                                break
                            for b in H_norm:
                                ab = a * b
                                if ab.size < degree:
                                    arr = ab.array_form + list(range(ab.size, degree))
                                    ab = Permutation(arr)
                                if ab not in H_norm:
                                    is_sub = False
                                    break
            
            q = is_sub
            neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: C_G(H) is not a normal subgroup of N_G(H), or N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1