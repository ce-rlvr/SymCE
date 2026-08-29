import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard groups
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    Hypotheses:
      1. G and H are groups
      2. G is an abelian group
    Conclusion:
      The image f(G) is an abelian subgroup of H.
      
    Witness is expected to be a tuple: (G, H, f)
    where f is a dictionary or callable mapping elements of G to elements of H.
    """
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is an abelian group
    try:
        h2 = bool(G.is_abelian)
    except Exception:
        h2 = False

    # neg_Q: The image f(G) is NOT an abelian subgroup of H
    try:
        if not h1:
            neg_q = False
        else:
            img = set()
            subset_valid = True
            
            # Compute the image f(G) and verify it is a subset of H
            for g in G.elements:
                if isinstance(f, dict):
                    val = f[g]
                elif callable(f):
                    val = f(g)
                else:
                    val = dict(f)[g]
                
                # Check membership in H
                try:
                    in_H = H.contains(val)
                except AttributeError:
                    in_H = val in H.elements
                    
                if not in_H:
                    subset_valid = False
                    break
                img.add(val)
            
            if not subset_valid:
                # f(G) is not even a subset of H, so it cannot be a subgroup
                neg_q = True
            else:
                # Check if img is a subgroup
                # For finite subsets of a group, closure under multiplication is sufficient
                is_subgroup = True
                for a in img:
                    for b in img:
                        if a * b not in img:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if not is_subgroup:
                    neg_q = True
                else:
                    # Check if the subgroup is abelian
                    is_abelian = True
                    for a in img:
                        for b in img:
                            if a * b != b * a:
                                is_abelian = False
                                break
                        if not is_abelian:
                            break
                    
                    neg_q = not is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is an abelian group",
    "¬Q: The image f(G) is not an abelian subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2