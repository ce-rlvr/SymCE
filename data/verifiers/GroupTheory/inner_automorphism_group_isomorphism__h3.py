import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def quotient_group(G, N):
    elements = list(G.generate())
    n_elems = list(N.generate())
    
    cosets = []
    coset_map = {}
    for g in elements:
        c = frozenset([g * n for n in n_elems])
        if c not in coset_map:
            coset_map[c] = len(cosets)
            cosets.append(c)
            
    if len(cosets) == 1:
        return PermutationGroup([Permutation([0])])
        
    gens = []
    for g in G.generators:
        perm = []
        for c in cosets:
            rep = next(iter(c))
            new_rep = g * rep
            new_c = frozenset([new_rep * n for n in n_elems])
            perm.append(coset_map[new_c])
        gens.append(Permutation(perm))
        
    return PermutationGroup(gens)

def inner_automorphism_group(G):
    elements = list(G.generate())
    n = len(elements)
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    if n == 1:
        return PermutationGroup([Permutation([0])])
        
    inn_gens = []
    for g in G.generators:
        perm_array = []
        for x in elements:
            y = g * x * ~g
            perm_array.append(elem_to_idx[y])
        inn_gens.append(Permutation(perm_array))
        
    grp = PermutationGroup(inn_gens)
    if grp.order() == 1:
        return PermutationGroup([Permutation([0])])
    return grp

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = h1
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            if witness.order() > 100:
                neg_q = False
            else:
                Z = witness.center()
                Q_grp = quotient_group(witness, Z)
                Inn_grp = inner_automorphism_group(witness)
                is_iso = Q_grp.is_isomorphic(Inn_grp)
                neg_q = not is_iso
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: G/Z(G) is not isomorphic to Inn(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2