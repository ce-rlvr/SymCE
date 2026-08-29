import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, p, P, H = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if isinstance(P, PermutationGroup) and all(G.contains(g) for g in P.generators):
            order_G = G.order()
            k = 0
            while order_G % p == 0:
                k += 1
                order_G //= p
            h3 = (P.order() == p**k)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # H_4: The normalizer N_G(P) is a subgroup of H
    try:
        if isinstance(H, PermutationGroup):
            N_gens = []
            for g in list(G.generate()):
                try:
                    normalizes = all(P.contains(g * x * ~g) for x in P.generators)
                except Exception:
                    normalizes = False
                if normalizes:
                    N_gens.append(g)
            
            h4 = all(H.contains(g) for g in N_gens)
        else:
            h4 = False
    except Exception:
        h4 = False
        
    # neg_Q: The index of H in G is NOT congruent to 1 modulo p
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = True
        elif not all(G.contains(g) for g in H.generators):
            # If H is not a subgroup of G, index is undefined, so conclusion fails.
            neg_q = True
        else:
            idx = G.order() / H.order()
            if idx != int(idx):
                neg_q = True
            else:
                neg_q = (int(idx) % p != 1)
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: The normalizer of P is a subgroup of H",
    "¬Q: The index of H in G is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4