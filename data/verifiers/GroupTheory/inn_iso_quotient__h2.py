import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
    "H_2: Inn(G) is the inner automorphism group of G",
    "¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def inner_automorphism_group(G):
    """Constructs the inner automorphism group of G as a permutation group."""
    elements = list(G.generate())
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    perms = []
    seen_perms = set()
    for g in elements:
        p = []
        for x in elements:
            # Conjugation: g * x * g^-1
            y = g * x * ~g
            p.append(elem_to_idx[y])
        perm = Permutation(p)
        if perm not in seen_perms:
            seen_perms.add(perm)
            perms.append(perm)
    return PermutationGroup(perms)

def quotient_group(G, N):
    """Constructs the quotient group G/N as a permutation group acting on left cosets."""
    elements = list(G.generate())
    n_elements = list(N.generate())
    
    cosets = []
    elem_to_coset_idx = {}
    
    # Find all left cosets
    for g in elements:
        if g not in elem_to_coset_idx:
            idx = len(cosets)
            coset = []
            for n in n_elements:
                gn = g * n
                if gn not in elem_to_coset_idx:
                    coset.append(gn)
                    elem_to_coset_idx[gn] = idx
            cosets.append(coset)
            
    # Construct the permutation representation of G acting on the cosets
    perms = []
    seen_perms = set()
    for g in elements:
        p = []
        for coset in cosets:
            c = coset[0]
            gc = g * c
            p.append(elem_to_coset_idx[gc])
        perm = Permutation(p)
        if perm not in seen_perms:
            seen_perms.add(perm)
            perms.append(perm)
    return PermutationGroup(perms)

def conditions(witness):
    try:
        # The witness can be just the group G, or a tuple (G, InnG)
        if isinstance(witness, tuple) and len(witness) == 2:
            G, InnG = witness
            witness_is_tuple = True
        else:
            G = witness
            InnG = None
            witness_is_tuple = False
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
        # Limit order to prevent timeouts on unreasonably large witnesses
        if h1 and G.order() > 1000:
            h1 = False
    except Exception:
        h1 = False

    # H_2: Inn(G) is the inner automorphism group of G
    try:
        if not h1:
            h2 = False
        else:
            actual_Inn = inner_automorphism_group(G)
            if witness_is_tuple:
                h2 = isinstance(InnG, PermutationGroup) and InnG.is_isomorphic(actual_Inn)
            else:
                InnG = actual_Inn
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)
    try:
        if not h1 or not isinstance(InnG, PermutationGroup):
            neg_q = False
        else:
            Z = G.center()
            G_mod_Z = quotient_group(G, Z)
            q = InnG.is_isomorphic(G_mod_Z)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]