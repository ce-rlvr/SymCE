import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, H = witness
            C_given = None
        elif len(witness) == 3:
            G, H, C_given = witness
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # Compute C_G(H) if H_1 and H_2 hold
    C_computed = None
    if h1 and h2:
        try:
            c_elements = []
            for g in G.generate():
                is_in_C = True
                for h in H.generators:
                    if g * h != h * g:
                        is_in_C = False
                        break
                if is_in_C:
                    c_elements.append(g)
            C_computed = PermutationGroup(c_elements)
        except Exception:
            pass

    # H_3: C_G(H) is the centralizer of H in G
    try:
        if not (h1 and h2 and C_computed is not None):
            h3 = False
        else:
            if C_given is not None:
                h3 = isinstance(C_given, PermutationGroup) and C_given.is_subgroup(G) and set(C_given.generate()) == set(C_computed.generate())
            else:
                h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: Conclusion fails
    try:
        if not (h1 and h2 and C_computed is not None):
            neg_q = False
        else:
            # Compute N_G(H)
            E_H = list(H.generate())
            set_H = set(E_H)
            n_elements = []
            for g in G.generate():
                is_in_N = True
                for h in H.generators:
                    if (g * h * ~g) not in set_H:
                        is_in_N = False
                        break
                if is_in_N:
                    n_elements.append(g)
            N_G_H = PermutationGroup(n_elements)
            
            C_G_H = C_computed
            
            # Check if C_G(H) is a normal subgroup of N_G(H)
            set_C = set(C_G_H.generate())
            is_normal = True
            for n in N_G_H.generators:
                for c in C_G_H.generators:
                    if (n * c * ~n) not in set_C:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
            # Check if N_G(H)/C_G(H) is isomorphic to a subgroup of Aut(H)
            # We construct the image of N_G(H) in Aut(H) via conjugation
            idx = {e: i for i, e in enumerate(E_H)}
            img_elements = []
            for g in N_G_H.generate():
                p = []
                for i in range(len(E_H)):
                    h = E_H[i]
                    ghg = g * h * ~g
                    p.append(idx[ghg])
                img_elements.append(Permutation(p))
            Img = PermutationGroup(img_elements)
            
            # By the First Isomorphism Theorem, the image is isomorphic to N_G(H)/C_G(H)
            # We verify the order matches to ensure the kernel is exactly C_G(H)
            is_iso = (Img.order() * C_G_H.order() == N_G_H.order())
            
            conclusion = is_normal and is_iso
            neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: C_G(H) is the centralizer of H in G",
    "¬Q: C_G(H) is not a normal subgroup of N_G(H) or N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3