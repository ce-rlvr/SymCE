import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: \phi is a group homomorphism from G to H",
    "¬Q: The preimage \phi^{-1}(M) is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Unpack witness
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        phi = witness.get('phi')
        M = witness.get('M')
    else:
        try:
            G, H, phi, M = witness
        except Exception:
            return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: \phi is a group homomorphism from G to H
    try:
        if callable(phi):
            mapping = {g: phi(g) for g in G.elements}
        elif isinstance(phi, dict):
            mapping = phi
        else:
            try:
                mapping = dict(phi)
            except Exception:
                mapping = None

        if mapping is not None and h1 and h2:
            domain_ok = set(mapping.keys()) == set(G.elements)
            codomain_ok = set(mapping.values()).issubset(set(H.elements))
            if domain_ok and codomain_ok:
                homo_ok = True
                for x in G.elements:
                    for y in G.elements:
                        if mapping[x * y] != mapping[x] * mapping[y]:
                            homo_ok = False
                            break
                    if not homo_ok:
                        break
                h3 = homo_ok
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The preimage \phi^{-1}(M) is NOT a normal subgroup of G
    try:
        if mapping is None or not h1:
            neg_q = False
        else:
            if isinstance(M, PermutationGroup):
                M_elements = set(M.elements)
            else:
                M_elements = set(M)
            
            preimage = set(g for g in G.elements if g in mapping and mapping[g] in M_elements)
            
            is_subgroup = True
            if not preimage:
                is_subgroup = False
            else:
                id_g = None
                for g in G.elements:
                    if g * g == g:
                        id_g = g
                        break
                
                if id_g not in preimage:
                    is_subgroup = False
                else:
                    for x in preimage:
                        if x**-1 not in preimage:
                            is_subgroup = False
                            break
                        for y in preimage:
                            if x * y not in preimage:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
            
            is_normal = True
            if is_subgroup:
                for g in G.elements:
                    g_inv = g**-1
                    for n in preimage:
                        if g * n * g_inv not in preimage:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            is_normal_subgroup = is_subgroup and is_normal
            neg_q = not is_normal_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]