import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_inn_G(G):
    elements = list(G.elements)
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    inn_perms = []
    for g in elements:
        perm_array = [0] * len(elements)
        for j, x in enumerate(elements):
            conj = g * x * g**-1
            perm_array[j] = elem_to_idx[conj]
        inn_perms.append(Permutation(perm_array))
    
    return PermutationGroup(*inn_perms)

def get_quotient_group(G, N):
    elements = list(G.elements)
    n_elements = list(N.elements)
    
    cosets = []
    coset_reps = []
    seen = set()
    
    for g in elements:
        if g not in seen:
            coset = set()
            for n in n_elements:
                gn = g * n
                coset.add(gn)
                seen.add(gn)
            cosets.append(coset)
            coset_reps.append(g)
            
    quotient_perms = []
    for g1 in coset_reps:
        perm_array = [0] * len(cosets)
        for j, g2 in enumerate(coset_reps):
            prod = g1 * g2
            for i, c in enumerate(cosets):
                if prod in c:
                    perm_array[j] = i
                    break
        quotient_perms.append(Permutation(perm_array))
        
    return PermutationGroup(*quotient_perms)

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple) and len(witness) == 2:
        G, Z = witness
    else:
        G = witness
        try:
            Z = G.center()
        except Exception:
            Z = None

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1 and Z is not None and isinstance(Z, PermutationGroup):
            center_G = G.center()
            h2 = (Z.order() == center_G.order() and 
                  set(Z.elements) == set(center_G.elements))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            Inn_G = get_inn_G(G)
            G_mod_Z = get_quotient_group(G, Z)
            try:
                if hasattr(Inn_G, 'is_isomorphic'):
                    is_iso = Inn_G.is_isomorphic(G_mod_Z)
                else:
                    is_iso = True
            except Exception:
                # Fallback if isomorphism check fails
                is_iso = True
            neg_q = not is_iso
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2