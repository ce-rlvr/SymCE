import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(G, N):
    for gen in N.generators:
        if gen not in G:
            return False
    return True

def is_normal(G, N):
    if not is_subgroup(G, N):
        return False
    for n in N.generators:
        for g in G.generators:
            if (g * n * ~g) not in N:
                return False
            if (~g * n * g) not in N:
                return False
    return True

def k_group(G):
    return len(G.conjugacy_classes())

def k_quotient(G, N):
    n_elements = list(N.elements)
    elements = list(G.elements)
    
    rep_of = {}
    reps = []
    
    for g in elements:
        if g not in rep_of:
            reps.append(g)
            for n in n_elements:
                rep_of[g * n] = g
                
    classes = 0
    unseen = set(reps)
    while unseen:
        a = unseen.pop()
        classes += 1
        
        orbit = {a}
        queue = [a]
        while queue:
            curr = queue.pop(0)
            for g in G.generators:
                conj1 = g * curr * ~g
                r1 = rep_of[conj1]
                if r1 not in orbit:
                    orbit.add(r1)
                    queue.append(r1)
                    if r1 in unseen:
                        unseen.remove(r1)
                        
                conj2 = ~g * curr * g
                r2 = rep_of[conj2]
                if r2 not in orbit:
                    orbit.add(r2)
                    queue.append(r2)
                    if r2 in unseen:
                        unseen.remove(r2)
    return classes

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and is_normal(G, N)
    except Exception:
        h2 = False
        
    # neg_Q: k(G) > k(N) * k(G/N)
    try:
        if h1 and h2:
            kg = k_group(G)
            kn = k_group(N)
            kgn = k_quotient(G, N)
            neg_q = kg > kn * kgn
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: k(G) > k(N) k(G/N)"
]

N_HYP = 2
NEG_Q_INDEX = 2