import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
D8 = DihedralGroup(8)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finite group and P is a subgroup of G",
    "H_2: p is a prime number dividing the order of G",
    "¬Q: N_G(N_G(P)) != N_G(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group and P is a subgroup of G
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup):
            G_elements = set(G.generate())
            if all(g in G_elements for g in P.generators):
                h1 = True
    except Exception:
        h1 = False
        
    # H_2: p is a prime number dividing the order of G
    try:
        h2 = False
        if isprime(p) and G.order() % p == 0:
            h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: N_G(N_G(P)) != N_G(P)
    try:
        neg_q = False
        if h1:
            P_elements = set(P.generate())
            
            # Compute N_G(P)
            N1_gens = []
            for g in G.generate():
                if all((g * x * ~g) in P_elements for x in P.generators):
                    N1_gens.append(g)
            N1 = PermutationGroup(N1_gens)
            
            # Compute N_G(N_G(P))
            N1_elements = set(N1.generate())
            N2_gens = []
            for g in G.generate():
                if all((g * x * ~g) in N1_elements for x in N1.generators):
                    N2_gens.append(g)
            N2 = PermutationGroup(N2_gens)
            
            # Since N_G(P) is always a subgroup of N_G(N_G(P)), 
            # they are equal iff their orders are equal.
            if N1.order() != N2.order():
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]