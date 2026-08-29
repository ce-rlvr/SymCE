import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings that the witness expression may reference.
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
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (Gal, G) or a dict {'Gal': Gal, 'G': G} where:
      - Gal is the Galois group of the finite Galois extension K/F.
      - G is a subgroup of Gal (representing the group G in the conjecture).
    """
    try:
        if isinstance(witness, dict):
            Gal = witness.get('Gal')
            G = witness.get('G')
        else:
            Gal, G = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: K/F is a finite Galois extension
    try:
        h1 = isinstance(Gal, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G' is the commutator subgroup of G
    # We verify that G is a valid subgroup of Gal.
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(Gal, PermutationGroup):
            h2 = False
        else:
            h2 = all(g in Gal for g in G.generators)
    except Exception:
        h2 = False

    # H_3: K^{G'} is the subfield of K consisting of elements fixed by all automorphisms in G'
    # This is definitional in our Galois correspondence model.
    try:
        h3 = h2
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails
    # The conclusion states that K^{G'} is the maximal abelian subextension of K/F.
    # By Galois theory, the maximal abelian subextension is uniquely K^{Gal'}.
    # Therefore, the conclusion holds if and only if K^{G'} = K^{Gal'}, which means G' = Gal'.
    # The conclusion fails if and only if G' != Gal'.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            Gal_prime = Gal.derived_subgroup()
            
            # Check if G_prime == Gal_prime
            is_equal = all(g in Gal_prime for g in G_prime.generators) and \
                       all(g in G_prime for g in Gal_prime.generators)
            neg_q = not is_equal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension",
    "H_2: G' is the commutator subgroup of G",
    "H_3: K^{G'} is the subfield of K consisting of elements fixed by all automorphisms in G'",
    "¬Q: The conclusion fails (K^{G'} is not the maximal abelian subextension)"
]

N_HYP = 3
NEG_Q_INDEX = 3