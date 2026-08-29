import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
    Checks the hypotheses and the negated conclusion for the conjecture:
    Hypotheses:
      - N is a normal subgroup of G
      - n is a non-negative integer
    Conclusion:
      - The n-th derived subgroup of G/N is equal to the subgroup (G^(n)N)/N
    """
    try:
        G, N, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = False
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            is_norm = True
            for g in G.generators:
                for n_gen in N.generators:
                    if (g * n_gen * ~g) not in N:
                        is_norm = False
                        break
                    if (~g * n_gen * g) not in N:
                        is_norm = False
                        break
                if not is_norm:
                    break
            h1 = is_norm
    except Exception:
        h1 = False

    # H_2: n is a non-negative integer
    try:
        h2 = isinstance(n, int) and n >= 0
    except Exception:
        h2 = False

    # neg_Q: The n-th derived subgroup of G/N is not equal to the subgroup (G^(n)N)/N
    try:
        # Compute the preimage of the n-th derived subgroup of G/N in G
        # P_0 = G, P_{k+1} = P_k' N
        P = G
        for _ in range(n):
            P_prime = P.derived_subgroup()
            gens = list(P_prime.generators) + list(N.generators)
            P = PermutationGroup(gens)
        
        # Compute the preimage of (G^(n)N)/N in G, which is G^(n)N
        H = G
        for _ in range(n):
            H = H.derived_subgroup()
        gens_H = list(H.generators) + list(N.generators)
        Gn_N = PermutationGroup(gens_H)
        
        # The subgroups of G/N are equal iff their preimages in G are equal
        are_equal = P.is_subgroup(Gn_N) and Gn_N.is_subgroup(P)
        neg_q = not are_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: n is a non-negative integer",
    "¬Q: The n-th derived subgroup of G/N is not equal to the subgroup (G^(n)N)/N"
]

N_HYP = 2
NEG_Q_INDEX = 2