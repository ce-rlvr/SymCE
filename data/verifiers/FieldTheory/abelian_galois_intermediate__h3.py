import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for group theory models of Galois extensions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    The witness should be a tuple of three PermutationGroup objects (G, H_K, H_E)
    representing the Galois correspondence:
      - G: The Galois group of some large finite Galois extension L/F.
      - H_K: The subgroup of G corresponding to the intermediate field K.
      - H_E: The subgroup of G corresponding to the field E.
    """
    try:
        G, H_K, H_E = witness
    except Exception:
        return [False, False, False]

    # H_1: K is a finite Galois extension of a field F
    # By the Fundamental Theorem of Galois Theory, K is Galois over F iff H_K is a normal subgroup of G.
    try:
        h1 = bool(H_K.is_subgroup(G) and G.is_normal(H_K))
    except Exception:
        h1 = False

    # H_2: The Galois group Gal(K/F) is an abelian group
    # Gal(K/F) is isomorphic to the quotient group G / H_K.
    # G / H_K is abelian iff the derived subgroup [G, G] is a subgroup of H_K.
    try:
        D = G.derived_subgroup()
        h2 = bool(D.is_subgroup(H_K))
    except Exception:
        h2 = False

    # neg_Q: E is NOT a Galois extension of F
    # E is Galois over F iff H_E is a normal subgroup of G.
    # We require E to be a valid field in our universe (H_E <= G) but NOT Galois over F.
    try:
        neg_q = bool(H_E.is_subgroup(G) and not G.is_normal(H_E))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a finite Galois extension of F",
    "H_2: The Galois group Gal(K/F) is an abelian group",
    "¬Q: E is not a Galois extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2