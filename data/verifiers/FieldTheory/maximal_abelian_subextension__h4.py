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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension",
    "H_2: G is the Galois group Gal(K/F)",
    "H_3: G' is the commutator subgroup of G",
    "¬Q: K^{G'}/F is not Galois abelian, or the intermediate field correspondence fails"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_normal_subgroup(G, H):
    if not H.is_subgroup(G):
        return False
    for g in G.generators:
        for h in H.generators:
            if not H.contains(g * h * ~g):
                return False
            if not H.contains((~g) * h * g):
                return False
    return True

def is_abelian_quotient(G, N):
    for g1 in G.generators:
        for g2 in G.generators:
            comm = g1 * g2 * (~g1) * (~g2)
            if not N.contains(comm):
                return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, G_prime, H = witness
            elif len(witness) == 2:
                G, G_prime = witness
                H = None
            else:
                return [False, False, False, False]
        else:
            G = witness
            G_prime = G.derived_subgroup()
            H = None
            
        h1 = isinstance(G, PermutationGroup)
        h2 = isinstance(G, PermutationGroup)
        
        if isinstance(G_prime, PermutationGroup):
            h3 = (G_prime == G.derived_subgroup())
        else:
            h3 = False
            
        if not (h1 and h2 and h3):
            return [h1, h2, h3, False]
            
        part1 = is_normal_subgroup(G, G_prime) and is_abelian_quotient(G, G_prime)
        
        if H is not None and isinstance(H, PermutationGroup):
            if H.is_subgroup(G):
                left = is_normal_subgroup(G, H) and is_abelian_quotient(G, H)
                right = G_prime.is_subgroup(H)
                part2 = (left == right)
            else:
                part2 = True
        else:
            part2 = True
            
        Q = part1 and part2
        neg_Q = not Q
        
        return [h1, h2, h3, neg_Q]
    except Exception:
        return [False, False, False, False]