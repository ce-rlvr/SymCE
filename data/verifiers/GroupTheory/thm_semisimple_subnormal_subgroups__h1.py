import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(H, G):
    """Check if H is a subgroup of G."""
    if H.order() == 1:
        return True
    for g in H.generators:
        if not G.contains(g):
            return False
    return True

def normal_closure(G, H):
    """Compute the normal closure of H in G."""
    if H.order() == 1:
        return H
    gens = list(H.generators)
    group = PermutationGroup(gens)
    while True:
        order = group.order()
        new_gens = list(group.generators)
        added = False
        for g in G.generators:
            ginv = g**-1
            for h in group.generators:
                c1 = g * h * ginv
                if not group.contains(c1):
                    new_gens.append(c1)
                    added = True
                c2 = ginv * h * g
                if not group.contains(c2):
                    new_gens.append(c2)
                    added = True
        if not added:
            break
        group = PermutationGroup(new_gens)
    return group

def is_subnormal(G, H):
    """Check if H is a subnormal subgroup of G."""
    if not is_subgroup(H, G):
        return False
    K = G
    while True:
        if K.order() == H.order():
            return True
        next_K = normal_closure(K, H)
        if next_K.order() == K.order():
            return False
        K = next_K

def is_semisimple(group):
    """
    Check if a finite group is semisimple.
    A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    Equivalently, it has no non-trivial solvable normal subgroups.
    """
    if group.order() == 1:
        return True
    for g in list(group.generate()):
        if g.is_Identity:
            continue
        nc = normal_closure(group, PermutationGroup([g]))
        solvable = nc.is_solvable
        if callable(solvable):
            solvable = solvable()
        if solvable:
            return False
    return True

def conditions(witness):
    """
    Check if the witness is a valid counterexample.
    The witness should be a tuple (G, H) where G and H are PermutationGroups.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_subgroup(H, G) and is_subnormal(G, H)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_semisimple(H)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subnormal subgroup of G",
    "¬Q: H is not a semisimple group"
]

N_HYP = 1
NEG_Q_INDEX = 1