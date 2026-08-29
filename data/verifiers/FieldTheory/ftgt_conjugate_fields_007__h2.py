import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            sigma = witness.get('sigma')
        elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'sigma'):
            G = witness.G
            H = witness.H
            sigma = witness.sigma
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, sigma = witness
            elif len(witness) == 6:
                K, F, E, G, H, sigma = witness
            else:
                groups = [x for x in witness if isinstance(x, PermutationGroup)]
                perms = [x for x in witness if isinstance(x, Permutation)]
                G, H = groups[0], groups[1]
                if not H.is_subgroup(G):
                    G, H = H, G
                sigma = perms[0]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: K/F is a finite Galois extension with Galois group G
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H = Gal(K/E) is the subgroup of G corresponding to E
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: \sigma is an automorphism in G
    try:
        h3 = isinstance(sigma, Permutation) and sigma in G
    except Exception:
        h3 = False

    # neg_Q: The subgroup corresponding to \sigma(E) is NOT \sigma H \sigma^{-1}
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            # In SymPy's right-action convention, the subgroup corresponding to \sigma(E) is \sigma^{-1} H \sigma
            true_subgroup_gens = [sigma**-1 * h * sigma for h in H.generators]
            true_subgroup = PermutationGroup(true_subgroup_gens)
            
            # The claimed subgroup in the false conjecture is \sigma H \sigma^{-1}
            claimed_subgroup_gens = [sigma * h * sigma**-1 for h in H.generators]
            claimed_subgroup = PermutationGroup(claimed_subgroup_gens)
            
            # The conclusion fails if the true subgroup does not equal the claimed subgroup
            neg_q = not true_subgroup.is_subgroup(claimed_subgroup) or not claimed_subgroup.is_subgroup(true_subgroup)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension with Galois group G",
    "H_2: H = Gal(K/E) is the subgroup of G corresponding to E",
    "H_3: sigma is an automorphism in G",
    "¬Q: The subgroup corresponding to sigma(E) is NOT sigma H sigma^-1"
]

N_HYP = 3
NEG_Q_INDEX = 3