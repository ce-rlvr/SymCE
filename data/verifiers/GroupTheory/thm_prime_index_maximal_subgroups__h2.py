import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, M = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if h1 and isinstance(M, PermutationGroup):
            is_sub = True
            for g in M.generators:
                if not G.contains(g):
                    is_sub = False
                    break
            
            if is_sub and M.order() < G.order():
                is_max = True
                for g in G.generate():
                    if not M.contains(g):
                        gens = list(M.generators) + [g]
                        H = PermutationGroup(gens)
                        if H.order() != G.order():
                            is_max = False
                            break
                h2 = is_max
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if h1 and isinstance(M, PermutationGroup):
            if M.order() > 0 and G.order() % M.order() == 0:
                index = G.order() // M.order()
                neg_q = not isprime(index)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: M is a maximal subgroup of G",
    "¬Q: The index of M in G is not a prime number"
]

N_HYP = 2
NEG_Q_INDEX = 2