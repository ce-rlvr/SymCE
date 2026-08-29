import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: M is a normal subgroup of H",
    "¬Q: The preimage phi^-1(M) is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    if not isinstance(witness, dict):
        return [False, False, False, False]

    try:
        G = witness.get('G')
        H = witness.get('H')
        phi = witness.get('phi')
        M = witness.get('M')
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        h2 = isinstance(H, PermutationGroup)
        if h2:
            G_elements = list(G)
            H_elements = set(H)
            
            if callable(phi):
                phi_dict = {g: phi(g) for g in G_elements}
            else:
                phi_dict = phi
            
            for g in G_elements:
                if g not in phi_dict or phi_dict[g] not in H_elements:
                    h2 = False
                    break
            
            if h2:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if phi_dict[g1 * g2] != phi_dict[g1] * phi_dict[g2]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: M is a normal subgroup of H
    try:
        h3 = isinstance(M, PermutationGroup) and M.is_subgroup(H) and M.is_normal(H)
    except Exception:
        h3 = False

    # ¬Q: The preimage \phi^{-1}(M) is NOT a normal subgroup of G
    try:
        G_elements = list(G)
        if callable(phi):
            phi_dict = {g: phi(g) for g in G_elements}
        else:
            phi_dict = phi
            
        M_elements = set(M)
        preimage = set(g for g in G_elements if phi_dict.get(g) in M_elements)
        
        is_subgroup = True
        if G.identity not in preimage:
            is_subgroup = False
        else:
            for a in preimage:
                if ~a not in preimage:
                    is_subgroup = False
                    break
                for b in preimage:
                    if a * b not in preimage:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        is_normal = True
        if is_subgroup:
            for a in preimage:
                for g in G_elements:
                    if g * a * ~g not in preimage:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        neg_q = not (is_subgroup and is_normal)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]