import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_normal(H, G):
    try:
        for h in H.generators:
            if not G.contains(h):
                return False
        for h in H.generators:
            for g in G.generators:
                if not H.contains(g**-1 * h * g):
                    return False
        return True
    except Exception:
        return False

def mutual_commutator(N, M):
    gens = []
    for n in N.generators:
        for m in M.generators:
            gens.append(n**-1 * m**-1 * n * m)
    
    if not gens:
        if N.generators:
            iden = N.generators[0]**0
        elif M.generators:
            iden = M.generators[0]**0
        else:
            iden = Permutation()
        return PermutationGroup([iden])
        
    closure_gens = list(gens)
    closure_group = PermutationGroup(closure_gens)
    NM_gens = list(N.generators) + list(M.generators)
    
    current_new = list(gens)
    while current_new:
        next_new = []
        for g in current_new:
            for x in NM_gens:
                conj = x**-1 * g * x
                if not closure_group.contains(conj):
                    next_new.append(conj)
                    closure_gens.append(conj)
                    closure_group = PermutationGroup(closure_gens)
        current_new = next_new
        
    return closure_group

def conditions(witness):
    try:
        if len(witness) == 3:
            G, N, M = witness
        elif len(witness) == 2:
            G, N = witness
            M = G
        else:
            return [False, False]
            
        h1 = is_normal(N, G)
        
        mut_comm = mutual_commutator(N, M)
        q = is_normal(mut_comm, G)
        
        return [h1, not q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of N and G is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1