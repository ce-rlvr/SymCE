import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def get_image_and_check_hom(G, S, phi):
    """
    Helper function to verify if phi is a valid homomorphism from G to S,
    and if so, return its image as a set of elements.
    """
    try:
        G_id = getattr(G, 'identity', Permutation())
        S_id = getattr(S, 'identity', Permutation())
        
        image = None
        is_hom = False
        
        if callable(phi):
            elements = list(G.generate())
            is_hom = True
            for g in elements:
                for h in elements:
                    if phi(g * h) != phi(g) * phi(h):
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                image = set(phi(g) for g in elements)
                
        elif isinstance(phi, dict):
            if all(g in phi for g in G.generators):
                mapping = {G_id: S_id}
                queue = [G_id]
                is_hom = True
                while queue:
                    u = queue.pop(0)
                    for g in G.generators:
                        v = u * g
                        val = mapping[u] * phi[g]
                        if v in mapping:
                            if mapping[v] != val:
                                is_hom = False
                                break
                        else:
                            mapping[v] = val
                            queue.append(v)
                    if not is_hom:
                        break
                if is_hom:
                    image = set(mapping.values())
            else:
                elements = list(G.generate())
                if all(g in phi for g in elements):
                    is_hom = True
                    for g in elements:
                        for h in elements:
                            if phi[g * h] != phi[g] * phi[h]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    if is_hom:
                        image = set(phi[g] for g in elements)
                        
        elif isinstance(phi, (list, tuple)):
            if len(phi) == len(G.generators):
                phi_dict = dict(zip(G.generators, phi))
                return get_image_and_check_hom(G, S, phi_dict)
            
        else:
            if hasattr(phi, 'image'):
                image_group = phi.image()
                image = set(image_group.generate())
                is_hom = True
                
        if is_hom and image is not None:
            try:
                if all(img in S for img in image):
                    return image, True
            except Exception:
                S_elements = set(S.generate())
                if image.issubset(S_elements):
                    return image, True
                    
    except Exception:
        pass
    return None, False

def conditions(witness) -> list[bool]:
    try:
        G, S, phi = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a semisimple finite group
    # A finite group is semisimple if it has no non-trivial normal abelian subgroups.
    try:
        h1 = True
        if not hasattr(G, 'normal_subgroups'):
            h1 = False
        else:
            for N in G.normal_subgroups():
                if N.order() == 1:
                    continue
                if N.is_abelian:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: S is a solvable group
    try:
        if hasattr(S, 'is_solvable'):
            h2 = bool(S.is_solvable)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The image of \phi is NOT the trivial subgroup of S
    try:
        neg_q = False
        image, is_hom = get_image_and_check_hom(G, S, phi)
        if is_hom and image is not None:
            # Trivial subgroup has exactly 1 element (the identity)
            if len(image) > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: S is a solvable group",
    "¬Q: The image of phi is not the trivial subgroup of S"
]

N_HYP = 2
NEG_Q_INDEX = 2