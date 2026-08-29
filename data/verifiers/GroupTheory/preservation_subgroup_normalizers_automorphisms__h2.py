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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    try:
        G, phi, H = witness
    except Exception:
        return [False, False, False, False]

    # Helper to get elements of G
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
    except Exception:
        elements = []

    # Helper to evaluate phi
    try:
        if callable(phi):
            phi_map = {g: phi(g) for g in elements}
        elif isinstance(phi, dict):
            phi_map = phi
        else:
            phi_map = {}
    except Exception:
        phi_map = {}

    # Helper to get elements of H
    try:
        if hasattr(H, 'elements'):
            H_elements = list(H.elements)
        else:
            H_elements = list(H)
    except Exception:
        H_elements = []

    # Helper for equality of lists as sets (avoids hashability issues)
    def lists_equal_as_sets(l1, l2):
        for x in l1:
            if x not in l2: return False
        for x in l2:
            if x not in l1: return False
        return True

    # H_1: G is a group
    try:
        if hasattr(G, 'is_group') and G.is_group:
            h1 = True
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            h1 = True
        else:
            h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: phi is an automorphism of G
    try:
        if not phi_map or len(phi_map) != len(elements):
            h2 = False
        else:
            vals = list(phi_map.values())
            uniques = []
            for x in vals:
                if x not in uniques:
                    uniques.append(x)
            
            is_bijection = len(uniques) == len(elements) and all(v in elements for v in vals)
            
            is_homo = True
            for g1 in elements:
                for g2 in elements:
                    if phi_map[g1 * g2] != phi_map[g1] * phi_map[g2]:
                        is_homo = False
                        break
                if not is_homo:
                    break
            h2 = is_bijection and is_homo
    except Exception:
        h2 = False

    # H_3: N_G(H) denotes the normalizer of H in G (H must be a valid subset of G)
    try:
        h3 = all(h in elements for h in H_elements)
    except Exception:
        h3 = False

    # ¬Q: N_G(phi(H)) != phi(N_G(H))
    try:
        def is_in_normalizer(g, subset):
            try:
                g_inv = g**-1
            except Exception:
                g_inv = ~g
            
            conjugated = []
            for h in subset:
                conjugated.append(g * h * g_inv)
            
            return lists_equal_as_sets(conjugated, subset)
            
        NG_H = [g for g in elements if is_in_normalizer(g, H_elements)]
        
        phi_H = [phi_map[h] for h in H_elements]
        NG_phi_H = [g for g in elements if is_in_normalizer(g, phi_H)]
        
        phi_NG_H = [phi_map[g] for g in NG_H]
        
        neg_q = not lists_equal_as_sets(NG_phi_H, phi_NG_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "H_3: N_G(H) denotes the normalizer of H in G",
    "¬Q: N_G(phi(H)) != phi(N_G(H))"
]

N_HYP = 3
NEG_Q_INDEX = 3