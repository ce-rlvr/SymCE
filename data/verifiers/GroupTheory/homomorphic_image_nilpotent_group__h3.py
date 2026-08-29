import sympy
import sympy.combinatorics
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple (G, H, f)
        # where f is a callable or a dictionary mapping elements of G to elements of H.
        G, H, f = witness
    except Exception:
        return [False, False, False]

    def apply_f(func, g):
        if callable(func):
            return func(g)
        elif isinstance(func, dict):
            return func[g]
        else:
            raise TypeError("f must be callable or dict")

    # H_1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: f is a group homomorphism from G to H
    try:
        if not h1_ok:
            h2_ok = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            
            is_homo = True
            for g in G_elements:
                img = apply_f(f, g)
                if img not in H_elements:
                    is_homo = False
                    break
                    
            if is_homo:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if apply_f(f, g1 * g2) != apply_f(f, g1) * apply_f(f, g2):
                            is_homo = False
                            break
                    if not is_homo:
                        break
            h2_ok = is_homo
    except Exception:
        h2_ok = False

    # ¬Q: The image f(G) is NOT a nilpotent subgroup of H
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            G_elements = list(G.elements)
            image_elements = [apply_f(f, g) for g in G_elements]
            
            unique_images = []
            for img in image_elements:
                if img not in unique_images:
                    unique_images.append(img)
                    
            img_group = PermutationGroup(*unique_images)
            neg_q_ok = not img_group.is_nilpotent
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a group homomorphism from G to H",
    "¬Q: The image f(G) is not a nilpotent subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2