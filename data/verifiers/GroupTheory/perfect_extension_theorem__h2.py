import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Perfect Extension Theorem conjecture.
    Witness is expected to be a tuple (G, N) where G is a group and N is a normal subgroup.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group (we also check N is a group to ensure the witness is well-formed)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a perfect group (N equals its commutator subgroup)
    try:
        h2 = N.derived_subgroup().order() == N.order()
    except Exception:
        h2 = False

    # H_3: The quotient group G/N is a perfect group
    # This implicitly requires N to be a normal subgroup of G.
    try:
        if not N.is_subgroup(G):
            h3 = False
        else:
            # Verify N is a normal subgroup of G
            is_normal = True
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        is_normal = False
                        break
                    if not N.contains(~g * n * g):
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if not is_normal:
                h3 = False
            else:
                # G/N is perfect iff G'N = G
                G_prime = G.derived_subgroup()
                gens = list(G_prime.generators) + list(N.generators)
                if not gens:
                    G_prime_N_order = 1
                else:
                    G_prime_N = PermutationGroup(gens)
                    G_prime_N_order = G_prime_N.order()
                h3 = G_prime_N_order == G.order()
    except Exception:
        h3 = False

    # ¬Q: G is not a perfect group
    try:
        neg_q = G.derived_subgroup().order() != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a perfect group",
    "H_3: The quotient group G/N is a perfect group",
    "¬Q: G is not a perfect group"
]

N_HYP = 3
NEG_Q_INDEX = 3