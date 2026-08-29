import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            # Check if N is a subgroup of G
            is_sub = all(gen in G for gen in N.generators)
            if not is_sub:
                h2 = False
            else:
                # Check normality: g * n * g^-1 in N for all generators
                h2 = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * g**-1) not in N:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # neg_Q: G' is not a subgroup of N
    try:
        G_prime = G.derived_subgroup()
        # It is NOT a subgroup if at least one generator of G_prime is not in N
        neg_q = not all(gen in N for gen in G_prime.generators)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The commutator subgroup G' is not a subgroup of N"
]

N_HYP = 2
NEG_Q_INDEX = 2