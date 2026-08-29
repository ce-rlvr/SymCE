import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_minimal_normal(G, N):
    if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
        return False
    if N.order() <= 1:
        return False
    
    try:
        for gen in N.generators:
            if not G.contains(gen):
                return False
    except Exception:
        return False

    try:
        for g in G.generators:
            for n in N.generators:
                if not N.contains(g * n * ~g):
                    return False
    except Exception:
        return False
    
    try:
        for x in list(N.generate()):
            if x.is_Identity:
                continue
            closure_gens = {x}
            queue = [x]
            while queue:
                curr = queue.pop(0)
                for g in G.generators:
                    conj = g * curr * ~g
                    if conj not in closure_gens:
                        closure_gens.add(conj)
                        queue.append(conj)
            closure_group = PermutationGroup(list(closure_gens))
            if closure_group.order() < N.order():
                return False
    except Exception:
        return False
        
    return True

def is_simple(N):
    return is_minimal_normal(N, N)

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_minimal_normal(G, N)
    except Exception:
        h2 = False
        
    try:
        if not isinstance(N, PermutationGroup):
            neg_q = False
        else:
            is_non_abelian_simple = is_simple(N) and not N.is_abelian
            neg_q = not is_non_abelian_simple
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a minimal normal subgroup of G",
    "¬Q: N is not a non-abelian simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2