import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should provide G, H, phi, and N.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            N = witness.get('N')
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            G, H, phi, N = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements')
        if h1:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            if len(G_elements) == 0 or len(H_elements) == 0:
                h1 = False
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            if callable(phi):
                for g in G_elements:
                    try:
                        if phi(g) not in H_elements:
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
                if h2:
                    for a in G_elements:
                        for b in G_elements:
                            if phi(a * b) != phi(a) * phi(b):
                                h2 = False
                                break
                        if not h2:
                            break
            else:
                for g in G_elements:
                    if g not in phi or phi[g] not in H_elements:
                        h2 = False
                        break
                if h2:
                    for a in G_elements:
                        for b in G_elements:
                            if phi[a * b] != phi[a] * phi[b]:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # ¬Q: The preimage phi^-1(N) is not a normal subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            if hasattr(N, 'elements'):
                N_set = set(N.elements)
            else:
                N_set = set(N)
                
            preimage = set()
            for g in G_elements:
                try:
                    mapped_g = phi(g) if callable(phi) else phi[g]
                    if mapped_g in N_set:
                        preimage.add(g)
                except Exception:
                    pass
            
            # Check if preimage is a subgroup
            is_subgroup = True
            if not preimage:
                is_subgroup = False
            else:
                # For finite groups, non-empty subset closed under multiplication is a subgroup
                for a in preimage:
                    for b in preimage:
                        if a * b not in preimage:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            
            # Check if preimage is normal
            is_normal = False
            if is_subgroup:
                is_normal = True
                for n in preimage:
                    for g in G_elements:
                        if g * n * (g**-1) not in preimage:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The preimage phi^-1(N) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2