import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = True
        if not hasattr(G, 'contains') or not hasattr(N, 'contains'):
            h1 = False
        else:
            # Check if N is a subgroup of G
            for gen in N.generators:
                if not G.contains(gen):
                    h1 = False
                    break
            
            # Check normality: g * n * g^-1 in N for all generators
            if h1:
                for g in G.generators:
                    for n in N.generators:
                        if not N.contains(g * n * ~g):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False
        
    # ¬Q: The index of N in G is a prime number
    try:
        order_G = G.order() if callable(G.order) else G.order
        order_N = N.order() if callable(N.order) else N.order
        if order_G % order_N == 0:
            index = order_G // order_N
            neg_q = bool(isprime(index))
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The index of N in G is a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1