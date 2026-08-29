import sympy
from sympy.combinatorics import PermutationGroup
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
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, G_prime) where G is a PermutationGroup representing
    the Galois group Gal(K/F), and G_prime is a subgroup of G.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, G_prime = witness
    except Exception:
        return [False, False, False, False]

    # H_1: K/F is a finite Galois extension (represented by a finite permutation group G)
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is the Galois group Gal(K/F)
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: K^{G'} is the subfield of K consisting of elements fixed by all automorphisms in G'
    # (represented by G_prime being a valid subgroup of G)
    try:
        h3 = isinstance(G_prime, PermutationGroup) and G_prime.is_subgroup(G)
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails.
    # The conclusion states that K^{G'}/F is the maximal abelian subextension.
    # By Galois theory, this holds if and only if G_prime is exactly the commutator subgroup of G.
    # Therefore, the conclusion fails iff G_prime is NOT the commutator subgroup of G.
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            D = G.derived_subgroup()
            # Check if G_prime == D (using mutual subgroup inclusion for safety with permutation groups)
            q = G_prime.is_subgroup(D) and D.is_subgroup(G_prime)
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension",
    "H_2: G is the Galois group Gal(K/F)",
    "H_3: K^{G'} is the subfield of K consisting of elements fixed by all automorphisms in G'",
    "¬Q: The conclusion fails (G' is not the commutator subgroup of G)"
]

N_HYP = 3
NEG_Q_INDEX = 3