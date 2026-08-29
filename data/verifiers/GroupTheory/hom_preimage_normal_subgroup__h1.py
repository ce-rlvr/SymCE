import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    Witness is expected to be a tuple: (G, H, phi, N)
    where:
      - G, H are groups (e.g., PermutationGroup or iterables of elements)
      - phi is a callable or dictionary mapping elements of G to elements of H
      - N is a normal subgroup of H (iterable of elements)
    """
    try:
        G, H, phi, N = witness
    except Exception:
        return [False, False, False]
        
    def get_phi(x):
        if callable(phi):
            return phi(x)
        return phi[x]

    # H_1: phi is a group homomorphism from G to H
    h1_ok = False
    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
        
        valid_mapping = True
        for g in G_elems:
            if get_phi(g) not in H_elems:
                valid_mapping = False
                break
                
        if valid_mapping:
            is_hom = True
            for g1 in G_elems:
                for g2 in G_elems:
                    if get_phi(g1 * g2) != get_phi(g1) * get_phi(g2):
                        is_hom = False
                        break
                if not is_hom:
                    break
            h1_ok = is_hom
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of H
    h2_ok = False
    try:
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
        N_set = set(N)
        
        if N_set and N_set.issubset(set(H_elems)):
            is_subgroup = True
            for n1 in N_set:
                if n1**-1 not in N_set:
                    is_subgroup = False
                    break
                for n2 in N_set:
                    if n1 * n2 not in N_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
            if is_subgroup:
                is_normal = True
                for h in H_elems:
                    for n in N_set:
                        if h * n * h**-1 not in N_set:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2_ok = is_normal
    except Exception:
        h2_ok = False

    # ¬Q: The preimage phi^{-1}(N) is NOT a normal subgroup of G
    neg_q_ok = False
    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
        N_set = set(N)
        
        preimage = set()
        for g in G_elems:
            if get_phi(g) in N_set:
                preimage.add(g)
                
        if not preimage:
            neg_q_ok = True
        else:
            is_subgroup = True
            for p1 in preimage:
                if p1**-1 not in preimage:
                    is_subgroup = False
                    break
                for p2 in preimage:
                    if p1 * p2 not in preimage:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
            if not is_subgroup:
                neg_q_ok = True
            else:
                is_normal = True
                for g in G_elems:
                    for p in preimage:
                        if g * p * g**-1 not in preimage:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q_ok = not is_normal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: N is a normal subgroup of H",
    "¬Q: The preimage phi^{-1}(N) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2