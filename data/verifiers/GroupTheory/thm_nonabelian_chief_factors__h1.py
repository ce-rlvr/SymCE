import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def is_normal(G, H):
    for h in H.generators:
        if not G.contains(h):
            return False
    for g in G.generators:
        for h in H.generators:
            if not H.contains(g * h * ~g):
                return False
            if not H.contains(~g * h * g):
                return False
    return True

def is_maximal_normal(N, M):
    if get_order(M) >= get_order(N):
        return False
    if not is_normal(N, M):
        return False
    
    try:
        elements = list(N.elements)
    except Exception:
        elements = list(N.generate())
        
    for x in elements:
        if M.contains(x):
            continue
        
        closure_gens = list(M.generators) + [x]
        H = PermutationGroup(closure_gens)
        N_gens = N.generators
        
        while True:
            added = False
            new_gens = list(H.generators)
            for g in H.generators:
                for n in N_gens:
                    c1 = n * g * ~n
                    if not H.contains(c1) and c1 not in new_gens:
                        new_gens.append(c1)
                        added = True
                    c2 = ~n * g * n
                    if not H.contains(c2) and c2 not in new_gens:
                        new_gens.append(c2)
                        added = True
            if not added:
                break
            H = PermutationGroup(new_gens)
            if get_order(H) == get_order(N):
                break
                
        if get_order(H) < get_order(N):
            return False
            
    return True

def conditions(witness):
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = is_normal(G, M)
    except Exception:
        h1 = False
        
    try:
        h2 = is_normal(G, N)
    except Exception:
        h2 = False
        
    try:
        h3 = is_maximal_normal(N, M)
    except Exception:
        h3 = False
        
    try:
        neg_q = True
        for x in N.generators:
            for y in N.generators:
                commutator = x * y * ~x * ~y
                if not M.contains(commutator):
                    neg_q = False
                    break
            if not neg_q:
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is a normal subgroup of G",
    "H_2: N is a normal subgroup of G",
    "H_3: M is a maximal proper normal subgroup of N",
    "¬Q: The quotient group N/M is abelian"
]

N_HYP = 3
NEG_Q_INDEX = 3